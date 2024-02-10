import random
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from data.config import dp, bot


async def check_operator_available(operator_id):
    state: FSMContext = FSMContext(
        storage=dp.storage,
        key=StorageKey(
            chat_id=operator_id,
            user_id=operator_id,
            bot_id=bot.id))

    state_str = str(await state.get_state())

    if state_str == 'OperatorCall:call' or state_str == 'OperatorCall:entering_id':
        return False
    else:
        return operator_id


async def get_operator(operators):
    random.shuffle(operators)
    for operator_id in operators:
        operator_id = await check_operator_available(operator_id)

        if operator_id:
            return operator_id
    else:
        return False
