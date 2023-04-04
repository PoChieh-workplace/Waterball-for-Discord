import asyncio
from discord import ForumChannel,ButtonStyle
from discord.ui import Button

from sample.bin.FacebookRequest import *
from sample.bin.message import embed,V
from sample.bin.time import RewriteTime, TimeZoneChange, getTempNowTime
from core import Color, Face, BACK
from sample.CmdCog import Command_Cog 
from sample.bin.json import open_json_FBpost

WHSH_FUCK_TO_TIME = '%Y年%m月%d日 %H:%M:%S'
WHSH_FUCK_TIME = '%Y-%m-%dT%H:%M:%S+0000'

KB = "https://cdn.discordapp.com/emojis/969047320467476500.webp"

class WHSHembed:
    title = "{}"
    description = "\n".join([
        "{} \n",
        "發布時間：{}"
    ])
    
class button(Button):
    def __init__(self,c,url):
        super().__init__(style=ButtonStyle.url, label=c, url=url)

class fb_totallink(V):
    def __init__(self,url,create):
        super().__init__(timeout=0)
        self.add_item(button("貼文連結",url))
        self.add_item(button("我想投稿",create))





class FBpost(Command_Cog):
    #a = datetime.datetime.now().strftime('%Y %m %d %H %M')
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        async def time_task():
            await self.bot.wait_until_ready()
            print(f"【SET-UP】KBwhsh start to run")
            class FbError:
                WordTooLong = "字數過多導致無法顯示{}".format(Face("sad"))
                ErrorNotfound = "基於某些問題，無法顯示本篇消息{}"
                IdNotFound = "突然找不到舊有的 id 了 {}，將為您更新重置到最新貼文"
            Id = "whsh"
            while not self.bot.is_closed():
                if getTempNowTime('%M')%5==0:
                    try:
                        data = getFbPost(Id)
                        count = getCount(Id,data)
                        print(f"【INFO】KBwhsh prodicted {count} posts")


                        if count==-1:
                            for k in open_json_FBpost()["sendchannel"]["whsh"]:
                                channel = self.bot.get_channel(k)
                                embeds = embed(f"{BACK} | 挖..神奇錯誤💦",FbError.IdNotFound.format(Face("sad")),Color.BLUE_LIGHT)
                                await channel.send(embed=embeds)
                        elif(count==0):pass
                        else:
                            for i in range(count-1,-1,-1):
                                await asyncio.sleep(1)
                                # try:
                                usedata = data['posts']['data'][i]
                                message = usedata['message']
                                Title = message.split("\n",1)
                                time = RewriteTime(TimeZoneChange(usedata['created_time'],WHSH_FUCK_TIME),WHSH_FUCK_TO_TIME)
                                image = getFbPhoto('whsh',usedata['id'])
                                embeds = embed(
                                    WHSHembed.title.format(Title[0]),
                                    WHSHembed.description.format(Title[1],time),
                                    Color.WHITE
                                )
                                embeds.set_author(name = '靠北文華管理群',icon_url=KB,url="https://www.facebook.com/FOURKBWHSH")
                                embeds.set_footer(text='Proffered by KBwhsh.IV')
                                if image!=None:embeds.set_image(url=image)

                                buttons = fb_totallink(
                                        f"https://www.facebook.com/{usedata['id']}",
                                        "https://www.crush.ninja/zh-tw/pages/FOURKBWHSH/"
                                )
                                fc:ForumChannel = self.bot.get_channel(1019927895772254228)
                                thread = await fc.create_thread(
                                    name=f"#{Title[0]}",
                                    content=f"{Title[1][:10]}",
                                    embed=embeds,
                                    view = buttons)
                                for k in open_json_FBpost()["sendchannel"]["whsh"]:
                                    channel = self.bot.get_channel(k)
                                    await channel.send(embed=embeds,view=buttons)

                            await asyncio.sleep(100) 
                        updateNowId(Id,data)
                    except:await asyncio.sleep(3000)

                await asyncio.sleep(50)
        self.bg_task = self.bot.loop.create_task(time_task())
async def setup(bot):
    await bot.add_cog(FBpost(bot))