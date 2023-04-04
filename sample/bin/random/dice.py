from random import randint
from discord import Client,Interaction,ButtonStyle
from discord.ext.commands import CommandError,Context
from discord.ui import Button,button
from sample.bin.message import embed,IC,V
from sample.Slash_permission import classic_error
from core import Color
from typing import Union

class MaxSmallerThanMin(CommandError,classic_error):
    """最大值不可小於最小值"""
class NumberError(CommandError,classic_error):
    """資料型態錯誤，必須輸入數字"""
class FloatError(CommandError,classic_error):
    """小數最多只能10位數"""


async def to_dice_a_number(ctx:Union[Context,Interaction],max:int,min:int,flo:int):
    if max<min:raise MaxSmallerThanMin("最大值不可小於最小值")
    elif flo>10:raise FloatError("小數最多只能10位數")
    t = 10**flo
    req = randint(min*t,max*t)/t

    ic = IC(ctx)

    if flo==0:
        req = int(req)

    await ic.send()(
        
        embed = embed(
            f"🎲骰出 {min}~{max}",
            f"♫˚♪•《 `{req}` 》♫˚♪•  ",
            Color.PURPLE_LIGHT
        ),
        view=dice_again(max,min,flo)
    )

class dice_again(V):
    def __init__(self,max,min,flo):
        super().__init__(timeout=0)
        self.max = max
        self.min = min
        self.flo = flo
    @button(
        style= ButtonStyle.blurple,
        label = "再骰一次",
        emoji = "🎲"
    )
    async def dice_(self,i:Interaction,b:Button):
        self.remove_item(b)
        await to_dice_a_number(i,self.max,self.min,self.flo)
        return await i.message.edit(view=self)