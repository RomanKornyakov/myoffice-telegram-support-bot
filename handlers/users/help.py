from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from data.config import operators_chat
from keyboards.default_keyboard import buttons

router = Router()


@router.message(Command('help'))
async def command_help(message: Message):
    if message.chat.id == operators_chat:
        await message.answer('Нужные команды:\n'
                             '/view_data - просмотр данных из таблиц\n'
                             '/add_data - добавление данных в таблицу support\n'
                             '/delete_data - удаление данных из таблицы support\n'
                             '/change_data - изменение данных в таблице support')
    else:
        await message.answer('Как же работает бот? Вы отправляете ему свой вопрос, и он отвечает на него. '
                             'Если вас не устраивает ответ бота, или если бот не смог ответить на ваш вопрос, '
                             'то вы можете позвать оператора командой /operator. Для вашего удобства в боте есть меню команд и кнопок.',
                             reply_markup=buttons)
