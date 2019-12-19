import telebot
from random import randint

from constants import BOT_TOKEN
from functions import print_dict

bot = telebot.TeleBot(BOT_TOKEN)
# telebot.apihelper.proxy = {'https': 'socks5://eternalvoiceproxy.duckdns.org:443'}
telebot.apihelper.proxy = {'https': 'socks5://eternalvoiceproxy.duckdns.org:443'}

STICKERS_LIST = [
    "CAADAgADSgkAAnlc4glshq449fyDqBYE",
    'CAADAgADZgkAAnlc4gmfCor5YbYYRAI'
]


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types=['text'])
def send_text(message):
    message_text = message.text.lower()
    if message_text == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message_text == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message_text == 'я тебя люблю':
        bot.send_sticker(message.chat.id, STICKERS_LIST[randint(0, len(STICKERS_LIST))])
    else:
        bot.send_message(message.chat.id, "Example")


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print_dict(message)
    bot.send_message(message.chat.id, message)


bot.polling()
