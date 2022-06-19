from utils import telebot
import utils

bot = telebot.TeleBot('1523365002:AAHf8bYnbIY7X_OPb1Jg2lPc9YoLJ4pxvFs', threaded=True)


@bot.message_handler(commands=['add_fword'], func=utils.check_chat_type)
def add_fword(m):
    chatid, words = utils.get_chatid_and_args(m)
    if utils.check_user_status(bot, m):
        if utils.is_in_dict(chatid):
            print(f'Words {words} have been added to the dict for {chatid=}')
            utils.add_word_to_data(chatid, words)
            print(utils.chats_data)
        else:
            utils.chats_data[chatid] = set(words)
            print(f'Created a new set of words for {chatid=}')


@bot.message_handler(content_types=["text", "sticker", "pinned_message"], func=utils.check_message)
def delete_hohol_msg(m):
    # If bot is not admin, then it will not be able to delete message.
    try:
        bot.delete_message(m.chat.id, m.message_id)
        print(f'Message {m.text} from user {m.from_user.username} {m.from_user.first_name} {m.from_user.last_name} '
              f'has been deleted in the chat {m.chat.title} with id {m.chat.id}')
    except:
        bot.send_message(m.chat.id,
                         "Please make me an admin in order for me to remove the join and leave messages on this group!")



@bot.message_handler(content_types=["photo", "audio", 'video'], func=utils.check_message)
def delete_leave_message(m):
    # If bot is the one that is being removed, it will not be able to delete the leave message.
    try:
        bot.delete_message(m.chat.id, m.message_id)
        print(f'Message {m.id} from user {m.from_user.username} {m.from_user.first_name} {m.from_user.last_name} '
              f'has been deleted in the chat {m.chat.title} with id {m.chat.id}')
    except:
        bot.send_message(m.chat.id,
                         "Please make me an admin in order for me to remove the join and leave messages on this group!")





if __name__ == '__main__':
    bot.infinity_polling()