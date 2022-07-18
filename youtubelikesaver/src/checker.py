import os
import re
import sys
from typing import Dict, Set

COMPLETED_DOWNLOAD_REGEX = re.compile(r"([^=]+)=(.+)\.(.+)")


def main():
    if len(sys.argv) == 1:
        backup_file_location = ""
    else:
        backup_file_location = sys.argv[1]

    video_id_to_file_extensions: Dict[str, Set] = dict()
    video_id_to_title: Dict[str, str] = dict()

    for root, dirs, files in os.walk(backup_file_location):
        for file in files:
            print(file)

            regex_result = COMPLETED_DOWNLOAD_REGEX.match(file)
            if regex_result is None:
                print("Error processing file! Does not match regex.")
                continue

            video_slug = regex_result.group(1)
            video_id = regex_result.group(2)
            video_extension = regex_result.group(3)

            if video_id in video_id_to_file_extensions:
                video_id_to_file_extensions[video_id].add(video_extension)
            else:
                video_id_to_file_extensions[video_id] = {video_extension}
                video_id_to_title[video_id] = video_slug

    print("\nRESULTS:\n")

    for video_id, video_extensions in video_id_to_file_extensions.items():
        if len(video_extensions) == 1:
            print(f"Only one file for video {video_id} - {video_id_to_title[video_id]}")


if __name__ == "__main__":
    main()
