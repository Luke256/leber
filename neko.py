from common import *

@tree.command(name="neko", description="ねこ🐈")
async def neko(interaction: discord.Interaction):
    await interaction.response.send_message("にゃーん")