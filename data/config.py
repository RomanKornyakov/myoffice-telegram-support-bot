import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()
bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')

dp = Dispatcher(storage=MemoryStorage())

# чат операторов
operators_chat = -1001646453733

# словарь с id и username операторов
operators = {1238334856: '@shaylushay84'}
