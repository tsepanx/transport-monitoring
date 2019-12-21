from datetime import datetime, timedelta

import requests

from functions import convert_dict_to_string, get_message_with_video_data
from private_keys import MY_TELEGRAM_BOT_TOKEN, MY_YOUTUBE_API_KEY
from telegram_handler import TelegramApiHandler
from update import Update
from youtube import YoutubeHandler

BOT_YOUTUBE_COMMAND = 'ping_youtube'

ME_CHAT_ID = 325805942
super_bot = TelegramApiHandler(MY_TELEGRAM_BOT_TOKEN)


def handle_message_request(last: Update, bot: TelegramApiHandler):
    if last.chat_type == "group" and "@" not in last.message_text:
        return

    # if last.message_text[0] == "/":
    #     command = last.message_text[1:]
    #     if command == BOT_YOUTUBE_COMMAND:
    #         send_yt_data(bot, last.chat_id, web_handler, )

    if last.message_text or last.sticker_id:
        bot.send_message(
            last.chat_id,
            last.get_reply())
    else:
        bot.send_message(
            last.chat_id,
            convert_dict_to_string(last.get_filtered_json()))


def send_yt_data(bot: TelegramApiHandler, chat_id, web_handler: YoutubeHandler, channels_update_metadata):
    bot.send_message(chat_id, "Gathering information in youtube")
    bot.send_message(chat_id, convert_dict_to_string(channels_update_metadata))
    for channel_id in channels_update_metadata:
        current_data = channels_update_metadata[channel_id]

        video = web_handler.get_latest_video_from_channel(channel_id)

        if not video:
            continue

        video_id = video["video_id"]
        print(video)

        if video_id == current_data[1]:
            return

        if not video:
            print(channel_id)
            continue

        preview_url = video["video_thumbnail"]
        text_to_send = get_message_with_video_data(video)

        bot.send_image(chat_id, preview_url)
        bot.send_message(chat_id, text_to_send, disable_preview=True)

        # updating values in channels dict
        channels_update_metadata[channel_id] = [datetime.now(), video_id]


def is_ping_needed():
    now = datetime.now()
    h = now.hour
    hours = [*range(1, 9)]

    return h not in hours


def main():
    yt_request_timeout = 600
    yt_handler = YoutubeHandler(
        MY_YOUTUBE_API_KEY,
        timedelta(days=3))

    channels_last_data = {}  # [datetime.now()], video_id
    for chan in yt_handler.CHANNELS.values():
        channels_last_data[chan] = [None, None]

    prev_updated = datetime.now()

    new_offset = None

    while True:
        super_bot.get_updates(new_offset)
        last_update = super_bot.get_last_update()

        current_command = None

        if not last_update.is_empty:
            print(convert_dict_to_string(last_update.get_filtered_json()))
            current_command = last_update.command if last_update.is_command else None

            handle_message_request(last_update, super_bot) if not current_command else None

            new_offset = last_update.id + 1

        from_last_update = datetime.now() - timedelta(seconds=yt_request_timeout)
        if (is_ping_needed() and from_last_update >= prev_updated) \
                or current_command == BOT_YOUTUBE_COMMAND:

            print(convert_dict_to_string(channels_last_data))

            try:
                send_yt_data(super_bot, ME_CHAT_ID, yt_handler, channels_last_data)
                prev_updated = datetime.now()
            except requests.HTTPError as e:
                arr = (e.strerror, e.response, e.request)

                print(*arr, sep='\n')
                super_bot.send_message(ME_CHAT_ID, '\n'.join(arr))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
