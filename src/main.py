import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeDefault

from src.handler.balance_handler import balance_router
from src.handler.start_handler import start_router
from src.logger_config import logger_config
from src.settings import commands, settings

logging.config.dictConfig(logger_config)


async def main():
    bot = Bot(token=settings.bot.token)
    dp = Dispatcher()
    dp.include_routers(start_router, balance_router)
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
