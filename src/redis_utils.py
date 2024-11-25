import os
from typing import Set

import redis.asyncio as redis

from src.consts import REDIS_BALANCE_KEY, REDIS_CHAT_IDS_KEY


class RedisClient:
    def __init__(self) -> None:
        # self._conn = redis.Redis(host=os.getenv("REDIS_HOST"))
        self._conn = redis.Redis()

    @classmethod
    async def update_balance(cls, balance_value: str) -> None:
        conn = cls()._conn
        await conn.set(REDIS_BALANCE_KEY, balance_value)
        await conn.aclose()

        return None

    @classmethod
    async def get_balance(cls) -> str:
        conn = cls()._conn
        data = await conn.get(REDIS_BALANCE_KEY)
        await conn.aclose()

        return data.decode("utf-8")

    @classmethod
    async def add_chat_id(cls, chat_id: int) -> None:
        conn = cls()._conn
        await conn.sadd(REDIS_CHAT_IDS_KEY, chat_id)
        await conn.aclose()

        return None

    @classmethod
    async def remove_chat_id(cls, chat_id: int) -> None:
        conn = cls()._conn
        await conn.srem(REDIS_CHAT_IDS_KEY, chat_id)
        await conn.aclose()

        return None

    @classmethod
    async def get_chat_ids(cls) -> Set[int]:
        conn = cls()._conn
        data = await conn.smembers(REDIS_CHAT_IDS_KEY)
        await conn.aclose()

        return set(map(int, data))
