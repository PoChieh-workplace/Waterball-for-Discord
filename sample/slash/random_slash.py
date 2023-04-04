from sample.bin.random import *
from sample.SlashCog import Slash_Cog
from discord.app_commands import command,rename
from discord import Interaction,Attachment,File

class Random_Slash(Slash_Cog,name = '指令包_隨機指令'):
    @command(
        name="dice-擲骰",
        description = "骰出自訂義範圍的數字"
    )
    @rename(maxs = "最大值",mins = "最小值",floats = "小數位")
    async def dice_a_number(self,i:Interaction,maxs:int=100,mins:int=1,floats:int=0):
        return await to_dice_a_number(i,maxs,mins,floats)
    

    @command(
        name="pick-決定",
        description = "由機器人決定可不可以這樣做！"
    )
    @rename(context = "內容")
    async def pick_a_thing(self,i:Interaction,context:str):
        return await random_is_ok(self.bot,i,context)


    @command(
        name="choose-選擇",
        description = "從給予的選項中抽出一個幸運兒吧～！"
    )
    async def choose_selection(self,i:Interaction):
        return await choose_the_option(i,())



async def setup(bot):
    await bot.add_cog(Random_Slash(bot))