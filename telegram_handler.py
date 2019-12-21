import requests

from update import Update


class TelegramApiHandler:
    GET_METHOD = 'getUpdates'
    SEND_MESSAGE_METHOD = 'sendMessage'
    SEND_IMAGE_METHOD = 'sendPhoto'
    GET_ME_METHOD = 'getMe'

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
        return self.__get_request(self.GET_ME_METHOD)

    def get_updates(self, offset=None, timeout=5):
        params = {'timeout': timeout, 'offset': offset}
        response = self.__get_request(self.GET_METHOD, params)

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
        return self.__post_request(self.SEND_MESSAGE_METHOD, params)

    def send_image(self, chat_id, photo_identifier, disable_preview=False):
        params = {'chat_id': chat_id, 'photo': photo_identifier, 'disable_web_page_preview': disable_preview}
        return self.__post_request(self.SEND_IMAGE_METHOD, params)

    def send_sticker(self, chat_id, sticker_id):
        pass  # TODO
