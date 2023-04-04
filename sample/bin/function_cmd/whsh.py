from sample.bin.message import embed,IC,V,define_inter_error
from sample.bin.sql import add_whsh_id
from sample.bin.system.whsh_curriculum import search_curriculum_from_class
from core import BACK, EIGHT, FIVE, FOUR, GREEN_CHECK, NINE, ONE, SEVEN, SIX, THREE, TWO, Color,ERROR
from discord import ButtonStyle, Embed,Interaction,Message, User
from discord.ui import button,Button



class whsh_check_setid(V):
    def __init__(self,msg:Message,user:User,name:str,classroom:int,ids:int):
        self.message = msg
        self.user = user
        self.name = name
        self.classroom = classroom
        self.ids = ids
        super().__init__(timeout=300)
    
    async def on_timeout(self) -> None:
        return await super().on_timeout()

    @button(emoji = f"{GREEN_CHECK}",label="通過",style=ButtonStyle.green,row=1)
    async def buy_stock_button_callback(self,interaction:Interaction, button:Button):

        a = add_whsh_id(self.user,self.name,self.ids,self.classroom)
        if isinstance(a,Embed):return await interaction.response.send_message(embed = a)

        embeds = embed(f"{GREEN_CHECK} | 通過審核",f"已讓 {self.user.name} 綁定資料 {self.classroom}",Color.GREEN)
        await interaction.response.edit_message(embed = embed,view=None)
        await self.message.edit(embed = embeds)

    @button(emoji = f"{BACK}",label="銷毀",style=ButtonStyle.danger,row=1)
    async def give_mate_button_callback(self,interaction:Interaction, button:Button):
        await interaction.response.edit_message(embed = embed(f"{ERROR} | 銷毀",f"反駁了 {self.user.name} 綁定資料",Color.RED),view =None)
        await self.message.edit(embed = embed(f"{ERROR} | 綁定反駁","",Color.RED))


class whsh_curriculum_button(V):
    def __init__(self,author:User,cls:str):
        self.object = search_curriculum_from_class(cls)
        self.author = author
        self.page = 0
        self.cls = cls
        super().__init__(timeout=300)


    async def start(self,ic:IC):
        
        self.msg = await ic.send()(embed = embed.load(),view = self)
        await self.msg.edit(embed=self.update(),view=self)


    async def on_timeout(self) -> None:
        for i in self.children:i.disabled = True
        await self.msg.edit(embed=self.update(),view=self)

    def update(self):
        day = self.object[self.page]
        embeds = embed(
            f"{self.cls} 的課表 - 周 {self.page+1}",
            f"早自習 07:30~08:00：\n"
            f"`{day[0].name} - {day[0].teacher}`\n\n"
            f"{ONE} 第一節 08:10~09:00：\n"
            f"`{day[1].name} - {day[1].teacher}`\n\n"
            f"{TWO} 第二節 09:10~10:00：\n"
            f"`{day[2].name} - {day[2].teacher}`\n\n"
            f"{THREE} 第三節 10:10~11:00：\n"
            f"`{day[3].name} - {day[3].teacher}`\n\n"
            f"{FOUR} 第四節 11:10~12:00：\n"
            f"`{day[4].name} - {day[4].teacher}`\n\n"
            f"{FIVE} 第五節 13:10~14:00：\n"
            f"`{day[5].name} - {day[5].teacher}`\n\n"
            f"{SIX} 第六節 14:10~15:00：\n"
            f"`{day[6].name} - {day[6].teacher}`\n\n"
            f"{SEVEN}第七節 15:10~16:00：\n"
            f"`{day[7].name} - {day[7].teacher}`\n\n"
            f"{EIGHT} 第八節 16:10~17:00：\n"
            f"`{day[8].name} - {day[8].teacher}`\n\n"
            f"{NINE} 第九節 None：\n"
            f"`{day[9].name} - {day[9].teacher}`\n\n",
            Color.WHITE
        )
        return embeds
        
    @button(emoji="◀",label="上一頁",style=ButtonStyle.blurple,row=1)
    async def last_page(self,interaction:Interaction,button:Button):
        if interaction.user != self.author:raise define_inter_error.NotCommandProposer()
        self.page -=1
        if self.page<=-1:self.page+=len(self.object)
        await interaction.response.edit_message(embed = self.update())

    @button(emoji="▶",label="下一頁",style=ButtonStyle.blurple,row=1)
    async def next_page(self,interaction:Interaction,button:Button):
        if interaction.user != self.author:raise define_inter_error.NotCommandProposer()
        self.page +=1
        if self.page>=len(self.object):self.page = 0
        await interaction.response.edit_message(embed = self.update())