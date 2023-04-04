import asyncio,discord
from datetime import date, timedelta
from sample.bin.FacebookRequest import *
from sample.bin.sql import datechannelSQL
from sample.bin.time import getTempNowTime
from sample.CmdCog import Command_Cog

class DateListener(Command_Cog):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        async def time_task():
            now_time = getTempNowTime("%d")-1
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                if now_time != getTempNowTime("%d"):
                    #倒數日
                    try:
                        print("【INFO】DateListener Running!")
                        data = datechannelSQL.get_all() #(id,date,context)
                        for id,d,c in data:
                            channel = self.bot.get_channel(id)
                            if channel==None:
                                datechannelSQL().remove(id)
                                continue
                            t:timedelta = d-date.today()
                            await channel.edit(name = c.format(t.days))
                    except:
                        await asyncio.sleep(1000)
                        continue
                    now_time = getTempNowTime("%d")
                await asyncio.sleep(1000)
        self.bg_task = self.bot.loop.create_task(time_task())
async def setup(bot):
    await bot.add_cog(DateListener(bot))