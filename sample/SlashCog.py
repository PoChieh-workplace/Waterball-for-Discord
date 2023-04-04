from sample.Slash_permission import classic_error
from discord import Client,Interaction
from discord.app_commands import AppCommandError
from discord.ext.commands import Cog
from sample.bin.message.embed import embed
from core import *

class Slash_Cog(Cog):
    def __init__(self,bot):
        self.bot:Client = bot
        
    def __init_subclass__(cls,help:bool = False) -> None:
        cls.help = help
        return super().__init_subclass__()

    async def cog_app_command_error(self, interaction: Interaction, error: AppCommandError) -> None:
        if interaction.is_expired:
            if isinstance(error,classic_error):
                return await interaction.response.send_message(
                    embed = embed(f"{ERROR} | 操作失敗",f"{error}",Color.RED),ephemeral=True)
            else:return await interaction.response.send_message(
                    embed = embed(f"{BACK} | 程式似乎發生問題",f"內容：```{error}```\n\n錯誤代碼：{type(error)}",Color.RED),ephemeral=True)
        else:
            return await interaction.channel.send(
                embed = embed(f"{BACK} | 程式似乎發生問題",f"內容：```{error}```\n\n錯誤代碼：{type(error)}",Color.RED))