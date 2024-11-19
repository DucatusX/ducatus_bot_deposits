from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.consts import BALANCE_COMMAND
from src.litecoin_rpc import ducatus_rpc_interface
from src.settings import settings

balance_router = Router()


@balance_router.message(Command(BALANCE_COMMAND))
async def balance(message: Message):
    await message.answer('Please wait...')
    balance_value = await ducatus_rpc_interface.call_async('getbalance')
    if balance_value:
        await message.answer(
            f'Balance: {balance_value} {settings.network.currency}'
        )
        return None

    await message.answer('Sorry, balance is not available now')
