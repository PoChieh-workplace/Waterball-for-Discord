from core.config import PRE
from core.color import Color
from discord.ext.commands import Context
from discord.ext.commands import command,is_owner
from sample.CmdCog import Command_Cog
from sample.bin.message.embed import embed
from sample.bin.computer import Ram,CPU
class Owner(Command_Cog,name = "管理員用指令",help = False):
    @command(name="load")
    @is_owner()
    async def load_pyfile(self,ctx:Context,extension):
        await self.bot.load_extension(f'sample.cmd.{extension}')
        await self.bot.load_extension(f'sample.slash.{extension}_slash')
        await ctx.channel.send(f'Load {extension} Done')



    @command(name = "reload")
    @is_owner()
    async def reload_pyfile(self,ctx:Context,extension):
        await self.bot.reload_extension(f'sample.cmd.{extension}')
        await self.bot.reload_extension(f'sample.slash.{extension}_slash')
        await ctx.channel.send(f'reLoad {extension} Done')



    @command(name = "unload")
    @is_owner()
    async def unload_pyfile(self,ctx:Context,extension):
        await self.bot.unload_extension(f'sample.cmd.{extension}')
        await self.bot.unload_extension(f'sample.slash.{extension}_slash')
        await ctx.channel.send(f'unLoad {extension} Done')

    @command(
        name="ping",
        aliases=[],
        brief = '偵測',
        usage = f'{PRE}ping',
        description = (
            "YEE~\n"
        )
    )
    @is_owner()
    async def _ping_test(self,ctx:Context):
        await ctx.send(embed=embed("測試","embed system testing",color=Color.BLUE))
    

    @command(name = "ram",aliases=[])
    @is_owner()
    async def send_now_Ram(self,ctx:Context):
        return await Ram(ctx)


    @command(name = "cpu",aliases=[])
    @is_owner()
    async def send_now_cpu(self,ctx:Context):
        return await CPU(ctx)


async def setup(bot):
    await bot.add_cog(Owner(bot))
