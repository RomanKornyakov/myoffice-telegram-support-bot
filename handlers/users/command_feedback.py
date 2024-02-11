from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from data.config import bot, operators_chat, db
from keyboards.inline_keyboard import inlinebuttons_change_feedback, inlinebutton_cancel

router = Router()


class Feedback(StatesGroup):
    feedback = State()


@router.message(Command('feedback'))
async def command_feedback(message: Message, state: FSMContext):
    if message.chat.id != operators_chat:
        try:
            await message.answer(
                f'Вы уже писали отзыв. Вот ваш прошлый отзыв:\n{db.get_feedback(message.chat.id)}\n\nХотите изменить его?',
                reply_markup=inlinebuttons_change_feedback)
        except TypeError:
            await message.answer('Напишите свой отзыв о работе бота.', reply_markup=inlinebutton_cancel)
            await state.set_state(Feedback.feedback)
            await state.update_data(type_feedback='new')


@router.message(Feedback.feedback)
async def send_feedback_to_operator(message: Message, state: FSMContext):
    await state.update_data(feedback=message.text)
    data = await state.get_data()
    type_feedback = data.get('type_feedback')
    feedback = data.get('feedback')
    if type_feedback == 'new':
        await bot.send_message(operators_chat, f'Новый отзыв от @{message.chat.username}:\n{feedback}')  # отправка отзыва в чат операторов
        db.add_feedback(message.chat.id, f'@{message.chat.username}', feedback)  # добавление отзыва в базу данных
        await bot.send_message(operators_chat,
                               'Отзыв добавлен в базу. Увидеть это можно, введя команду /view_data')
    elif type_feedback == 'change':
        await bot.send_message(operators_chat, f'Новый изменённый отзыв от @{message.chat.username}:'
                                               f'\n{feedback}\n'
                                               f'Прошлый отзыв:\n'
                                               f'{db.get_feedback(message.chat.id)}')  # отправка нового и старого отзывов в чат операторов
        db.change_feedback(message.chat.id, feedback)  # изменение отзыва в базе данных
        await bot.send_message(operators_chat,
                               'Отзыв изменен в базе. Увидеть это можно, введя команду /view_data')

    await message.answer('Спасибо за Ваш отзыв!')
    await state.clear()


@router.callback_query(F.data == 'change_feedback')
async def inlinebutton_change_feedback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    yes_list = [
        [
            InlineKeyboardButton(text='Да', callback_data='yes'),
        ]
    ]
    yes = InlineKeyboardMarkup(inline_keyboard=yes_list)
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=yes)

    await callback.message.answer('Напишите новый отзыв.', reply_markup=inlinebutton_cancel)
    await state.set_state(Feedback.feedback)
    await state.update_data(type_feedback='change')


@router.callback_query(F.data == 'not_change_feedback')
async def inlinebutton_not_change_feedback(callback: CallbackQuery):
    await callback.answer()

    no_list = [
        [
            InlineKeyboardButton(text='Нет', callback_data='no'),
        ]
    ]
    no = InlineKeyboardMarkup(inline_keyboard=no_list)
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=no)


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
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
    await state.clear()


@router.callback_query(F.data == 'cancel_cancel')
async def inlinebutton_cancel_cancel(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == 'yes')
async def inlinebutton_yes(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == 'no')
async def inlinebutton_no(callback: CallbackQuery):
    await callback.answer()
