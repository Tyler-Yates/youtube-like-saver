from youtubelikesaver.youtube_client import YoutubeClient


CLIENT_SECRETS_FILE_NAME = "client_secrets.json"


def main():
    youtube_client = YoutubeClient(CLIENT_SECRETS_FILE_NAME)

    liked_videos = youtube_client.get_liked_videos()
    print(liked_videos)
    print(len(liked_videos))


if __name__ == "__main__":
    main()
