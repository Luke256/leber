from common import *

@tree.command(name="neko", description="γ­γπ")
async def neko(interaction: discord.Interaction):
    client.logger.info(f"Neko request from {interaction.user} ({interaction.user.id})")
    await interaction.response.send_message("γ«γγΌγ")