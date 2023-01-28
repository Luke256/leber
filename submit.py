from common import *
from leber.utility import get_answers
from leber.client import LeberClient
from discord.app_commands import Choice
import sqlite3
import json
import traceback
import typing

@tree.command(name="submit", description="ヘルスデータを送信します")
@app_commands.choices(
    temperture=[Choice(name=i, value=i) for i in tempertures],
    time=[Choice(name=i, value=i) for i in times]
)
async def submit(interaction: discord.Interaction, 
                 temperture: Choice[str], 
                 time: Choice[str] = None):
    if time == None:
        time = Choice(name="06:00", value="06:00")
    logger.info(f"Submit request from {interaction.user.name} ({interaction.user.id})")
    logger.info(f"temperture: {temperture.value}, time: {time.value}")
    try:
        
        con = sqlite3.connect(database=dbname)
        cur = con.cursor()
        cur.execute('SELECT * FROM users WHERE id = ?', (str(interaction.user.id), ))
        info = cur.fetchall()[0][1]
        info = json.loads(info)
        
        lclient = LeberClient(info=info)
        
        questions = lclient.getTemprtureQuestion()['result']
        
        answers = get_answers(questions=questions, answers=[temperture.value, time.value, "良い"], logger=logger)
        
        # lclient.submitTemperture(answer=answers)

        res = discord.Embed(
            title="ヘルスデータ提出官僚",
            description=f"ヘルスデータを提出したよ！(してない)\n{info['patients'][0]['first_name']}さん、今日も一日頑張ろう！",
            color=0x44bdff
        )
        res.add_field(name="体温", value=f"{temperture.name}", inline=False)
        res.add_field(name="時間", value=f"{time.name}", inline=False)

        await interaction.response.send_message(embed=res)
        logger.info(f"Successfully executed submit request from {interaction.user.name} ({interaction.user.id})")
        
    except Exception as e:
        res = discord.Embed(
            title="ヘルスデータ提出エラー",
            description="ヘルスデータが提出できなかったみたい...",
            color=0xff0000
        )
        res.add_field(name="体温", value=f"{temperture.name}", inline=False)
        res.add_field(name="時間", value=f"{time.name}", inline=False)
        
        await interaction.response.send_message(embed=res)
        
        t = list(traceback.TracebackException.from_exception(e).format())
        t = "".join(t)
        t = t.split("\n")
        for i in t:
            logger.error(i[:-1])