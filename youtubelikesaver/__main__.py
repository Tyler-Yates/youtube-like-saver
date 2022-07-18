import os
import re
import sys
import unicodedata
from typing import List

from youtubelikesaver.src.backup_util import BackupUtil
from youtubelikesaver.src.youtube_client import YoutubeClient
from youtubelikesaver.src.youtube_video import YoutubeVideo

CLIENT_SECRETS_FILE_NAME = "client_secrets.json"


def _slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def backup_playlist_video_information(
    backup_file_location: str, temp_file_path: str, playlist_name: str, videos: List[YoutubeVideo], chrome_cookies: bool
):
    backup_util = BackupUtil()

    playlist_path = os.path.join(backup_file_location, playlist_name)
    os.makedirs(playlist_path, exist_ok=True)
    for video in videos:
        try:
            _process_video(video, playlist_path, temp_file_path, playlist_name, backup_util, chrome_cookies)
        except Exception as e:
            print(f"Error: {e}")


def _process_video(
    video: YoutubeVideo,
    playlist_path: str,
    temp_file_path: str,
    playlist_name: str,
    backup_util: BackupUtil,
    chrome_cookies: bool,
):
    print(f"\nProcessing {video.video_title}...")
    if backup_util.already_downloaded(video.video_url, playlist_name):
        print("Already downloaded")
        return

    slugified_video_title = _slugify(video.video_title) + f"={video.video_id}"
    video_file_path = os.path.join(playlist_path, f"{slugified_video_title}.txt")
    if os.path.exists(video_file_path):
        print(f"Already saved metadata for video {playlist_name}: {video.video_title}")
    else:
        print(f"Saving metadata for video {playlist_name}: {video.video_title}")
        with open(video_file_path, mode="w", encoding="utf-8") as video_file:
            video_file.write(video.video_url)
            video_file.write("\n")
            video_file.write(video.video_title)
            video_file.write("\n")
            video_file.write(video.description)

    # Save video and audio for select playlists
    if playlist_name.lower().startswith("save video"):
        print("Saving video...")
        backup_util.save_video(video.video_url, playlist_path, slugified_video_title, temp_file_path, chrome_cookies)
    else:
        # Save only audio for all other playlists
        print("Saving audio...")
        backup_util.save_audio(video.video_url, playlist_path, slugified_video_title, chrome_cookies)

    backup_util.record_download(video.video_url, playlist_name)


def main():
    chrome_cookies = False
    if len(sys.argv) == 1:
        backup_file_location = ""
        temp_file_location = ""
    elif len(sys.argv) == 2:
        backup_file_location = sys.argv[1]
        temp_file_location = backup_file_location
    elif len(sys.argv) == 3:
        backup_file_location = sys.argv[1]
        temp_file_location = sys.argv[2]
    elif len(sys.argv) == 4:
        backup_file_location = sys.argv[1]
        temp_file_location = sys.argv[2]
        if "--chrome-cookies" == sys.argv[3]:
            chrome_cookies = True
    else:
        print("Incorrect number of arguments.")
        sys.exit(1)

    youtube_client = YoutubeClient(CLIENT_SECRETS_FILE_NAME)

    playlist_name_to_videos = youtube_client.get_playlists_and_liked_videos()

    for playlist_name, playlist_videos in playlist_name_to_videos.items():
        backup_playlist_video_information(
            backup_file_location, temp_file_location, playlist_name, playlist_videos, chrome_cookies
        )


if __name__ == "__main__":
    main()
