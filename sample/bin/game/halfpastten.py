import asyncio,discord
from random import choice,randint
from discord import Interaction
from discord.ui import Button,Select,Modal,button,select
from sample.bin.message import embed,V,define_inter_error
from .game_model import GameModel,GameError
# from sample.bin.rpg.rpgsql import *
from core import Color,MONEY_PAPER,BLUE_STAR,BACK,WHITE_STAR

HALF_PAST_TEN_JOIN_EMBED_TITLE = "🃏 | {} 發起了遊戲 `十點半`"
HALF_PAST_TEN_JOIN_EMBED_DES = "加入玩家：{}"

HALF_PAST_TEN_BANKER_EMBED_TITLE = "💲 | 請選擇莊家(僅限指令發起者)"
HALF_PAST_TEN_PVP_EMBED_TITLE = "🎲 | 請選擇競點玩家 (莊家限定)"


HALF_PAST_TEN_MAIN_EMBED_TITLE = "🃏 | 十點半 Half-Past-Ten (BETA)"
HALF_PAST_TEN_MAIN_EMBED_DES = "\n".join([
    "{} | {}",
    "",
    "{}",
    "{}"
])



class GAME_player:
    def __init__(self,player:discord.User) -> None:
        self.realname = player.name
        self.name = player.mention
        self.id = player.id
        self.get_value = 0
        self.disSaw = 0
        self.count = 0
        self.situation = "未輪到"
        self.money:int = 0
        self.earn:int = 0
class computer:
    def __init__(self,list) -> None:
        self.name = "電腦"
        self.id = randint(1,10000000)
        while(self.id in list):self.id = randint(1,10000000)
        self.get_value = 0
        self.disSaw = 0
        self.count = 0
        self.situation = "未輪到"
        self.money:int = 10
        self.earn:int = 0


class HalfPastTen(GameModel,name = "💰 | 十點半",player = (2,100)):
    def __init__(self, timeout: int = 0):
        super().__init__(timeout)
            # HALF_PAST_TEN_JOIN_EMBED_TITLE.format(self.author.name),
            # HALF_PAST_TEN_JOIN_EMBED_DES.format("`{}`".format(self.author.name)),


    async def gamestart(self, i: Interaction):
        self.player = [GAME_player(p) for p in self.player]
        banker = Banker(self)
        self.banker = await banker.return_banker(i)
        del banker
        for i in self.player:
            if int(i.id) == int(self.banker):
                i.name += "(莊家)"
                self.player = [value for value in self.player if value!=i]
                self.player.append(i)
                break
        money = set_money(self)
        await self.message.edit(embed = money.embed(),view=money)
        await money.main()
        game_start = game_main(self)
        await self.message.edit(embed=game_start.embed(),view = game_start)
        if isinstance(self.player[game_start.turn],computer):await game_start.to_computer()
        while game_start.end==False:await asyncio.sleep(1)
        await self.message.edit(embed=game_start.embed(),view=None)
        for k in [i for i in self.player if isinstance(i,GAME_player)]:earn_money(k.id,k.earn)
        


############ 玩家下注時間


SETMONEY_EMBED_TITLE = "💰十點半 | 籌碼下注時間"
SETMONEY_EMBED_DES = "\n".join([
    f"{MONEY_PAPER} | 請下注金額：(注意！現實生活請勿賭博)",
    "",
    "{}",
    "{}下注進度：{}"
])




class set_money(V):
    def __init__(self,game:HalfPastTen):
        super().__init__(timeout=0)
        self.game = game
        self.check = []
    def embed(self):
        return embed(
                SETMONEY_EMBED_TITLE,
                SETMONEY_EMBED_DES.format(
                    "\n".join([f"{value.name}： `{value.money}`元 \n" for value in self.game.player[:-1]]),
                    f"`{len(self.check)}`/`{len([i for i in self.game.player[:-1] if isinstance(i,GAME_player)])}` 人"
                ),
                Color.PURPLE
            )
    async def update(self,interaction:Interaction=None):
        if interaction==None:await self.game.message.edit(embed=self.embed(),view=self)
        else:await interaction.response.edit_message(embed=self.embed(),view=self)
        
    async def main(self):
        while(len(self.check) != len([i for i in self.game.player[:-1] if isinstance(i,GAME_player)])): await asyncio.sleep(1)
    
    @button(label="下注",custom_id="money",emoji=f"{MONEY_PAPER}",style=discord.ButtonStyle.blurple)
    async def set_button_click(self,i:discord.Interaction,button:Button):
        if i.user.id in [i.id for i in self.game.player[:-1]]:
            await i.response.send_modal(halfpastten_money_modal(self))
        elif i.user.id== self.game.player[-1].id:raise define_inter_error("莊家無法在遊戲中下注喔！")
        else:raise GameError.UserNotInGame()
    
    @button(label="鎖定",custom_id="check",emoji=f"{MONEY_PAPER}",style=discord.ButtonStyle.green)
    async def lock_button_click(self,interaction:discord.Interaction,button:Button):
        if interaction.user.id in [i.id for i in self.game.player[:-1]]:
            if interaction.user.id in self.check:raise define_inter_error("你已經鎖定過了")
            else:
                self.check.append(interaction.user.id)
                await self.update(interaction)
        elif interaction.user.id == self.game.player[-1].id: raise define_inter_error("莊家無法在此遊戲中下注喔！")
        else:await GameError.UserNotInGame()



class halfpastten_money_modal(Modal,title=f"💰下注金額"):
    def __init__(self,view:set_money):
        super().__init__()
        self.view = view
    money = discord.ui.TextInput(label="🍡填入數字",style=discord.TextStyle.short,placeholder="範例：1000",max_length=20,required=True)
    async def on_submit(self, interaction: discord.Interaction) -> None:
        if self.money.value.isdigit():
            # if int(self.money.value) > get_money_info(interaction.user.id):raise define_inter_error("缺錢要說！！ 這叫一昧賭博，不是姨妹賭博")
            [value for value in self.view.game.player if value.id == interaction.user.id][0].money = int(self.money.value)
            await self.view.update()
        else:return await define_inter_error("這是甚麼海螺數字？")
        await self.view.update(interaction)

############## 遊戲進行


class game_main(V):
    def __init__(self,game:HalfPastTen):
        self.turn = 0
        self.game = game
        self.cards = []
        self.purge = None
        self.end = False
        super().__init__(timeout=0)


    def choice_cards(self):
        if len(self.cards)<=0 :self.cards = [i+1 for i in range(52)]
        choose = choice(self.cards)
        self.cards.remove(choose)
        return choose
    def turn_value(self,value):
        if value>40:return 0.5
        else:return ((value-1)//4)+1 
    def embed(self):
        return embed(
                HALF_PAST_TEN_MAIN_EMBED_TITLE,
                HALF_PAST_TEN_MAIN_EMBED_DES.format(
                    BLUE_STAR,
                    f"現在輪到：**{self.game.player[self.turn].name}** 剩餘卡片：{len(self.cards)}張",
                    "\n".join([
                        f"{value.name} 《？+{value.get_value}點》\n狀態：`{value.situation}` 獲得：`{value.earn}`元 \n UUID：`{value.id}` \n" for value in self.game.player[:-1]
                    ]),
                    f"{self.game.player[-1].name} 《{self.game.player[-1].get_value}點》\n狀態：`{self.game.player[-1].situation}` 獲得：`{self.game.player[-1].earn}`元\n UUID：`{self.game.player[-1].id}`"
        ),Color.BLACK)
    async def update(self,interaction:Interaction=None,msg:str=None):
        if (interaction==None and msg==None):await self.game.message.edit(embed=self.embed(),view = self)
        elif(msg == "re_send" and interaction != None):return await interaction.channel.send(embed=self.embed(),view=self)
        elif(interaction != None):await interaction.response.edit_message(embed=self.embed(),view = self)
    async def to_computer(self):
        for i in [value for value in self.children if isinstance(value,Button)]:i.disabled=True
        await self.update()
        card = self.choice_cards()
        value = self.turn_value(card)
        p = self.game.player[self.turn]
        p.situation = "正在抽牌"
        p.disSaw = value
        await self.game.message.channel.send(content=f"🃏 | {self.turn+1}號電腦玩家 抽取了第一張牌",file=discord.File("assets/photo/card/0.jpg"),delete_after=5)
        await self.update()
        p.count+=1
        await asyncio.sleep(1)
        while (p.disSaw + p.get_value) <6:
            card = self.choice_cards()
            value = self.turn_value(card)
            p.get_value += value
            await self.game.message.channel.send(content=f"🃏 | 抽取了第 {p.count+1} 張牌",file=discord.File("assets/photo/card/{}d{}.jpg".format(((card-1)//4)+1,card%4+1)),delete_after=5)
            if p.disSaw + p.get_value > 10.5:
                p.situation = "爆了🌟"
                p.earn = -(p.money)
                self.game.player[-1].earn+=p.money
                break
            elif p.count==4:
                p.count+=1
                p.situation = "過五關🎉"
                p.earn = p.money*5
                self.game.player[-1].earn-=p.money*5
                break
            elif p.disSaw + p.get_value == 10.5:
                p.situation = "十點半🎀"
                p.earn = p.money*2
                self.game.player[-1].earn-=p.money*2
                break
            await self.update()
            p.count+=1
            await asyncio.sleep(1)
        for i in [value for value in self.children if isinstance(value,Button)]:
            if (i.custom_id =="stop" or i.custom_id =="re_send"):i.disabled=False
        await self.update()
        self.purge = await self.game.message.channel.send(content=f"✨ | 電腦已完成抽卡，請`莊家`按按鈕繼續")
        
    @discord.ui.button(emoji = "🃏",label="抽卡",style=discord.ButtonStyle.green,custom_id="chioce")
    async def button_callback(self,inter:discord.Interaction, button:discord.ui.Button):
        if inter.user.id != int(self.game.player[self.turn].id):
            raise GameError.NotNowTurn() 
        if self.turn<len(self.game.player)-1:
            p = self.game.player[self.turn]
            count = p.count
            if count==0:
                card = self.choice_cards()
                value = self.turn_value(card)
                for i in [value for value in self.children if isinstance(value,Button)]:
                    if (i.custom_id =="stop" or i.custom_id =="re_send"):i.disabled=False
                p.situation = "正在抽牌"
                p.disSaw = value
                await inter.channel.send(content=f"🃏 | {self.turn+1}號玩家 抽取了第一張牌",file=discord.File("assets/photo/card/0.jpg"),delete_after=8)
                await self.update()
                await inter.response.send_message(ephemeral=True,file=discord.File("assets/photo/card/{}d{}.jpg".format(((card-1)//4)+1,card%4+1)))
            else:
                card = self.choice_cards()
                value = self.turn_value(card)
                p.get_value += value
                await inter.channel.send(content=f"🃏 | 抽取了第 {count+1} 張牌",file=discord.File("assets/photo/card/{}d{}.jpg".format(((card-1)//4)+1,card%4+1)),delete_after=8)
                if p.disSaw + p.get_value > 10.5:
                    button.disabled = True
                    p.situation = f"爆了🎇"
                    p.earn = -p.money
                    self.game.player[-1].earn += p.money
                elif count==4:
                    button.disabled = True
                    p.situation = "過五關🎉"
                    p.earn = p.money*5
                    self.game.player[-1].earn -= p.money*5
                elif p.disSaw + p.get_value == 10.5:
                    button.disabled = True
                    p.situation = "十點半🎀"
                    self.game.player[-1].earn -= p.money*2
                    p.earn = p.money*2
                await self.update(inter)
            p.count+=1
        else:
            count = self.game.player[self.turn].count
            if count==0:
                [value for value in self.children if isinstance(value,player_list)][0].disabled = False
            card = self.choice_cards()
            value = self.turn_value(card)
            p = self.game.player[self.turn]
            p.get_value += value
            await inter.channel.send(content=f"🃏 | 莊家抽取了第 {count+1} 張牌",file=discord.File("assets/photo/card/{}d{}.jpg".format(((card-1)//4)+1,card%4+1)),delete_after=8)
            if p.disSaw + p.get_value > 10.5:
                for i in self.children:i.disabled = True
                for i in [value for value in self.game.player if value.situation=="等待競技"]:
                    i.situation = "贏了！"
                    i.earn = i.money
                    p.earn -= i.money
                p.situation = "爆了🎇"
                self.end = True
                return await inter.channel.send(embed = embed(f"{BLUE_STAR} | 莊家爆了🎇，遊戲結束","",Color.PURPLE))
            elif count==4:
                for i in self.children:i.disabled = True
                for i in [value for value in self.game.player if value.situation=="等待競技"]:
                    i.situation = "輸了QwQ"
                    i.earn = -(i.money*5)
                    p.earn += i.money*5
                p.situation = "過五關🎉"
                self.end = True
                return await inter.channel.send(embed = embed(f"{BLUE_STAR} | 莊家過五關🎉，遊戲結束","",Color.PURPLE))
            elif p.disSaw + p.get_value == 10.5:
                for i in self.children:i.disabled = True
                for i in [value for value in self.game.player if value.situation=="等待競技"]:
                    i.situation = "輸了QwQ"
                    i.earn = -(i.money)*2
                    p.earn += i.money*2
                p.situation = "十點半🎀"
                self.end = True
                return await inter.channel.send(embed = embed(f"{BLUE_STAR} | 莊家十點半🎀，遊戲結束","",Color.PURPLE))
            await self.update(inter)
            self.game.player[self.turn].count+=1
    @discord.ui.button(emoji = BACK,label="下一位",style=discord.ButtonStyle.danger,custom_id="stop")
    async def stop_button_callback(self,interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id != self.game.player[self.turn].id:
            if isinstance(self.game.player[self.turn],computer) and interaction.user.id == int(self.game.player[-1].id):pass
            else: raise GameError.NotNowTurn
        button.disabled = True
        if self.game.player[self.turn].situation == "正在抽牌":self.game.player[self.turn].situation = "等待競技"
        if not isinstance(self.game.player[self.turn+1],computer):
            for i in [value for value in self.children if isinstance(value,Button)]:
                if i.custom_id=="chioce":i.disabled = False
        self.turn+=1
        await self.update(interaction)
        if self.purge != None:
            await self.purge.delete()
            self.purge = None
        if (self.turn>=len(self.game.player)-1):
            button.disabled = True
            player_select = player_list(self)
            if len(player_select.options)==0:
                await self.game.message.channel.send(embed=embed(f"{BACK} | 沒有人可以競點，遊戲結束","",Color.BLUE))
                self.end = True
                return await self.game.message.edit(view=None)
            self.add_item(player_select)
            await self.update()
        elif isinstance(self.game.player[self.turn],computer):await self.to_computer()
    @discord.ui.button(emoji = "🔄",label="重發訊息",style=discord.ButtonStyle.blurple,custom_id="re_send")
    async def re_button_callback(self,interaction:discord.Interaction, button:discord.ui.Button):
        await self.game.message.delete()
        self.game.message = await self.update(interaction=interaction,msg="re_send")











############## 莊家競技玩家清單

class player_list(Select):
    def __init__(self,vw:game_main) -> None:
        self.vw = vw
        options = []
        for i in [value for value in self.vw.game.player if (value.count<5 and value.disSaw+value.get_value<10.5 and (value.id is not self.vw.game.player[-1].id))]:
            if isinstance(i,computer):emoji = "💻"
            else:emoji = "🙋🏻‍♂️"
            options.append(discord.SelectOption(label=i.name,value = i.id,emoji=emoji,description=f"成員UUID：{i.id}"))
        super().__init__(options=options,placeholder=HALF_PAST_TEN_PVP_EMBED_TITLE,disabled=True,custom_id="choose_player")
    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.vw.game.player[-1].id:
            to_player = [value for value in self.vw.game.player if value.id==int(self.values[0])][0]
            pvp_value1 = self.vw.game.player[-1].get_value
            pvp_value2 = to_player.get_value + to_player.disSaw
            if pvp_value1 > pvp_value2:
                await interaction.channel.send(embed = embed(
                    f"{WHITE_STAR} | 莊家選擇抓 {to_player.name}",
                    f"莊家(`{pvp_value1}`) > 玩家(`{pvp_value2}`) \n 恭喜 {self.vw.game.player[-1].name} 獲勝",
                    Color.PURPLE
                ))
                to_player.situation = "輸了 QwQ"
                to_player.earn = -to_player.money
                self.vw.game.player[-1].earn += to_player.money

            else:
                await interaction.channel.send(embed = embed(
                    f"{WHITE_STAR} | 莊家選擇抓 {to_player.name}",
                    f"莊家(`{pvp_value1}`) <= 玩家(`{pvp_value2}`) \n 恭喜 {to_player.name} 獲勝",
                    Color.PURPLE
                ))
                to_player.situation = "贏了！"
                to_player.earn = to_player.money
                self.vw.game.player[-1].earn -= to_player.money
            self.options = [value for value in self.options if int(value.value) != int(self.values[0])]
            if len(self.options)==0:
                self.vw.game.player[-1].situation="已結束競點"
                self.vw.end = True
            else:await self.vw.update(interaction)
        else:raise GameError.NoPermission("莊家")








############## 莊家選擇介面

class Banker(V):
    def __init__(self,g:HalfPastTen):
        super().__init__(timeout=0)
        self.chosen = None
        self.g = g
        self.add_item(banker_select(self))
    async def return_banker(self,i:discord.Interaction):
        await self.g.update(i,self,Color.BROWN)
        while (self.chosen==None):await asyncio.sleep(1)
        return self.chosen




############## 莊家選項

class banker_select(Select):
    def __init__(self,banker:Banker) -> None:
        self.banker = banker
        _options = []
        for i in [value for value in self.banker.g.player if isinstance(value,GAME_player)]:
            if isinstance(i,computer):emoji = "💻"
            else:emoji = "🙋🏻‍♂️"
            _options.append(discord.SelectOption(label=i.realname,value = i.id,emoji=emoji,description=f"成員UUID：{i.id}"))
        super().__init__(options=_options,placeholder=HALF_PAST_TEN_BANKER_EMBED_TITLE)


    async def callback(self, i: Interaction):
        if i.user == self.banker.g.author:
            await i.response
            self.banker.chosen = self.values[0]
        else:raise GameError.NoPermission("遊戲發起者")
        