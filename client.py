import random
import sqlite3
import typing
import traceback
import datetime

import discord
from discord.ext import tasks

from badButton import BadButton
from goodButton import GoodButton, sendGoodHealth
from leber.logger import Logger
from static import *
from leber.utility import get_time

Querytime = datetime.time(hour=7, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))

class Leberse(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = Logger()
        
    @tasks.loop(time=Querytime)
    async def auto_healthcheck(self):
        guild = self.get_guild(624134396018163712)
        channel = guild.get_channel(1068824419943845919)
        now = get_time()
        embed = discord.Embed(
            title=f"定期送信({now.tm_year}年{now.tm_mon}月{now.tm_mday}日)",
            description="おはよう！今日の体調は？",
            color=0x00ff98
        )
        view = discord.ui.View()
        goodString = ["良好！", "絶好調！", "健康だよ！", "異常なし！"]
        badString = ["よくない...", "具合が悪い...", "すぐれない..."]
        view.add_item(GoodButton(label=random.choice(goodString), style=discord.ButtonStyle.primary))
        view.add_item(BadButton(label=random.choice(badString), style=discord.ButtonStyle.danger))
        # await channel.send(embed=embed, view=view)
        
        users = self.getUserList()
        
        for id, data in users:
            user = self.get_user(id)
            
            try:
                if (data.user['auto_submit']):
                    sendGoodHealth(id)
                else:
                    await user.send(embed=embed, view=view)
            except discord.errors.Forbidden:
                self.logger.warning(f"Failed to send health check to {user} ({user.id}). Maybe blocked.")
            except Exception as e:
                self.log_exception(e)
        
        self.logger.info("Sent health check information")
        
    def getUserList(self):
        try:
            con = sqlite3.connect(dbname)
            cur = con.cursor()

            cur.execute('SELECT * FROM users')
            users = [(int(user[0]), getLeberClient(user[0], info=json.loads(user[1]))) for user in cur.fetchall()]
            
            con.close()
            
            return users
        
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