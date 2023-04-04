from discord import ButtonStyle, Interaction, User
from discord.ui import View,button,Button
from discord.ext.commands import Context
from bin.rpg.rpgsql import cost_money, earn_money, get_money_info
from bin.embed import getembed
from config.color import GREEN, RED
from config.emoji import BACK, BLUE_STAR, MONEY_FLY
from config.zh_tw import CONCIAL



async def remit_mon(ctx:Context,user:User,money:int):
    if money <= 0:return await ctx.send(embed = getembed(
        f"{BACK} | 數值錯誤",f"{ctx.author.mention}，WB國似乎沒有這個幣值",RED),ephemeral=True)
    m = get_money_info(ctx.author.id)
    if  m < money:
        return await ctx.send(embed = getembed(
            f"{BACK} | 錢錢不足",
            f"{ctx.author.mention}，你的錢錢似乎不夠\n\n"
            f"> 目前金額 {m}元",RED
        ))
    else:
        return await ctx.send(embed = getembed(
            f"{MONEY_FLY} | WBATM - 匯款\n",
            f"{BLUE_STAR} {ctx.author.mention}，確定要匯款 `{money}`元 給 {user.mention}？\n\n"
            f"> 匯款慎防有心之人，詐騙害人害己，請牢記三步驟\n"
            f"> **愛水球、疼水球、匯給水球**\n",
            GREEN
        ),view = check_if_remit(ctx.author,user,money)) 


class check_if_remit(View):
    def __init__(self,author:User,to_user:User,money:int):
        super().__init__(timeout=100)
        self.a = author
        self.to = to_user
        self.m = money
    @button(label="確認匯款",emoji=MONEY_FLY,custom_id="accept_remit",style=ButtonStyle.blurple,row=1)
    async def accept_callback(self,interaction:Interaction,button:Button):
        if interaction.user != self.a:return await interaction.response.send_message(embed = getembed(f"{BACK} | 請不要打擾他","shhh...，他在思考是否要匯給小三",RED),ephemeral=True)
        try:
            a = cost_money(self.a.id,self.m)
            b = earn_money(self.to.id,self.m)
        except:return await interaction.response.send_message(embed = getembed(f"{BACK} | 匯款時發生錯誤","",RED),ephemeral=True)
        return await interaction.response.edit_message(embed = getembed(
            f"{MONEY_FLY} | 確認匯款",
            f"{self.a.mention} 成功匯款 {self.m} 元給 {self.to.mention}\n\n"
            f"> 金錢剩餘：{a}元 ， 對方所得：{b}元",
            GREEN
        ),view = None)
    @button(label="取消操作",emoji=BACK,custom_id="cancel",style=ButtonStyle.danger,row=1)
    async def delete_callback(self,interaction:Interaction,button:Button):
        if interaction.user != self.a:return await interaction.response.send_message(embed = getembed(f"{BACK} | 請不要打擾他","shhh...，他在思考是否要匯給小三",RED),ephemeral=True)
        return await interaction.response.edit_message(embed = CONCIAL,view = None)