from sample.bin.message.embed import embed
from core.emoji import TIME_GIF,ALART_GIF
from discord import Message,Interaction,TextChannel
from discord.ext.commands import Context
from discord.ui import View
from datetime import datetime,timedelta
from typing import Union
import asyncio

# timer 顯示比例長度，預設 12
DEF = 12


# async def timer(mg:Union[Message,Interaction,TextChannel,Context],embed:embed,time:int,view:View=None):

#     tmp_word = embed.description
#     if tmp_word == None:tmp_word = ""

#     emoji = TIME_GIF
#     timebar = "".join([emoji]+["▬"*DEF])
#     embed.description = f"{timebar}\n\n{tmp_word}"

#     if isinstance(mg,Context) or isinstance(mg,TextChannel):
#         msg = await mg.send(embed=embed,view = None)
#     elif isinstance(mg,Message):
#         msg = mg
#     elif isinstance(mg,Interaction):
#         msg = await mg.response.edit_message(embed=embed,view = None)

#     maxtime = datetime.now()+timedelta(seconds=time)
#     tx = int((time-(maxtime-datetime.now()).seconds)/time*DEF)

#     while(tx<=DEF and tx>=0):
#         await asyncio.sleep(2)
#         if tx>(DEF/2):emoji = ALART_GIF
        

#         timebar = "".join(["▬"*tx]+[emoji]+["▬"*(DEF-tx)])
#         embed.description = f"{timebar}\n\n{tmp_word}"
#         await msg.edit(embed=embed,view = None)
#         tx = int((time-(maxtime-datetime.now()).seconds)/time*DEF)
#     return msg

class timer_message:
    def __init__(self,msg:Union[Message,Interaction,TextChannel,Context],embed:embed,time:int,view:View=None) -> None:
        self.mg = msg
        self.embed = embed
        self.time = time
        self.view = view
        self.stop = False

    def __del__(self) -> None:
        self.stop = True

    async def main(self):
        maxtime = datetime.now()+timedelta(seconds=self.time)
        tx = int((self.time-(maxtime-datetime.now()).seconds)/self.time*DEF)

        tmp_word = self.embed.description
        if tmp_word == None:tmp_word = ""

        emoji = TIME_GIF
        timebar = "".join([emoji]+["▬"*DEF])
        self.embed.description = f"{timebar}\n\n{tmp_word}"

        if isinstance(self.mg,Context) or isinstance(self.mg,TextChannel):
            self.msg = await self.mg.send(embed=self.embed,view = None)
        elif isinstance(self.mg,Message):self.msg = self.mg
        elif isinstance(self.mg,Interaction):
            self.msg = await self.mg.response.edit_message(embed=self.embed,view = None)
        
        while(tx<=DEF and tx>=0 and (not self.stop)):
            await asyncio.sleep(2)
            if tx>(DEF/2):emoji = ALART_GIF

            timebar = "".join(["▬"*tx]+[emoji]+["▬"*(DEF-tx)])
            self.embed.description = f"{timebar}\n\n{tmp_word}"
            await self.msg.edit(embed=self.embed,view = None)
            tx = int((self.time-(maxtime-datetime.now()).seconds)/self.time*DEF)