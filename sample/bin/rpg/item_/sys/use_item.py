from sample.bin.message import V,embed,define_inter_error as d
from discord import Interaction
from sample.bin.rpg import player
from .. import item_,player_edition
from core import Color,s,SO,S,ERROR
from typing import List

__all__ = [
    'item_gui'
]

class item_gui(V):
    def __init__(
        self,
        player:player,
        item:item_
    ):
        super().__init__(timeout = 0)
        self.p = player
        self.it = item

        [i for i in self.children if isinstance(i,S) and i.custom_id=="selection"][0].options = [
            SO(label = "使用一次",emoji=self.it.emoji,value='once'),
            SO(label = "使用十次",emoji=self.it.emoji,value='ten'),
            SO(label = "關閉介面",emoji=ERROR,value='close')
        ]
    
    @s(
        placeholder="功能",custom_id="selection",
        options=[
            SO(label="發生錯誤",value='error',description="拿取資料時發生錯誤")
        ]
    )
    async def selection_submit(self,i:Interaction,s:S):
        if i.user!=self.p.user:
            raise d("你不是角色的主人喔！")
        
        await i.response.defer()

        def it_use(c:int) ->List[player_edition]:
            self.it.count-=c
            return [self.it.use() for i in range(c)]
        
        edit = []
        match s.values[0]:
            case 'once':
                if self.it.count<1:
                    raise d("數量似乎不夠呢")
                edit = it_use(1)    
            case 'ten':
                if self.it.count<10:
                    raise d("數量似乎不夠呢")
                edit = it_use(10)
            case 'close':
                return await i.followup.delete_message(i.message.id)
        

        power = sum([u.power for u in edit])
        text = ""

        for u in edit:
            for j in u.item:
                text += f"{j.name} × {j.count}、"
                self.p.backpack.add_item(j)
        
        self.p.backpack.check()
        self.p.power+=power
        self.p.save()

        if self.it.count<=0:
            return await i.message.delete()

        await i.message.edit(
            embed = embed(
                f"使用{self.it.name}",
                f"> 歸屬：{self.p.user.mention}的 `{self.p.name}`\n"
                f"> 剩餘：{self.it.count}個",
                Color.BLUE_INDIGO
            ),view=self
        )

        return await i.followup.send(
            embed = embed(
                f"使用{self.it.name}",
                f"**獲得：**\n"
                f"體力 × {power}\n"
                f"{text}",
                Color.DARK_RED
            ),ephemeral=True
        )

        

    async def open_gui(self,i:Interaction):
        return await i.response.send_message(
            embed = embed(
                f"使用{self.it.name}",
                f"> 歸屬：{self.p.user.mention}的 `{self.p.name}`\n"
                f"> 剩餘：{self.it.count}個",
                Color.BLUE_INDIGO
            ),view=self
        )

