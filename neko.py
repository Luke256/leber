from common import *

@tree.command(name="neko", description="ねこ🐈")
async def neko(interaction: discord.Interaction):
    client.logger.info(f"Neko request from {interaction.user.name} ({interaction.user.id})")
    await interaction.response.send_message("にゃーん")