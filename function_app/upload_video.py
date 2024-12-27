from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from get_character_from_file import get_character_from_file
from google.auth.transport.requests import Request
import os
from datetime import datetime

def upload_youtube_short(file_path):
    # Authenticate with YouTube API using refresh token
    creds = Credentials(
        None,
        refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN'),
        client_id = os.getenv('YOUTUBE_CLIENT_ID'),
        client_secret = os.getenv('YOUTUBE_CLIENT_SECRET'),
        token_uri = "https://oauth2.googleapis.com/token"

    )
    creds.refresh(Request())  # Get a new access token

    youtube = build("youtube", "v3", credentials=creds)

    character = get_character_from_file('./prompts/characters.txt')
    # Upload the video with privacyStatus = 'private' (acts as a draft)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "If your club is a " + character,
                "description": "Ask AI to draw your club as a" + character,
                "tags": ["shorts", "automated", "test"],
                "categoryId": "17"  # "People & Blogs"
            },
            "status": {
                "privacyStatus": "public"  # Acts as a draft
            }
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    print("Uploading YouTube Short...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print("Short uploaded successfully! Video ID:", response.get("id"))
    return response.get("id")

if __name__ == "__main__":
    # Video file must be under 60 seconds and vertical (9:16)
    upload_youtube_short("./"+get_character_from_file('./prompts/characters.txt')+"_"+datetime.now().strftime("%Y_%m_%d")+".mp4")
