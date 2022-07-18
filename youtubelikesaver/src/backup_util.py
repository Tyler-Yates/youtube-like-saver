import logging
import os
from typing import Dict, Set

import yt_dlp

MAX_RETRIES = 5

MAX_VIDEO_DOWNLOAD_SIZE = "200M"
MAX_AUDIO_DOWNLOAD_SIZE = "75M"

COMPLETED_DOWNLOADS_FILENAME = "completed_downloads.txt"

LOG = logging.getLogger("BackupUtil")
logging.basicConfig()


class BackupUtil:
    def __init__(self):
        self.completed_downloads = self._read_already_downloaded()

    @staticmethod
    def _read_already_downloaded() -> Set[str]:
        completed_downloads = set()
        if not os.path.exists(COMPLETED_DOWNLOADS_FILENAME):
            return completed_downloads

        with open(COMPLETED_DOWNLOADS_FILENAME, mode="r") as completed_downloads_file:
            for line in completed_downloads_file.readlines():
                completed_downloads.add(line.strip())

        return completed_downloads

    def already_downloaded(self, video_url: str):
        return video_url in self.completed_downloads

    def record_download(self, video_url: str):
        self.completed_downloads.add(video_url)
        with open(COMPLETED_DOWNLOADS_FILENAME, mode="a+", encoding="utf-8") as completed_downloads_file:
            completed_downloads_file.write(video_url)
            completed_downloads_file.write("\n")

    def save_video(self, video_url: str, output_path: str, output_file_name: str, temp_file_location: str = None):
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
        self._save_with_retry(video_url, ydl_config)

    def save_audio(self, video_url: str, output_path: str, output_file_name: str):
        ydl_config = {
            "format": "bestaudio",
            "format_sort": [f"size:{MAX_AUDIO_DOWNLOAD_SIZE}"],
            "paths": {"home": output_path},
            "outtmpl": f"{output_file_name}.%(ext)s",
            "windowsfilenames": True,
            "writethumbnail": True,
            "overwrites": False,
        }
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
