from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# кнопки
buttons_list = [
    [
        KeyboardButton(text='О нас'),
        KeyboardButton(text='Наши контакты')
    ]
]
buttons = ReplyKeyboardMarkup(keyboard=buttons_list, resize_keyboard=True)
