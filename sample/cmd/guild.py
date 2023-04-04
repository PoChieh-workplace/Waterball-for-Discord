from discord import User, Message
from discord.ext.commands import command,Cog,Context
from sample.bin.function_cmd.whsh import whsh_curriculum_button
from sample.bin.function_cmd.function import whsh_selection
from sample.bin.rpg.system.checkin import check_in
from sample.bin.guild import *
from sample.bin.message import IC
from sample.bin.datechannel import datechannel
from sample.CmdCog import Command_Cog
from sample.Cmdpermission import is_admin_cmd,have_registered_cmd
from core import PRE,WHITE_STAR



class guild(Command_Cog,name = '伺服器'):
    @command(
        name = "guild",
        aliases=["server"],
        brief = '查詢伺服器資訊',
        usage = f'{PRE}guild',
        description = (
            "顯示資訊\n"
        )
    )
    async def _guild_information(self,ctx:Context):
        return await search_guild_inf(IC(ctx))

    @command(
        name = "member",
        aliases=["user"],
        brief = '查詢成員資訊',
        usage = f'{PRE}member <@人/人id>',
        description = (
            "顯示玩家資料\n"
            "範例\n"
            f"`{PRE}r @水球` 顯示水球資料\n\n"
            f"`{PRE}r 45623` 顯示id為45623的玩家資料\n\n"
        )
    )
    async def _member_information(self,ctx:Context,arg:User=None):
        return await search_member_inf(IC(ctx),arg)



    @command(
        name = "function",
        aliases=['whsh','f'],
        brief = '伺服器功能快捷鍵',
        usage = f'{PRE}f',
        description = (
            "管理身分組、徵選管管、意見回饋、學號綁定"
        )
    )
    async def _whsh_control(self,ctx:Context):
        v = whsh_selection()
        await v.main(IC(ctx))



    @command(
        name = "purge",
        aliases = ['clean'],
        brief = '清理訊息',
        usage = f'{PRE}purge <數量>',
        description = (
            "清理數則訊息"
        )
    )
    @is_admin_cmd()
    async def _clean_message(self,ctx:Context,count:int):
        await purge_messages(ctx,count)


    # 沒用的東西
    # @commands.command(name= "history",aliases = ['his','past'])
    # async def _check_histury(self,ctx,channel:discord.TextChannel=None):
    #     if channel==None:channel = ctx.channel
    #     for i in [message async for message in channel.history(limit=123)]:print(type(i))


    #以下為文華群專用功能

    @command(
        name = "curriculum",
        aliases = ['c','class'],
        brief = '查詢文華課表',
        usage = f'{PRE}c <班級代號>',
        description = (
            "顯示班級的文華每周課表"
        )
    )
    @have_registered_cmd()
    async def classc(self,ctx:Context,cls:str):
        c = whsh_curriculum_button(ctx.author,cls)
        await c.start(IC(ctx))
    

    @command(
        name = "datechannel",
        aliases = ['date'],
        brief = '設定倒數日頻道',
        usage = f'{PRE}datechannel [年] [月] [日] [名稱(不可有空白)]',
        description = (
            "設定頻道名稱為可倒數日子的標題\n"
            "在內容中插入`{}` 將替換成日子，注意！discord頻道名稱不可有空白\n"
            "範例：\n"
            f"`{PRE}date`\n\n"
            f"`{PRE}date 2023 7 24`\n\n"
            f"`{PRE}date 2024 1 1 跨年倒數{'{}'}天` -> 跨年倒數***天\n\n"
        )
    )
    async def _Set_Date_Channel(self,ctx:Context,y:int=None,m:int=1,d:int=1,context = None):
        if y == None:v = datechannel(ctx.author,ctx.channel.id,None,None)
        else:v = datechannel(ctx.author,ctx.channel.id,(y,m,d),context)
        await ctx.channel.send(embed=v.embed(),view = v)


    # 文華群簽到
    @Cog.listener()
    async def on_message(self,message:Message):
        return await check_in(self.bot,message)


    # 阿傑教室自動改名
    # @Cog.listener()
    # async def on_voice_state_update(self,user:Member,bf:VoiceState,af:VoiceState):
    #     try:
    #         r = get_whsh_inf(user)
    #         i = self.bot.get_channel(976787068518809640)
    #         if r != None:
    #             if af.channel!=None:
    #                 if af.channel.category==i:
    #                     if bf.channel==None:set_tmp_nickname(user)
    #                     elif bf.channel.category!=i:set_tmp_nickname(user)
    #                     await user.edit(nick=f"{r[3]}{r[1]}")
    #                 elif bf.channel!=None:
    #                     if bf.channel.category==i and af.channel.category!=i:
    #                         await user.edit(nick=get_tmp_nickname(user))
    #             elif bf.channel.category==i:
    #                 await user.edit(nick=get_tmp_nickname(user))
    #     except Forbidden:pass




    # 私人聊天室


    @command(
        name = "chatchannel",
        aliases = ['cc'],
        brief = '設置私人聊天室指令專用頻道',
        usage = f'{PRE}cc',
        description = (
            f"設立後可使用 {PRE}pt 功能創立私人討論串。"
            "供所有成員各自管理屬於自己的聊天室，"
            "享有伺服之各功能，成員隨創立者更動"
        )
    )
    @is_admin_cmd()
    async def set_private_system_channel(self,ctx:Context):
        return await set_private_system(IC(ctx))



    @command(
        name = "private",
        aliases = ['pt','thread'],
        brief = '設置私人聊天室指令專用頻道',
        usage = f'{PRE}pt <名稱>',
        description = (
            f"{WHITE_STAR}注意｜本指令需要二級加成才能使用\n"
        )
    )
    async def add_private_channel(self,ctx:Context,*,name):
        return await set_private_thread(IC(ctx),name)

    @command(
        name = "local",
        aliases = ['selfchannel','sc','pc'],
        brief = '設置私人聊天室指令專用頻道(未開發)',
        usage = f'{PRE}pc',
        description = (
            f"建立半公共頻道\n"
            f"> {WHITE_STAR}注意｜本頻道未開發\n"
        )
    )
    async def add_self_channel(self,ctx:Context):
        return await set_selfchannel(IC(ctx))
    

    @command(
        name = "delchannel",
        aliases = ['dlc'],
        brief = '刪除私人討論串',
        usage = f'{PRE}dlc',
        description = (
            f"{WHITE_STAR}注意｜本系統需要二級加成且為討論串開啟者才能使用\n"
        )
    )
    async def del_private_channel(self,ctx:Context):
        return await delete_private_thread(IC(ctx))
    

    @command(
        name = "kick",
        aliases = ['k'],
        brief = '在私人討論串中剔除指定人物',
        usage = f'{PRE}k @水球',
        description = (
            f"{WHITE_STAR}注意｜本指令只限於 WB私人系統中 討論串開啟者使用\n"
        )
    )
    async def kick_private_thread(self,ctx:Context,user:User):
        return await kick_private_thread(IC(ctx),user)

    @command(
        name = "save",
        aliases = ['s'],
        brief = '儲存在私人討論串中的所有資料',
        usage = f'{PRE}s',
        description = (
            f"注意｜本指令只限於 WB私人系統中 討論串開啟者使用\n"
        )
    )
    async def save_private_channel(self,ctx:Context):
        return await save_thread(IC(ctx))



async def setup(bot):
    await bot.add_cog(guild(bot))