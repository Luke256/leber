from common import *

@tree.command(name="eko", description="てすとー")
async def neko(interaction: discord.Interaction):
    await interaction.response.send_message("にゃーん")