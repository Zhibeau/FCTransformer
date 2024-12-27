from datetime import datetime
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