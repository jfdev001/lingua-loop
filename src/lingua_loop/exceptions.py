class TranscriptNotFoundError(Exception):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(f"Transcript not found for video_id={video_id}")
