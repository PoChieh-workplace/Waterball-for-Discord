from sample.SlashCog import Slash_Cog
from core.config import PRE
from discord.app_commands import command,Group
from discord import Interaction,User
from sample.bin.message import IC
from sample.bin.game import Game_select
from sample.bin.meme import to_rip_user,Incense






class Game_Slash(Slash_Cog,name = "指令包_遊戲與迷因",help = False):
    
    meme = Group(name='meme',description='迷因梗圖')

    @command(
        name = "game-遊戲聽",
        description = '是遊戲！！可以玩嗎？'
    )
    async def _play_game_slash(self,i:Interaction):
        return await Game_select().main(i)
    
    @meme.command(
        name = "rip-埋葬",
        description = "傳送一張你祖宗的照片，農曆七月別亂用本指令喔！"
    )
    async def _rip_user(self,i:Interaction,成員:User = None):
        return await to_rip_user(IC(i),成員)

    @meme.command(
        name = "incense-上香",
        description = "祭拜你的朋友吧，說不定他會下凡找你呢！"
    )
    async def _incense_user(self,i:Interaction,成員:User = None):
        return await Incense().main(i=IC(i),user=成員)
    


async def setup(bot):
    await bot.add_cog(Game_Slash(bot))
