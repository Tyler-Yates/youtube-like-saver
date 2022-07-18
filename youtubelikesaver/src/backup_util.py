import json
import logging
import os
from typing import Dict, List

import yt_dlp

MAX_RETRIES = 5

MAX_VIDEO_DOWNLOAD_SIZE = "200M"
MAX_AUDIO_DOWNLOAD_SIZE = "75M"

COMPLETED_DOWNLOADS_FILENAME = "completed_downloads.json"

LOG = logging.getLogger("BackupUtil")
logging.basicConfig()


class BackupUtil:
    def __init__(self):
        self.completed_downloads = self._read_already_downloaded()

    @staticmethod
    def _read_already_downloaded() -> Dict[str, List[str]]:
        completed_downloads = dict()
        if not os.path.exists(COMPLETED_DOWNLOADS_FILENAME):
            return completed_downloads

        with open(COMPLETED_DOWNLOADS_FILENAME, mode="r") as completed_downloads_file:
            return json.load(completed_downloads_file)

    def already_downloaded(self, video_url: str, playlist_name: str):
        return video_url in self.completed_downloads.get(playlist_name, [])

    def record_download(self, video_url: str, playlist_name: str):
        if playlist_name in self.completed_downloads:
            self.completed_downloads[playlist_name].append(video_url)
        else:
            self.completed_downloads[playlist_name] = [video_url]

        with open(COMPLETED_DOWNLOADS_FILENAME, mode="w+", encoding="utf-8") as completed_downloads_file:
            json.dump(self.completed_downloads, completed_downloads_file, indent=4)

    def save_video(
        self,
        video_url: str,
        output_path: str,
        output_file_name: str,
        temp_file_location: str = None,
        chrome_cookies: bool = False,
    ):
        if temp_file_location is None:
            temp_file_location = output_path

        ydl_config = {
            "format": "bestvideo[height>=720]+bestaudio/bestvideo+bestaudio",
            "merge_output_format": "mkv",
            "format_sort": [f"size:{MAX_VIDEO_DOWNLOAD_SIZE}"],
            "paths": {"home": output_path, "temp": temp_file_location},
            "outtmpl": f"{output_file_name}.%(ext)s",
            "windowsfilenames": True,
            "overwrites": False,
        }

        if chrome_cookies:
            ydl_config["cookiesfrombrowser"] = ("chrome",)

        self._save_with_retry(video_url, ydl_config)

    def save_audio(self, video_url: str, output_path: str, output_file_name: str, chrome_cookies: bool = False):
        ydl_config = {
            "format": "bestaudio",
            "format_sort": [f"size:{MAX_AUDIO_DOWNLOAD_SIZE}"],
            "paths": {"home": output_path},
            "outtmpl": f"{output_file_name}.%(ext)s",
            "windowsfilenames": True,
            "writethumbnail": True,
            "overwrites": False,
        }

        if chrome_cookies:
            ydl_config["cookiesfrombrowser"] = ("chrome",)

        self._save_with_retry(video_url, ydl_config)

    @staticmethod
    def _save_with_retry(video_url: str, ydl_config: Dict):
        for i in range(MAX_RETRIES):
            try:
                with yt_dlp.YoutubeDL(ydl_config) as ydl:
                    ydl.download([video_url])
                    return
            except Exception as e:
                LOG.error(f"Error downloading {video_url}", e)

        # Raise exception if we were never able to download
        raise ValueError(f"Could not download video {video_url}")
