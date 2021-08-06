# youtube-like-saver

![tox workflow](https://github.com/Tyler-Yates/youtube-like-saver/actions/workflows/tox-workflow.yml/badge.svg)

Simple Python application to save metadata about liked videos in YouTube and then backup the audio and video stream.

Videos can be taken down or made private, at which point the title of the video will become unavailable.
By backing up your liked videos, you can ensure that you don't lose access to them.

## Authentication

Fetching the user's list of liked videos requires authentication, so you will need to set up OAuth flow.

1. Create a new project in [Google Cloud Platform](https://console.cloud.google.com/apis/dashboard).
1. Add the "YouTube Data API v3" to your project.
1. Create a new OAuth credential.
1. Add your desired YouTube account as a test user for your application.
1. Save the client secrets JSON file to the root of this repository with the name `client_secrets.json`.
1. This file is in `.gitignore` so it should not be committed to the repository.

## Local Setup

In a terminal, go to the root of this repository.

Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

## Running

Run the program from the root of the repository:
```
python3 -m youtubelikesaver
```

Open the link printed out to the console and go through the necessary steps until you can copy the credential string.
Paste the credential back into the terminal.
The program will save the credential to disk as a file called `credentials.pickle`.
This file is in `.gitignore` so it should not be committed to the repository.

On future executions of this program, the `credentials.pickle` file will be loaded, so you should not need to go through
the OAuth flow again.

If authentication is successful, the program will fetch your liked videos.
After fetching the list of liked videos, the program will save the videos in a JSON file called `liked_videos.json`.
This file is in `.gitignore` so it should not be committed to the repository.

You can set the location to save `liked_videos.json` by using the environment variable `BACKUP_FILE_LOCATION`.
