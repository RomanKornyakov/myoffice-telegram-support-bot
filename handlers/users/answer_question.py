from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from data.config import bot, operators_chat, operators
from aiogram.fsm.state import StatesGroup, State
from utils.comparison import comparison
from database import Database
from keyboards.inline_keyboard import inlinebuttons_need_operator, inlinebutton_otvet_operator
from keyboards.default_keyboard import buttons
from utils.operator_selection import get_operator

router = Router()

db = Database('database/myoffice_database.db')


class OperatorCall(StatesGroup):
    waiting_operator = State()
    entering_id = State()
    call = State()


@router.message(F.text)
async def answer_to_question(message: Message):  # ответ на вопрос пользователя
    if message.chat.id != operators_chat:
        try:
            answer_id = comparison(message.text.lower(), db.get_questions())

            await message.answer(db.get_answer(answer_id), reply_markup=buttons)
            db.add_user_question_to_bot(message.chat.id, f'@{message.chat.username}', message.text,
                                        db.get_answer(answer_id))
        except TypeError:
            db.add_user_question_to_bot(message.chat.id, f'@{message.chat.username}', message.text)
            await message.answer('Я не могу ответить на этот вопрос. Позвать оператора?', reply_markup=inlinebuttons_need_operator)


@router.callback_query(F.data == 'need_operator')
async def inlinebutton_need_operator(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    yes_list = [
        [
            InlineKeyboardButton(text='Да', callback_data='yes'),
        ]
    ]
    yes = InlineKeyboardMarkup(inline_keyboard=yes_list)
    await bot.edit_message_reply_markup(callback.message.chat.id,
                                        callback.message.message_id,
                                        reply_markup=yes)

    operator_id = await get_operator(list(operators.keys()))

    if not operator_id:
        await callback.message.answer('К сожалению, сейчас нет свободных операторов. Попробуйте позже.')
        return

    cancel_list = [
        [
            InlineKeyboardButton(text='Я передумал(а)', callback_data='cancel'),
        ]
    ]
    cancel = InlineKeyboardMarkup(inline_keyboard=cancel_list)

    await callback.message.answer('Ожидайте ответа оператора!', reply_markup=cancel)

    await state.update_data(second_id=operator_id)

    await state.set_state(OperatorCall.waiting_operator)

    await bot.send_message(operators_chat, 'Был вызван оператор!\n'
                                           f'Оператор: {operators[operator_id]}\n'
                                           f'Пользователь: @{callback.message.chat.username}\n')

    await bot.send_message(operator_id, 'Был вызван оператор!\n'
                                        f'Пользователь: @{callback.message.chat.username}\n'
                                        f'Id обращения: <code>{db.add_appeal_to_operator(callback.message.chat.id, callback.message.chat.username)}</code>',
                           reply_markup=inlinebutton_otvet_operator)


@router.callback_query(F.data == 'not_need_operator')
async def inlinebutton_not_need_operator(callback: CallbackQuery):
    await callback.answer()

    no_list = [
        [
            InlineKeyboardButton(text='Нет', callback_data='no')
        ]
    ]
    no = InlineKeyboardMarkup(inline_keyboard=no_list)
    await bot.edit_message_reply_markup(callback.message.chat.id,
                                        callback.message.message_id,
                                        reply_markup=no)

    await callback.message.answer('Тогда можете задать мне другой вопрос.')


@router.callback_query(F.data == 'yes')
async def inlinebutton_yes(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == 'no')
async def inlinebutton_no(callback: CallbackQuery):
    await callback.answer()
