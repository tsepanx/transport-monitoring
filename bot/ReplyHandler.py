from enum import Enum


class ReplyHandler:
    def __init__(self, bot, chat_name, chat_id):
        self.bot = bot
        self.chat_name = chat_name
        self.chat_id = chat_id

    def reply_message(self, message):
        message_text = message.text.lower()
        if message_text == 'привет':
            return 'Привет, мой создатель'
        elif message_text == 'пока':
            return 'Прощай, создатель'
        elif message_text == 'я тебя люблю':
            self.bot.send_sticker(message.chat.id)
        else:
            self.bot.on_text_message_recieved(message.chat.id, "Example")
