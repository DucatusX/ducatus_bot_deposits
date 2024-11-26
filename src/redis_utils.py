import os
from typing import Set

import redis.asyncio as redis

from src.consts import REDIS_BALANCE_KEY, REDIS_CHAT_IDS_KEY


class RedisClient:
    def __init__(self) -> None:
        self.pool = redis.ConnectionPool(
            host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379),
            db=os.getenv("REDIS_DB", 0), decode_responses=True
        )

    async def update_balance(self, balance_value: str) -> None:
        conn = redis.Redis(connection_pool=self.pool)
        await conn.set(REDIS_BALANCE_KEY, balance_value)

        return None

    async def get_balance(self) -> str:
        conn = redis.Redis(connection_pool=self.pool)
        data = await conn.get(REDIS_BALANCE_KEY)

        return data

    async def add_chat_id(self, chat_id: int) -> None:
        conn = redis.Redis(connection_pool=self.pool)
        await conn.sadd(REDIS_CHAT_IDS_KEY, chat_id)

        return None

    async def remove_chat_id(self, chat_id: int) -> None:
        conn = redis.Redis(connection_pool=self.pool)
        await conn.srem(REDIS_CHAT_IDS_KEY, chat_id)

        return None

    async def get_chat_ids(self) -> Set[int]:
        conn = redis.Redis(connection_pool=self.pool)
        data = await conn.smembers(REDIS_CHAT_IDS_KEY)

        return set(map(int, data))


redis_client: RedisClient = RedisClient()
