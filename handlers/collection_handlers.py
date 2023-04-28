from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon_eng import LEXICON_ENG
from lexicon.lexicon_ru import LEXICON_RU
from services.FSM import FSMFillForm
from services.db_functions import save_to_database, update_text, print_entry


async def add_coffeeshop(message: Message):
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['fill_name'])
    else:
        await message.answer(LEXICON_ENG['fill_name'])
    await FSMFillForm.fill_name.set()


async def name_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = update_text(message.text)
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['fill_city'])
    else:
        await message.answer(LEXICON_ENG['fill_city'])
    await FSMFillForm.fill_city.set()


async def city_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = update_text(message.text)
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['fill_address'])
    else:
        await message.answer(LEXICON_ENG['fill_address'])
    await FSMFillForm.fill_address.set()


async def address_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = update_text(message.text)
    lang_code: str = message.from_user.language_code
    if lang_code == 'ru':
        await message.answer(LEXICON_RU['fill_description'])
    else:
        await message.answer(LEXICON_ENG['fill_description'])

    await FSMFillForm.fill_description.set()


async def description_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = update_text(message.text)
    if message.from_user.language_code == 'ru':
        await message.answer(LEXICON_RU['fill_rating'])
    else:
        await message.answer(LEXICON_ENG['fill_rating'])
    await FSMFillForm.fill_rating.set()


async def rating_sent(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['rating'] = update_text(message.text)
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

    await save_to_database(await state.get_data(), str(message.from_user.id))

    await check_success(message, state)

    await state.finish()


async def check_success(message: Message, state: FSMContext):
    async with state.proxy() as data:
        name = data['name']
    string, imag = print_entry((name, 0), "ru", message.from_user.id)
    await message.answer_photo(imag, caption=string)


def register_collection_handlers(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(add_coffeeshop, commands='add')
    dp.register_message_handler(name_sent, state=FSMFillForm.fill_name)
    dp.register_message_handler(city_sent, state=FSMFillForm.fill_city)
    dp.register_message_handler(address_sent, state=FSMFillForm.fill_address)
    dp.register_message_handler(description_sent, state=FSMFillForm.fill_description)
    dp.register_message_handler(rating_sent, state=FSMFillForm.fill_rating)
    dp.register_message_handler(photo_sent, content_types='photo',
                                state=FSMFillForm.fill_photo)
