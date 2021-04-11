from telegram.ext import Updater, MessageHandler, Filters
import requests
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup
import time
import random

TOKEN = '1626176954:AAFdiHbSGPA8td6gFYQx_XI-Wb6pEwJAWcs'


def get_ll_spn(toponym):
    ll = toponym['Point']['pos'].replace(' ', ',')
    envelope = toponym['boundedBy']['Envelope']
    lower_corner_pos = envelope['lowerCorner'].split()
    lower_corner_pos = list(map(lambda x: float(x), lower_corner_pos))

    upper_corner_pos = envelope['upperCorner'].split()
    upper_corner_pos = list(map(lambda x: float(x), upper_corner_pos))

    spn = f"{upper_corner_pos[0] - lower_corner_pos[0]},{upper_corner_pos[1] - lower_corner_pos[1]}"

    return ll, spn


def geocoder(update, context):
    geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": update.message.text
    })
    if not response:
        update.message.reply_text(f'Произошла ошибка:\n{response.reason}')
        return

    feature_member = response.json()["response"]["GeoObjectCollection"][
        "featureMember"]

    if not feature_member:
        update.message.reply_text(f'Ничего не найдено.')
        return

    toponym = feature_member[0]["GeoObject"]

    name = toponym['name']
    ll, spn = get_ll_spn(toponym)
    #  ll = '30.620070,60.753630'
    #  spn = '0.01,0.01'

    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={ll},pm2dom"
    context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption=name
    )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, geocoder)
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
