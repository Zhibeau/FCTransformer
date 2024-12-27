import os
from moviepy import concatenate_videoclips, VideoFileClip
from datetime import datetime
from get_character_from_file import get_character_from_file

def main(video_dir, output_dir, final_output):
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

    character = get_character_from_file('./prompts/characters.txt')
    video_files = sorted([os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(('.mp4'))])
    for video_file in video_files:
        video_clips.append(video_file)

    # Combine all individual videos
    final_clips = [VideoFileClip(clip) for clip in video_clips]
    final_video = concatenate_videoclips(final_clips, method="compose")
    final_video.write_videofile(final_output, fps=24, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
    # Replace these paths with your actual directories
    VIDEO_DIR = "./videostoday"
    OUTPUT_DIR = "./videos"
    FINAL_OUTPUT = get_character_from_file('./prompts/characters.txt')+"_"+datetime.now().strftime("%Y_%m_%d")+".mp4"

    main(VIDEO_DIR, OUTPUT_DIR, FINAL_OUTPUT)
