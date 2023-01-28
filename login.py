from common import *
from leber.client import LeberClient
import sqlite3
import json
import traceback

@tree.command(name="login", description="LEBERにログインします")
async def login(interaction: discord.Interaction, phone_number: str, password: str):
    logger.info(f"Login request from {interaction.user.name} ({interaction.user.id})")
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
        else:
            conn.execute("INSERT INTO users VALUES (?, ?)", (str(interaction.user.id), json.dumps(client.user)))
            conn.commit()
            
        conn.close()

        await interaction.response.send_message(embed=res)
        
        logger.info(f"Successfully executed login request from {interaction.user.name} ({interaction.user.id})")
        
    except Exception as e:
        res = discord.Embed(
            title="ログインに失敗しました",
            description="IDまたはパスワードが正しくないのかも!",
            color=0xff0000
        )
        await interaction.response.send_message(embed=res)
        
        t = list(traceback.TracebackException.from_exception(e).format())
        t = "".join(t)
        t = t.split("\n")
        for i in t:
            logger.error(i[:-1])