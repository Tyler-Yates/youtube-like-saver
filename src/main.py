import json
import os
import sys
from typing import List

from src.youtubelikesaver.backup_util import save_audio_and_video
from youtubelikesaver.youtube_client import YoutubeClient
from youtubelikesaver.youtube_video import YoutubeVideo

CLIENT_SECRETS_FILE_NAME = "client_secrets.json"
BACKUP_FILE_NAME = "liked_videos.json"


def save_liked_videos(liked_videos: List[YoutubeVideo], backup_file_location: str):
    json_data = dict()
    for liked_video in liked_videos:
        json_data[liked_video.video_url] = liked_video.video_title

    backup_file_path = os.path.join(backup_file_location, BACKUP_FILE_NAME)
    print(f"Saving liked videos backup file at {backup_file_path}")
    with open(backup_file_path, mode='w', encoding="utf-8") as backup_file:
        json.dump(json_data, backup_file, indent=4, ensure_ascii=False)


def backup_liked_videos(liked_videos: List[YoutubeVideo], backup_file_location: str):
    for liked_video in liked_videos:
        save_audio_and_video(liked_video.video_url, backup_file_location)


def main():
    if len(sys.argv) == 1:
        backup_file_location = ""
    elif len(sys.argv) == 2:
        backup_file_location = sys.argv[1]
    else:
        print("Incorrect number of arguments.")
        sys.exit(1)

    youtube_client = YoutubeClient(CLIENT_SECRETS_FILE_NAME)

    print("Fetching liked videos...")
    liked_videos = youtube_client.get_liked_videos()
    print(liked_videos)
    print(len(liked_videos))

    save_liked_videos(liked_videos, backup_file_location)
    backup_liked_videos(liked_videos, backup_file_location)


if __name__ == "__main__":
    main()
