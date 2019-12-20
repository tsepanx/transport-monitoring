from datetime import datetime, timedelta

import requests

from update import Update
from youtube import YoutubeHandler
from private_keys import MY_TELEGRAM_BOT_TOKEN, MY_YOUTUBE_API_KEY
from functions import print_dict, convert_dict_to_string, get_pretty_str_video_data

BOT_GET_METHOD = 'getUpdates'
BOT_SEND_MESSAGE_METHOD = 'sendMessage'
BOT_SEND_IMAGE_METHOD = 'sendPhoto'
BOT_GET_ME_METHOD = 'getMe'

BOT_YOUTUBE_COMMAND = 'ping_youtube'


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"
        print(self.api_url)

    def __post_request(self, send_method, params=None):
        send_url = self.api_url + send_method
        print(send_url, "POST")

        return requests.post(send_url, params)

    def __get_request(self, get_method, params=None):
        get_url = self.api_url + get_method
        print(get_url, "GET")

        return requests.get(get_url, params).json()

    def get_me(self):
        return self.__get_request(BOT_GET_ME_METHOD)

    def get_updates(self, offset=None, timeout=5):
        params = {'timeout': timeout, 'offset': offset}
        response = self.__get_request(BOT_GET_METHOD, params)

        result_json = response['result']

        return result_json

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return Update(last_update)

    def send_message(self, chat_id, text, disable_preview=False):
        params = {'chat_id': chat_id, 'text': text, 'disable_web_page_preview': disable_preview}
        return self.__post_request(BOT_SEND_MESSAGE_METHOD, params)

    def send_image(self, chat_id, photo_identifier, disable_preview=False):
        params = {'chat_id': chat_id, 'photo': photo_identifier, 'disable_web_page_preview': disable_preview}
        return self.__post_request(BOT_SEND_IMAGE_METHOD, params)

    def send_sticker(self, chat_id, sticker_id):
        pass


ME_CHAT_ID = 325805942

super_bot = BotHandler(MY_TELEGRAM_BOT_TOKEN)
now = datetime.now()


def handle_message_request(last: Update, bot: BotHandler):
    if last.chat_type == "group" and "@" not in last.message_text:
        return

    # if last.message_text[0] == "/":
    #     command = last.message_text[1:]
    #     if command == BOT_YOUTUBE_COMMAND:
    #         send_yt_data(bot, last.chat_id, web_handler, )

    if last.message_text or last.sticker_id:
        bot.send_message(
            last.chat_id,
            last.get_reply())
    else:
        bot.send_message(
            last.chat_id,
            convert_dict_to_string(last.get_filtered_json()))


def send_yt_data(bot: BotHandler, chat_id, web_handler: YoutubeHandler, channels_update_metadata):
    for channel_id in channels_update_metadata:
        current_data = channels_update_metadata[channel_id]

        video = web_handler.get_latest_video_from_channel(channel_id)

        if not video:
            continue

        video_id = video["video_id"]
        print(video)

        if video_id == current_data[1]:
            return

        if not video:
            print(channel_id)
            continue

        preview_url = video["video_thumbnail"]
        text_to_send = get_pretty_str_video_data(video)

        bot.send_image(chat_id, preview_url)
        bot.send_message(chat_id, text_to_send, disable_preview=True)

        # updating values in channels dict
        channels_update_metadata[channel_id] = [datetime.now(), video_id]


def main():
    yt_request_timeout = 180
    yt_handler = YoutubeHandler(
        MY_YOUTUBE_API_KEY,
        timedelta(days=3))

    channels_last_data = {}  # [datetime.now()], video_id
    for chan in yt_handler.CHANNELS.values():
        channels_last_data[chan] = [None, None]

    prev_updated = datetime.now()

    new_offset = None

    while True:
        super_bot.get_updates(new_offset)
        last_update = super_bot.get_last_update()

        ping_flag = False

        if not last_update.is_empty:
            print_dict(last_update.get_filtered_json())

            ping_flag = last_update.message_text == '/' + BOT_YOUTUBE_COMMAND

            handle_message_request(last_update, super_bot) if not ping_flag else None

            new_offset = last_update.id + 1

        from_last_update = datetime.now() - timedelta(seconds=yt_request_timeout)
        if from_last_update >= prev_updated or ping_flag:
            print_dict(channels_last_data)
            send_yt_data(super_bot, ME_CHAT_ID, yt_handler, channels_last_data)
            prev_updated = datetime.now()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
