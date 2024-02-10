from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from data.config import dp, bot


# миддлварь для вызова оператора
class OperatorCallMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any],
    ) -> Any:
        state: FSMContext = FSMContext(
            storage=dp.storage,
            key=StorageKey(
                chat_id=message.from_user.id,
                user_id=message.from_user.id,
                bot_id=bot.id))

        state_str = str(await state.get_state())

        if state_str == 'OperatorCall:call':
            state_data = await state.get_data()
            second_id = state_data.get('second_id')
            await message.copy_to(second_id)
        elif state_str == 'OperatorCall:waiting_operator':
            await message.answer('Дождитесь ответа оператора или отмените сеанс.')
        else:
            return await handler(message, data)
