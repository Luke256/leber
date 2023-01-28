secret = __import__("TOKEN_SECRET")

import discord
from discord import app_commands
import logging, sys, datetime

def get_logfile_name() -> str:
    date = datetime.date.today().strftime("%Y-%m-%d")
    filename = "logs/"+date+".log";

    return filename

intents = discord.Intents.default()

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

handler = logging.FileHandler(filename=get_logfile_name(), encoding='utf-8', mode='w')