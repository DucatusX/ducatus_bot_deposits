import asyncio
import logging
from aiogram import Bot,Dispatcher
from aiogram.types import BotCommandScopeDefault

from settings import settings, commands
from handler.start_handler import start_router
from handler.balance_handler import balance_router


async def main():
    bot = Bot(token=settings.bot.token)
    dp = Dispatcher()
    dp.include_routers(start_router, balance_router)
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='../logs/.log',
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    asyncio.run(main())
