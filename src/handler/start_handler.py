from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from src.consts import STOP_COMMAND
from src.redis_utils import redis_client

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await redis_client.add_chat_id(message.chat.id)
    await message.answer(
        f"Hello, {message.chat.first_name}! Alerts are activated."
    )

    return None


@start_router.message(Command(STOP_COMMAND))
async def cmd_stop(message: Message):
    await redis_client.remove_chat_id(message.chat.id)
    await message.answer("Alerts are terminated.")

    return None
