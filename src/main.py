import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.handler.balance_handler import balance_router
from src.handler.start_handler import start_router
from src.logger_config import logger_config
from src.settings import commands, settings
from src.tasks import update_balance

logging.config.dictConfig(logger_config)


async def main():
    bot = Bot(token=settings.bot.token)
    dp = Dispatcher()
    dp.include_routers(start_router, balance_router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_balance, "interval", minutes=1)
    scheduler.start()

    await bot.set_my_commands(commands, BotCommandScopeDefault())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
