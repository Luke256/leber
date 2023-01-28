from common import *

@tree.command(name="neko", description="てすとー")
async def neko(interaction: discord.Interaction):
    await interaction.response.send_message("にゃーん")