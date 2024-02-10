from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from data.config import operators_chat
from keyboards.default_keyboard import buttons

router = Router()


@router.message(Command('start'))
async def start_message(message: Message):
    if message.chat.id != operators_chat:
        await message.answer('Добрый день! Чем могу помочь?\n'
                             'О функционале бота Вы можете узнать введя команду /help',
                             reply_markup=buttons)
