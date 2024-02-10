from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# inline кнопки для вызова оператора, если бот не смог ответить
inlinebuttons_list_need_operator = [
    [
        InlineKeyboardButton(text='Да', callback_data='need_operator'),
        InlineKeyboardButton(text='Нет', callback_data='not_need_operator')
    ]
]
inlinebuttons_need_operator = InlineKeyboardMarkup(inline_keyboard=inlinebuttons_list_need_operator)

# inline кнопки для изменения отзыва
inlinebuttons_list_change_feedback = [
    [
        InlineKeyboardButton(text='Да', callback_data='change_feedback'),
        InlineKeyboardButton(text='Нет', callback_data='not_change_feedback')
    ]
]
inlinebuttons_change_feedback = InlineKeyboardMarkup(inline_keyboard=inlinebuttons_list_change_feedback)

# inline кнопки для просмотра данных в таблицах
inlinebuttons_list_view_data = [
    [
        InlineKeyboardButton(text='support', callback_data='view_data_in_support'),
        InlineKeyboardButton(text='feedbacks', callback_data='view_data_in_feedbacks')
    ],
    [
        InlineKeyboardButton(text='user_questions_to_bot', callback_data='view_data_in_user_questions_to_bot')
    ],
    [
        InlineKeyboardButton(text='Отмена', callback_data='cancel')
    ]
]
inlinebuttons_view_data = InlineKeyboardMarkup(inline_keyboard=inlinebuttons_list_view_data)

# inline кнопки для изменения данных в таблице support
inlinebuttons_list_change_data = [
    [
        InlineKeyboardButton(text='id', callback_data='change_id_in_support'),
        InlineKeyboardButton(text='questions', callback_data='change_questions_in_support'),
        InlineKeyboardButton(text='answer', callback_data='change_answer_in_support')
    ],
    [
        InlineKeyboardButton(text='Отмена', callback_data='cancel')
    ]
]
inlinebuttons_change_data = InlineKeyboardMarkup(inline_keyboard=inlinebuttons_list_change_data)

# inline кнопки для связи с оператором для пользователя
inlinebuttons_list_start_chat_with_operator = [
    [
        InlineKeyboardButton(text='Связаться с оператором', callback_data='start_chat_with_operator')
    ],
    [
        InlineKeyboardButton(text='Я передумал(а)', callback_data='not_start_chat_with_operator')
    ]
]
inlinebuttons_start_chat_with_operator = InlineKeyboardMarkup(inline_keyboard=inlinebuttons_list_start_chat_with_operator)

# inline кнопка для ответа пользователю для оператора
inlinebutton_list_otvet_operator = [
    [
        InlineKeyboardButton(text='Ответить пользователю', callback_data='otvet_operator')
    ]
]
inlinebutton_otvet_operator = InlineKeyboardMarkup(inline_keyboard=inlinebutton_list_otvet_operator)

# inline кнопка для завершения звонка с оператором для оператора
inlinebutton_list_cancel_operator = [
    [
        InlineKeyboardButton(text='Завершить общение', callback_data='cancel_operator')
    ]
]
inlinebutton_cancel_operator = InlineKeyboardMarkup(inline_keyboard=inlinebutton_list_cancel_operator)

# inline кнопка для завершения звонка с оператором для пользователя
inlinebutton_list_cancel_user = [
    [
        InlineKeyboardButton(text='Завершить общение', callback_data='cancel_user')
    ]
]
inlinebutton_cancel_user = InlineKeyboardMarkup(inline_keyboard=inlinebutton_list_cancel_user)

# inline кнопка отмены
inlinebutton_list_cancel = [
    [
        InlineKeyboardButton(text='Отмена', callback_data='cancel')
    ]
]
inlinebutton_cancel = InlineKeyboardMarkup(inline_keyboard=inlinebutton_list_cancel)
