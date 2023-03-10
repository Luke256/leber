import discord

class BadButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="体調チェック完了",
            description="お大事に...",
            color=0xFFB444
        )
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="LEBERを開く", 
            url="https://web.leber.jp/index.html", 
            style=discord.ButtonStyle.link
        ))
        await interaction.followup.send(embed=embed, view=view)
