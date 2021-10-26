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
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,"Чтобы ваш бот работал как надо, следуйте четким инструкциям.\n\n1️⃣Добавьте бота в те группы, куда вы хотите рассылать сообщения.\n\n️2️⃣Отправьте пробное сообщение, чтобы ваш чат был зарегистрирован ботом.\n\nВСЕ! Ваш бот готов. Тепреь просто отправляйте сообщения боту, какие хотите отправлять в группы.")

@bot.message_handler(content_types=CONTENT_TYPES)
def get_text_messages(message):
    global i

    cursor.execute(
        """SELECT EXISTS (SELECT 1 FROM users WHERE user_id={});""".format(message.from_user.id)

    )
    if not cursor.fetchone()[0]:
        cursor.execute("""INSERT INTO users(user_id,chats_id) VALUES ({},ARRAY{})""".format(int(message.from_user.id),
                                                                                            [int(message.chat.id)]))
    else:
        cursor.execute("""SELECT chats_id FROM users WHERE user_id={}""".format(int(message.from_user.id)))
        lisr = cursor.fetchone()[0]
        if int(message.chat.id) not in lisr and int(message.chat.id)!=int(message.from_user.id):
            lisr.append(int(message.chat.id))
        cursor.execute("""UPDATE users SET chats_id=ARRAY{} WHERE user_id={}""".format(lisr, message.from_user.id))
    cursor.execute("""SELECT chats_id FROM users WHERE user_id={}""".format(int(message.from_user.id)))
    list_of_chats = cursor.fetchone()[0]
    for id in list_of_chats:
        if message.content_type == "text":
            bot.send_message(id, message.text)
        elif message.content_type == "photo":

            file_info = bot.get_file(message.json['photo'][0]['file_id'])
            downloaded_file = bot.download_file(file_info.file_path)

            src = './' + str(i) + '.jpg'
            name_of_photo.append(i)
            new_file = open(src, 'wb')

            new_file.write(downloaded_file)
            new_file.close()

            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = "./0.jpg"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            foto = open('0.jpg', 'rb')
            bot.send_photo(id, foto, caption=message.caption)
            foto.close()
            os.remove(src)
        elif message.content_type == "document":

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = './' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            new_file = open(src, 'rb')

            bot.send_document(id, new_file)
            new_file.close()
            os.remove(src)

            bot.send_document(id, new_file, caption=message.caption)
            new_file.close()
            os.remove(src)
        elif message.content_type == "sticker":
            src = './0'
            file_info = bot.get_file(message.sticker.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            new_file = open(src, 'rb')

            bot.send_sticker(id, new_file)
            new_file.close()
            os.remove(src)


bot.polling(none_stop=True)
