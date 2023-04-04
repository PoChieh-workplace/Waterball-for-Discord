from sample.bin.message import embed
from sample.bin.rpg.rpgsql import limit
from ..player import get_player_from_user
from ..item_.model import item_
from ..item_.get import get_item
from core import Color,TREASURE
from discord import Client, Message
from datetime import date

CHECK_IN_ITEM = ('daily_chest',1)
CHECK_IN_CHANNEL_ID = 985692580228530227  #1080482707068440667

async def check_in(bot:Client,message:Message):
    if message.channel.id == CHECK_IN_CHANNEL_ID:
        id = message.author.id
        limit.check_data(id)
        #確認上次登入時間
        data = limit.get_data_from_date(id,'check_in')
        if data != date.today():
            limit.set_date_to_now(id,'check_in')
            
            ps = get_player_from_user(message.author)
            if len(ps)==0:return

            for i in ps:
                item:item_ = get_item(CHECK_IN_ITEM[0])(count = CHECK_IN_ITEM[1])
                i.backpack.add_item(item)
                i.save()
            
            await message.add_reaction(bot.get_emoji(1081208615509168209))
            await message.author.send(
                embed=embed(
                    f"{TREASURE} | 簽到成功",
                    f"已為角色 {' 、 '.join([f'`{n.name}`' for n in ps])} 成功領取 `{item.name}*{CHECK_IN_ITEM[1]}`",
                    Color.LIGHT_ORANGE
                )
            )   