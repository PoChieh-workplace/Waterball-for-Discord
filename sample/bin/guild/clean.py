from sample.bin.message import embed,IC
from sample.Cmdpermission import CommandError
from sample.Slash_permission import classic_error
from discord import Interaction,Message,File
from discord.ext.commands import Context
from core import Union,Color,ONLINE
import asyncio


class CountError(CommandError,classic_error):
    """數字大小錯誤"""

async def purge_messages(i:Union[Interaction,Context],count:int):
    c = i.channel
    ic = IC(i)
    if isinstance(i,Interaction):await i.response.defer()
    file = File("docs/image/single/loading.gif", filename="thumbnail.gif")
    load = await c.send(embed = embed("系統運作中",f"{ic.user().mention} 正在刪除 {count} 則訊息",Color.WHITE,thumbnail_type="gif"),file=file)
    def check(msg:Message):
        return msg.id!=load.id
    if count < 1 or count > 100:
        raise CountError("刪除數量只能在 1~100 則間")
    await c.purge(limit = count+1,check=check)
    await asyncio.sleep(1)
    await load.edit(embed=embed(f"{ONLINE} | 清除完成",f"成功清除 {count} 則訊息",Color.GREEN_GRASS).delafter(s=5),delete_after=5,attachments=[])#\n\n將於 <t:{timemethod.after(s=5)}:R> 刪除本訊息