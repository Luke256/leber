secret = __import__("TOKEN_SECRET")

import datetime
import logging
import sys
import traceback

import discord
from discord import app_commands

from client import Leberse
from leber.logger import Logger
from leber.utility import *
from static import *

intents = discord.Intents.all()

client = Leberse(intents=intents)

tree = app_commands.CommandTree(client)

handler = logging.FileHandler(filename=get_logfile_name(), encoding='utf-8', mode='a')
handler.setFormatter(get_formatter())

client.logger = Logger()

def log_exception(e: Exception):
    t = list(traceback.TracebackException.from_exception(e).format())
    t = "".join(t)
    t = t.split("\n")
    for i in t:
        if len(i) > 0 and i[-1] == '\n':
            i = i[:-1]
        client.logger.error(i)