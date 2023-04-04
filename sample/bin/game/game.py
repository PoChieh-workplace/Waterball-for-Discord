from discord.ui import Select,View,select
from discord import Interaction,SelectOption
from discord.ext.commands import Context
from sample.bin.message import embed,IC,V,define_inter_error
from sample.bin.game import ConnectFour,SituationPuzzle,HalfPastTen,TicTacToe#,WereWolf
from core import Union,GAME_ICON

class GAME_EDITING(define_inter_error):
    """遊戲維修中"""

options = [
    ["SMALL - 圈圈叉叉 Tic-tac-toe",        "TicTacToe",            "建議人數：2人，遊玩時間：1分鐘",                             "⭕"],
    ["SMALL - 四連棋 Connect-four",         "ConnectFour",          "開發版，建議人數：2人，最低4人，遊玩時間：30~60 分鐘",       "<:yellow_piece:1025808026508218488>"],
    ["MIDDLE - 十點半 Half-past-ten",       "HalfPastTen",          "建議人數：2~8人，遊玩時間：5分鐘",                           "🃏"],
    ["MIDDLE - 海龜湯 Situation-puzzle",    "SituationPuzzle",      "建議人數：2人以上，遊玩時間：20分鐘",                        "🥣"],
    ["LARGE - 狼人殺 Ultimate-Werewolf",    "WereWolf",             "測試版，建議人數：8人以上，最低4人，遊玩時間：30~60 分鐘",   "🐺"]
]






class Game_select(V):
    def __init__(self) -> None:
        super().__init__(timeout=0)

    async def main(self,i:Union[Interaction,Context]):
        await IC(i).send()(embed = embed(
            f"{GAME_ICON} WaterBall 遊戲大廳",
            "遊戲廳仍然持續維修中，僅有部分可以運作，敬請見諒！！ <:Rinahehe:969985025103781948> 如有發生問題或想給予建議，歡迎提供給開發人員，他很耐操的"
        ),view = self)


    @select(
        placeholder="遊戲選單",
        options=[
            SelectOption(label=c[0],value = c[1],description=c[2],emoji=c[3]) for c in options
        ]
    )
    async def callback(self, i: Interaction,select:Select):
        v = select.values[0]
        if v == "TicTacToe":game = TicTacToe()
        elif v == "HalfPastTen":game = HalfPastTen()
        elif v == "SituationPuzzle":game = SituationPuzzle()
        elif v == "ConnectFour":game = ConnectFour()
        else:raise GAME_EDITING(f"ㄟ？你按出一個蟲蟲了(Bug)，...請日後再試或歡迎告知開發者")
        await game.main(i)
        # raise GAME_EDITING(
        #     "遊戲廳正在重新打造中！更新訊息請關注文華伺服公告欄"
        #     f"\n[{WHSH_ICON} 查看布告欄](https://discord.com/channels/910150769624358914/944944940239183872)"
        # )