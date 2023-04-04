from discord.app_commands import command,Choice,rename,Group,guilds,guild_only
from discord import Interaction,User
from discord.ext import commands
from datetime import date
from sample.SlashCog import Slash_Cog
from sample.bin.guild import *
from sample.bin.message import IC
from sample.bin.datechannel import datechannel
from sample.Slash_permission import is_admin,have_registered
from sample.bin.function_cmd.whsh import whsh_curriculum_button
from sample.bin.function_cmd.function import whsh_selection

from typing import List

class Guild_Slash(Slash_Cog,name = "指令包_伺服器",help = False):

    guild = Group(name='guild',description='伺服器功能')
    @guild.command(
        name = "guild-伺服器資訊",
        description = "顯示伺服器資訊"
    )
    @guild_only()
    async def _guild_information(self,i:Interaction):
        return await search_guild_inf(IC(i))

    @guild.command(
        name = "member-成員資訊",
        description = "顯示成員資料"
    )
    @guild_only()
    @rename(members = "成員")
    async def _member_information(self,i:Interaction,members:User=None):
        return await search_member_inf(IC(i),members)


    @command(
        name = "function-快捷功能",
        description = "管理身分組、徵選管管、意見回饋、學號綁定"
    )
    @guilds(910150769624358914)
    async def _whsh_control(self,i:Interaction):
        v = whsh_selection()
        await v.main(IC(i))

    @guild.command(
        name = "purge-清理",
        description = "清理數則訊息"
    )
    @is_admin()
    @rename(count = "數量")
    async def _clean_message(self,i:Interaction,count:int):
        await purge_messages(i,count)


    #以下為文華群專用功能

    @guild.command(
        name = "curriculum-文華課表",
        description = "顯示班級的文華每周課表"
    )
    @have_registered()
    @rename(cls = "班級")
    async def classc(self,i:Interaction,cls:str):
        c = whsh_curriculum_button(i.user,cls)
        await c.start(IC(i))


    # 私人聊天室


    @guild.command(
        name = "chatchannel-wb私人系統",
        description = "創立私人討論串，供所有成員各自管理屬於自己的聊天室，"
    )
    @is_admin()
    @guild_only()
    async def set_private_system_channel(self,i:Interaction):
        return await set_private_system(IC(i))



    @guild.command(
        name = "private-私人討論串",
        description = "本指令需要二級加成才能使用"
    )
    @rename(name = "討論串名稱")
    @guild_only()
    async def add_private_channel(self,i:Interaction,name:str):
        return await set_private_thread(IC(i),name)

    @guild.command(
        name = "local-私人頻道",
        description = "(未開發完成)"
    )
    async def add_self_channel(self,i:Interaction):
        return await set_selfchannel(IC(i))
    

    @guild.command(
        name = "delchannel-刪除討論串",
        description = "需為 wb 私人系統 的私人討論串"
    )
    @guild_only()
    async def del_private_channel(self,i:Interaction):
        return await delete_private_thread(IC(i))
    

    @guild.command(
        name = "kick-剔除人員",
        description = "本指令只限於 wb 私人系統中 討論串開啟者使用"
    )
    @rename(user = "人員")
    async def kick_private_thread(self,i:Interaction,user:User):
        return await kick_private_thread(IC(i),user)

    @guild.command(
        name = "save-儲存討論串",
        description = (
            f"本指令只限於 wb 私人系統中 討論串開啟者使用\n"
        )
    )
    async def save_private_channel(self,i:Interaction):
        return await save_thread(IC(i))
    
    @guild.command(
        name = "date-倒數日設定",
        description = '設定倒數日頻道'
    )
    @is_admin()
    @guild_only()
    @rename(y = "年",m = "月",d = "日",name = "頻道名稱")
    async def _set_date_channel_lash(self,i:Interaction,y:int=int(date.today().strftime('%Y'))+1,m:int=1,d:int=1,name:str = None):
        v = datechannel(i.user,i.channel.id,(y,m,d),name)
        return await i.response.send_message(embed=v.embed(),view = v)

    @_set_date_channel_lash.autocomplete('y')
    async def fruits_autocomplete(self,interaction: Interaction,current: str) -> List[Choice[str]]:
        y = int(date.today().strftime('%Y'))
        msgs = [f"{y}",f"{y+1}",f"{y+2}"]
        return [Choice(name=i, value=i)for i in msgs if current.lower() in i.lower()]


async def setup(bot:commands.Bot):
    await bot.add_cog(Guild_Slash(bot))
