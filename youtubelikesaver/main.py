import json
import os
from typing import List

from youtubelikesaver.youtube_client import YoutubeClient
from youtubelikesaver.youtube_video import YoutubeVideo

CLIENT_SECRETS_FILE_NAME = "client_secrets.json"
BACKUP_FILE_NAME = "liked_videos.json"


def save_liked_videos(liked_videos: List[YoutubeVideo]):
    backup_file_location = os.environ.get("BACKUP_FILE_LOCATION", "")

    json_data = dict()
    for liked_video in liked_videos:
        json_data[liked_video.video_id] = liked_video.video_title

    with open(os.path.join(backup_file_location, BACKUP_FILE_NAME), mode='w') as backup_file:
        json.dump(json_data, backup_file, ensure_ascii=False)


def main():
    youtube_client = YoutubeClient(CLIENT_SECRETS_FILE_NAME)

    print("Fetching liked videos...")
    liked_videos = youtube_client.get_liked_videos()
    print(liked_videos)
    print(len(liked_videos))

    save_liked_videos(liked_videos)


if __name__ == "__main__":
    main()
