# -*- coding: utf-8 -*-

import telebot
import os
import psycopg2
from config import host, user, password, db_name

connection = psycopg2.connect(host=host,
                              user=user,
                              password=password,
                              database=db_name)
connection.autocommit = True
cursor = connection.cursor()

bot = telebot.TeleBot('2039868360:AAE9y-GNxzx3LeRyY6MOYGMokH2TDFwIN7A')
CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]
name_of_photo = []
i = 0


@bot.message_handler(content_types=CONTENT_TYPES)
def get_text_messages(message):
    global i
    print(message)

bot.polling(none_stop=True)
