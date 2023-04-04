from discord import Interaction, User,ButtonStyle,SelectOption
from discord.ui import Button, Select, button, select
from core import PEOPLE, EXIT, Color, OFFLINE,GAME_ICON,DISCORD
from typing import List
from sample.bin.message import V, embed,define_inter_error as d
# from sample.bin.rpg.rpgsql import cost_money

class GameError:
    """遊戲機本錯誤"""
    @classmethod
    def GameNotCompletedDone(cls):
        return cls("遊戲尚未開發完成")
    @classmethod
    def UserNotInGame(cls):
        return cls("你並不在遊戲裡")
    @classmethod
    def NotNowTurn(cls):
        return cls("還沒輪到你喔！")
    @classmethod
    def NoPermission(cls,admin = "管理員"):
        return cls(f"你不是 {admin}，沒有權限使用這項功能")



class GameModel:
    def __init__(self):
        self.description = "None"
        self.progress = 0

    def __init_subclass__(cls,name:str = "未命名遊戲",player:tuple = (2,2)) -> None:
        super().__init_subclass__()
        cls.name = name
        cls.pc = player # player count (max,min)
        cls.request:List[load_data] = []
        cls.description = "None"
    
    
    
    async def main(self,i:Interaction,need_player:bool=True):
        if not need_player:
            return await self.gamestart(i)
        self.author = i.user
        self.bot = i.client
        self.channel = i.channel
        self.player = load.player(self.pc,self)
        await self.player.update(i)
    
    async def update(self,i:Interaction = None,view:V=None,color:str = Color.WHITE,img:str=None,thumb:str=None):
        e = embed(
            title=f"{self.name}",
            description = (
                f"> 管理員：{self.author.mention}\n"
                f"> 遊玩人數：{len(self.player.data)}\n"
                f"> 備份：{OFFLINE}\n"
                f"========================\n\n"
                f"{self.description}"
            ),
            color=color,
            image_type=img,thumbnail_type=thumb
        )
        if i!=None:await i.response.edit_message(
            embed=e,view=view)
        else:i
    async def next(self,i):
        if len(self.request)==self.progress:
            return await self.gamestart(i)
        else:
            await self.request[self.progress].update(i)
    
    async def gamestart(self,i:Interaction):
        raise GameError.GameNotCompletedDone()
    
    async def GameEnd(self,i:Interaction,view:V,embed:embed):
        for i in view.children:i.disable = True
        return await i.response.edit_message(view=view)



class load_data(V):
    """遊戲載入資料模板"""
    async def update(self,i:Interaction):
        """更新訊息"""


class load:
    class player(load_data):
        def __init__(self,pc:tuple,g:GameModel):
            super().__init__(timeout=0)
            self.data:List[User] = [g.author]
            self.ban:List[User] = []
            self.pc = pc
            self.g = g

        def indata(self,u:User) -> bool:
            if u in self.data:
                return True
            else:return False
        
        async def update(self,i:Interaction):
            if self.g.pc[1]==self.g.pc[0]:
                p = self.g.pc[0]
            else:p = f"{self.g.pc[1]}~{self.g.pc[0]}"
            self.g.description = (
                f"正在等待玩家加入...\n"
                f"人數限制：{p}人\n"
                f"目前玩家：{'、'.join([i.mention for i in self.data])}"
            )
            c = len(self.data)
            j,l = [u for u in self.children if isinstance(u,Button) and u.custom_id in ["join","leave"]]
            j.label = f"加入：{c}人"
            j.disabled = c>=self.pc[0]
            self.start = c>=self.pc[1]
            return await self.g.update(i=i,view=self)

        @button(label="加入：0人",style=ButtonStyle.blurple,emoji=PEOPLE,disabled=False,custom_id="join")
        async def player_join(self,i:Interaction,b:Button):
            # if self.indata(i.user):raise d("你已經加入了遊戲")
            if i.user in self.ban:raise d("你沒有權限加入遊戲，請詢問本遊戲管理員！")
            elif len(self.data)>=self.pc[0]:raise d('人數已經滿了')
            else:self.data.append(i.user)
            return await self.update(i)
        
        @button(label="離開",style=ButtonStyle.blurple,emoji=EXIT,disabled=False,custom_id="leave")
        async def player_leave(self,i:Interaction,b:Button):
            if not self.indata(i.user):raise d("你不在遊戲裡")
            else:self.data.remove(i.user)
            return await self.update(i)

        @select(
            placeholder="🔧 | 管理員操作",
            options=[
                SelectOption(label="更換管理員",value="change_admin",emoji=PEOPLE,description="轉移權限給另一位玩家"),
                SelectOption(label="取消遊戲",value="cancel",emoji=OFFLINE,description="關閉訊息並取消遊戲"),
                SelectOption(label="完成動作",value="done",emoji=GAME_ICON,description="進行下一步或開始遊戲")
            ]
        )
        async def author_options(self,i:Interaction,s:Select):
            if i.user != self.g.author:raise GameError.NoPermission()
            v = s.values[0]

            if v=="done":
                if self.start == False:raise d("人數不足！無法開始遊戲")
                self.stop()
                return await self.g.gamestart(i)
            elif v=="cancel":
                await i.response.send_message(embed=embed.cancel(self.g.author),delete_after=5)
                return await i.message.delete()
            elif v=="change_admin":
                await self.ChangeAdmin(i)
        
        async def ChangeAdmin(self,i:Interaction):
            if len([u for u in self.data if u!=i.user])==0:
                raise d("遊戲廳裡沒有可以轉移權限的玩家！")
            await i.response.send_message(embed=embed(
                f"{DISCORD} | 轉移遊戲廳權限",
                "轉移權限給遊戲廳中的其他玩家，請在下方選擇欲轉移的對象\n\n> 無法轉移不在遊戲裡的玩家"
            ),view=V(timeout=0).add_item(ManageOption(self,i.user)),ephemeral=True)


class ManageOption(Select):
    def __init__(self,p:load.player,user:User):
        super().__init__(
            placeholder = "🔧 | 管理員操作",
            options = [SelectOption(label = u.name,value=f"{u.id}",description=f"UUID - {u.id}") for u in p.data if u!=user]
        )
        self.p = p
    async def callback(self, i: Interaction):
        u = i.client.get_user(int(self.values[0]))
        self.p.g.author = u
        await i.response.defer()
        return await i.message.delete()