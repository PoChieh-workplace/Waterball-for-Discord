from bin.message.embed import embed
from discord import Message
from discord.ui import View
from datetime import datetime,timedelta
import asyncio

class GameModel(View):
    def __init__(self,msg:Message,name = "未命名遊戲"):
        super().__init__(timeout=0)
        self.msg = msg
    
    
    def embed(self,string:str):
        return embed()
    
    async def main(self):
        pass

    async def timer(self,description:str,time:int):
        DEF = 12
        maxtime = datetime.now()+timedelta(seconds=time)
        tx = int((time-(maxtime-datetime.now()).seconds)/time*DEF)
        while(tx<DEF and tx>=0):
            timebar = "".join(["▬" for i in range(tx)]+["🕐"]+["▬" for i in range(DEF-tx)])
            await self.msg.edit(embed=self.embed(f"{timebar}\n\n{description}"),view = None)
            await asyncio.sleep(2)
            tx = int((time-(maxtime-datetime.now()).seconds)/time*12)
        timebar = "".join(["▬" for i in range(DEF)]+["🕐"])
        await self.msg.edit(embed=self.embed(f"{timebar}\n\n{description}"),view = None)