import os
import pickle
from typing import Dict, List

import google_auth_httplib2
import google_auth_oauthlib.flow
import googleapiclient.discovery
import httplib2
from google.auth.credentials import Credentials
from google.auth.exceptions import RefreshError

from .youtube_video import YoutubeVideo

MAX_RESULTS = 100

CREDENTIALS_FILE = "credentials.pickle"

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


class YoutubeClient:
    def __init__(self, client_secrets_file_name: str):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        credentials: Credentials = None

        # See if the credentials are already saved locally
        if os.path.exists(CREDENTIALS_FILE):
            print("Loading credentials from file...")
            with open(CREDENTIALS_FILE, mode="rb") as credentials_file:
                credentials = pickle.load(credentials_file)

        # Try to refresh the token first
        if credentials and credentials.expired and credentials.refresh_token:
            # We have expired credentials so we can just refresh them
            print("Refreshing access token...")
            http = httplib2.Http()
            request = google_auth_httplib2.Request(http)
            try:
                credentials.refresh(request)
            except RefreshError:
                print("Refresh token has expired. Must generate a new one.")

        # If we do not have credentials then we need to fetch them from scratch
        if not credentials or not credentials.valid:
            # Get credentials and create an API client
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file_name, scopes)
            credentials = flow.run_local_server()

            # Save the credentials for the next run
            with open(CREDENTIALS_FILE, "wb") as f:
                print("Saving Credentials for future use...")
                pickle.dump(credentials, f)

        # Create the Youtube client
        self.youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def get_playlists_and_liked_videos(self) -> Dict[str, List[YoutubeVideo]]:
        playlist_name_to_videos = dict()

        request = self.youtube.playlists().list(part="id,snippet", mine=True)
        response = request.execute()

        # Fetch playlists
        while response is not None:
            for playlist in response["items"]:
                playlist_id = playlist["id"]
                playlist_name = playlist["snippet"]["title"]
                print(f"Processing playlist {playlist_name}...")
                playlist_name_to_videos[playlist_name] = self._get_videos_for_playlist(playlist_id)
            if response.get("nextPageToken"):
                response = self.youtube.playlists().list(part="id,snippet", mine=True).execute()
            else:
                response = None

        # Liked videos are not a playlist so get them separately
        print("Processing liked videos...")
        playlist_name_to_videos["Liked"] = self._get_liked_videos()

        return playlist_name_to_videos

    def _get_videos_for_playlist(self, playlist_id: str) -> List[YoutubeVideo]:
        playlist_videos = []

        request = self.youtube.playlistItems().list(
            playlistId=playlist_id, part="snippet,contentDetails,id", maxResults=MAX_RESULTS
        )
        response = request.execute()

        while response is not None:
            for playlist_video in response["items"]:
                playlist_videos.append(YoutubeVideo(playlist_video))
            if response.get("nextPageToken"):
                response = (
                    self.youtube.playlistItems()
                    .list(playlistId=playlist_id, part="snippet,contentDetails,id", maxResults=MAX_RESULTS)
                    .execute()
                )
            else:
                response = None

        return playlist_videos

    def _get_liked_videos(self):
        liked_videos = []

        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics", maxResults=MAX_RESULTS, myRating="like"
        )
        response = request.execute()

        while response is not None:
            for liked_video in response["items"]:
                liked_videos.append(YoutubeVideo(liked_video))
            if response.get("nextPageToken"):
                response = (
                    self.youtube.videos()
                    .list(
                        part="snippet,contentDetails,statistics",
                        maxResults=MAX_RESULTS,
                        pageToken=response["nextPageToken"],
                        myRating="like",
                    )
                    .execute()
                )
            else:
                response = None

        return liked_videos
