import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database import Database

load_dotenv()
bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')

db = Database('database/myoffice_database.db')

dp = Dispatcher(storage=MemoryStorage())

# чат операторов
operators_chat = -1001646453733

# словарь с id и username операторов
operators = {1238334856: '@shaylushay84',
             6124541482: '@hvnsof'}
