from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from data.config import bot, operators_chat, db
from keyboards.inline_keyboard import inlinebuttons_change_data, inlinebutton_cancel

router = Router()


class ChangeData(StatesGroup):
    id = State()
    column = State()
    new_data = State()


@router.message(Command('change_data'))
async def command_change_data(message: Message, state: FSMContext):
    if message.chat.id == operators_chat:
        await message.answer('Введите id строки, которую нужно изменить.', reply_markup=inlinebutton_cancel)
        await state.set_state(ChangeData.id)


@router.message(ChangeData.id)
async def choose_column(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer('Выберите какие данные нужно изменить.',
                         reply_markup=inlinebuttons_change_data)
    await state.set_state(ChangeData.column)


@router.callback_query(F.data == 'change_id_in_support', ChangeData.column)
async def change_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    id_list = [
        [
            InlineKeyboardButton(text='id', callback_data='id'),
        ]
    ]
    id = InlineKeyboardMarkup(inline_keyboard=id_list)

    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=id)

    await state.update_data(column='id')
    await callback.message.answer('Введите новые данные.', reply_markup=inlinebutton_cancel)
    await state.set_state(ChangeData.new_data)


@router.callback_query(F.data == 'change_questions_in_support', ChangeData.column)
async def change_questions(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    questions_list = [
        [
            InlineKeyboardButton(text='questions', callback_data='questions'),
        ]
    ]
    questions = InlineKeyboardMarkup(inline_keyboard=questions_list)
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=questions)

    await state.update_data(column='questions')
    await callback.message.answer('Введите новые данные.', reply_markup=inlinebutton_cancel)
    await state.set_state(ChangeData.new_data)


@router.callback_query(F.data == 'change_answer_in_support', ChangeData.column)
async def change_answer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    answer_list = [
        [
            InlineKeyboardButton(text='answer', callback_data='answer'),
        ]
    ]
    answer = InlineKeyboardMarkup(inline_keyboard=answer_list)
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=answer)

    await state.update_data(column='answer')
    await callback.message.answer('Введите новые данные.', reply_markup=inlinebutton_cancel)
    await state.set_state(ChangeData.new_data)


@router.message(ChangeData.new_data)
async def change_data(message: Message, state: FSMContext):
    await state.update_data(new_data=message.text)
    data = await state.get_data()
    column = data.get('column')
    new_data = data.get('new_data')
    id = data.get('id')
    if column == 'id':
        db.change_id_in_support(new_data, id)  # изменение колонки id в таблице support
    elif column == 'questions':
        db.change_questions_in_support(new_data, id)  # изменение колонки questions в таблице support
    elif column == 'answer':
        db.change_answer_in_support(new_data, id)  # изменение колонки answer в таблице support
    await message.answer('Данные изменены.\n'
                         'Увидеть изменения можно, введя команду /view_data.')
    await state.clear()


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
