import logging
from decimal import Decimal

from src.litecoin_rpc import ducatus_rpc_interface
from src.redis_utils import redis_client
from src.settings import settings


async def update_balance() -> None:
    balance_value = await ducatus_rpc_interface.call_async('getbalance')
    if balance_value:
        decimal_balance = Decimal(str(balance_value)) * 10**settings.network.decimals
        await redis_client.update_balance(str(decimal_balance))
        logging.info(f"update balance (current value: {decimal_balance})")

    return None
