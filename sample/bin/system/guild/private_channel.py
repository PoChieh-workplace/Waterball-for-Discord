import asyncio

from bin.embed import getembed
from bin.json import open_pc, write_pc

from discord.ext.commands import Context
from discord import ButtonStyle, ChannelType, Client, Interaction, TextChannel, Thread, User
from discord.ui import View,Button,button
from core import BACK, BLUE_STAR, DISCORD, GREEN_CHECK, LIGHT_PINK_CHECK, PENCIL, RED_CHECK, WHITE_STAR,PRE,Color
from sample.bin.message import embed,IC
from typing import Union

async def set_private_system(i:Union[Context,Interaction]):
    ctx = IC(i)
    c = ctx.ic.channel
    data = open_pc()
    if f"{c.id}" in data:
        if data[f"{c.id}"]["author"] != "None":return await ctx.send(embed = getembed(
            f"{BACK}｜系統錯誤",
            f"{ctx.user().mention}，\n這裡不是私人頻道母系統",
            Color.RED
        ))
        del data[f"{c.id}"]
        embeds = embed(
            f"{RED_CHECK}｜成功移除私人系統",
            f"{ctx.user().mention}，你已成功移除本頻道的私人系統功能",
            Color.GREEN
        )
    else:
        data[f"{c.id}"] = {"from_channel":"None","author":"None"}
        embeds = embed(
            f"{GREEN_CHECK}｜成功設立私人系統",
            f"{ctx.user().mention}，你成功設立本頻道的私人系統功能。\n> 如何使用？ 請使用`{PRE}help {ctx.command.cog_name}`",
            Color.GREEN
        )
    write_pc(data)
    return await ctx.send(embed=embeds)


#半公共頻道
async def set_selfchannel(ctx:Context):
    pass




#建立私人討論串
async def set_private_thread(ctx:Context,name:str):
    data = open_pc()
    if f"{ctx.channel.id}" not in data:
        return await ctx.send(embed = getembed(f"{BACK}｜錯誤",f"{ctx.author.mention}，此頻道並未設立私人系統",Color.RED))
    elif data[f"{ctx.channel.id}"]["from_channel"]!= "None":
        return await ctx.send(embed = getembed(f"{BACK}｜錯誤",f"{ctx.author.mention}，此頻道並不是私人系統控制區，若要建立子討論串，請創立本頻道者編輯頻道",RED))
    td = await ctx.channel.create_thread(name = f"{name}",invitable=True,reason=f"{ctx.author.name}-{ctx.author.id} 創建了頻道",auto_archive_duration=4320)
    await td.send(
        content=f"{ctx.author.mention}",
        embed = getembed(
            f"{LIGHT_PINK_CHECK}｜成功創立私人討論串",
            f"```感謝使用 WaterBall 私人系統，這裡是您建立的私人區域，本區域只有右側成員列表看的到本討論串，"
            f"請放心使用。若有遇到問題可告知管理員。以下為使用說明：```\n\n"
            f"{BLUE_STAR} 提及(@)某人(或機器人)即可以使他加入此討論區\n"
            f"> 使用 `{PRE}kick @人` 移除討論串中的人\n"
            f"> 使用 `{PRE}save` 來儲存本隱藏資料\n"
            f"> 使用 `{PRE}delchannel` 來刪除本頻道資料\n\n"
            f"💦 如果不放心開發者，可以先將我踢出去喔，覺得我有用再叫我也行",
            Color.PURPLE
        )
    )
    data[f"{td.id}"] = {"from_channel":ctx.channel.id,"author":ctx.author.id}
    write_pc(data)
    await ctx.message.delete()
    await ctx.send(embed = getembed(f"{DISCORD}｜已創立討論串",f"{ctx.author.mention}，請確認左側聊天欄的新討論串",PURPLE),delete_after=10.0)




async def kick_private_thread(ctx:Context,user:User):
    data = open_pc()
    if f"{ctx.channel.id}" not in data:return await ctx.send(ephemeral=True,embed = getembed(f"{BACK}｜錯誤","此頻道並未設立私人系統",RED))
    elif ctx.author.id != data[f"{ctx.channel.id}"]["author"]:return await ctx.send(embed = getembed(
        f"{BACK}｜指令錯誤",
        f"{ctx.author.mention}，你無法在此頻道使用本指令",
        RED
    ))
    else:
        mem = ctx.channel.guild.get_member(user)
        if isinstance(ctx.channel,TextChannel):await ctx.channel.set_permissions(mem,read_messages=False)
        elif isinstance(ctx.channel,Thread):await ctx.channel.remove_user(user)
        return await ctx.send(embed = getembed(
            f"{DISCORD}｜成功移除成員",
            f"{ctx.author.mention} 踢掉了成員 `{user.name}`",
            WHITE
        ))



#刪除討論串

async def delete_private_thread(ctx:Context):
    data = open_pc()
    if f"{ctx.channel.id}" not in data:return await ctx.send(ephemeral=True,embed = getembed(f"{BACK}｜錯誤","此頻道並未設立私人系統",RED))
    if data[f"{ctx.channel.id}"]["author"] == ctx.author.id:
        v = check_if_delete()
        msg = await ctx.channel.send(embed = getembed(
            f"❓｜確定刪除頻道",
            f"{ctx.author.mention}，此動作將會刪除本頻道(討論串)的所有資料，將一滴不漏的關閉，也無法被任何人復原\n\n"
            f"> {WHITE_STAR}想要留下來做紀念？或是暫停遊戲之後再回來？ `{PRE}save` 或許是你想要的",
            BLUE
        ),view = v)
        await asyncio.sleep(200)
        return await msg.edit(view = v)
    else:return await ctx.send(embed=getembed(
        f"{BACK}｜頻道錯誤",
        f"{ctx.author.mention}，\n本功能只能在討論串中進行",
        RED
    ))



#儲存討論串

async def save_thread(bot:Client,ctx:Context):
    if not isinstance(ctx.channel,Thread):return await ctx.send(embed=getembed(
        f"{BACK}｜頻道錯誤",
        f"{ctx.author.mention}，\n本功能只能在討論串中進行",
        RED
    ))
    data = open_pc()
    if f"{ctx.channel.id}" in data:
        await ctx.send(embed = getembed(
            f"{DISCORD}｜已存檔",
            f"{ctx.author.mention}，\n已儲存討論串，離開本頻道後將會隱藏，若要再次開啟，可至 `已儲存討論串` 操作",
            PURPLE
        ),delete_after=60)
        await ctx.channel.edit(archived=True)
        return await bot.get_channel(data[f"{ctx.channel.id}"]["from_channel"]).send(embed = getembed(
            f"{DISCORD}｜存檔公告",
            f"{ctx.author.mention}，\n已儲存一討論串，若要再次開啟，可至 `已儲存討論串` 操作",
            PURPLE
        ),delete_after=60)
    else:
        return await ctx.send(ephemeral=True,embed = getembed(f"{BACK}｜錯誤",f"{ctx.author.mention}，\n此頻道並未設立私人系統。",RED))


class check_if_delete(View):
    def __init__(self) -> None:
        super().__init__(timeout=180)
    async def on_timeout(self) -> None:
        for i in self.children:
            if isinstance(i,Button):i.disabled = True
    @button(label="確定刪除",emoji=PENCIL,style=ButtonStyle.green,custom_id="check_to_delete")
    async def check_delete(self,interaction:Interaction,button:Button):
        data = open_pc()
        if interaction.user.id == data[f"{interaction.channel_id}"]["author"]:
            await interaction.channel.delete()
            await interaction.client.get_channel(data[f"{interaction.channel_id}"]["from_channel"]).send(
                embed = getembed(
                    f"{DISCORD}｜關閉討論串",
                    f"{interaction.user.mention}，\n感謝使用 WaterBall 頻道管理功能，已刪除指定頻道\n\n> 代號: `{interaction.channel.id}`，此動作無法返回",PURPLE
                )
            ,delete_after=60)
            delete = [k for k,v in data.items() if v["from_channel"]==interaction.channel_id or k==f"{interaction.channel_id}"]
            for i in delete:del data[i]
            return write_pc(data)
    @button(label="取消動作",emoji=BACK,style=ButtonStyle.danger,custom_id="cancel")
    async def cancel(self,interaction:Interaction,button:Button):
        return await interaction.response.edit_message(embed = CONCIAL,view = None)