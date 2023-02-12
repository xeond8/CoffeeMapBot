from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.admin_keyboards import fill_food_keyboard
from lexicon.lexicon_eng import LEXICON_ENG
from lexicon.lexicon_ru import LEXICON_RU
from services.FSM import FSMFillForm
from services.db_functions import save_to_database


async def add_coffeeshop(message: Message):
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['fill_name'])
    else:
        await message.answer(LEXICON_ENG['fill_name'])
    await FSMFillForm.fill_name.set()


async def name_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['fill_city'])
    else:
        await message.answer(LEXICON_ENG['fill_city'])
    await FSMFillForm.fill_city.set()


async def city_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['fill_address'])
    else:
        await message.answer(LEXICON_ENG['fill_address'])
    await FSMFillForm.fill_address.set()


async def address_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text.replace('-', '\-').replace('.', '\.')
    lang_code: str = message.from_user.language_code
    if lang_code == 'ru':
        await message.answer(LEXICON_RU['fill_food'], reply_markup=fill_food_keyboard(lang_code))
    else:
        await message.answer(LEXICON_ENG['fill_food'], reply_markup=fill_food_keyboard(lang_code))

    await FSMFillForm.fill_food.set()


async def food_sent(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.data == 'yes':
            data['food'] = True
        else:
            data['food'] = False
    if callback.from_user.language_code == 'ru':
        await callback.message.answer(LEXICON_RU['fill_latte'])
    else:
        await callback.message.answer(LEXICON_ENG['fill_latte'])
    await FSMFillForm.fill_latte_price.set()


async def latte_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['latte_price'] = message.text
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['fill_photo'])
    else:
        await message.answer(LEXICON_ENG['fill_photo'])
    await FSMFillForm.fill_photo.set()


async def photo_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['file_id'] = message.photo[0].file_id
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['end_fill'])
    else:
        await message.answer(LEXICON_ENG['end_fill'])

    await save_to_database(await state.get_data())

    await state.finish()


def register_admin_handlers(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(add_coffeeshop, lambda x: x.from_user.id == admin_id, commands='fillform')
    dp.register_message_handler(name_sent, lambda x: x.from_user.id == admin_id, state=FSMFillForm.fill_name)
    dp.register_message_handler(city_sent, lambda x: x.from_user.id == admin_id, state=FSMFillForm.fill_city)
    dp.register_message_handler(address_sent, lambda x: x.from_user.id == admin_id, state=FSMFillForm.fill_address)
    dp.register_callback_query_handler(food_sent, lambda x: x.from_user.id == admin_id, state=FSMFillForm.fill_food)
    dp.register_message_handler(latte_sent, lambda x: x.from_user.id == admin_id, state=FSMFillForm.fill_latte_price)
    dp.register_message_handler(photo_sent, lambda x: x.from_user.id == admin_id, content_types='photo',
                                state=FSMFillForm.fill_photo)
