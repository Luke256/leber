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