import random
import sqlite3

import discord
from discord.ext import tasks

from badButton import BadButton
from goodButton import GoodButton
from leber.logger import Logger
from static import *


class Leberse(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = Logger()
        
    @tasks.loop(seconds=100000)
    async def auto_healthcheck(self):
        guild = self.get_guild(624134396018163712)
        channel = guild.get_channel(1068824419943845919)
        # user = self.get_user(649819692529090561)
        embed = discord.Embed(
            title="定期実行",
            description="おはよう！今日の体調は？"
        )
        view = discord.ui.View()
        goodString = ["良好！", "絶好調！", "健康だよ！", "異常なし！"]
        badString = ["よくない...", "具合が悪い...", "すぐれない..."]
        view.add_item(GoodButton(label=random.choice(goodString), style=discord.ButtonStyle.primary))
        view.add_item(BadButton(label=random.choice(badString), style=discord.ButtonStyle.danger))
        await channel.send(embed=embed, view=view)
        self.logger.info("Sent health check information")
        
    def getUserList(self):
        pass