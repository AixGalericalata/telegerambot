from telegram import ReplyKeyboardMarkup
import re
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler

TOKEN = '1626176954:AAFdiHbSGPA8td6gFYQx_XI-Wb6pEwJAWcs'

novel = ['Я помню чудное мгновенье:',
         'Передо мной явилась ты',
         'Как мимолетное виденье,',
         'Как гений чистой красоты.']


def transform_string(s):
    return re.sub(r'[^\w\s]', '', s).lower()


def is_equal(s1, s2):
    return transform_string(s1) == transform_string(s2)


def start(update, context):
    context.user_data['index'] = 0
    update.message.reply_text(
        novel[context.user_data['index']])
    context.user_data['index'] += 1


def suphler(update, context):
    word = novel[context.user_data['index']].split()[0] + '...'
    update.message.reply_text(f'Подсказка:\n{word}')


suphler_handler = CommandHandler("suphler", suphler)


def check_message(update, context: CallbackContext):
    if context.user_data['index'] >= len(novel):
        update.message.reply_text(
            'Если хотите повторить, воспользуйтесь командой /start.')
        return
    user_message = update.message.text
    if is_equal(user_message, novel[context.user_data['index']]):
        context.user_data['index'] += 1
        if context.user_data['index'] == len(novel):
            update.message.reply_text(
                'Потрясающе! Если хотите повторить, воспользуйтесь командой /start.')
            return

        update.message.reply_text(
            novel[context.user_data['index']])
        context.user_data['index'] += 1
        context.dispatcher.remove_handler(suphler_handler, -1)
    else:
        update.message.reply_text(
            'Нет, не так\n'
            'Вы можете воспользоваться командой /suphler.')
        context.dispatcher.add_handler(suphler_handler, -1)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text & ~Filters.command, check_message)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
