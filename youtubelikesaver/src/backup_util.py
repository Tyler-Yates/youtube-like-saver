import os

import youtube_dl

BACKUP_SUBFOLDER = "videoaudio"


class BackupUtil:
    def __init__(self, backup_location: str):
        if not os.path.exists(backup_location):
            raise ValueError(f"Backup location {backup_location} does not exist")
        if not os.path.isdir(backup_location):
            raise ValueError(f"Backup location {backup_location} is not a directory")

        self.backup_location = os.path.join(backup_location, BACKUP_SUBFOLDER)
        if not os.path.exists(self.backup_location):
            os.makedirs(self.backup_location)

        self.videos_already_backed_up = set()
        self.completed_file_path = os.path.join(backup_location, "completed.txt")
        if os.path.exists(self.completed_file_path):
            with open(self.completed_file_path, mode="r") as completed_file:
                for line in completed_file.readlines():
                    line = line.strip()
                    if line:
                        self.videos_already_backed_up.add(line.strip())

    def save_audio_and_video(self, video_url: str):
        if video_url in self.videos_already_backed_up:
            print(f"Video {video_url} already backed up")
            return

        ydl_config = {
            "format": "bestvideo+bestaudio",
            "outtmpl": os.path.join(self.backup_location, "%(title)s.%(ext)s"),
            "merge_output_format": "mkv",
            "writethumbnail": True,
        }
        with youtube_dl.YoutubeDL(ydl_config) as ydl:
            result = ydl.download([video_url])
            print(result)
        ydl_config = {
            "format": "bestaudio",
            "outtmpl": os.path.join(self.backup_location, "%(title)s.%(ext)s"),
        }
        with youtube_dl.YoutubeDL(ydl_config) as ydl:
            result = ydl.download([video_url])
            print(result)

        with open(self.completed_file_path, mode="a+") as completed_file:
            completed_file.write(f"{video_url}\n")
