import logging
from bitcoinrpc import BitcoinRPC
from http.client import RemoteDisconnected, CannotSendRequest
from httpx import ReadTimeout, Timeout
from socket import timeout
from ducatus_bot_deposits.src.settings import NetworkSettings

class DucatuscoreInterface:
    def __init__(self, settings: NetworkSettings):
        self.__rpc = self.__setup_rpc(settings)
        self.__attempts = settings.request_attempts

    def __setup_rpc(self, settings: NetworkSettings):
        return BitcoinRPC.from_config(
            f"http://{settings.host}:{settings.port}",
            (settings.username, settings.password),
            timeout=Timeout(
                timeout=60,
                connect=30.0, # Connection timeout in seconds
                read=60.0,    # Read timeout in seconds
                write=60.0    # Write timeout in seconds
            )
        )

    async def call_async(self, method: str, *params):
        for i in range(self.__attempts):
            try:
                return await self.__rpc.acall(method, list(params))
            except (timeout, TimeoutError, CannotSendRequest, ReadTimeout, RemoteDisconnected) as e:
                logging.warning(f"error while trying send rpc request with method {method} (attempt {i + 1}) (details: {e})")
        return None
