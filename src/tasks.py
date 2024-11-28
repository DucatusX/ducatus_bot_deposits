from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from src.consts import CRITICAL_LEVEL, MEDIUM_LEVEL, NORMAL_LEVEL
from src.litecoin_rpc import ducatus_rpc_interface
from src.redis_utils import redis_client
from src.settings import settings


class AlertStateInterface(ABC):
    def __init__(self, forced=False):
        self.forced = forced
        self._context = None

    @property
    def context(self) -> AlertContext:
        return self._context

    @context.setter
    def context(self, context: AlertContext) -> None:
        self._context = context

    @abstractmethod
    async def alert(self) -> None:
        pass


class AlertContext:
    _state = None

    def __init__(self, state: AlertStateInterface, bot: Bot):
        self.transition_to(state)
        self.bot = bot

    def transition_to(self, state: AlertStateInterface):
        self._state = state
        self._state.context = self

    async def update_balance(self) -> None:
        balance_value = await ducatus_rpc_interface.call_async('getbalance')

        if not balance_value:
            return None

        decimal_balance = Decimal(str(balance_value)) * settings.degree
        await redis_client.update_balance(str(decimal_balance))
        logging.info(f"update balance (current value: {decimal_balance})")

        return None

    async def send_alerts(self):
        await self._state.alert()


class NoAlertState(AlertStateInterface):
    async def alert(self) -> None:
        balance_decimal = await redis_client.get_balance()
        if not balance_decimal:
            return None

        balance_value = Decimal(balance_decimal) / settings.degree
        if balance_value <= NORMAL_LEVEL['high']:
            self.context.transition_to(LowBalanceAlertState(forced=True))
        return None


class LowBalanceAlertState(AlertStateInterface):
    async def alert(self) -> None:
        balance_decimal = await redis_client.get_balance()
        if not balance_decimal:
            return None

        balance_value = Decimal(balance_decimal) / settings.degree

        last_alert = await redis_client.get_last_alert()
        if not last_alert:
            await redis_client.update_last_alert()
            self.forced = True
            return None

        time_diff = datetime.now() - last_alert

        if NORMAL_LEVEL['high'] >= balance_value > NORMAL_LEVEL['low']:
            message = NORMAL_LEVEL['message']
            time_delta = NORMAL_LEVEL['time_delta']
        elif MEDIUM_LEVEL['high'] >= balance_value > MEDIUM_LEVEL['low']:
            message = MEDIUM_LEVEL['message']
            time_delta = MEDIUM_LEVEL['time_delta']
        elif balance_value <= CRITICAL_LEVEL['high']:
            message = CRITICAL_LEVEL['message']
            time_delta = CRITICAL_LEVEL['time_delta']
        else:
            self.context.transition_to(NoAlertState())
            return None

        if self.forced or time_diff.days >= time_delta:
            await alert_all_chats(
                self.context.bot,
                message
            )
            await redis_client.update_last_alert()

            if self.forced:
                self.forced = False

        return None


async def alert_all_chats(bot: Bot, message: str) -> None:
    chat_ids = await redis_client.get_chat_ids()
    if not chat_ids:
        return None

    for chat_id in chat_ids:
        await send_msg(bot, chat_id, message)

    return None


def retry_send_msg(req):
    async def wrapper(*args, **kwargs):
        for attempt in range(settings.bot.request_attempts):
            try:
                await req(*args, **kwargs)
                return None
            except TelegramBadRequest as e:
                logging.warning(f"attempt {attempt} ({e})")
                await asyncio.sleep(settings.bot.request_delay)
        return None
    return wrapper


@retry_send_msg
async def send_msg(bot: Bot, chat_id: int, message: str) -> None:
    await bot.send_message(chat_id, message)
    return None
