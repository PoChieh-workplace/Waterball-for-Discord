from discord import Interaction,ButtonStyle,Client
from sample.bin.message import V,embed,define_inter_error as d
from sample.bin.rpg import item_
from ..player import get_player_from_uuid
from .. import NAME 
from core import Color,S,s,B,b,SO,STAR,HOLLOW_STAR,ONLINE,BACK
from typing import List

async def backpack_open(i:Interaction,uuid:int):
    await i.response.defer(thinking=True)
    v = backpack_view(uuid,i.client)
    v.update()
    return await i.followup.send(
        embed=v.embed,view = v
    )

class backpack_view(V):
    def __init__(self,uuid:int,c:Client):
        super().__init__(timeout=0)
        self.c = c # 儲存 bot 資訊
        self.reload(uuid)
        self.turn = 0 # 道具切換位置 0~2
    
    #重新載入玩家資訊
    def reload(self,uuid:int): 
        self.p = get_player_from_uuid(self.c,uuid)
        b = self.p.backpack
        self.strs = [
            ("、".join([f"{o.name}×{o.count}" for o in j]) if len(j)!=0 else "空的") 
            for j in [b.item,b.unlimit_items,b.treasure]
        ]

    # 更新訊息
    def update(self):
        self.embed = embed(
            f"{NAME} - {self.p.name}的背包",
            f"歸屬：{self.p.user.mention} | 背包等級：{self.p.backpack.level}\n\n"
            f"> {STAR if self.turn==0 else HOLLOW_STAR} 物品：{self.strs[0]}\n"
            f"> {STAR if self.turn==1 else HOLLOW_STAR} 道具：{self.strs[1]}\n"
            f"> {STAR if self.turn==2 else HOLLOW_STAR} 寶箱：{self.strs[2]}",
            Color.BROWN
        )

        match self.turn:
            case 0:
                ops:List[item_] = []
                for h in self.p.backpack.item:
                    c = [t for t in ops if t.id_==h.id_]
                    if len(c)!=0:
                        c[0].count+=h.count
                    else:
                        ops.append(h)
            case 1:
                ops = self.p.backpack.unlimit_items
            case 2:
                ops = self.p.backpack.treasure
            case _:
                raise d("切換道具的程式似乎發生了錯誤")
            
        # 確認選項不可為空
        sel = [k for k in self.children if isinstance(k,S) and k.custom_id=="item"][0]
        ops = [k for k in ops if k.useable==True]
        if len(ops)!=0:
            sel.disabled = False
            sel.options = [
                SO(label=u.name,value=u.id_,emoji=u.emoji,description=f"擁有 {u.count} 個") for u in ops
            ]
        else:
            sel.disabled = True

    
    @b(label="切換",style=ButtonStyle.blurple,emoji="🔄",custom_id="switch")
    async def toswitch(self,i:Interaction,b:B):
        if i.user!=self.p.user:
            raise d("你不是角色的主人喔！")
        
        self.turn = self.turn+1 if self.turn <2 else 0
        self.update()
        return await i.response.edit_message(
            embed=self.embed,view = self
        )
    
    @b(label="刷新",style=ButtonStyle.blurple,emoji=ONLINE,custom_id="updates")
    async def updates(self,i:Interaction,b:B):
        if i.user!=self.p.user:
            raise d("你不是角色的主人喔！")
        
        await i.response.defer(ephemeral=True)
        self.reload(self.p.uuid)
        self.update()
        return await i.followup.edit_message(
            message_id=i.message.id,embed=self.embed,view = self
        )
    @b(label="關閉",style=ButtonStyle.danger,emoji=BACK,custom_id="close")
    async def close(self,i:Interaction,b:B):
        if i.user!=self.p.user:
            raise d("你不是角色的主人喔！")
        
        await i.response.defer()
        self.stop()
        await i.message.delete()
        
    @s(custom_id="item",placeholder = "點擊使用",options = [SO(label="錯誤",value="error")])
    async def use_item(self,i:Interaction,s:S):
        return await self.p.use_item(i,s.values[0])