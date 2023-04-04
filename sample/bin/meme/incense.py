from sample.bin.image import make_incense_with_user,add_incense
from sample.bin.message import IC,V,define_inter_error
from discord.ui import button,Button
from discord import ButtonStyle,Interaction,User
from typing import List
from core import PEOPLE

class Incense(V):
    def __init__(self, timeout: int = 0):
        super().__init__(timeout)
        self.incense_player:List[User] = []
        self.editing = False
    
    async def main(self,i:IC,user):
        if user==None:user = i.user()
        self.filed = await make_incense_with_user(user=user)
        return await i.send()(file=self.filed,view=self)


    @button(custom_id='count',label='上香 - 人數：0',emoji='🎐',style=ButtonStyle.blurple)
    async def to_incense(self,i:Interaction,b:Button):
        if self.editing:
            raise define_inter_error(f"{PEOPLE} 有人正在上香，請不要推擠！！`請稍後再試`")
        elif i.user in self.incense_player:
            raise define_inter_error("你已經上過香了")
        else:
            await i.response.defer()
            self.editing=True
            file = await add_incense(i.message.attachments[0])
            self.incense_player.append(i.user)
            b.label = f'上香 - 人數：{len(self.incense_player)}'
            await i.message.edit(attachments=[file],view=self)
            self.editing = False