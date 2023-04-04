from sample.bin.select.part import part
from discord.ui import Select,View
from discord import Client,Guild,User,Message



class part_view_for_JL(View):
    def __init__(self,bot:Client,guild:Guild,user:User):
        super().__init__(timeout=180)
        self.add_item(part(bot,guild,user))
    def set_msg(self,msg:Message):   
        self.msg = msg
    async def on_timeout(self) -> None:
        select= next(i for i in self.children if isinstance(i,Select))
        select.placeholder = f"❌ | 操作逾時！請至 🥐註冊組 領取"
        select.disabled = True
        await self.msg.edit(view = self)