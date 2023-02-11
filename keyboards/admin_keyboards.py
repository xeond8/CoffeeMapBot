from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def fill_food_keyboard(lang_code: str):
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    if lang_code == 'ru':
        yes_button: InlineKeyboardButton = InlineKeyboardButton(text='Да', callback_data='yes')
        no_button: InlineKeyboardButton = InlineKeyboardButton(text='Нет', callback_data='no')
    else:
        yes_button: InlineKeyboardButton = InlineKeyboardButton(text='Yes', callback_data='yes')
        no_button: InlineKeyboardButton = InlineKeyboardButton(text='No', callback_data='no')
    return keyboard.add(yes_button, no_button)
