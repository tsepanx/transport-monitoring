import datetime

import requests

from constants import BOT_TOKEN, BOT_SEND_METHOD, BOT_GET_METHOD, Tags
from functions import print_dict, conver_dict_to_string


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"
        # self.api_url = f"http://my-telegram-proxy.server/bot{token}/"
        # self.api_url = f'{proxy_url}bot{token}'
        print(self.api_url)

    def get_updates(self, offset=None, timeout=5):
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + BOT_GET_METHOD, params).json()

        result_json = response['result']
        # JsonFile("bot_updates").write(result_json)

        return result_json

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update

    def send_text_reply(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        send_url = self.api_url + BOT_SEND_METHOD
        print(send_url, "POST")

        return requests.post(send_url, params)

    def send_sticker_reply(self, chat_id, sticker_id):
        pass


greet_bot = BotHandler(BOT_TOKEN)
greetings = ('здравствуй', 'привет', 'ку', 'здорово', 'hi', 'hello')
now = datetime.datetime.now()


def handle_message_request(request_json: dict, bot: BotHandler):
    message = request_json[Tags.MESSAGE]
    chat = message[Tags.CHAT]

    last_chat_id = chat['id']
    last_chat_name = chat['first_name']

    if Tags.TEXT in message:
        sent_mess = message[Tags.TEXT]
        reply = get_reply_on_text(last_chat_name, sent_mess)

        print(sent_mess, reply)

        bot.send_text_reply(
            last_chat_id,
            reply
        )

    elif "sticker" in message:
        sticker = message["sticker"]

        sticker_set_name = sticker["set_name"]
        sticker_id = sticker["file_id"]

        reply_text = sticker_set_name + "\n" + sticker_id

        bot.send_text_reply(
            last_chat_id,
            reply_text
        )

        return

    else:
        bot.send_text_reply(
            last_chat_id,
            conver_dict_to_string(request_json))


def get_reply_on_text(chat_name, message):
    today = now.day
    hour = now.hour

    if message.lower() in greetings:
        if today == now.day and 6 <= hour < 12:
            return f'Good morning, {chat_name}'

        elif today == now.day and 12 <= hour < 17:
            return f'Добрый день, {chat_name}'

        elif today == now.day and 17 <= hour < 23:
            return f'Good evening, {chat_name}'
    else:
        return f"Sorry, I don't understand you, {chat_name}"


def main():
    new_offset = None

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        print_dict(last_update)

        if not last_update:
            continue

        handle_message_request(last_update, greet_bot)

        last_update_id = last_update[Tags.UPDATE_ID]
        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
