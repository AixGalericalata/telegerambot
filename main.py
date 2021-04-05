from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup
import time
import random

TOKEN = '1626176954:AAFdiHbSGPA8td6gFYQx_XI-Wb6pEwJAWcs'

start_keyboard = [['/dice', '/timer']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

close_keyboard = [['/close']]
close_markup = ReplyKeyboardMarkup(close_keyboard, one_time_keyboard=True)


def draw_one_dice():
    return str(random.randint(1, 6))


def draw_two_dices():
    return f"{random.randint(1, 6)}, {random.randint(1, 6)}"


def draw_big_dice():
    return str(random.randint(1, 20))


time_dict = {'30 секунд': 3, '1 минута': 60, '5 минут': 300}
dice_dict = {'Кинуть один шестигранный кубик': draw_one_dice,
             'Кинуть 2 шестигранных кубика одновременно': draw_two_dices,
             'Кинуть 20-гранный кубик': draw_big_dice}

dice_keyboard = list(dice_dict.keys())
dice_keyboard.append('Вернуться назад')
dice_keyboard = list(map(lambda x: [x], dice_keyboard))
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)

timer_keyboard = list(time_dict.keys())
timer_keyboard.append('Вернуться назад')
timer_keyboard = list(map(lambda x: [x], timer_keyboard))
timer_markup = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def start(update, context):
    update.message.reply_text(
        "Я JustBot. Чем сегодня займётесь?",
        reply_markup=start_markup
    )


def timer(update, context):
    update.message.reply_text(
        "Хотите засечь время?",
        reply_markup=timer_markup
    )


def dice(update, context):
    update.message.reply_text(
        "Хотите кинуть кубик?",
        reply_markup=dice_markup
    )


def close(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(
        str(chat_id),
        context
    )
    update.message.reply_text(
        "Таймер сброшен. Хотите засечь время?" if job_removed else 'Таймер не запущен.',
        reply_markup=timer_markup
    )


def set_my_timer(update, context, number, msg):
    chat_id = update.message.chat_id
    try:
        due = number
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context={'chat_id': chat_id, 'due': msg},
            name=str(chat_id)
        )
        text = f'Засек {msg}.'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text, reply_markup=close_markup)

    except (IndexError, ValueError):
        update.message.reply_text('Ошибка.')


def task(context):
    job = context.job
    context.bot.send_message(job.context['chat_id'], text=f'{job.context["due"]} истекло')


def echo(update, context):
    text = update.message.text
    if text == 'Вернуться назад':
        start(update, context)
        return
    func = dice_dict.get(text)
    if func:
        update.message.reply_text(func())
        return
    number = time_dict.get(text)
    if number:
        set_my_timer(update, context, number, text)
        return
    update.message.reply_text(f'Я получил сообщение {text}')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("close", close))

    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
