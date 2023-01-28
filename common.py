secret = __import__("TOKEN_SECRET")

import discord
from discord import app_commands
import logging, sys, datetime
from leber.utility import *
from leber.logger import Logger

dbname = 'database.db'

intents = discord.Intents.default()

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

handler = logging.FileHandler(filename=get_logfile_name(), encoding='utf-8', mode='a')

logger = Logger()

tempertures = [
    "36.0°C", "36.1°C", "36.2°C", "36.3°C", "36.4°C", "36.5°C", "36.6°C", "36.7°C", "36.8°C"
]

times = [
    "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00",
]