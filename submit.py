import json
import sqlite3

from discord.app_commands import Choice

from common import *
from leber.utility import get_answers


@tree.command(name="submit", description="ヘルスデータを送信します")
@app_commands.choices(
    temperture=[Choice(name=i, value=i) for i in tempertures],
    time=[Choice(name=i, value=i) for i in times]
)
async def submit(interaction: discord.Interaction, 
                 temperture: Choice[str], 
                 time: Choice[str] = None):
    await interaction.response.defer()
    if time == None:
        time = Choice(name="06:00", value="06:00")
    client.logger.info(f"Submit request from {interaction.user.name} ({interaction.user.id})")
    client.logger.info(f"temperture: {temperture.value}, time: {time.value}")
    try:
        if not checkLoginState(str(interaction.user.id)):
            res = discord.Embed(
                title="ログインしていません",
                description="あなたのユーザー情報がありません\nヘルスデータを提出するためにはまずログインしてね！",
                color=0xFFB444
            )
            await interaction.followup.send(embed=res)
            client.logger.info(f"There isn't user data of {interaction.user} ({interaction.user.id}) (Submit Failed).")
            return
        
        con = sqlite3.connect(database=dbname)
        cur = con.cursor()
        cur.execute('SELECT * FROM users WHERE id = ?', (str(interaction.user.id), ))
        info = cur.fetchall()[0][1]
        info = json.loads(info)
        con.close()
        
        lclient = getLeberClient(id=str(interaction.user.id), info=info)
        
        questions = lclient.getTemprtureQuestion()['result']
        
        answers = get_answers(questions=questions, answers=[temperture.value, time.value, "良い"], logger=client.logger)
        
        lclient.submitTemperture(answer=answers)

        res = discord.Embed(
            title="ヘルスデータ提出完了",
            description=f"ヘルスデータを提出したよ！\n{info['patients'][0]['first_name']}さん、今日も一日頑張ろう！",
            color=0x44bdff
        )
        res.add_field(name="体温", value=f"{temperture.name}")
        res.add_field(name="時間", value=f"{time.name}")

        await interaction.followup.send(embed=res)
        client.logger.info(f"Successfully executed submit request from {interaction.user} ({interaction.user.id})")
        
    except Exception as e:
        res = discord.Embed(
            title="ヘルスデータ提出エラー",
            description="ヘルスデータが提出できなかったみたい...",
            color=0xff0000
        )
        res.add_field(name="体温", value=f"{temperture.name}", inline=False)
        res.add_field(name="時間", value=f"{time.name}", inline=False)
        
        await interaction.followup.send(embed=res)
        
        client.log_exception(e)