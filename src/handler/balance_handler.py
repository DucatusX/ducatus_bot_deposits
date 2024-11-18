from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ducatus_bot_deposits.src.litecoin_rpc import DucatuscoreInterface
from ducatus_bot_deposits.src.settings import settings

balance_router = Router()

@balance_router.message(Command('balance'))
async def balance(message: Message):
    await message.answer('Please wait...')
    rpc = DucatuscoreInterface(settings.network)
    balance_value = await rpc.call_async('getbalance')
    if balance_value:
        await message.answer(f'Balance: {balance_value} {settings.network.currency}')
    else:
        await message.answer('Sorry, balance is not available now')
