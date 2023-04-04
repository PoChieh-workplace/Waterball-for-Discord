from sample.SlashCog import Slash_Cog
from core.config import PRE
from core.color import Color
from discord.app_commands import command,Choice
from sample.Slash_permission import is_owner_slash
from discord import Interaction
from discord.ext import commands
from sample.bin.message.embed import embed
from typing import List

class Owner_Slash(Slash_Cog,name = "指令包_服主指令",help = False):

    @command(
        name="ping",
        description = "測試系統"
    )
    @is_owner_slash()
    async def _ping_test_slash(self,interaction:Interaction):
        await interaction.response.send_message(embed=embed("測試","11",color=Color.BLUE))
    
    @command(name="load")
    @is_owner_slash()
    async def load_pyfile(self,ctx:Interaction,extension:str):
        await self.bot.load_extension(f'sample.cmd.{extension}')
        await self.bot.load_extension(f'sample.slash.{extension}_slash')
        await ctx.response.send_message(embed = embed("",f'載入 {extension} 完成',Color.WHITE))

    @command(name = "reload")
    @is_owner_slash()
    async def reload_pyfile(self,ctx:Interaction,extension:str):
        await self.bot.reload_extension(f'sample.cmd.{extension}')
        await self.bot.reload_extension(f'sample.slash.{extension}_slash')
        await ctx.response.send_message(embed = embed("",f'重載 {extension} 完成',Color.WHITE))

    @command(name = "unload")
    @is_owner_slash()
    async def unload_pyfile(self,ctx:Interaction,extension:str):
        await self.bot.unload_extension(f'sample.cmd.{extension}')
        await self.bot.unload_extension(f'sample.slash.{extension}_slash')
        await ctx.response.send_message(embed = embed("",f'卸載 {extension} 完成',Color.WHITE))


async def setup(bot:commands.Bot):
    await bot.add_cog(Owner_Slash(bot))
