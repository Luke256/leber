import discord
import random
import sqlite3
import json
from static import *
from leber.client import LeberClient
from leber.logger import Logger

def sendGoodHealth(id: int):
    temperture = random.randint(21,27)
    time = 118
    state = 136
    
    con = sqlite3.connect(dbname)
    cur = con.cursor()
        
    cur.execute('SELECT * FROM users WHERE id = ?', (str(id), ))
    info = cur.fetchall()[0][1]
        
    con.close()

    info = json.loads(info)
    lclient = getLeberClient(id=str(id), info=info)
    
    lclient.submitTemperture([temperture, time, state])

class GoodButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def callback(self, interaction: discord.Interaction):
        logger = Logger()
        
        logger.info(f"Good health request from {interaction.user} ({interaction.user.id})")
        
        try:
            if checkLoginState(str(interaction.user.id)) == False:
                embed = discord.Embed(
                    title="未ログインです",
                    description="まずはログインをしてください！(/login)",
                    color=0xFFB444
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                logger.info(f"User isn't logged in: {interaction.user} ({interaction.user.id})")
                return

            sendGoodHealth(interaction.user.id)

            embed = discord.Embed(
                title="体調チェック完了",
                description="了解！今日も一日がんばろー！",
                color=0x44bdff
            )
            await interaction.response.send_message(embed=embed, ephemeral=interaction.channel.type != discord.enums.ChannelType.private)
            logger.info(f"Successfully executed good-health request from {interaction.user} ({interaction.user.id})")
        
        except Exception as e:
            
            res = discord.Embed(
                title="ヘルスデータ提出エラー",
                description="ヘルスデータが提出できなかったみたい...",
                color=0xff0000
            )
        
            await interaction.response.send_message(embed=res)

            logger.error(e)
