from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_city = State()
    fill_address = State()
    fill_description = State()
    fill_rating = State()
    fill_photo = State()
