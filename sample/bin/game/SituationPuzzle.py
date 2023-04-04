
import asyncio
from datetime import datetime
import io
from typing import List
from discord import Client, Embed, File, Message,ButtonStyle,Interaction, SelectOption, TextStyle,User
from discord.ui import View,Button,button,Modal,TextInput,select,Select
from sample.bin.message import embed,define_inter_error
from .game_model import GameModel,GameError
from core import BACK, BLUE_STAR, PINK_STAR, PURPLE_CHECK, WHITE_STAR, Color


class SituationPuzzle(GameModel,name = "🥣 | 海龜湯系統 SituationPuzzle",player = None):
    class option:
        def __init__(self,author:User,ask:str,answer = None) -> None:
            self.author = author
            self.ask = ask
            self.answer = answer
            self.time = datetime.now().strftime("%H:%M")
            self.logtime = datetime.now().strftime("%H:%M:%S")
    def __init__(self,message:Message,client:Client,author:User) -> None:
        self.page = 1
        self.msg = message
        self.bot = client
        self.author = author
        self.description:str = "\u200b"
        self.asks:List[self.option] = []
        self.answers:List[self.option] = []
    async def main(self):
        await self.msg.edit(embed = self.to_embed(),view = game_setting(self))

    def to_embed(self) -> Embed:
        t = datetime.now().strftime("%H:%M:%S")
        if self.asks!=[]:asks = f"{BLUE_STAR} 即將回答：\n 【 **{self.asks[0].ask}** 】\n由 {self.asks[0].author.mention} 提問 `{self.asks[0].time}`\n\n"
        else:asks = ""
        asks += "\n\n".join([f"{PINK_STAR} 【 **{u.ask}** 】\n由 {u.author.mention} 提問 `{u.time}`" for u in self.asks[1:] if isinstance(u,self.option)])
        answers = "\n\n".join([f"{WHITE_STAR}【 **{u.ask}** 】| {u.answer} `{u.time}`" for u in self.answers[(self.page-1)*8:(self.page*8)] if isinstance(u,self.option)])
        if asks=="":asks = "空"
        if answers=="":answers = "空"
        embede = embed("🥣 | 海龜湯系統 SituationPuzzle",f"由 {self.author.mention} 發起,\n\n時間：{t}，頁數：{self.page}/{int((len(self.answers)-1)/8)+1}",Color.LIGHT_BLUE)
        embede.add_field(name="🍡湯麵", value=f"{self.description}", inline=False)
        embede.add_field(name="目前提問", value=asks, inline=False)
        embede.add_field(name="取得線索", value=answers, inline=False)
        return embede


class game_setting(View):
    def __init__(self,main:SituationPuzzle):
        super().__init__(timeout=0)
        self.main = main
    
    @button(emoji="🔧",label="設定湯麵",row=1,custom_id="set_description",style=ButtonStyle.blurple)
    async def set_des_callback(self,i:Interaction,b:Button):
        if i.user != self.main.author:raise GameError.NoPermission()
        return await i.response.send_modal(game_modal(self.main,self))
    
    @button(emoji=f"{PURPLE_CHECK}",label="確認",row=1,custom_id="done",style=ButtonStyle.green,disabled=True)
    async def callback_done(self,i:Interaction,b:Button):
        if i.user != self.main.author:raise GameError.NoPermission()
        return await i.response.edit_message(embed=self.main.to_embed(),view = main_respond_and_answer(self.main))

#設定遊戲說明

class game_modal(Modal):
    def __init__(self,main:SituationPuzzle,setting:game_setting) -> None:
        super().__init__(title="🍡設定湯麵",timeout=0)
        self.setting = setting
        self.main = main
    description = TextInput(label="填入說明",style=TextStyle.paragraph,placeholder="一天...水球疲憊的躺在文華裡",max_length=300,min_length=10,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        self.main.description = self.description.value
        [u for u in self.setting.children if isinstance(u,Button) and u.custom_id=="done"][0].disabled = False
        await interaction.response.edit_message(embed = self.main.to_embed(),view = self.setting)

#主回覆

class main_respond_and_answer(View):


    def __init__(self,main:SituationPuzzle):
        super().__init__(timeout=0)
        self.main = main

    async def send_log(self,interaction:Interaction,filename:str = 'WaterBall-SituationPuzzle'):
        time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        ask = "\n".join([f"[{u.logtime}] - {u.author.name} 提問 【 {u.ask} 】" for u in self.main.asks if isinstance(u,self.main.option)])
        answer = "\n".join([f"[{u.logtime}] - {u.author.name} 提問 【 {u.ask} 】，回答為 {u.answer}" for u in self.main.answers if isinstance(u,self.main.option)])
        txt = "\n\n".join([
            f"🥣 | 海龜湯系統日誌 SituationPuzzle Log - Code by 老乾捷水球",
            f"┌ 遊戲發起者：{self.main.author.name}\n├ 群組：{self.main.msg.guild.name} - {self.main.msg.channel.name}\n└ 資料請求時間：{time}",
            f"🍡題目說明：\n{self.main.description}",
            f"待回答問題：\n{ask}",
            f"已知線索：\n{answer}"
        ])
        buf = io.BytesIO(bytes(txt, 'utf-8'))
        f = File(buf, filename=f'{filename}.txt')
        await interaction.response.send_message(
            content=f"{interaction.user.name}，已傳送遊戲日誌",
            file = f
        )


    async def respond_ask(self,interaction:Interaction,emoji):
        if interaction.user != self.main.author:
            raise GameError.NoPermission()
        elif len(self.main.asks)==0:
            raise define_inter_error("似乎還沒有人提出問題")
        else:
            self.main.asks[0].answer = emoji
            self.main.answers.insert(0,self.main.asks[0])
            del self.main.asks[0]
            return await interaction.response.edit_message(embed = self.main.to_embed())


    @button(emoji="👍🏻",label="是",row=1,custom_id="yes",style=ButtonStyle.green)
    async def yes_callback(self, interaction: Interaction,button:Button):
        return await self.respond_ask(interaction,button.emoji)

    @button(emoji="❔",label="無關",row=1,custom_id="nothing",style=ButtonStyle.gray)
    async def nothing_callback(self, interaction: Interaction,button:Button):
        return await self.respond_ask(interaction,button.emoji)

    @button(emoji="👎🏻",label="否",row=1,custom_id="no",style=ButtonStyle.red)
    async def no_callback(self, interaction: Interaction,button:Button):
        return await self.respond_ask(interaction,button.emoji)


    @button(emoji="◀",label="前",row=2,custom_id="last",style=ButtonStyle.blurple)
    async def last_callback(self, interaction: Interaction,button:Button):
        if self.main.page - 1 <= 0:self.main.page = int((len(self.main.answers)-1)/8)+1
        else:self.main.page-=1
        return await interaction.response.edit_message(embed=self.main.to_embed())


    @button(emoji="💬",label="回答",row=2,custom_id="reply",style=ButtonStyle.gray)
    async def respond_callback(self, interaction: Interaction,button:Button):
        if interaction.user == self.main.author:
            raise define_inter_error("發起者不可提問喔")
        elif len(self.main.asks)>=8:
            raise define_inter_error("資料塞車拉！請等待版主回答前面的後再試一次")
        return await interaction.response.send_modal(ask_modal(self.main))


    @button(emoji="▶",label="後",row=2,custom_id="next",style=ButtonStyle.blurple)
    async def next_callback(self, interaction: Interaction,button:Button):
        if self.main.page + 1 > int((len(self.main.answers)-1)/8)+1:self.main.page = 1
        else:self.main.page+=1
        return await interaction.response.edit_message(embed=self.main.to_embed())
    



    @select(
        placeholder="🎈其他選項",
        options=[
            SelectOption(label="刷新訊息",value = "resend",description="更新資料並移動至最新訊息",emoji="🔄"),
            SelectOption(label="輸出日誌",value = "send_txt",description="將目前狀況轉成文檔傳送",emoji="📜"),
            SelectOption(label="提示",value = "remind",description="為遊戲給予提示 | 僅限版主",emoji="💡"),
            SelectOption(label="填寫答案並結束",value = "disconnect",description="結束遊戲 | 僅限版主",emoji=f"{BACK}")
        ],
        row=3
    )
    async def select_callback(self, interaction: Interaction,select:Select):
        a = select.values[0]
        if a=="send_txt":
            return await self.send_log(interaction)
        elif a=="resend":
            await interaction.message.delete()
            self.main.msg = await interaction.channel.send(embed=self.main.to_embed(),view = self)
            return
        elif a=="remind":
            if interaction.user != self.main.author:
                raise GameError.NoPermission()
            return await interaction.response.send_modal(remind_modal(self.main))
        elif a=="disconnect":
            if interaction.user != self.main.author:
                raise GameError.NoPermission()
            else:return await interaction.response.send_modal(end_game_modal(self))


#學生提問表單

class ask_modal(Modal):
    def __init__(self,main:SituationPuzzle) -> None:
        super().__init__(title="🍡提出問題",timeout=0)
        self.main = main
    description = TextInput(label="填入",style=TextStyle.short,placeholder="主角是水球嗎？",max_length=50,min_length=3,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        self.main.asks.append(self.main.option(interaction.user,self.description.value))
        await interaction.response.edit_message(embed = self.main.to_embed())


#提示

class remind_modal(Modal):
    def __init__(self,main:SituationPuzzle) -> None:
        super().__init__(title="💡 給點提示",timeout=0)
        self.main = main
    description = TextInput(label="填入",style=TextStyle.short,placeholder="主角是水球喔！",max_length=50,min_length=3,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        self.main.answers.insert(0,self.main.option(interaction.user,self.description.value,"💡"))
        await interaction.response.edit_message(embed = self.main.to_embed())


#結束遊戲
class end_game_modal(Modal):
    def __init__(self,op:main_respond_and_answer) -> None:
        super().__init__(title="✅ 提供湯底",timeout=0)
        self.op =op
        self.main = op.main
    answer = TextInput(label="填入解答",style=TextStyle.paragraph,placeholder="水球被說非常的帥！",max_length=200,min_length=1,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        self.main.description += f"\n(遊戲已經結束)\n\n__提供湯底__：\n{self.answer.value}"
        for i in self.op.children:
            if i.custom_id not in ['last','next']:i.disabled = True
        await self.op.send_log(interaction)
        await interaction.message.edit(embed=self.main.to_embed(),view=self.op)
        await asyncio.sleep(300)
        return await self.main.msg.edit(view=None)