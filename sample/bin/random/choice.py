from random import choice
from discord import ButtonStyle,Interaction,TextStyle
from discord.ext.commands import Context
from discord.ui import View,Button,button,Modal,TextInput

from sample.bin.message.embed import embed
from core import Color, BACK, BLUE_STAR,Union



choose_respond  = [
    "當然是 {} 摟 ！",
    "就決定是你了，{}！",
    "日月同生，千靈重元，天地無量乾坤圈，急急如律令，我決定選 {}！",
    "經過一番深思，{} 才是最好的！",
    "阿你是要想多久，{} 不就好了"
]




class choose_option(Modal,title = "⚙ 隨機抽籤"):
    title_res = TextInput(label="🍡標題",style=TextStyle.short,placeholder="(可不填)",max_length=50,required=False)
    option = TextInput(label="🍡請填寫選項",style=TextStyle.paragraph,placeholder="(以換行區隔)\n選項一\n選項二\n選項三",max_length=1000,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        z = [u for u in self.option.value.split("\n") if u!=""]
        if len(z)==1:return await interaction.response.send_message(ephemeral=True,embed=embed(f"{BACK} | 選項不能只有一項","",Color.RED))
        try:await interaction.message.delete()
        except:pass
        m = "、".join([f"__{k}__" for k in z])
        if self.title_res.value == "":title = "挑選"
        else:title = self.title_res.value
        o = choice(choose_respond).format(str(choice(z)))
        return await interaction.response.send_message(embed=embed(f"{title}",f"{BLUE_STAR} **{o}** \n\n 從 {m} 中挑選",Color.BLUE))



class check_to_write(View):
    @button(label="確認", emoji=f"🎈", custom_id="check", style=ButtonStyle.green)
    async def check_option_callback(self, interaction: Interaction, button: Button):
        return await interaction.response.send_modal(choose_option())
    @button(label="取消", emoji=f"{BACK}", custom_id="ok", style=ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: Button):
        return await interaction.response.edit_message(embed=embed("",f"{interaction.user.mention} 取消了操作"),view=None)




async def choose_the_option(ctx:Union[Context,Interaction],arg:tuple = ()):
    view = None
    
    if isinstance(ctx,Context):user = ctx.author
    else:user = ctx.user

    if len(arg)==0:
        embeds = embed(
        "❔ |缺乏選項",f"{user.mention}，是否新增選項？",Color.ORANGE)
        view = check_to_write()
    elif len(arg)==1:
        embeds=embed(
        f"{BACK} | 資料錯誤",f"{user.mention},選項不能只有一個",Color.RED)
    else:
        m = "、".join([f"__{k}__" for k in arg])
        o = choice(choose_respond).format(str(choice(arg)))
        embeds = embed(f"挑選",f"{BLUE_STAR} **{o}** \n\n 從 {m} 中挑選",Color.BLUE)

    if isinstance(ctx,Interaction):
        return await ctx.response.send_message(embed=embeds,view = view)
    else:return await ctx.send(embed=embeds,view = view)