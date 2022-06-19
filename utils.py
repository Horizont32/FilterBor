import telebot
from telebot import util
import sqlite3

con = sqlite3.connect('chat_data.db')
cur = con.cursor()
# cur.execute('create table general_info (chatid, flag)')

chats_data = {}
forbidden_words = ('русня', 'кацап', 'оккупант', 'оккупанты', '🇺🇦', 'рашист', 'орк', 'орки')
forbidden_symbols = set('іїєґ')


def check_message(m):
    match m.content_type:
        case 'text' | "sticker" | "pinned_message":
            text = m.text.strip().lower()
        case "photo" | "audio" | 'video':
            text = m.caption.strip().lower()
        case _:
            text = ''
    try:
        flag_symbols = set(text) & forbidden_symbols
        # flag_words = any(word in text for word in forbidden_words)
        flag_words = any(word in text for word in chats_data[m.chat.id])
        return flag_words or flag_symbols
    except:
        print('Error')
        return False


def get_chatid_and_args(m):
    args = util.extract_arguments(m.text).split()
    chat_id, *words = (int(elem) if i == 0 else elem for i, elem in enumerate(args))
    return chat_id, set(words)


def check_user_status(obj, m):
    chat_id = get_chatid_and_args(m)[0]
    print(f'Chat id given {chat_id}')
    status = obj.get_chat_member(chat_id, m.from_user.id).status
    match status:
        case 'creator':
            obj.send_message(m.chat.id, 'NORM, TI SOZDAL')
            return True
        case _:
            obj.send_message(m.chat.id, 'You are not allowed to modify chat values')
            return False


def check_chat_type(m):
    return m.chat.type == 'private'


def is_in_dict(chatid):
    return chats_data.get(chatid, None) is not None


def add_word_to_data(chatid, words):
    chats_data[chatid].update(words)
