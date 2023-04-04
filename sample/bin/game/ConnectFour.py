from discord import User,ButtonStyle,Interaction
from discord.ui import Button,button
from sample.bin.message import embed,V
from .game_model import GameModel,GameError
from core import BACK, FIVE, FOUR, ONE, SEVEN, SIX, THREE, TWO, RAD_PIECE, Color

class piece:
    def __init__(self,color:str="w") -> None:
        self.color = color

    @property
    def color(self):
        return self._e
    
    @property
    def value(self):
        return self._value

    @color.setter
    def color(self,value):
        if value == "w":self._e = "<:white_piece:1025810272604139520>"
        elif value == "r":self._e = "<:rad_piece:1025808022649458699>"
        elif value == "y":self._e = "<:yellow_piece:1025808026508218488>"
        else:raise ValueError('角色設定錯誤')
        self._value = value

class p:
    def __init__(self,user:User,color:str) -> None:
        self.user = user
        self.color = color
        self.value = color
    
    @property
    def color(self):
        return self._c
    
    @color.setter
    def color(self,value):
        if value == "r":self._c = Color.RED
        elif value == "y":self._c = Color.YELLOW

class ConnectFour(GameModel,name = f"{RAD_PIECE} | 四連棋",player =(2,2)):
    async def gamestart(self, i: Interaction):
        self.sys = main_game(self,(7,6))
        return await self.update(i,view=self.sys)

class main_game(V):
    def __init__(self,sys:ConnectFour,value:tuple):
        super().__init__(timeout=0)
        self.weight = value[0]
        self.hight = value[1]
        user = sys.player.data
        self.sys = sys
        if value[0]>10 or value[0]<6:raise ValueError('行數只能藉於 6~10 行')
        if value[1]>10 or value[1]<4:raise ValueError('列數只能藉於 4~10 行')
        else:self.board = [[piece(color='w') for j in range(value[0])] for i in range(value[1])]
        self.user = [p(user = user[0],color='r'),p(user = user[1],color='y')]

        for i in range(value[0]):self.add_item(line_button(i,self))
        self.change_des()

    def change_des(self):
        txt = '\n'.join(['┃{}┃'.format(' '.join([u.color for u in c])) for c in self.board])
        self.sys.description = (
            f'> 現在輪到了 {self.user[0].user.mention} 擲棋\n\n'
            f'┃{ONE} {TWO} {THREE} {FOUR} {FIVE} {SIX} {SEVEN}┃\n'
            f'{txt}\n'
        )
    
    @button(label=None,emoji='⏬',row=3,style=ButtonStyle.gray)
    async def resend_callback(self,interaction:Interaction,button:Button):
        await interaction.channel.send(embed = self.embed,view = self)
        await interaction.message.delete()
    
        
    
    async def button_recall(self,i:Interaction,id:int):
        if i.user not in [k.user for k in self.user]:
            raise GameError.UserNotInGame()
        if i.user.id != self.user[0].user.id:
            raise GameError.NotNowTurn()

        # 更改資料與版面
        c = [(i[1][id],(i[0],id)) for i in enumerate(self.board) if i[1][id].value=='w']
        if len(c)==1:
            [i for i in self.children if isinstance(i,Button) and i.custom_id==f'{id}'][0].disabled=True
            if len([i for i in self.children if isinstance(i,line_button) and i.disabled==False])==0:return await self.end(i)
        c = c[-1]
        c[0].color = self.user[0].value
        # 辨識輸贏
        if self.if_win(c):return await self.win(i)
        # 更改接續玩家
        self.user.append(self.user.pop(0))
        # 回覆訊息
        self.change_des()
        await self.sys.update(i,view=self)

    def if_win(self,c):
        color = c[0].value
        d = [((0,1),(0,-1)),((1,0),(-1,0)),((1,1),(-1,-1)),((1,-1),(-1,1))]
        for i in d:
            if self.c(now=c[1],d=i[0],color=color)+self.c(now=c[1],d=i[1],color=color)+1>=4:return True
        return False

    #結束遊戲
    async def win(self,interaction:Interaction):
        txt = '\n'.join(['┃{}┃'.format(' '.join([u.color for u in c])) for c in self.board])
        await interaction.response.edit_message(embed = embed(
            '<:rad_piece:1025808022649458699> 雙人四連棋',
            f'> 恭喜 {self.user[0].user.mention} 獲勝\n\n'
            f'┃{ONE} {TWO} {THREE} {FOUR} {FIVE} {SIX} {SEVEN}┃\n'
            f'{txt}\n',
        self.user[0].color),view = None)
        self.stop()
    async def end(self,interaction:Interaction):
        txt = '\n'.join(['┃{}┃'.format(' '.join([u.color for u in c])) for c in self.board])
        await interaction.response.edit_message(embed = embed(
            '<:rad_piece:1025808022649458699> 雙人四連棋',
            f'> 兩人平手\n\n'
            f'┃{ONE} {TWO} {THREE} {FOUR} {FIVE} {SIX} {SEVEN}┃\n'
            f'{txt}\n',
        self.user[0].color),view = None)
        self.stop()
    def c(self,now,d,color:str,len=0):
        n = (now[0]+d[0],now[1]+d[1])
        if n[0]>=self.hight or n[0]<0 or n[1]>=self.weight or n[1]<0 or (self.board[n[0]][n[1]].value!=color):return len
        else:return self.c(n,d,color,len+1)


class line_button(Button):
    def __init__(self,id,sys:main_game):
        super().__init__(style=ButtonStyle.blurple, label=f'{id+1}', disabled=False, custom_id=f'{id}', row=round(id%2))
        self.sys = sys
    async def callback(self, i: Interaction):
        return await self.sys.button_recall(i=i,id = int(self.custom_id))