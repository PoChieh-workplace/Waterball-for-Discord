from .game_model import GameModel
from discord import Interaction
from core import PEOPLE
class PollGame(GameModel,name = f"{PEOPLE} | 人數調查",player = (100000,1),repeat = False):
    async def gamestart(self, i: Interaction):
        self.description = f"人數調查完畢...\n參與人員：{'、'.join([j.mention for j in self.player.data])}"
        return await self.update(i=i,view=None)