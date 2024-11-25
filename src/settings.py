import os
from dataclasses import dataclass

import yaml
from aiogram.types import BotCommand
from marshmallow_dataclass import class_schema

import src.consts as consts


@dataclass
class BotSettings:
    token: str


@dataclass
class NetworkSettings:
    is_testnet: bool
    currency: str
    host: str
    port: int
    username: str
    password: str
    decimals: int
    master_wallet: str
    request_attempts: int


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
]
