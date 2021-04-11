from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler

TOKEN = '1626176954:AAFdiHbSGPA8td6gFYQx_XI-Wb6pEwJAWcs'

begin_visit = 'Начать посещение'
exit = 'Выход'
goodbye_text = 'Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!'

entering_first_hall = 'Войти в 1-ый зал'
entering_second_hall = 'Войти во 2-ой зал'
entering_third_hall = 'Войти в 3-ий зал'
entering_fourth_hall = 'Войти в 4-ый зал'
entering_fourth_hall = 'Войти в 4-ый зал'


def hall_4(update, context):
    if update.message.text == entering_first_hall:
        hall_1_keyboard = [[entering_second_hall, exit]]
        update.message.reply_text(
            'Вы входите в первый зал. В данном зале представлено первобытное искусство.',
            reply_markup=ReplyKeyboardMarkup(hall_1_keyboard, one_time_keyboard=True))
        return 1
    else:
        update.message.reply_text('Ошибка.')


def hall_3(update, context):
    if update.message.text == entering_fourth_hall:
        hall_4_keyboard = [[entering_first_hall]]
        update.message.reply_text(
            'Вы входите в четвёртый зал. В данном зале представлено искусство Древней Греции.',
            reply_markup=ReplyKeyboardMarkup(hall_4_keyboard, one_time_keyboard=True))
        return 4
    else:
        update.message.reply_text('Ошибка.')


def hall_2(update, context):
    if update.message.text == entering_third_hall:
        hall_3_keyboard = [[entering_fourth_hall]]
        update.message.reply_text(
            'Вы входите в третий зал. В данном зале представлено искусство Древнего Египта.',
            reply_markup=ReplyKeyboardMarkup(hall_3_keyboard, one_time_keyboard=True))
        return 3
    else:
        update.message.reply_text('Ошибка.')


def hall_1(update, context):
    if update.message.text == entering_second_hall:
        hall_2_keyboard = [[entering_third_hall]]
        update.message.reply_text(
            'Вы входите во второй зал. В данном зале представлено искусство Древнего Рима.',
            reply_markup=ReplyKeyboardMarkup(hall_2_keyboard, one_time_keyboard=True))
        return 2
    elif update.message.text == exit:
        update.message.reply_text(goodbye_text)
        return ConversationHandler.END
    else:
        update.message.reply_text('Ошибка.')


def entering(update, context):
    if update.message.text == begin_visit:
        hall_1_keyboard = [[entering_second_hall, exit]]
        update.message.reply_text(
            'Вы входите в первый зал. В данном зале представлено первобытное искусство.',
            reply_markup=ReplyKeyboardMarkup(hall_1_keyboard, one_time_keyboard=True))
        return 1
    elif update.message.text == exit:
        update.message.reply_text(goodbye_text)
        return ConversationHandler.END
    else:
        update.message.reply_text('Ошибка.')


def start(update, context):
    start_keyboard = [[begin_visit, exit]]
    update.message.reply_text(
        'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!',
        reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)
    )
    return 0


def stop(update, context):
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            0: [MessageHandler(Filters.text, entering)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            1: [MessageHandler(Filters.text, hall_1)],
            2: [MessageHandler(Filters.text, hall_2)],
            3: [MessageHandler(Filters.text, hall_3)],
            4: [MessageHandler(Filters.text, hall_4)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
