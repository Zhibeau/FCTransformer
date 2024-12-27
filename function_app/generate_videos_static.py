import os
import get_character_from_file
from datetime import datetime
from combine_image_audio import combine_image_audio

def main(image_dir, audio_dir, output_dir):

    os.makedirs(output_dir, exist_ok=True)
    video_clips = []
    fc_names = ['Barca',
                'RealMadrid',
                'AtleticoMadrid',
                'Juventus',
                'InterMilan',
                'ACMilan',
                'Bayern',
                'Dortmund',
                'Arsenal',
                'Liverpool',
                'ManUnited',
                'ManCity',
                'Chelsea']
    character = get_character_from_file.get_character_from_file('./prompts/characters.txt')
    for fc_name in fc_names:
        output_file = os.path.join(output_dir, fc_name+"_video_"+datetime.now().strftime("%Y_%m_%d")+".mp4")
        image_file = os.path.join(image_dir, fc_name+"_"+character+"_"+datetime.now().strftime("%Y_%m_%d")+'.png')
        audio_file = os.path.join(audio_dir, fc_name+'_snippet_normalized.mp3')
        combine_image_audio(image_file, audio_file, output_file)

main("./", "./output_snippets", "./videostoday")
