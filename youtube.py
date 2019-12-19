import datetime

import youtube_api
import private_keys

from functions import print_dict

CHANNELS = {
    "ikakprosto": "UCQWeDEwQruA_CcyR08bIE9g"
}


class YoutubeHandler:

    def __init__(self, key: str, request_timeout: datetime.timedelta):
        self.CHANNELS = {
            "ikakprosto": "UCQWeDEwQruA_CcyR08bIE9g"
        }

        self.API_KEY = key
        self.request_timeout = request_timeout
        self.__yt_object = youtube_api.YouTubeDataAPI(self.API_KEY)

    def get_channel_data(self, channel_id):
        channel_data = self.__yt_object.get_channel_metadata(channel_id)
        # channel_data = self.__yt_object.search("ikakprosto2", order_by="date")

        return channel_data

    def get_video_data(self, video_id):
        video_data = self.__yt_object.get_video_metadata(video_id)
        return video_data

    def get_video_comments(self, video_id, elements=None, sorted_by_tag=None):
        comments = self.__yt_object.get_video_comments(video_id)

        if sorted_by_tag:
            comments.sort(key=lambda x: x[sorted_by_tag], reverse=True)

        return comments[:elements] if elements else comments

    def get_playlist_data(self, playlist_id, published_after):
        videos = self.__yt_object.get_videos_from_playlist_id(
            playlist_id,
            published_after=published_after
        )

        # print(len(videos))

        return videos

    def get_latest_video_from_channel(self, channel_id):
        channel_data = self.get_channel_data(channel_id)
        uploads_playlist_id = channel_data['playlist_id_uploads']

        timedelta = datetime.datetime.now() - self.request_timeout

        playlist_data = self.get_playlist_data(
            uploads_playlist_id,
            timedelta
        )

        latest_video_id = playlist_data[0]['video_id']

        return self.get_video_data(latest_video_id)


if __name__ == '__main__':
    now = datetime.datetime.now()
    yt_handler = YoutubeHandler(private_keys.MY_YOUTUBE_API_KEY)

    print_dict(yt_handler.get_latest_video_from_channel(CHANNELS["ikakprosto"],
                                                        now - datetime.timedelta(days=1)))
    # print_dict(yt_handler.get_video_comments())
