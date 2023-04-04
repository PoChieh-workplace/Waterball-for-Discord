# from bin.View.function_view import whsh_selection
from core import PENCIL,BACK,GREEN_CHECK
from discord import Interaction,Client,User,Guild,SelectOption,Message,Member
from discord.ui import Select,View
from sample.bin.message import embed,define_inter_error



class part_chosen(Select):
    def __init__(self,op:View,bot:Client,guild:Guild,user:User) -> None:
        self.op = op
        self.bot = bot
        self.guild = guild
        self.user = guild.get_member(user.id)
        super().__init__(
            custom_id="part_chosen",
            placeholder="🙋🏻‍♂️請選擇適合的身分",
            min_values = 0,
            options = [
                SelectOption(label=f"{v.name}",value = f"{v.id}",default=f"{v.id in [i.id for i in self.user.roles]}")
                for v in guild.get_member(bot.application_id).roles if v.permissions.administrator==False and v.is_assignable()
            ]
        )
        self.max_values = len(self.options)
    async def callback(self, interaction: Interaction) -> None:
        if interaction.user.id != self.user.id:
            raise define_inter_error("你不是指令觸發者")
        self.op.remove_item(self)
        for i in self.op.children:i.disabled = False
        await interaction.response.edit_message(
            view = self.op,embed = embed("f")
            )
        msg:Message = await interaction.channel.send(content="身分組作業中請稍後")
        for k in [self.guild.get_role(int(u.value)) for u in self.options if int(u.value) in [r.id for r in self.user.roles] and not (u.value in self.values)]:await self.user.remove_roles(k)
        for i in self.values:
            if int(i) not in [k.id for k in self.user.roles]:
                await msg.edit(content=f"{PENCIL} | 正在處理身分組 {self.guild.get_role(int(i)).name}")
                await self.user.add_roles(self.guild.get_role(int(i)))
        await msg.edit(content=f"{GREEN_CHECK} | 身分組更新完畢",delete_after=5)


class part(Select):
    def __init__(self,bot:Client,guild:Guild,user:Member) -> None:
        self.bot = bot
        self.guild = guild
        self.user = guild.get_member(user.id)
        super().__init__(
            custom_id="part_chosen",
            placeholder="🙋🏻‍♂️請選擇適合的身分",
            min_values = 0,
            options = [
                SelectOption(label=f"{v.name}",value = f"{v.id}",default=f"{v.id in [i.id for i in self.user.roles]}")
                for v in guild.get_member(bot.application_id).roles if v.permissions.administrator==False and v.is_assignable()
            ] 
        )
        self.max_values = len(self.options)
    async def callback(self, interaction: Interaction) -> None:
        if interaction.user.id != self.user.id:
            raise define_inter_error("你不是指令觸發者")
        await interaction.response.edit_message(content="")
        msg:Message = await interaction.channel.send(content="身分組作業中請稍後")
        for k in [self.guild.get_role(int(u.value)) for u in self.options if int(u.value) in [r.id for r in self.user.roles] and not (u.value in self.values)]:await self.user.remove_roles(k)
        for i in self.values:
            if int(i) not in [k.id for k in self.user.roles]:
                await msg.edit(content=f"{PENCIL} | 正在處理身分組 {self.guild.get_role(int(i)).name}")
                await self.user.add_roles(self.guild.get_role(int(i)))
        await msg.edit(content=f"{GREEN_CHECK} | 身分組更新完畢",delete_after=5)
