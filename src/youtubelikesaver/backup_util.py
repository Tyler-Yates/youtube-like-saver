import os

import pafy


class BackupUtil:
    def __init__(self, backup_location: str):
        self.backup_location = backup_location
        if not os.path.exists(self.backup_location):
            raise ValueError(f"Backup location {self.backup_location} does not exist")
        if not os.path.isdir(self.backup_location):
            raise ValueError(f"Backup location {self.backup_location} is not a directory")

        self.videos_already_backed_up = set()
        self.completed_file_path = os.path.join(backup_location, "completed.txt")
        if os.path.exists(self.completed_file_path):
            with open(self.completed_file_path, mode='r') as completed_file:
                for line in completed_file.readlines():
                    line = line.strip()
                    if line:
                        self.videos_already_backed_up.add(line.strip())

    def save_audio_and_video(self, video_url: str):
        if video_url in self.videos_already_backed_up:
            print(f"Video {video_url} already backed up")
            return

        video = pafy.new(video_url)
        video.getbestvideo().download(filepath=self.backup_location)
        video.getbestaudio().download(filepath=self.backup_location)

        with open(self.completed_file_path, mode='a+') as completed_file:
            completed_file.write(f"{video_url}\n")
