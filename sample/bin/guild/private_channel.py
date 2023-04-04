import asyncio
from sample.bin.message import embed,IC
from sample.bin.json import open_pc, write_pc
from sample.Cmdpermission import CommandError
from sample.Slash_permission import classic_error
from discord.ext.commands import Context
from discord import ButtonStyle, Interaction, TextChannel, Thread, User
from discord.ui import View,Button,button

from core import BACK, BLUE_STAR, DISCORD, GREEN_CHECK, LIGHT_PINK_CHECK, PENCIL, OFFLINE, WHITE_STAR, PRE, Color


class typeError(classic_error,CommandError):
    """無法操作"""
    @classmethod
    def PrivateChannelUnset(cls):
        return cls(f"此頻道並未設立私人系統，設立請用 `/chatchannel`")
    
    @classmethod
    def NotParentSystem(cls):
        return cls("這裡不是私人頻道母系統")
    
    @classmethod
    def ThreadOnly(cls):
        return cls("本功能只能在討論串中進行")


async def set_private_system(ic:IC):
    u = ic.user()
    c = ic.ic.channel
    data = open_pc()
    if f"{c.id}" in data:
        if data[f"{c.id}"]["author"] != "None":raise typeError.NotParentSystem()
        del data[f"{c.id}"]
        embeds = embed(
            f"{OFFLINE}｜成功移除私人系統",
            f"{u.mention}，你已成功移除本頻道的私人系統功能",
            Color.GREEN
        )
    else:
        data[f"{c.id}"] = {"from_channel":"None","author":"None"}
        embeds = embed(
            f"{GREEN_CHECK}｜成功設立私人系統",
            f"{u.mention}，你成功設立本頻道的私人系統功能。",
            Color.GREEN
        )
    write_pc(data)
    return await ic.send()(embed=embeds)


#半公共頻道
async def set_selfchannel(ctx:Context):
    pass




#建立私人討論串
async def set_private_thread(ctx:IC,name:str):
    data = open_pc()
    c = ctx.ic.channel

    if f"{c.id}" not in data: raise typeError.PrivateChannelUnset()
    elif data[f"{c.id}"]["from_channel"]!= "None":raise typeError("此頻道並不是私人系統控制區，若要建立子討論串，請創立本頻道者編輯頻道")

    td = await c.create_thread(name = f"{name}",invitable=True,reason=f"{ctx.user().name}-{ctx.user().id} 創建了頻道",auto_archive_duration=4320)
    await td.send(
        content=f"{ctx.user().mention}",
        embed = embed(
            f"{LIGHT_PINK_CHECK}｜成功創立私人討論串",
            f"```感謝使用 WaterBall 私人系統，這裡是您建立的私人區域，本區域只有右側成員列表看的到本討論串，"
            f"請放心使用。若有遇到問題可告知管理員。以下為使用說明：```\n\n"
            f"{BLUE_STAR} 提及(@)某人(或機器人)即可以使他加入此討論區\n"
            f"> 使用 `{PRE}kick @人` 移除討論串中的人\n"
            f"> 使用 `{PRE}save` 來儲存本隱藏資料\n"
            f"> 使用 `{PRE}delchannel` 來刪除本頻道資料\n\n",
            Color.PURPLE
        )
    )
    data[f"{td.id}"] = {"from_channel":c.id,"author":ctx.user().id}
    write_pc(data)
    try:await ctx.ic.message.delete()
    except:pass
    embeds = embed(f"{DISCORD}｜已創立討論串",f"{ctx.user().mention}，請確認左側聊天欄的新討論串",Color.PURPLE).delafter(s=5)
    if isinstance(ctx.ic,Interaction):return await ctx.send()(embed=embeds,delete_after=10.0,ephemeral=True)
    else:return await ctx.send()(embed = embeds,delete_after=10.0)




async def kick_private_thread(ctx:IC,user:User):

    data = open_pc()
    c = ctx.ic.channel
    
    if f"{c.id}" not in data:raise typeError("此頻道並未設立私人系統")
    elif ctx.user().id != data[f"{c.id}"]["author"]:raise typeError("你無法在此頻道使用本指令")
    else:
        mem = c.guild.get_member(user)
        if isinstance(c,TextChannel):await c.set_permissions(mem,read_messages=False)
        elif isinstance(c,Thread):await c.remove_user(user)
        return await ctx.send()(embed = embed(
            f"{DISCORD}｜成功移除成員",
            f"{ctx.user().mention} 踢掉了成員 `{user.name}`",
            Color.WHITE
        ).delafter(s=5),delete_after=10.0)





#刪除討論串

async def delete_private_thread(ctx:IC):
    data = open_pc()
    c = ctx.ic.channel
    if f"{c.id}" not in data:raise typeError("此頻道並未設立私人系統")
    if data[f"{c.id}"]["author"] == ctx.user().id:
        v = check_if_delete()
        msg = await ctx.send()(embed = embed(
            f"❓｜確定刪除頻道",
            f"{ctx.user().mention}，此動作將會刪除本頻道(討論串)的所有資料，將一滴不漏的關閉，也無法被任何人復原\n\n"
            f"> {WHITE_STAR}想要留下來做紀念？或是暫停遊戲之後再回來？ `{PRE}save` 或許是你想要的",
            Color.BLUE
        ),view = v)
        await asyncio.sleep(200)
        return await msg.edit(view = v)
    else:raise typeError("本功能只能在討論串中進行")



#儲存討論串

async def save_thread(ctx:IC):
    bot = ctx.ic.client
    c = ctx.ic.channel
    if not isinstance(c,Thread):raise typeError.ThreadOnly()
    data = open_pc()
    if f"{c.id}" in data:
        await ctx.send(embed = embed(
            f"{DISCORD}｜已存檔",
            f"{ctx.user().mention}，\n已儲存討論串，離開本頻道後將會隱藏，若要再次開啟，可至 `已儲存討論串` 操作",
            Color.PURPLE
        ),delete_after=60)
        await c.edit(archived=True)
        return await bot.get_channel(data[f"{c.id}"]["from_channel"]).send(embed = embed(
            f"{DISCORD}｜存檔公告",
            f"{ctx.user().mention}，\n已儲存一討論串，若要再次開啟，可至 `已儲存討論串` 操作",
            Color.PURPLE
        ).delafter(min=1),delete_after=60)
    else:raise typeError.PrivateChannelUnset()


class check_if_delete(View):
    def __init__(self) -> None:
        super().__init__(timeout=180)
    async def on_timeout(self) -> None:
        for i in self.children:
            if isinstance(i,Button):i.disabled = True


    @button(label="確定刪除",emoji=PENCIL,style=ButtonStyle.green,custom_id="check_to_delete")
    async def check_delete(self,interaction:Interaction,button:Button):
        data:dict = open_pc()
        if interaction.user.id == data[f"{interaction.channel_id}"]["author"]:
            await interaction.channel.delete()
            await interaction.client.get_channel(data[f"{interaction.channel_id}"]["from_channel"]).send(
                embed = embed(
                    f"{DISCORD}｜關閉討論串",
                    f"{interaction.user.mention}，\n感謝使用 WaterBall 頻道管理功能，已刪除指定頻道\n\n> 代號: `{interaction.channel.id}`，此動作無法返回",Color.PURPLE
                ).delafter(min=1)
            ,delete_after=60)
            delete = [k for k,v in data.items() if v["from_channel"]==interaction.channel_id or k==f"{interaction.channel_id}"]
            for i in delete:del data[i]
            return write_pc(data)

    @button(label="取消動作",emoji=BACK,style=ButtonStyle.danger,custom_id="cancel")
    async def cancel(self,interaction:Interaction,button:Button):
        await interaction.response.defer()
        return await interaction.message.edit(embed = embed.cancel(),view = None,delete_after=10.0)