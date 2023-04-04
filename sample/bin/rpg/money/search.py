from discord import User
from discord.ext.commands import Context
from bin.embed import getembed
from bin.rpg.rpgsql import get_money_info, power, search_stock_from_name
from bin.View.stock import stock
from config.emoji import BACK, STOCK
from config.zh_tw import MONEY_PAPER
from config.color import ORANGE, RED

###查詢錢錢

async def search_money(ctx:Context,user:User):
    if user==None:user = ctx.author
    embed = getembed(
        f"{MONEY_PAPER} | 查詢財產",
        "\n\n".join([
            f"你目前擁有：",
            f"💰 存款：{get_money_info(user.id)} 元",
            f"⚡ 體力：{power.get(user.id)}%",
            f"🧾 股票：開發中"
        ]),
        ORANGE
    )
    await ctx.channel.send(embed=embed)


###查詢股票

async def search_stock(ctx,name:str):
    id = search_stock_from_name(name)
    if len(id)==0:return await ctx.send(embed = getembed(f"{BACK} | 查不到具有 {name} 的股票","",RED))
    else : id = id[0]
    embed = getembed(
        f"{STOCK} | 查詢到股票 {id[1]}",
        "\n\n".join([
            f"股票名稱：**{id[1]}**",
            f"股票代號：{id[0]}",
            f"📆 上市日期：`{id[3]}`",
            f"🧾 股票國際代碼(ISIN)：`{id[2]}`",
            f"🏭 公司類別：{id[5]}",
            f"✨ 股票狀態：{id[4]}",
            f"✨ CFI：{id[6]}"
        ]),
        ORANGE
    )
    await ctx.channel.send(embed=embed,view = stock())