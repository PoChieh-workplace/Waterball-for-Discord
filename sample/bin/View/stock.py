from core import STOCK
from discord.ui import View,Button,button
from discord import ButtonStyle,Interaction




class stock(View):
    def __init__(self):
        super().__init__(timeout=0)
    @button(emoji = f"{STOCK}",label="購買股票",style=ButtonStyle.blurple,disabled=True,row=1)
    async def buy_stock_button_callback(self,interaction:Interaction, button:Button):
        pass