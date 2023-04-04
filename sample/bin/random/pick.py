from random import choice

from discord import Client,Interaction
from sample.bin.message import embed,IC
from sample.bin.image.rate import pick_img
from core import Color,Union

from discord.ext.commands import Context


async def random_is_ok(bot:Client,i:Union[Context,Interaction],title:str):
    i = IC(i)
    files,num = pick_img(title)
    if num >= 100 and num < 150:msg = "我覺得一定是了拉"
    elif num >= 150:msg = "我覺得一定不是喔"
    else:msg = choice([f"我覺得 {100-num}% 是",f"我覺得 {num}% 不行"])

    await i.send()(
        embed = embed(
            f" 詢問",
            f"{i.author.mention}：**{title}**\n\n{bot.user.mention}：`{msg}`",
            Color.BLACK,"png"
        ),
        file = files
    )