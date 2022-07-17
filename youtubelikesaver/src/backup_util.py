import logging
from typing import Dict

import yt_dlp

MAX_RETRIES = 5

MAX_VIDEO_DOWNLOAD_SIZE = "200M"
MAX_AUDIO_DOWNLOAD_SIZE = "75M"

LOG = logging.getLogger("BackupUtil")
logging.basicConfig()


class BackupUtil:
    def __init__(self):
        pass

    def save_video(self, video_url: str, output_path: str, output_file_name: str):
        ydl_config = {
            "format": "bestvideo+bestaudio",
            "merge_output_format": "mkv",
            "format_sort": [f"size:{MAX_VIDEO_DOWNLOAD_SIZE}"],
            "paths": {"home": output_path},
            "outtmpl": f"{output_file_name}.%(ext)s",
            "writethumbnail": True,
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
