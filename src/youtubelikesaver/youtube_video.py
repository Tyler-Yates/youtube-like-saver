class YoutubeVideo:
    def __init__(self, video_json: dict):
        self.video_json = video_json
        self.video_id = video_json["id"]
        self.video_title = video_json["snippet"]["title"]

    def __hash__(self):
        return self.video_id

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.video_id} - {self.video_title}"
