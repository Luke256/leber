import discord
import random
import sqlite3
from static import *
from leber.client import LeberClient
from leber.logger import Logger

class GoodButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def callback(self, interaction: discord.Interaction):
        logger = Logger()
        
        logger.info(f"Good health request from {interaction.user} ({interaction.user.id})")
        
        temperture = random.randint(21, 28)
        time = 118
        state = 136
        
        try:
            if checkLoginState(str(interaction.user.id)) == False:
                embed = discord.Embed(
                    title="未ログインです",
                    description="まずはログインをしてください！(/login)"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                logger.info(f"User isn't logged in: {interaction.user} ({interaction.user.id})")
                return

            con = sqlite3.connect(dbname)
            cur = con.cursor()
            
            cur.execute('SELECT * FROM users WHERE id = ?', (str(interaction.user.id), ))
            info = cur.fetchall()[0][1]
            
            con.close()
            
            lclient = LeberClient(info=info)

            lclient.submitTemperture([temperture, time, state])

            embed = discord.Embed(
                title="体調チェック完了(送信してないよ)",
                description="了解！今日も一日がんばろー！"
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