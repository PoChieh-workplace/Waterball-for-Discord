from discord import Interaction,ButtonStyle,User,Message
from discord.ui import button,Button,TextInput as T
from sample.bin.message import IC,embed,V,modal,define_inter_error as d
from ..player import get_player_from_user,insert_player_sql
from .. import NAME
from core import Color,PENCIL,PEOPLE,ONLINE

MAX_REGISTER = 2


class register_buttons(V):
    def __init__(self):
        super().__init__(timeout=0)
        self.choose = 0


    async def reload(self,i:Interaction,first:bool = False):
        self.user = i.user
        self.data = get_player_from_user(i.user)
        l = len(self.data)

        # 按鈕重製
        ban = []
        if l >= MAX_REGISTER:
            ban.append('create')
        if  l < 2:
            ban.append('choose')
            if l==0:
                ban.append('login')
        
        for iu in [o for o in self.children if isinstance(o,Button) and o.custom_id in ban]:
            iu.disabled = True
        
        # 訊息
        name = [u.name for u in self.data]
        p = "\n> ".join(
            [f"{'◆' if i==self.choose else '◇'} `{j}`" for i,j in enumerate(name)]
        )+"\n\n使用 `/rpg backpack` 查看背包" if l != 0 else "你似乎沒有註冊過呢！點擊下方按鈕創建角色吧"

        e = embed(
            f"{NAME} - 註冊組",
            f"歡迎光臨！！{i.user.mention}\n"
            f"請選擇要登入的角色\n"
            f"註冊人數：{l}/{MAX_REGISTER}\n\n"
            f"> {p}",
            Color.PURPLE_LIGHT
        )

        if first:
            return await i.response.send_message(
            embed=e,
            view=self
        )
        return await i.response.edit_message(
            embed=e,
            view=self
        )


    @button(
        label="創建",
        emoji=PENCIL,
        style=ButtonStyle.blurple,
        custom_id="create"
    )
    async def create(self,i:Interaction,b:Button):
        if i.user!=self.user:raise d("你不是指令發起人")

        return await i.response.send_modal(
            create_player_name())
    
    @button(
        label="切換",
        emoji=PENCIL,
        style=ButtonStyle.blurple,
        custom_id="choose"
    )
    async def chooses(self,i:Interaction,b:Button):
        if i.user!=self.user:raise d("你不是指令發起人")
        
        self.choose = 1 if self.choose==0 else 0
        return await self.reload(i)

class create_player_name(modal,title = "創建角色"):
    
    name = T(
        label="玩家名稱",
        required=True,
        placeholder="水球好帥",
        max_length=10,
        min_length=3
    )

    def __init__(self) -> None:
        super().__init__(timeout=0, custom_id = "create_player")

    async def on_submit(self, i: Interaction) -> None:
        if insert_player_sql(i.user,self.name.value):
            return await i.response.send_message(
                embed=embed(
                    f"{NAME} - 註冊組",
                    f"{ONLINE} 成功創建角色！！更新訊息後即可登入！",
                    Color.GREEN
                ),
                ephemeral=True
            )
        else:
            raise d("註冊人數已滿！！")