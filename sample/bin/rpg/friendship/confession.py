from sample.bin.message import embed,IC,V
from sample.bin.rpg.friendship.config import RELATION_LIMIT
from sample.bin.rpg.rpgsql import check_relation, set_Mate
from core import BACK, BLUE_CHECK, YELLOW_HEART, HAPPY_FACE, Color
from discord import Interaction, User,ButtonStyle,TextStyle,Message
from discord.ext.commands import CommandError
from discord.ui import button,Button,Modal,TextInput
from datetime import datetime,timedelta

class something_went_error(CommandError):
    """系統錯誤"""

class check_if_want_confess(V):  #確認告白
    def __init__(self,user:User,to:User):
        super().__init__(timeout=300)
        self.user=user
        self.to = to


    @button(label="確定",custom_id="check_want_confess",style = ButtonStyle.green ,emoji="📜")
    async def confess_callback(self,interaction:Interaction,button:Button):
        if interaction.user==self.user:
            await interaction.response.send_modal(edit_member_introduce_modal(interaction.user,self.to)) #np
            await interaction.message.delete()
        else:
            return await interaction.response.send_message(ephemeral=True,embed = embed(f"{BACK} | 怎麼想替他告白了？心懷不軌喔 {HAPPY_FACE}！","",Color.RED))


    @button(label="取消",custom_id="cansole",style = ButtonStyle.danger ,emoji=f"{BACK}")
    async def cansole_callback(self,interaction:Interaction,button:Button):
        if interaction.user==self.user:
            return await interaction.response.edit_message(embed=embed.cancel(),view = None) #np
        else:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=embed(
                    f"{BACK} | 沒事別亂錯這顆按鈕拉！","我知道他在劈腿，但讓他當個圓規不行嗎？",Color.RED
                ))



class edit_member_introduce_modal(Modal):   #告白誓言
    def __init__(self,fro:User,to:User) -> None:
        super().__init__(title="🎀告白誓言")
        self.fro = fro
        self.to = to
    birthday = TextInput(
        label="我想對你說",
        style=TextStyle.paragraph,
        placeholder="我...一直在等著你...",
        min_length = 10,
        max_length = 99,
        required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.send_message(ephemeral=True,embed = embed(f"{BLUE_CHECK} | 傳送成功",f"紀錄：\n{self.birthday.value}",Color.PURPLE))
        message = await interaction.channel.send(
            embed = embed(f"{self.fro.name} 想跟 {self.to.name} 說個秘密",f"{self.to.mention},請檢視私人訊息,他似乎.....眼神飄浮不定",Color.YELLOW)
        )
        return await self.to.send(
            embed=embed(
                f"{YELLOW_HEART} | 請你跟我交往",f"{self.fro.name} 說：\n {self.birthday.value}",Color.WHITE
                ),
            view = confess_request(
                self.fro,self.to,message,self.birthday.value
            ))


class confess_request(V):  #接受表白
    def __init__(self,user:User,to:User,msg:Message,info:str):
        super().__init__(timeout=300)
        self.message = msg
        self.info = info
        self.user=user
        self.to = to


    @button(label="我答應你",custom_id="check_want_confess",style = ButtonStyle.green ,emoji="❤")
    async def confess_callback(self,interaction:Interaction,button:Button):
        set_Mate(self.user.id,self.to.id,self.info)
        await interaction.response.edit_message(embed = embed(f"{YELLOW_HEART} | 你接受了告白","",Color.YELLOW),view=None)
        await self.message.edit(embed = embed(f"{YELLOW_HEART} | 賀",f"{self.to.mention} 答應了了 {self.user.mention} 的告白！！",Color.YELLOW))


    @button(label="垃圾郵件",custom_id="cansole",style = ButtonStyle.danger ,emoji=f"💬")
    async def cansole_callback(self,interaction:Interaction,button:Button):
        await interaction.response.edit_message(embed = embed.cancel(),view = None)
        await self.message.edit(embed = embed(f"{BACK} | 挖",f"{self.to.mention} 閉門羹了 {self.user.mention}",Color.RED))





async def confession_system(ctx:IC,member:User):
    # [id1,id2,exp,level,認識日期,, None, None, None]
    check = check_relation(ctx.user.id,member.id)
    if  check == -1:
        return await ctx.send(embed = embed(
            "",f"{BACK} | 跟陌生人告白？不太好吧...",Color.RED
        ))
    elif check[3]>=1:
        return await ctx.send(embed = embed(
            "",f"**{BACK} | 你忘了你已經向 {member.name} 告白過了嗎？完了完了...**",Color.RED
        ))
    elif check[3]==0:
        if check[2]< RELATION_LIMIT[0]:
            return await ctx.send(
                embed = embed(
                    "",f"**哇！你跟 {member.mention} 的親密度不夠耶...**",Color.RED
                )
            )
        return await ctx.send(embed = embed(
            f"{YELLOW_HEART} | 告白",
            f"**你想好要與 {member.mention} 告白了嗎？**\n\n`按鈕將於`<{datetime.now()+timedelta(minutes=5)}>`失效`",
            Color.YELLOW
            ),view = check_if_want_confess(ctx.user,member)
        )
    else:raise something_went_error("系統似乎發生了問題")



