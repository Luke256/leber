from common import *
from static import checkLoginState


@tree.command(name="check", description="ログイン状況を確かめます")
async def check(interaction: discord.Interaction):
    client.logger.info(f"Check request from {interaction.user.name} ({interaction.user.id})")
    try:
        res = discord.Embed(
            title="未ログインです",
            description=f"まだログインしていないよ！",
            color=0x00ff98
        )
        
        state = checkLoginState(str(interaction.user.id))
        
        if state:
            res.title = "ログイン済みです"
            res.description = "もうログイン済みだよ！"
            client.logger.info(f"the User is already logged in: {interaction.user.name} ({interaction.user.id})")
        else :
            client.logger.info(f"the User is not logged in: {interaction.user.name} ({interaction.user.id})")

        await interaction.response.send_message(embed=res)
        
        client.logger.info(f"Successfully executed check request from {interaction.user.name} ({interaction.user.id})")
        
    except Exception as e:
        res = discord.Embed(
            title="ログイン状況の確認に失敗しました",
            description="時間をおいて再度試してみてください",
            color=0xff0000
        )
        await interaction.response.send_message(embed=res)
        
        log_exception(e)