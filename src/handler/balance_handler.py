from decimal import Decimal

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.consts import BALANCE_COMMAND
from src.redis_utils import redis_client
from src.settings import settings

balance_router = Router()


@balance_router.message(Command(BALANCE_COMMAND))
async def balance(message: Message):
    await message.answer('Please wait...')
    balance_value = await redis_client.get_balance()
    if balance_value:
        normal_balance = Decimal(balance_value) / settings.degree
        await message.answer(
            f'Balance: {normal_balance} {settings.network.currency}'
        )
        return None

    await message.answer('Sorry, balance is not available now')
