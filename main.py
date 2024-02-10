from aiogram.types import BotCommand
from middlewares.operator_middleware import OperatorCallMiddleware
from data.config import bot, dp, operators_chat, operators
from handlers.operators import command_change_data, command_add_data, command_view_data, command_delete_data
from handlers.users import start, help, keyboard, answer_question, command_operator, command_feedback
import logging


async def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
                        datefmt='%d/%m/%Y %I:%M:%S',)
    # регистрируем миддлвари и роутеры
    dp.message.middleware.register(OperatorCallMiddleware())
    dp.include_routers(start.router,
                       help.router,
                       keyboard.router,
                       command_operator.router,
                       command_feedback.router,
                       command_view_data.router,
                       command_add_data.router,
                       command_change_data.router,
                       command_delete_data.router,
                       answer_question.router,
                       )

    # создание меню команд
    await bot.set_my_commands([BotCommand(command='help', description='Как работает бот?'),
                               BotCommand(command='operator', description='Вызов оператора'),
                               BotCommand(command='feedback', description='Написать отзыв')])

    await bot.send_message(operators_chat, 'Бот начал работу!')
    for operator in list(operators.keys()):
        await bot.send_message(operator, 'Бот начал работу!')

    print('Бот начал работу!')

    # запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
