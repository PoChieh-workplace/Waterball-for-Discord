from sample.bin.message import embed
from sample.bin.rpg.money.config import CHECK_IN_CHANNEL_ID, CHECK_IN_MONEY
from sample.bin.rpg.rpgsql import get_money_info, limit,earn_money
from core import Color
from discord import Client, Message
from datetime import date

CHECK_IN_ITEM = ('daily_chest',1)


async def check_in(bot:Client,message:Message):
    if message.channel.id == CHECK_IN_CHANNEL_ID:
        id = message.author.id
        limit.check_data(id)
        #確認上次登入時間
        data = limit.get_data_from_date(id,'check_in')
        if data != date.today():
            limit.set_date_to_now(id,'check_in')

            await message.add_reaction(bot.get_emoji(967781525737320579))
            await message.author.send(
                embed=embed(
                    "💳 | 簽到成功",
                    f"成功領取 {CHECK_IN_MONEY} 元 | 目前存款：{get_money_info(id)}",
                    Color.WHITE
                )
            )    
    return