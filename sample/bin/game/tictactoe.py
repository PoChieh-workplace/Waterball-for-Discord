import asyncio
import discord
from discord.ui import Button,button
from discord import Interaction
from sample.bin.message import embed,V,define_inter_error
from .game_model import GameError,GameModel
from core import WHITE_STAR,Color


CIRCLE_EMOJI_GAME = "🟢"
FORK_EMOJI_GAME = "❌"
NOW_PLAYERS_TURN = "{} | 現在輪到了 {}"
WIN_GAME = "{} | 恭喜 {} {} 獲勝"

class turn:
    def __init__(self,turn:int,player:discord.User,emoji:str,button_color:discord.ButtonStyle,color) -> None:
        self.turn = turn
        self.player=player
        self.emoji=emoji
        self.button_color=button_color
        self.color=color


win_list = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    [1,4,7],
    [2,5,8],
    [3,6,9],
    [1,5,9],
    [3,5,7]
]




class TicTacToe(GameModel,name = "⭕❌ | 圈圈叉叉",player = (2,2)):
    def __init__(self) -> None:
        self.game_end = False
        self.turn = 0
        self.view = board(self)

    def n(self):
        if self.turn ==0:return self.player1
        elif self.turn ==1:return self.player2
        else: return None

    async def gamestart(self, i: Interaction):
        
        self.player1 = turn(0,self.player.data[0],CIRCLE_EMOJI_GAME,discord.ButtonStyle.green,Color.GREEN)
        self.player2 = turn(1,self.player.data[1],FORK_EMOJI_GAME,discord.ButtonStyle.danger,Color.RED)
        
        self.description = NOW_PLAYERS_TURN.format(self.n().emoji,self.n().player.mention)
        await self.update(i,board(self),self.n().color)





class board(V):
    def __init__(self,game:TicTacToe):
        self.g = game
        super().__init__(timeout=0)
        for i in range(3):
            for j in range(3):
                self.add_item(game_button_modal(ids = i*3+j,b=self))


    async def update(self,i:Interaction):
        n = self.g.n()
        list1=[]
        for j in [k for k in self.children if isinstance(k,game_button_modal)]:
            if j.user == self.g.turn:
                list1.append(int(j.custom_id))
        for j in win_list:
            if (j[0] in list1) and (j[1] in list1) and (j[2] in list1):
                self.g.description = WIN_GAME.format(WHITE_STAR,n.emoji,n.player.mention)
                for j in self.children:j.disabled = True
                return await self.g.update(i,view = self,color=n.player.color)
            elif len(list1) >=5:
                self.g.description = "平手，遊戲結束"
                for j in self.children:j.disabled = True
                return await self.g.update(i,view = self,color=n.player.color)

        self.g.turn=(self.g.turn+1)%2
        n = self.g.n()
        self.g.description = NOW_PLAYERS_TURN.format(n.emoji,n.player.mention)
        return await self.g.update(i,view=self,color=n.color)



class game_button_modal(Button):
    def __init__(self,ids:int,b:board):
        super().__init__(emoji = "⬜", custom_id = f"{ids+1}",row=ids//3)
        self.b = b
        self.user = None
    async def callback(self, i: Interaction):
        if i.user!=self.b.g.n().player:
            raise define_inter_error("還敢亂啊？")
        # self.style=self.b.g.n().button_color
        self.emoji=self.b.g.n().emoji
        self.user = self.b.g.turn
        self.disabled=True
        return await self.b.update(i=i)