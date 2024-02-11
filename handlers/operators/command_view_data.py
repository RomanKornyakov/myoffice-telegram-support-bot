from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from data.config import bot, operators_chat, db
from keyboards.inline_keyboard import inlinebuttons_view_data

router = Router()


@router.message(Command('view_data'))
async def command_view_data(message: Message):
    if message.chat.id == operators_chat:
        await message.answer('Выберите таблицу, в которой нужно посмотреть данные.',
                             reply_markup=inlinebuttons_view_data)


@router.callback_query(F.data == 'view_data_in_support')
async def view_data_in_support(callback: CallbackQuery):
    await callback.answer()

    support_list = [
        [
            InlineKeyboardButton(text='support', callback_data='support'),
        ]
    ]
    support = InlineKeyboardMarkup(inline_keyboard=support_list)
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=support)

    data = ''
    for row in db.view_data_in_support():  # создание сообщения с данными
        data += f'{str(row)}\n\n'

    if len(data) > 4096:
        for i in range(0, len(data), 4096):
            await callback.message.answer(data[i:i + 4096])
    else:
        await callback.message.answer(data[:-2])  # отправка данных из таблицы support


@router.callback_query(F.data == 'support')
async def inlinebutton_support(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == 'view_data_in_feedbacks')
async def view_data_in_feedbacks(callback: CallbackQuery):
    await callback.answer()

    feedbacks_list = [
        [
            InlineKeyboardButton(text='feedbacks', callback_data='feedbacks'),
        ]
    ]
    feedbacks = InlineKeyboardMarkup(inline_keyboard=feedbacks_list)
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=feedbacks)

    data = ''
    for row in db.view_data_in_feedbacks():  # создание сообщения с данными
        data += f'{str(row)}\n\n'

    if len(data) > 4096:
        for i in range(0, len(data), 4096):
            await callback.message.answer(data[i:i + 4096])
    else:
        await callback.message.answer(data[:-2])  # отправка данных из таблицы feedbacks


@router.callback_query(F.data == 'feedbacks')
async def inlinebutton_feedbacks(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == 'view_data_in_user_questions_to_bot')
async def view_data_in_user_questions_to_bot(callback: CallbackQuery):
    await callback.answer()

    user_questions_to_bot_list = [
        [
            InlineKeyboardButton(text='user_questions_to_bot', callback_data='user_questions_to_bot'),
        ]
    ]
    user_questions_to_bot = InlineKeyboardMarkup(inline_keyboard=user_questions_to_bot_list)
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=user_questions_to_bot)

    data = ''
    for row in db.view_data_in_user_questions_to_bot():  # создание сообщения с данными
        data += f'{str(row)}\n\n'

    if len(data) > 4096:
        for i in range(0, len(data), 4096):
            await callback.message.answer(data[i:i + 4096])
    else:
        await callback.message.answer(data[:-2])  # отправка данных из таблицы user_questions_to_bot


@router.callback_query(F.data == 'user_questions_to_bot')
async def inlinebutton_user_questions_to_bot(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery):
    await callback.answer()

    cancel_cancel_list = [
        [
            InlineKeyboardButton(text='Отменено', callback_data='cancel_cancel'),
        ]
    ]
    cancel_cancel = InlineKeyboardMarkup(inline_keyboard=cancel_cancel_list)
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=cancel_cancel)


@router.callback_query(F.data == 'cancel_cancel')
async def inlinebutton_cancel_cancel(callback: CallbackQuery):
    await callback.answer()
