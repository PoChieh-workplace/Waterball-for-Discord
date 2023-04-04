from discord import User
from discord.ext.commands import command,Context
from core import PRE
from sample.CmdCog import Command_Cog
from sample.bin.game import Game_select
from sample.bin.meme import to_rip_user,Incense
from sample.bin.message import IC


class Game(Command_Cog,name = '遊戲與迷因'):
    @command(
        name="game",
        aliases=['g'],
        brief = '是遊戲！！可以玩嗎？',
        usage = f'{PRE}game',
        description = (
            "允許虛擬賭博，但別搞到家庭分裂呦！\n"
        )
    )
    async def _play_game(self,ctx:Context):
        return await Game_select().main(ctx)
    
    @command(
        name = "rip",
        aliases=[],
        brief = '埋葬一個人！記得上香喔！',
        usage = f'{PRE}rip',
        description = (
            "傳送一張你祖宗的照片，農曆七月別亂用本指令喔！\n"
        )
    )
    async def _rip_user(self,ctx:Context,user:User = None):
        return await to_rip_user(IC(ctx),user)
    
    @command(
        name = "incense",
        aliases=['inc'],
        brief = '上香祖先，希望他不要害自己單身',
        usage = f'{PRE}incense',
        description = (
            "為衰人上香，記得埋葬喔！\n"
        )
    )
    async def _rip_user(self,ctx:Context,user:User = None):
        return await Incense().main(i=IC(ctx),user=user)

async def setup(bot):
    await bot.add_cog(Game(bot))