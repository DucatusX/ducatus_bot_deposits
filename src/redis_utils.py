import os
from typing import Set
from datetime import datetime

import redis.asyncio as redis

import src.consts as consts
from src.consts import REDIS_DATETIME_FORMAT, REDIS_DATETIME_KEY


class RedisClient:
    def __init__(self) -> None:
        self.pool = redis.ConnectionPool(
            host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379),
            db=os.getenv("REDIS_DB", 0), decode_responses=True
        )

    async def update_balance(self, balance_value: str) -> None:
        conn = redis.Redis(connection_pool=self.pool)
        await conn.set(consts.REDIS_BALANCE_KEY, balance_value)

        return None

    async def get_balance(self) -> str:
        conn = redis.Redis(connection_pool=self.pool)
        data = await conn.get(consts.REDIS_BALANCE_KEY)

        return data

    async def add_chat_id(self, chat_id: int) -> None:
        conn = redis.Redis(connection_pool=self.pool)
        await conn.sadd(consts.REDIS_CHAT_IDS_KEY, chat_id)

        return None

    async def remove_chat_id(self, chat_id: int) -> None:
        conn = redis.Redis(connection_pool=self.pool)
        await conn.srem(consts.REDIS_CHAT_IDS_KEY, chat_id)

        return None

    async def get_chat_ids(self) -> Set[int]:
        conn = redis.Redis(connection_pool=self.pool)
        data = await conn.smembers(consts.REDIS_CHAT_IDS_KEY)

        return set(map(int, data))

    async def update_last_alert(self) -> None:
        conn = redis.Redis(connection_pool=self.pool)
        str_time = datetime.now().strftime(REDIS_DATETIME_FORMAT)
        await conn.set(consts.REDIS_DATETIME_KEY, str_time)

        return None

    async def get_last_alert(self) -> datetime | None:
        conn = redis.Redis(connection_pool=self.pool)
        str_time = await conn.get(REDIS_DATETIME_KEY)
        if str_time:
            return datetime.strptime(str_time, REDIS_DATETIME_FORMAT)

        return None

redis_client: RedisClient = RedisClient()
