import os

import pafy


def save_audio_and_video(video_url: str, backup_location: str):
    if not os.path.exists(backup_location):
        raise ValueError(f"Backup location {backup_location} does not exist")
    if not os.path.isdir(backup_location):
        raise ValueError(f"Backup location {backup_location} is not a directory")

    video = pafy.new(video_url)
    video.getbestvideo().download(filepath=backup_location)
    video.getbestaudio().download(filepath=backup_location)
