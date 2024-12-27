import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, VideoFileClip
def combine_image_audio(image_file, audio_file, output_file, duration=None):
    """Combine a single image and audio into a video."""
    audio = AudioFileClip(audio_file)
    if duration is None:
        duration = audio.duration

    image = ImageClip(image_file, duration=duration)
    video = image.with_audio(audio)

    video.write_videofile(output_file, fps=24, codec='libx264', audio_codec='aac')