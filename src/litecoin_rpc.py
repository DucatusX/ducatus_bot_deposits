import logging
from http.client import CannotSendRequest, RemoteDisconnected
from socket import timeout

from bitcoinrpc import BitcoinRPC
from httpx import ReadTimeout, Timeout

import src.consts as consts
from src.settings import NetworkSettings, settings


def retry_on_http_disconnection(req):
    async def wrapper(*args, **kwargs):
        for attempt in range(settings.network.request_attempts):
            try:
                result = await req(*args, **kwargs)
            except (timeout, TimeoutError, CannotSendRequest,
                        ReadTimeout, RemoteDisconnected) as e:
                logging.warning(
                    f"error while trying send rpc request (attempt {attempt + 1}) ({e})"
                )
            else:
                return result
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
                connect=consts.CONNECT_TIMEOUT,
                read=consts.READ_TIMEOUT,
                write=consts.WRITE_TIMEOUT
            )
        )

    @retry_on_http_disconnection
    async def call_async(self, method: str, *params):
        return await self.__rpc.acall(method, list(params))


ducatus_rpc_interface = DucatuscoreInterface(net_settings=settings.network)
