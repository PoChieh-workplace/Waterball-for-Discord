from core import *
from discord.ext.commands import Context,command
from sample.CmdCog import Command_Cog
from sample.bin.message.limit import timer_message
from sample.bin.message.embed import embed

class Message_test(Command_Cog,name = "訊息測試",help = True):

    @command(
        name="limit",
        aliases=["lim"],
        brief = '限時訊息',
        usage = f'{PRE}lim',
        description = (
            "YEE~\n"
        )
    )
    async def _limit_message(self,ctx:Context):
        a = timer_message(msg=ctx,embed=embed("Yee","Yee",Color.CYAN),time=60)
        await a.main()

async def setup(bot):
    await bot.add_cog(Message_test(bot))
