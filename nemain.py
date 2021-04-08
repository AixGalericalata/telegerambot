from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler

reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
TOKEN = '1626176954:AAFdiHbSGPA8td6gFYQx_XI-Wb6pEwJAWcs'


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def start(update, context):
    context.user_data['locality'] = None
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?\n"
        "Если не хотите отвечать, напишите команду /skip.")

    return 1


def first_response(update, context):
    context.user_data['locality'] = update.message.text
    update.message.reply_text(
        "Какая погода в городе {0}?".format(
            context.user_data['locality']))
    return 2


def second_response(update, context):
    weather = update.message.text
    if context.user_data['locality']:
        update.message.reply_text(
            "Спасибо за участие в опросе! Привет, {0}!".format(
                context.user_data['locality']))
    else:
        update.message.reply_text(
            "Спасибо за участие в опросе!")

    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text(
        "Пока.")
    return ConversationHandler.END


def skip(update, context):
    update.message.reply_text(
        'Какая погода у вас за окном?')
    return 2


def address(update, context):
    update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


def phone(update, context):
    update.message.reply_text("Телефон: +7(495)776-3030")


def site(update, context):
    update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("close", close_keyboard))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [CommandHandler('skip', skip),
                MessageHandler(Filters.text & ~Filters.command, first_response,
                               pass_user_data=True),
                ],
            2: [MessageHandler(Filters.text & ~Filters.command, second_response,
                               pass_user_data=True)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
