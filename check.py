from common import *
from static import checkLoginState


@tree.command(name="check", description="ログイン状況、自動送信設定を確認します")
async def check(interaction: discord.Interaction):
    client.logger.info(f"Check request from {interaction.user} ({interaction.user.id})")
    try:
        res = discord.Embed(
            title="未ログインです",
            description=f"まだログインしていないよ！",
            color=0x00ff98
        )
        
        state = checkLoginState(str(interaction.user.id))
        
        if state:
            con = sqlite3.connect(database=dbname)
            cur = con.cursor()
            cur.execute('SELECT * FROM users WHERE id = ?', (str(interaction.user.id), ))
            info = cur.fetchall()[0][1]
            info = json.loads(info)
            con.close()
            
            lclient = getLeberClient(id=str(interaction.user.id), info=info)
            
            res.title = "ログイン済みです"
            res.description = "もうログイン済みだよ！"
            res.add_field(name="自動送信設定", value=f'{"オン" if lclient.user["auto_submit"] else "オフ"}')
            client.logger.info(f"the User is already logged in: {interaction.user} ({interaction.user.id})")
        else :
            client.logger.info(f"the User is not logged in: {interaction.user} ({interaction.user.id})")

        await interaction.response.send_message(embed=res)
        
        client.logger.info(f"Successfully executed check request from {interaction.user} ({interaction.user.id})")
        
    except Exception as e:
        res = discord.Embed(
            title="ログイン状況の確認に失敗しました",
            description="時間をおいて再度試してみてください",
            color=0xff0000
        )
        await interaction.response.send_message(embed=res)
        
        client.log_exception(e)