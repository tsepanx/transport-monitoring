from constants import Tags
from functions import print_dict, convert_dict_to_string
from datetime import datetime


class Update:
    def __init__(self, update_json: dict, debug=False):

        self.type = None

        self.is_empty = True if not update_json or "edited_message" in update_json else False
        if self.is_empty:
            return

        if debug:
            print_dict(update_json)
        self.__json = update_json

        self.id = update_json["update_id"]

        message = update_json[Tags.MESSAGE]
        chat = message[Tags.CHAT]
        author = message["from"]

        self.chat_id = chat['id']

        self.chat_type = chat["type"]
        self.chat_title = chat["title"] if self.chat_type == "group" else chat["first_name"]

        self.author_username = author['username']
        self.author_name = (
            author["first_name"],
            author["last_name"]
        )

        self.sent_time = message["date"]

        self.message_text = message[Tags.TEXT] if Tags.TEXT in message else None

        if 'entities' in message:
            entities = message['entities']

            self.is_command = entities[0]['type'] == 'bot_command'
            if self.is_command and self.message_text:
                self.command = self.message_text[1:]
            else:
                self.command = None
        else:
            self.is_command = False

        if Tags.STICKER in message:
            sticker = message[Tags.STICKER]
            self.sticker_set_name = sticker["set_name"]
            self.sticker_id = sticker["file_id"]
        else:
            self.sticker_id, self.sticker_set_name = None, None

    def get_filtered_json(self):
        res = {}

        for tag in self.__json:
            if tag not in ["from", "chat"]:
                res[tag] = self.__json[tag]

        return res

    def __get_reply_on_text(self):
        now = datetime.now()
        hour = now.hour

        greetings = ('здравствуй', 'привет', 'ку', 'здорово', 'hi', 'hello')

        if self.message_text.lower() in greetings:
            if 6 <= hour < 12:
                return f'Good morning, {self.author_name[0]}'

            elif 12 <= hour < 17:
                return f'Добрый день, {self.author_name[0]}'

            elif 17 <= hour < 23:
                return f'Good evening, {self.author_name[0]}'
        else:
            return convert_dict_to_string(self.get_filtered_json()) + "\n@" + self.author_username
            # return f"Sorry, I don't understand you, {self.author_name[0]}"

    def __get_reply_on_command(self, commands_list=None):
        if commands_list and self.message_text[1:] not in commands_list:
            return

    def get_reply(self):
        # if self.is_command:
        #     return self.__get_reply_on_command()
        if self.message_text:
            return self.__get_reply_on_text()
        elif self.sticker_id:
            return self.sticker_set_name + "\n" + self.sticker_id
