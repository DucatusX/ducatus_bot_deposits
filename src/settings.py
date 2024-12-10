import os
from dataclasses import dataclass
from typing import Optional

import yaml
from aiogram.types import BotCommand
from marshmallow_dataclass import class_schema

import src.consts as consts


@dataclass
class BotSettings:
    token: str
    request_attempts: int
    request_delay: int


@dataclass
class NetworkSettings:
    is_testnet: bool
    currency: str
    host: str
    port: int
    username: str
    password: str
    decimals: int
    request_attempts: int

    def __post_init__(self):
        self.degree = 10**self.decimals


@dataclass
class Settings:
    bot: BotSettings
    network: NetworkSettings


config_path = "/../config.yaml"

with open(os.path.dirname(__file__) + config_path) as config_file:
    config_data = yaml.safe_load(config_file)

settings: Settings = class_schema(Settings)().load(config_data)


commands = [
    BotCommand(command=consts.BALANCE_COMMAND, description='get balance'),
    BotCommand(command=consts.START_COMMAND, description='activate alerts'),
    BotCommand(command=consts.STOP_COMMAND, description='stop alerts'),
]
