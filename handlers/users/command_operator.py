from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from data.config import bot, dp, operators_chat, operators, db
from keyboards.inline_keyboard import inlinebuttons_start_chat_with_operator, inlinebutton_otvet_operator, inlinebutton_cancel_operator, inlinebutton_cancel_user
from utils.operator_selection import get_operator

router = Router()


class OperatorCall(StatesGroup):
    waiting_operator = State()
    entering_id = State()
    call = State()


@router.message(Command('operator'))
async def command_operator(message: Message):
    if message.chat.id != operators_chat:
        await message.answer('Хотите связаться с оператором? Нажмите кнопку ниже!',
                             reply_markup=inlinebuttons_start_chat_with_operator)


# вызов оператора
@router.callback_query(F.data == 'start_chat_with_operator')
async def call_operator(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    operator_id = await get_operator(list(operators.keys()))

    if not operator_id:
        await callback.message.edit_text('К сожалению, сейчас нет свободных операторов. Попробуйте позже.')
        return

    cancel_start_list = [
        [
            InlineKeyboardButton(text='Я передумал(а)', callback_data='cancel_start'),
        ]
    ]
    cancel_start = InlineKeyboardMarkup(inline_keyboard=cancel_start_list)

    await callback.message.edit_text('Ожидайте ответа оператора!', reply_markup=cancel_start)

    await state.update_data(second_id=operator_id)

    await state.set_state(OperatorCall.waiting_operator)

    await bot.send_message(operators_chat, 'Был вызван оператор!\n'
                                           f'Оператор: {operators[operator_id]}\n'
                                           f'Пользователь: @{callback.message.chat.username}\n')

    await bot.send_message(operator_id, 'Был вызван оператор!\n'
                                        f'Пользователь: @{callback.message.chat.username}\n'
                                        f'Id обращения: <code>{db.add_appeal_to_operator(callback.message.chat.id, callback.message.chat.username)}</code>',
                           reply_markup=inlinebutton_otvet_operator)


@router.callback_query(F.data == 'not_start_chat_with_operator')
async def inlinebutton_not_call_operator(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()


@router.callback_query(F.data == 'cancel_start')
async def inlinebutton_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    second_id = data.get('second_id')

    await bot.send_message(operators_chat, f'@{callback.message.chat.username} закончил(а) звонок.')
    await bot.send_message(second_id, f'@{callback.message.chat.username} закончил(а) звонок.')

    await callback.message.edit_text('Общение завершено!')
    await state.clear()


@router.callback_query(F.data == 'otvet_operator')
async def entering_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id)

    await callback.message.answer('Введите id обращения.')

    await state.set_state(OperatorCall.entering_id)


@router.message(OperatorCall.entering_id)
async def operator_call(message: Message, state: FSMContext):
    second_id = db.get_user_id_from_appeals_to_operators(int(message.text))

    user_state: FSMContext = FSMContext(
        storage=dp.storage,
        key=StorageKey(
            chat_id=second_id,
            user_id=second_id,
            bot_id=bot.id))

    await user_state.set_state(OperatorCall.call)
    await state.set_state(OperatorCall.call)

    await state.update_data(second_id=second_id)

    await bot.send_message(second_id, 'Оператор подключился! Можете задавать ему свой вопрос.\n'
                                      'Если хотите завершить общение, нажмите кнопку ниже.', reply_markup=inlinebutton_cancel_user)

    await message.answer('Вы на связи с пользователем!\n'
                         'Для отмены нажмите кнопку ниже', reply_markup=inlinebutton_cancel_operator)


@router.callback_query(F.data == 'cancel_operator')
async def cancel_from_operator(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text('Сеанс завершен!')

    data = await state.get_data()
    second_id = data.get('second_id')
    user_state: FSMContext = FSMContext(
        storage=dp.storage,
        key=StorageKey(
            chat_id=second_id,
            user_id=second_id,
            bot_id=bot.id))
    user_state_str = str(await user_state.get_state())

    if user_state_str != 'None':
        await bot.send_message(second_id, 'Оператор завершил сеанс!')

        await state.clear()
        await user_state.clear()


@router.callback_query(F.data == 'cancel_user')
async def cancel_from_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text('Общение завершено!')
    state_str = str(await state.get_state())
    if state_str != 'None':
        data = await state.get_data()
        second_id = data.get('second_id')

        await bot.send_message(second_id, 'Пользователь завершил сеанс!')

        operator_state: FSMContext = FSMContext(
            storage=dp.storage,
            key=StorageKey(
                chat_id=second_id,
                user_id=second_id,
                bot_id=bot.id))

        await state.clear()
        await operator_state.clear()
