from core import RED_HEART, STOCK
from discord import ButtonStyle,Interaction
from discord.ui import View,button,Button



class money(View):
    def __init__(self):
        super().__init__(timeout=0)
    @button(emoji = f"{STOCK}",label="購買股票",style=ButtonStyle.blurple,disabled=True,row=1)
    async def buy_stock_button_callback(self,interaction:Interaction, button:Button):
        pass
    @button(emoji = f"{RED_HEART}",label="贈與伴侶",style=ButtonStyle.blurple,disabled=True,row=1)
    async def give_mate_button_callback(self,interaction:Interaction, button:Button):
        pass