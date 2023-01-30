from common import *
from static import checkLoginState

from discord.app_commands import Choice


@tree.command(name="setting", description="ユーザーの設定を行います")
@app_commands.describe(
    auto_submit="ヘルスデータの送信を自動で行うかを設定します"
)
@app_commands.choices(
    auto_submit=[Choice(name="オン", value="on"), Choice(name="オフ", value="off")],
)
async def setting(interaction: discord.Interaction, 
                  auto_submit: Choice[str] = None
                  ):
    client.logger.info(f"Setting request from {interaction.user.name} ({interaction.user.id})")
    try:
        if not checkLoginState(str(interaction.user.id)):
            res = discord.Embed(
                title="ログインしていません",
                description="あなたのユーザー情報がありません\n設定を変更するためにはまずログインしてね！",
                color=0xFFB444
            )
            await interaction.response.send_message(embed=res)
            client.logger.info(f"There isn't user data of {interaction.user} ({interaction.user.id}) (Setting Failed).")
            return
        
        res = discord.Embed(
            title="設定変更完了",
            description=f"設定の変更を完了しました！",
            color=0x4E4E63
        )
        
        con = sqlite3.connect(database=dbname)
        cur = con.cursor()
        cur.execute('SELECT * FROM users WHERE id = ?', (str(interaction.user.id), ))
        info = cur.fetchall()[0][1]
        info = json.loads(info)
        
        lclient = getLeberClient(id=str(interaction.user.id), info=info)
        
        if auto_submit != None:
            client.logger.info(f"Setting item: 'auto_submit' set to {auto_submit.value} {interaction.user.name} ({interaction.user.id})")
            lclient.user['auto_submit'] = True if auto_submit.value=="on" else False
            res.add_field(name="自動送信", value=f"{auto_submit.name}")
            client.logger.info(f"   'auto_submit': {auto_submit.value} {interaction.user.name} ({interaction.user.id})")
        
        cur.execute("UPDATE users SET data = ? WHERE id = ?", (json.dumps(lclient.user), str(interaction.user.id)))
        
        con.commit()
        con.close()
        

        await interaction.response.send_message(embed=res)
        client.logger.info(f"Successfully executed setting request from {interaction.user.name} ({interaction.user.id})")
            
    except Exception as e:
        res = discord.Embed(
            title="設定変更時エラー",
            description="設定が変更できなかったみたい...",
            color=0xff0000
        )
        
        await interaction.response.send_message(embed=res)
        
        client.log_exception(e)
        client.logger.error(f"Failed to change setting. {interaction.user.name} ({interaction.user.id})")