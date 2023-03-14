from common import *
from leber.client import LeberClient
import sqlite3
import json

@tree.command(name="login", description="LEBERにログインします")
async def login(interaction: discord.Interaction, phone_number: str, password: str):
    await interaction.response.defer()
    client.logger.info(f"Login request from {interaction.user} ({interaction.user.id})")
    try:
        lclient = LeberClient(mobile=phone_number, password=password)
        
        res = discord.Embed(
            title="ログインに成功しました",
            description=f"ログインできたよ！こんにちは、{lclient.user['patients'][0]['first_name']}さん！",
            color=0x00ff98
        )
        
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE id = ?", (str(interaction.user.id),))
        
        if len(cur.fetchall()) > 0:
            res.title = "すでにログイン済みです"
            res.description = "もうログイン済みだよ！"
            client.logger.info(f"the User is already logged in: {interaction.user} ({interaction.user.id})")
        else:
            conn.execute("INSERT INTO users VALUES (?, ?)", (str(interaction.user.id), json.dumps(lclient.user)))
            conn.commit()
            
        conn.close()

        await interaction.followup.send(embed=res, ephemeral=True)
        
        client.logger.info(f"Successfully executed login request from {interaction.user} ({interaction.user.id})")
        
    except Exception as e:
        res = discord.Embed(
            title="ログインに失敗しました",
            description="IDまたはパスワードが正しくないのかも！",
            color=0xff0000
        )
        await interaction.followup.send(embed=res, ephemeral=True)
        
        client.log_exception(e)