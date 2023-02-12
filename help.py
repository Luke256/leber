from common import *

@tree.command(name="help", description="コマンドの一覧を返信します")
async def neko(interaction: discord.Interaction):
    client.logger.info(f"Help request from {interaction.user} ({interaction.user.id})")

    res = discord.Embed(
        title="コマンド一覧",
        color=0xFFC6C6
    )
    
    res.add_field(name="/help", value=f"このメッセージを表示します", inline=False)
    res.add_field(name="/check", value=f"ログインの状況と、自動送信の設定が確認できます", inline=False)
    res.add_field(name="/login `電話番号` `パスワード`", value=f"LEBERにログインします", inline=False)
    res.add_field(name="/logout", value=f"LEBERからログアウトします(設定は削除されます)", inline=False)
    res.add_field(name="/setting `自動送信(任意)`", value=f"自動送信の設定ができます", inline=False)
    res.add_field(name="/submit `体温` `検温時間(任意)`", value=f"ヘルスデータを送信します", inline=False)
    res.add_field(name="/neko", value=f"鳴きます。にゃーん", inline=False)

    await interaction.response.send_message(embed=res)