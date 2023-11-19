import pathlib
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import discord
import json


# pega o TOKEN (Old)
'''def read_token():
    with open("bot_t0k3n_h3r3.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


bot_token = read_token()'''
# Vortex Configs

# BOT
file_storage_data = os.path.join(os.path.dirname(__file__), 'storage_data.json')
with open(file_storage_data, 'r') as data_file:
    storage_data = json.load(data_file)
bot_prefix = storage_data['bot']['dados']['bot_prefix']


# Outras Configs
load_dotenv()

# Discord
discord_api_token = os.getenv("DISCORD_API_TOKEN")  # TOKEN
# discord_bot_id = os.getenv("DISCORD_BOT_ID")  # BOT ID
# discord_public_key = os.getenv("DISCORD_PUBLIC_KEY")  # PUBLIC_KEY
discord_guild_id = 1174122080778866799
discord_ch_id_players_on = 1174421965939933214

BASE_DIR = pathlib.Path(__file__).parent
CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"

# MySQL5
mysql_user = os.getenv("MYSQL_USER")  # MySQL5
mysql_pass = os.getenv("MYSQL_PASS")  # MySQL5
mysql_host = os.getenv("MYSQL_HOST")  # MySQL5
mysql_port = int(os.getenv("MYSQL_PORT"))  # MySQL5
mysql_mydb = os.getenv("MYSQL_MYDB")  # MySQL5

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
            "filename": os.path.join(os.path.dirname(__file__), "logs", "infos.log"),
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
