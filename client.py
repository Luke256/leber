import random
import sqlite3
import typing
import traceback
import datetime

import discord
from discord.ext import tasks

from badButton import BadButton
from goodButton import GoodButton
from leber.logger import Logger
from static import *

Querytime = datetime.time(hour=16, minute=40, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))

class Leberse(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = Logger()
        
    @tasks.loop(time=Querytime)
    async def auto_healthcheck(self):
        guild = self.get_guild(624134396018163712)
        channel = guild.get_channel(1068824419943845919)
        embed = discord.Embed(
            title="定期実行",
            description="おはよう！今日の体調は？"
        )
        view = discord.ui.View()
        goodString = ["良好！", "絶好調！", "健康だよ！", "異常なし！"]
        badString = ["よくない...", "具合が悪い...", "すぐれない..."]
        view.add_item(GoodButton(label=random.choice(goodString), style=discord.ButtonStyle.primary))
        view.add_item(BadButton(label=random.choice(badString), style=discord.ButtonStyle.danger))
        # await channel.send(embed=embed, view=view)
        
        users = self.getUserList()
        
        for id in users:
            user = self.get_user(id)
            
            try:
                await user.send(embed=embed, view=view)
            except discord.errors.Forbidden:
                self.logger.warning(f"Failed to send health check to {user} ({user.id}). Maybe blocked.")
            except Exception as e:
                self.log_exception(e)
        
        self.logger.info("Sent health check information")
        
    def getUserList(self) -> typing.List[int]:
        try:
            con = sqlite3.connect(dbname)
            cur = con.cursor()

            cur.execute('SELECT id FROM users')
            ids = [int(id[0]) for id in cur.fetchall()]
            
            con.close()
            
            return ids
        
        except Exception as e:
            self.log_exception(e)
            self.logger.error("Failed to get user list.")
            return []
                
    def log_exception(self, e: Exception):
        t = list(traceback.TracebackException.from_exception(e).format())
        t = "".join(t)
        t = t.split("\n")
        for i in t:
            if len(i) > 0 and i[-1] == '\n':
                i = i[:-1]
            self.logger.error(i)