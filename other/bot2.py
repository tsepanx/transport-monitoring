import telebot

from constants import BOT_TOKEN
from functions import print_dict

bot = telebot.TeleBot(BOT_TOKEN)

STICKERS_LIST = [
    "CAADAgADSgkAAnlc4glshq449fyDqBYE",
    'CAADAgADZgkAAnlc4gmfCor5YbYYRAI'
]


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, message.text + "111")


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print_dict(message)
    bot.send_message(message.chat.id, message)


def main():
    bot.polling()


if __name__ == '__main__':
    main()
