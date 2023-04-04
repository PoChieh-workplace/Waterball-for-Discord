from discord.ui import View,Item
from discord import Interaction
from sample.bin.message import embed
from core import ERROR,BACK,Color
from typing import Any

class define_inter_error(Exception):
    """已被定義錯誤(for View)"""
    
    @classmethod
    def NotCommandProposer(cls):
        return cls("你不是指令發起者")

class Unknow_Error(Exception):
    """未知錯誤"""

class V(View):
    """修正式操作介面"""

    def __init__(self,timeout:int=0):
        super().__init__(timeout=timeout)

    async def on_error(self, i: Interaction, error: Exception, item: Item[Any], /) -> None:
        try:
            if isinstance(error,define_inter_error):
                return await i.response.send_message(embed=embed(f"{ERROR} | 操作失敗",f"{error}",Color.RED),ephemeral=True)
        except:
            return await i.channel.send(
                embed = embed(f"{BACK} | 程式似乎發生問題",f"{i.user.mention},內容：```{error}```\n\n錯誤代碼：{type(error)}",Color.RED))
        
        return await i.response.send_message(embed=embed(f"{BACK} | 程式似乎發生異常",f"如果重複發生，可告知開發人員\n錯誤代碼：```{error}```\n\n錯誤類別：`{type(error)}`",Color.RED),ephemeral=True)