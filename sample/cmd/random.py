from discord.ext.commands import command,Context
from sample.bin.random import *
from core import PRE
from sample.CmdCog import Command_Cog

###### 隨機指令


class Random(Command_Cog,name = '隨機指令'):
    @command(
        name="dice",
        aliases=['d','number'],
        brief = "骰出數字",
        usage = f'{PRE}dice [最大值=100] [最小值=1] [小數位=0]',
        description = (
            "範例：\n"
            f"`{PRE}dice 60` 骰出介於1~60\n\n"
            f"`{PRE}dice 80 10` 骰出介於10~80\n\n"
            f"`{PRE}dice 10 1 1` 骰出介於1.0~10.0\n\n"
        )
    )
    async def dice_a_number(self,ctx:Context,max:int=100,min:int=1,flo:int=0):
        return await to_dice_a_number(ctx,max,min,flo)
    

    @command(
        name="pick",
        aliases=['think'],
        brief = "由機器人決定可不可以！",
        usage = f'{PRE}pick <事件名稱>',
        description = (
            "範例：\n"
            f"`{PRE}pick 周爵崙失去了一切`"
        )
    )
    async def pick_a_thing(self,ctx:Context,*,title:str):
        return await random_is_ok(self.bot,ctx,title)


    @command(
        name="choose",
        aliases=['choice','take'],
        brief = "從給予的選項中抽出一個幸運兒吧～！",
        usage = f'{PRE}choice [選項一] [選項二] [選項三]...',
        description = (
            f"範例：\n"
            f"`{PRE}choice` 不填選項：將會給你表單填寫選項\n"
            f"`{PRE}choice 讀書 睡覺`"
        )
    )
    async def choose_selection(self,ctx:Context,*arge):
        return await choose_the_option(ctx,arge)



async def setup(bot):
    await bot.add_cog(Random(bot))
