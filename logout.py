from common import *
import sqlite3
import traceback

@tree.command(name="logout", description="LEBERアカウントからログアウトします")
async def logout(interaction: discord.Interaction):
    client.logger.info(f"Logout Request from {interaction.user} ({interaction.user.id})")
    try:
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        
        cur.execute('SELECT * FROM users WHERE id = ?', (str(interaction.user.id), ))
        
        if len(cur.fetchall()) == 0:
            res = discord.Embed(
                title="ログアウトできません",
                description="あなたのユーザー情報がありません\nログアウトするためにはまずログインしてね！",
                color=0xFFB444
            )
            await interaction.response.send_message(embed=res)
            client.logger.info(f"There isn't user data of {interaction.user} ({interaction.user.id}) (Logout Failed).")
            return

        cur.execute('DELETE FROM users WHERE id = ?', (str(interaction.user.id), ))
        
        con.commit()
        con.close()
        
        res = discord.Embed(
                title="ログアウトしました",
                description="ログアウトが正常にできたみたい！",
                color=0x00ff98
            )
        await interaction.response.send_message(embed=res)
        
        client.logger.info(f"Successfully executed logout request from {interaction.user} ({interaction.user.id}).")
        
    except Exception as e:
        res = discord.Embed(
            title="ログアウトに失敗しました",
            description="ごめんなさい...\n時間をおいてもう一度試してみてください！",
            color=0xff0000
        )
        await interaction.response.send_message(embed=res)
        
        client.log_exception(e)