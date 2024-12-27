from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime
import pandas as pd
import os

def generate_dalle_image(my_prompt, my_key, size="1024x1792"):
    """
    Generate a tall image using OpenAI's DALL·E model.
    
    Args:
        prompt (str): The description of the image to generate.
        api_key (str): Your OpenAI API key.
        size (str): Image resolution (default "1024x1792").
        
    Returns:
        str: URL of the generated image.
    """
    client = OpenAI(
    api_key=my_key,  # this is also the default, it can be omitted
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=my_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    print(f"Image generated: {image_url}")
    return image_url


def resize_image_to_youtube_shorts(image_url, output_path):
    """
    Crop the image to the 9:16 aspect ratio (1080x1920) focusing on the central lower part and resize it to 1080x1920 for YouTube Shorts.

    Args:
        image_url (str): URL of the image to download and resize.
        output_path (str): Path to save the resized image.
    """
    try:
        # Download the image
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # Target aspect ratio (9:16)
        target_aspect_ratio = 9 / 16
        original_width, original_height = image.size
        original_aspect_ratio = original_width / original_height

        # Determine cropping dimensions
        if original_aspect_ratio > target_aspect_ratio:
            # Image is wider than 9:16, crop width
            new_width = int(original_height * target_aspect_ratio)
            left = (original_width - new_width) // 2
            right = left + new_width
            bottom = original_height
            top = bottom - int(new_width / target_aspect_ratio)
        else:
            # Image is taller than 9:16, crop height
            new_height = int(original_width / target_aspect_ratio)
            bottom = original_height
            top = bottom - new_height
            left = 0
            right = original_width

        # Crop the image
        cropped_image = image.crop((left, top, right, bottom))

        # Resize to 1080x1920
        resized_image = cropped_image.resize((1080, 1920), Image.LANCZOS)

        # Save the resized image
        resized_image.save(output_path)
        print(f"Image cropped, resized, and saved to: {output_path}")

    except Exception as e:
        print(f"Error resizing image: {e}")
        
def get_character_from_file(file_path):
    """
    Get the i-th character from the file based on the difference in days
    between the system date and December 18, 2024.

    Args:
        file_path (str): Path to the characters.txt file.
    
    Returns:
        str: The character from the file, or an error message.
    """
    try:
        # Calculate the difference in days
        target_date = datetime(2024, 12, 18)
        current_date = datetime.now()
        day_difference = abs((current_date - target_date).days)

        # Read the characters from the file
        with open(file_path, 'r') as file:
            characters = [line.strip() for line in file.readlines()]

        # Get the character at the index (mod to handle out-of-bounds)
        character = characters[day_difference % len(characters)]
        return character

    except Exception as e:
        return f"Error: {e}"
fc_full_names = {'Barca':"Barcelona",
                'RealMadrid': "Real Madrid CF",
                'AtleticoMadrid': "Atlético Madrid",
                'Juventus': "Juventus",
                'InterMilan': "Inter Milan",
                'ACMilan': "AC Milan",
                'Bayern': "Bayern Munich",
                'Dortmund': "Borussia Dortmund",
                'Arsenal': "Arsenal",
                'Liverpool': "Liverpool",
                'ManUnited': "Manchester United",
                'ManCity': "Manchester City",
                'Chelsea': "Chelsea"}

if __name__ == "__main__":
    # Replace with your OpenAI API key
    my_key = os.getenv('OPENAI_API')

    character = get_character_from_file('./prompts/characters.txt')
    df = pd.read_csv('./prompts/fc_prompts.csv')
    dfc = df.sample(frac=1).reset_index(drop=True)
    current_date = datetime.now()
    date_str = current_date.strftime("%Y_%m_%d")
    # Prompt for DALL·E
    for i in range(dfc.shape[0]):
        fc_name = dfc.loc[i]['fc_name']
        fc_full_name = fc_full_names[fc_name]
        prompt = "Draw a highly detailed and realistic " + character + " with features of Football club " + fc_full_name + \
        " with dynamic lighting. The color of the club should be used. The full body of the "+ character +\
        " should stand on the grassfield in the stadium"
        if not pd.isna(dfc.loc[i]['fc_elements']):
            prompt += "Here are some elements you could included in the "+character+":" + dfc.loc[i]['fc_elements']
        if not pd.isna(dfc.loc[i]['fc_memes']):
            prompt += dfc.loc[i]['fc_memes']
        output_path = fc_name+"_"+character+"_"+date_str+".png"
        # Step 1: Generate Image
        image_url = generate_dalle_image(prompt, my_key)

        # Step 2: Resize Image for YouTube Shorts
        if image_url:
            resize_image_to_youtube_shorts(image_url,output_path)
