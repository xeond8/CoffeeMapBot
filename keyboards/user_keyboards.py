from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton

from lexicon.lexicon_eng import LEXICON_ENG
from lexicon.lexicon_ru import LEXICON_RU


def send_geolocation_keyboard(lang_code: str) -> ReplyKeyboardMarkup:
    if lang_code == 'ru':
        geo_button1: KeyboardButton = KeyboardButton(text=LEXICON_RU['author_col'], request_location=True)
    else:
        geo_button1: KeyboardButton = KeyboardButton(text=LEXICON_ENG['author_col'], request_location=True)
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(geo_button1)
    return keyboard
