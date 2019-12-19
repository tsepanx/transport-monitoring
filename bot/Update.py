from constants import Tags
from functions import print_dict


class Update:
    def __init__(self, update_json: dict):
        self.is_empty = True if not update_json or "edited_message" in update_json else False
        if self.is_empty:
            return

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

        if Tags.STICKER in message:
            sticker = message[Tags.STICKER]
            self.sticker_set_name = sticker["set_name"]
            self.sticker_id = sticker["file_id"]

    def get_mess_json(self):
        res = {}

        for tag in self.__json:
            if tag not in ["from", "chat"]:
                res[tag] = self.__json[tag]

        return res
