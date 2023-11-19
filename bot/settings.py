import pathlib
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import discord
import json


# Vortex Configs

# BOT
with open("storage_data.json", 'r') as data_file:
    storage_data = json.load(data_file)
bot_prefix = storage_data['bot']['dados']['bot_prefix']


# Outras Configs
load_dotenv()

# Discord
discord_api_token = os.getenv("DISCORD_API_TOKEN")  # TOKEN
# discord_bot_id = os.getenv("DISCORD_BOT_ID")  # BOT ID
# discord_public_key = os.getenv("DISCORD_PUBLIC_KEY")  # PUBLIC_KEY
discord_guild_id = 0000000
discord_ch_id_players_on = 000000

BASE_DIR = pathlib.Path(__file__).parent
CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"

# MySQL5
mysql_user = os.getenv("MYSQL_USER")  # MySQL
mysql_pass = os.getenv("MYSQL_PASS")  # MySQL
mysql_host = os.getenv("MYSQL_HOST")  # MySQL
mysql_port = int(os.getenv("MYSQL_PORT"))  # MySQL
mysql_mydb = os.getenv("MYSQL_MYDB")  # MySQL

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)
