from core import Union
from discord import Interaction,User,Member,Message
from discord.ext.commands import Context

# 合成 Context 與 interaction 功能

class IC:
    def __init__(self,ic:Union[Interaction,Context]) ->None:
        self.ic = ic
        if isinstance(ic,Interaction):
            self.isinter = True
        else:
            self.isinter = False

    def user(self) -> Union[User,Member]:
        if self.isinter:
            return self.ic.user
        else:return self.ic.author

    # function 可視為 object
    def send(self):
        if self.isinter:
            return self.ic.response.send_message
        else:return self.ic.send