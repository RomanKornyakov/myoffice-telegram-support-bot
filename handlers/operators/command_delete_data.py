from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from data.config import operators_chat, db
from keyboards.inline_keyboard import inlinebutton_cancel

router = Router()


class DeleteData(StatesGroup):
    id = State()


@router.message(Command('delete_data'))
async def command_delete_data(message: Message, state: FSMContext):
    if message.chat.id == operators_chat:
        await message.answer('Введите id строки, которую нужно удалить.', reply_markup=inlinebutton_cancel)
        await state.set_state(DeleteData.id)


@router.message(DeleteData.id)
async def delete_data(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    id = data.get('id')
    db.delete_data_from_support(id)  # удаление данных из таблицы support
    await message.answer('Данные удалены.\n'
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
