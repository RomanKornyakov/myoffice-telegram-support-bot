from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from data.config import operators_chat, db
from keyboards.inline_keyboard import inlinebutton_cancel

router = Router()


class AddData(StatesGroup):
    questions = State()
    answer = State()


@router.message(Command('add_data'))
async def command_add_data(message: Message, state: FSMContext):
    if message.chat.id == operators_chat:
        await message.answer('Введите данные для столбца questions.', reply_markup=inlinebutton_cancel)
        await state.set_state(AddData.questions)


@router.message(AddData.questions)
async def add_questions_to_support(message: Message, state: FSMContext):
    await state.update_data(questions=message.text)
    await message.answer('Введите данные для столбца answers.', reply_markup=inlinebutton_cancel)
    await state.set_state(AddData.answer)


@router.message(AddData.answer)
async def add_answer_to_support(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    questions = data.get('questions')
    answer = data.get('answer')
    db.add_data_to_support(questions, answer)  # добавление данных в таблицу support
    await message.answer('Данные добавлены.\n'
                         'Увидеть их можно, введя команду /view_data.')
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
