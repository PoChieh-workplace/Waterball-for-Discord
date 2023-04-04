from discord.ui import Modal
from discord import Interaction
from core import Color,OFFLINE,ONLINE
from sample.bin.message import embed
from typing import Optional
#discord 嵌入式訊息腳本

class modal(Modal,title="未定義表單"):
    def __init__(self,timeout: Optional[float] = None, custom_id: str = ...) -> None:
        super().__init__(timeout=timeout, custom_id=custom_id)
    def __init_subclass__(cls, *, title: str = ...) -> None:
        return super().__init_subclass__(title=title)
    
    async def on_error(self, i: Interaction, error: Exception, /) -> None:
        return await i.response.send_message(
            embed=embed(
                "錯誤",
                f"似乎發生了問題！！Error:```{error}```",
                Color.RED
            ),ephemeral=True
        )