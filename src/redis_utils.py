from typing import Set

import redis.asyncio as redis

from src.consts import REDIS_BALANCE_KEY, REDIS_CHAT_IDS_KEY


class RedisClient:
    def __init__(self) -> None:
        self.pool = redis.ConnectionPool(
            host="localhost", port=6379, db=0, decode_responses=True
        )
        self._conn = redis.Redis(connection_pool=self.pool)

    @classmethod
    async def update_balance(cls, balance_value: str) -> None:
        conn = cls()._conn
        await conn.set(REDIS_BALANCE_KEY, balance_value)

        return None

    @classmethod
    async def get_balance(cls) -> str:
        conn = cls()._conn
        data = await conn.get(REDIS_BALANCE_KEY)

        return data

    @classmethod
    async def add_chat_id(cls, chat_id: int) -> None:
        conn = cls()._conn
        await conn.sadd(REDIS_CHAT_IDS_KEY, chat_id)

        return None

    @classmethod
    async def remove_chat_id(cls, chat_id: int) -> None:
        conn = cls()._conn
        await conn.srem(REDIS_CHAT_IDS_KEY, chat_id)

        return None

    @classmethod
    async def get_chat_ids(cls) -> Set[int]:
        conn = cls()._conn
        data = await conn.smembers(REDIS_CHAT_IDS_KEY)

        return set(map(int, data))
