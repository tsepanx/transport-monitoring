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

    def send_sticker_reply(self, chat_id, sticker_id):
        pass


ME_CHAT_ID = 325805942

greet_bot = BotHandler(MY_TELEGRAM_BOT_TOKEN)
greetings = ('здравствуй', 'привет', 'ку', 'здорово', 'hi', 'hello')
now = datetime.now()


def handle_message_request(last: Update, bot: BotHandler):
    if last.chat_type == "group" and "@" not in last.message_text:
        return

    if last.message_text:
        reply = get_reply_on_text(last)
        # print(last.message_text, reply)

        bot.send_message(
            last.chat_id,
            reply)
    elif last.sticker_id:
        reply_text = last.sticker_set_name + "\n" + last.sticker_id

        bot.send_message(
            last.chat_id,
            reply_text)
    else:
        bot.send_message(
            last.chat_id,
            convert_dict_to_string(last.get_filtered_json()))


def get_reply_on_text(last: Update):
    today = now.day
    hour = now.hour

    # if last.message_text == "/get_me":
    #     return

    if last.message_text.lower() in greetings:
        if today == now.day and 6 <= hour < 12:
            return f'Good morning, {last.author_name[0]}'

        elif today == now.day and 12 <= hour < 17:
            return f'Добрый день, {last.author_name[0]}'

        elif today == now.day and 17 <= hour < 23:
            return f'Good evening, {last.author_name[0]}'
    else:
        return convert_dict_to_string(last.get_filtered_json()) + "\n@" + last.author_username
        # return f"Sorry, I don't understand you, {last.author_name[0]}"


def get_yt_latest_video(yt: YoutubeHandler, channel_id, prev_video_id):
    video = yt.get_latest_video_from_channel(channel_id)
    if not video:
        return

    print(video)
    video_id = video["video_id"]

    if video_id == prev_video_id:
        return

    # raw = convert_dict_to_string(video)
    preview_url = video["video_thumbnail"]

    return get_pretty_str_video_data(video), video_id, preview_url


def main():
    yt_request_timeout = 300
    yt_handler = YoutubeHandler(
        MY_YOUTUBE_API_KEY,
        timedelta(days=3))

    channels_last_data = {}  # [datetime.now()], video_id
    for chan in yt_handler.CHANNELS.values():
        channels_last_data[chan] = [None, None]

    prev_updated = datetime.now()

    new_offset = None

    while True:
        from_last_update = datetime.now() - timedelta(seconds=yt_request_timeout)
        if from_last_update >= prev_updated:
            print_dict(channels_last_data)
            for channel_id in channels_last_data:
                current_data = channels_last_data[channel_id]

                print("Getting data from youtube...")

                collected_data = get_yt_latest_video(yt_handler, channel_id, current_data[1])
                if not collected_data:
                    print(channel_id)
                    continue

                yt_text, video_id, preview_url = collected_data

                print("received", video_id)

                greet_bot.send_image(ME_CHAT_ID, preview_url)
                greet_bot.send_message(ME_CHAT_ID, yt_text, disable_preview=True)

                # updating values in channels dict
                channels_last_data[channel_id] = [datetime.now(), video_id]

        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        if last_update.is_empty:
            continue

        print_dict(last_update.message_text)

        handle_message_request(last_update, greet_bot)

        new_offset = last_update.id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
