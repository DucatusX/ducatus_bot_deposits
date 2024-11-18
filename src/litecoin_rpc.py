import logging
from bitcoinrpc import BitcoinRPC
from http.client import RemoteDisconnected, CannotSendRequest
from httpx import ReadTimeout, Timeout
from socket import timeout
from ducatus_bot_deposits.src.settings import NetworkSettings, settings
import ducatus_bot_deposits.src.consts as consts


def retry_on_http_disconnection(req):
    async def wrapper(*args, **kwargs):
        for attempt in range(settings.network.request_attempts):
            try:
                return await req(*args, **kwargs)
            except (timeout, TimeoutError, CannotSendRequest, ReadTimeout, RemoteDisconnected) as e:
                logging.warning(
                    f"error while trying send rpc request (attempt {attempt + 1}) (details: {e})"
                )
        return None
    return wrapper


class DucatuscoreInterface:
    def __init__(self, net_settings: NetworkSettings):
        self.__rpc = self.__setup_rpc(net_settings)

    def __setup_rpc(self, net_settings: NetworkSettings):
        return BitcoinRPC.from_config(
            f"http://{net_settings.host}:{net_settings.port}",
            (net_settings.username, net_settings.password),
            timeout=Timeout(
                timeout=consts.TIMEOUT,
                connect=consts.CONNECT_TIMEOUT,  # Connection timeout in seconds
                read=consts.READ_TIMEOUT,        # Read timeout in seconds
                write=consts.WRITE_TIMEOUT       # Write timeout in seconds
            )
        )

    @retry_on_http_disconnection
    async def call_async(self, method: str, *params):
        return await self.__rpc.acall(method, list(params))


ducatus_rpc_interface = DucatuscoreInterface(net_settings=settings.network)
