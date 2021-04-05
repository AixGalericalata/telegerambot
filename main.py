from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import time

TOKEN = '1626176954:AAFdiHbSGPA8td6gFYQx_XI-Wb6pEwJAWcs'


def echo(update, context):
    update.message.reply_text(f'Я получил сообщение {update.message.text}')


def time_handler(update, context):
    current_time = time.localtime()
    time_string = time.strftime("%H:%M:%S", current_time)
    update.message.reply_text(time_string)


def date_handler(update, context):
    current_time = time.localtime()
    time_string = time.strftime("%m/%d/%Y", current_time)
    update.message.reply_text(time_string)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(CommandHandler("time", time_handler))
    dp.add_handler(CommandHandler("date", date_handler))

    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
