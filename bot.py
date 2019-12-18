import datetime
import requests

from classes import JsonFile
from constants import BOT_TOKEN, BOT_SEND_METHOD, BOT_GET_METHOD
from functions import print_dict


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"
        # self.api_url = f'{proxy_url}bot{token}'
        print(self.api_url)

    def get_updates(self, offset=None, timeout=5):
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + BOT_GET_METHOD, params).json()

        result_json = response['result']

        JsonFile("bot_updates").write(result_json)

        return result_json

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        return requests.post(self.api_url + BOT_SEND_METHOD, params)


proxy_url = 'http://eternalvoiceproxy.duckdns.org:443/'

greet_bot = BotHandler(BOT_TOKEN)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()


def get_reply_message(chat_name, message):
    today = now.day
    hour = now.hour

    if message.lower() in greetings and today == now.day and 6 <= hour < 12:
        return f'Good morning, {chat_name}'

    elif message.lower() in greetings and today == now.day and 12 <= hour < 17:
        return f'Добрый день, {chat_name}'

    elif message.lower() in greetings and today == now.day and 17 <= hour < 23:
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

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        reply = get_reply_message(last_chat_name, last_chat_text)
        print(last_update_id, last_chat_text, last_chat_id, last_chat_name)
        print(reply)

        greet_bot.send_message(last_chat_id, reply)

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
