from datetime import datetime, timedelta

import requests

from update import Update
from youtube import YoutubeHandler
from private_keys import MY_TELEGRAM_BOT_TOKEN, MY_YOUTUBE_API_KEY
from functions import print_dict, convert_dict_to_string

BOT_GET_METHOD = 'getUpdates'
BOT_SEND_METHOD = 'sendMessage'
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

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        return self.__post_request(BOT_SEND_METHOD, params)

    def send_image(self, file_id):
        pass

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
        print(last.message_text, reply)

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
            convert_dict_to_string(last.get_mess_json()))


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
        return convert_dict_to_string(last.get_mess_json()) + "\n@" + last.author_username
        # return f"Sorry, I don't understand you, {last.author_name[0]}"


def main():
    yt_request_timeout = 60
    yt_handler = YoutubeHandler(
        MY_YOUTUBE_API_KEY,
        timedelta(days=1))

    prev_updated = datetime.now()

    prev_received_video_id = None

    new_offset = None

    while True:

        from_last_update = datetime.now() - timedelta(seconds=yt_request_timeout)

        if from_last_update >= prev_updated:
            video = yt_handler.get_latest_video_from_channel(yt_handler.CHANNELS["ikakprosto"])
            video_id = video["video_id"]

            if video_id == prev_received_video_id:
                continue
            else:
                prev_received_video_id = video_id

            text = convert_dict_to_string(video)
            greet_bot.send_message(ME_CHAT_ID, text)

            prev_updated = datetime.now()

        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        if last_update.is_empty:
            continue

        print_dict(last_update.get_mess_json())

        handle_message_request(last_update, greet_bot)

        # last_update_id = last_update[Tags.UPDATE_ID]
        new_offset = last_update.id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
