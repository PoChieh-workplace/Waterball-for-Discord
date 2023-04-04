from ..bin.rpg.system.register import register_buttons
from ..bin.rpg.system.backpack_use import backpack_open
from ..bin.rpg.player import get_player_from_user
from sample.SlashCog import Slash_Cog
from discord.app_commands import command,rename,Group,Choice
from discord import Interaction
from typing import List
from ..bin.chatgpt.sys import LANGS,chatgpt_view

class Random_Slash(Slash_Cog,name = '指令包_RPG',help = False):

    rpg = Group(name='rpg',description='文華魔法高級中等學校')


    @rpg.command(
        name="register-登入",
        description = "參加文華魔法高級中等學校課程"
    )
    async def register_rpg(self,i:Interaction):
        return await register_buttons(i.user).reload(i,first=True)
    

    # 背包
    @rpg.command(
        name="backpack-背包",
        description="打開背包查看或使用物品"
    )
    @rename(uuid = "角色")
    async def open_backpack(self,i:Interaction,uuid:int):
        return await backpack_open(i,uuid)
    @open_backpack.autocomplete('uuid')
    async def langs_complete(self,i: Interaction,c: str) -> List[Choice[str]]:
        p = get_player_from_user(i.user)
        return [
            Choice(name=j.name , value = j.uuid) for j in p
        ]
    

    # chatgpt
    @command(
        name = "chatgpt-聊天",
        description="採用 chatgpt 系統聊天"
    )
    @rename(chat = "內容",lang = "語言")
    async def chat_gpt(self,i:Interaction,chat:str,lang:int = 0):
        return await chatgpt_view().start(i,chat,lang)
    
    @chat_gpt.autocomplete('lang')
    async def langs_complete(self,interaction: Interaction,current: str) -> List[Choice[str]]:
        l = [k[1] for k in LANGS]
        return [
            Choice(name=i[1], value=i[0]) for i in enumerate(l)
        ]


async def setup(bot):
    await bot.add_cog(Random_Slash(bot))