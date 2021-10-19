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

    cursor.execute(
        """SELECT EXISTS (SELECT 1 FROM users WHERE user_id={});""".format(message.user_id)

    )
    if cursor.fetchone()[0]:
        cursor.execute("""INSERT INTO users(user_id,chats_id) VALUES ({},ARRAY{})""".format(int(message.user_id),[message.chat_id]))
    else:
        cursor.execute("""SELECT chats_id FROM users WHERE chat_id={}""".format(int(message.user_id)))


    list_of_chats = []
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
            foto = open('0.jpg', 'rb')
            bot.send_photo(id, foto)
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
    if message.chat.id not in list_of_chats:
        list_of_chats.append(message.chat.id)


bot.polling(none_stop=True)
