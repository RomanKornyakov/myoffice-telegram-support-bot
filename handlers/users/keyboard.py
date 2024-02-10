from aiogram import Router, F
from aiogram.types import Message
from data.config import operators_chat

router = Router()


@router.message(F.text.lower() == 'наши контакты')
async def button_contacts(message: Message):
    if message.chat.id != operators_chat:
        await message.answer('Наш сайт: https://myoffice.ru/')


@router.message(F.text.lower() == 'о нас')
async def button_information_about_company(message: Message):
    if message.chat.id != operators_chat:
        await message.answer('МойОфис – российская IT-компания, которая разрабатывает безопасные офисные решения для общения и совместной работы с документами в облаке, '
                             'в мобильных и настольных приложениях на всех популярных ОС и платформах. '
                             'С помощью МойОфис вы можете создавать и редактировать текстовые и табличные файлы, работать с презентациями и электронной почтой.\n'
                             'Приложения в составе продуктов МойОфис: Документы, Текст, Таблица, Презентация, Почта, Календарь, Контакты и Хранилище.')
