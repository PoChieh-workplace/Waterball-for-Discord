import asyncio
from collections import Counter
from datetime import datetime, timedelta


from sample.bin.message import embed
from core import BACK, BLUE_STAR, GREEN_CHECK, PINK_STAR, WHITE_STAR,Color

from random import choice
from discord import ButtonStyle, Client, Embed, File, Interaction, Message, SelectOption, User, VoiceChannel
from discord.ui import View,Button,Select,button,select







class WereWolf:
    def __init__(self,msg:Message,bot:Client,author:User) -> None:
        self.vc = msg.channel
        self.msg = msg
        self.bot = bot
        self.author = author
        self.cp = False
        self.setting = False
        self.sys = WereWolf_sys(author)



    async def main(self):
        #系統配置
        if not isinstance(self.vc,VoiceChannel):await self.cvc()
        elif self.cp == False:await self.check_player()
        elif self.sys.playorder[0].order == "-1": await self.check_order()
        #基礎設置已完畢
        else:await self.check_part()
            




    def embed(self,description) -> Embed:
        return embed(
            f"🐺 │ Discord 狼人殺系統 (Pre-v2.4.3)",
            f"> 🎲 玩家：{len(self.sys.playerList)}人 | {self.vc.mention}\n"
            f"> 🕙 目前遊戲時間：第 {self.sys.day} 天 - {self.sys.time}\n\n"
            f"{description}",
            Color.LIGHT_ORANGE
        )
    async def timer(self,description,time:int):
        DEF = 12
        maxtime = datetime.now()+timedelta(seconds=time)
        tx = int((time-(maxtime-datetime.now()).seconds)/time*DEF)
        while(tx<DEF and tx>=0):
            timebar = "".join(["|"]+["▬" for i in range(tx)]+["🕐"]+["▬" for i in range(DEF-tx)]+["|"])
            await self.msg.edit(embed=self.embed(f"{description}\n\n{timebar}"),view = None)
            await asyncio.sleep(2)
            tx = int((time-(maxtime-datetime.now()).seconds)/time*12)
        timebar = "".join(["|"]+["▬" for i in range(DEF)]+["🕐"]+["|"])
        await self.msg.edit(embed=self.embed(f"{description}\n\n{timebar}"),view = None)
    


    async def cvc(self):
        await self.msg.edit(embed = self.embed("正在嘗試連接你的語音頻道"))
        vc = self.msg.guild.get_member(self.author.id).voice
        if vc != None:await self.msg.edit(embed = self.embed(f"確定將遊戲語音設置在 {vc.channel.mention} 嗎？"),view = check_vc(self,vc.channel))
        else:await self.msg.edit(embed = self.embed(f"你似乎不在一個語音頻道。"),view = check_vc(self))
    
    async def check_player(self):
        view = check_p(self)
        await view.v_update()

    async def check_order(self):
        view = choose_order(self)
        await view.v_update()

    async def check_part(self):
        await self.msg.edit(embed = self.embed(f"正在隨機分配角色"))
        self.sys.auto_selectpart()
        await self.timer(f"**{WHITE_STAR}遊戲即將開始，請各位玩家預備**",20)
        await self.msg.edit(embed = self.embed(f"{BLUE_STAR} 請領取自己的角色卡，並確認身分\n\n0 / {len(self.sys.playerList)} 已確認"),view=check_self_part(self))


    async def night(self):
        if len([i for i in self.sys.playorder if isinstance(i.part,WereWolf_sys.wolf)]) >= len([i for i in self.sys.playorder if isinstance(i.part,WereWolf_sys.good) or isinstance(i.part,WereWolf_sys.god)]):
            return await self.msg.edit(embed = self.embed("🎉🐺恭喜狼人方獲勝🎉"),view = None)
        elif len([i for i in self.sys.playorder if isinstance(i.part,WereWolf_sys.wolf)])==0:
            return await self.msg.edit(embed = self.embed("🎉🙋🏻‍♂️恭喜好人方獲勝🎉"),view = None)

        self.sys.time = "23:00"

        self.n = night_borad(self)
        await self.msg.edit(embed = self.embed("資料處理中"),view = self.n)
        await self.n.next()

    async def noon(self,killed):
        self.n = noon_board(self,killed)
        await self.msg.edit(embed = self.embed("資料處理中"),view = None)
        await self.n.run()




# 預設角色分布
# "狼人"、"狼王"、"隱狼"、"平民"、"預言"、"女巫"、"獵人"、"騎士"
PART_DEFAULT = [
    ["狼人","狼王","隱狼","平民","預言","女巫","獵人","騎士"], 
    [1,0,0,0,0,0,0,0], #1
    [0,0,1,0,1,0,0,0], #2
    [1,0,0,1,1,0,0,0], #3
    [0,1,0,0,0,1,1,1], #4
    [0,1,0,3,0,1,0,0], #5
    [2,0,0,3,0,1,0,0], #6
    [1,1,0,3,1,1,0,0], #7
    [1,1,0,4,1,1,0,0], #8
    [2,1,0,3,1,1,1,0], #9
    [2,1,0,4,1,1,1,0], #10
    [2,1,0,5,1,1,1,0], #11
    [1,1,1,5,1,1,1,1] #12
]

class WereWolf_sys:

    def __init__(self,author:User) -> None:
        self.author = author
        self.playerList = []
        self.time = "23:00"
        self.day = 0
        self.playorder = [self.ids("-1")]
        self.tmppart = []

    def auto_selectpart(self):
        #角色分配
        part = ["wolf","wolf_king","invisible_wolf","villager","prophet","witch","hunter","knight"]
        chooselist = []
        for i, it in enumerate(PART_DEFAULT[len(self.playerList)]):
            for k in range(it):chooselist.append(part[i])
            if it != 0: self.tmppart.append(part[i])
        for j in self.playorder:
            choose = choice(chooselist)
            if choose=="wolf":j.part = self.normal_wolf()
            elif choose=="wolf_king":j.part = self.wold_king()
            elif choose=="invisible_wolf":j.part = self.invisible_wolf()
            elif choose=="villager":j.part = self.villager()
            elif choose=="prophet":j.part = self.prophet()
            elif choose=="witch":j.part = self.witch()
            elif choose=="hunter":j.part = self.hunter()
            elif choose=="knight":j.part = self.knight()
            chooselist.remove(choose)
            
            

    class ids:
        def __init__(self,order,user:User=None) -> None:
            # if user==None:
            #     self.mention = "< 電腦 >"
            #     self.id = randint(10000000,9999999)
            #     self.part = None
            self.order = order
            self.user = user
            self.part:WereWolf_sys.part = None
            self.alive = True
    
    class logs:
        def __init__(self,user:User) -> None:
            self.time = datetime.now().strftime("[ %H:%M:%S ]")
            self.user = user

    class part(object):
        def __init__(self) -> None:
            super().__init__()
            self.type = "玩家"
            self.description = "你是 **玩家**，但系統似乎崩潰了，導致你沒有被分配到角色"
            self.isplayer = True
            self.log = "你似乎都再耍廢，沒有做事"
            self.history = []
            self.skill = []
            self.photo = None
        def show_log(self):
            return "你使用了技能，水之形·第三式·系統崩潰術(請聯絡開發者)"

        def reset(self):
            pass

    class referee(part):
        def __init__(self) -> None:
            super().__init__()
            self.type = "上帝"
            self.isplayer = False
            self.description = "你是場外人"

    class good(object):
        def __init__(self) -> None:
            super().__init__()
            self.team_name = "好人方"
    
    class god(object):
        def __init__(self) -> None:
            super().__init__()
            self.team_name = "神職方"

    class wolf(part):
        def __init__(self) -> None:
            super().__init__()
            self.log = "你們犯下的兇殺案，罄竹難書："
            self.team_name = "狼人方"
        def show_log(self):
            txt = "\n".join([f"{i.time} - " for i in {self.history} if isinstance(i,WereWolf_sys.logs)])
            return f"{self.log}\n"f""

    class villager(part,good):
        def __init__(self) -> None:
            super().__init__()
            self.type = "平民"
            self.photo = "assets/photo/werewolf/villager.jpg"
            self.description = f"你的角色是 **平民** ，屬於 {self.team_name}，但你小時候只顧玩鬧，導致你沒有技能，請您於白天參與討論，究竟你是天才還是天兵呢？"
    
    class prophet(part,god):
        def __init__(self) -> None:
            super().__init__()
            self.type = "預言家"
            self.photo = "assets/photo/werewolf/prophet.jpg"
            self.description = f"你的角色是 **預言家** ，屬於 {self.team_name}，你家的貓讓你學會預判未來。所有人將會被一覽無疑，只是時間的問題"
            self.skill = [skill.prophet_skill()]
        def reset(self):
            self.skill[0].able_use = True

    class witch(part,god):
        def __init__(self) -> None:
            super().__init__()
            self.used = False
            self.type = "女巫"
            self.photo = "assets/photo/werewolf/witch.jpg"
            self.description = f"你的角色是 **女巫** ，屬於 {self.team_name}，你似乎是家族最後一名女巫，但你的祖宗八代只研發了一瓶解藥與毒藥。請利用你的傳家寶保護大家吧"
            self.skill = [skill.witch_alive(),skill.witch_posion()]

    class hunter(part,god):
        def __init__(self) -> None:
            super().__init__()
            self.type = "獵人"
            self.photo = "assets/photo/werewolf/hunter.jpg"
            self.description = f"你的角色是 **獵人** ，屬於 {self.team_name}，身為八十歲的您，身上只剩下一發子彈，對上天發誓，只能在生離死別的時候使用這一發遺願"
            self.skill = [skill.hunter_hunt()]
    
    class knight(part,god):
        def __init__(self) -> None:
            super().__init__()
            self.type = "騎士"
            self.photo = "assets/photo/werewolf/knight.jpg"
            self.description = f"你的角色是 **騎士** ，屬於 {self.team_name}，身為上等首位，尊嚴與榮耀無比重要，一次的判斷決定你的生死"
            self.skill = [skill.knight_fight()]
    
    class normal_wolf(wolf):
        def __init__(self) -> None:
            super().__init__()
            self.type = "狼人"
            self.photo = "assets/photo/werewolf/wolf.jpg"
            self.description = f"你的角色是 **狼人** ，屬於 {self.team_name}，身為狼族的你，盡可能隱藏身分並殺掉任一陣營"
    
    class invisible_wolf(wolf):
        def __init__(self) -> None:
            super().__init__()
            self.type = "隱狼"
            self.photo = "assets/photo/werewolf/invisible_wolf.jpg"
            self.description = f"你的角色是 **隱狼** ，屬於 {self.team_name}，擅長隱藏氣息的你懂得騙過眾人，預言家將無法正確查驗你的身分"
    
    class wold_king(wolf):
        def __init__(self) -> None:
            super().__init__()
            self.type = "狼王"
            self.photo = "assets/photo/werewolf/wolf_king.jpg"
            self.description = f"你的角色是 **狼王** ，屬於 {self.team_name}，身為狼方領袖，能力強大也具領導能力"
            self.skill = [skill.wolf_king_show()]
        





# 個人技能程式區

class skill:
    class single_skill:
        def __init__(self) -> None:
            self.able_use = True  # 是否使用技能 1(可) 0(無)
            self.daily = False
            self.use_time = ["night"] # 技能重置時間 night(晚上使用) noon(白天使用) dead(被殺死時) self(自身發言時)
            self.name = "未命名技能"
            self.description = "你似乎沒有技能"

        def reset_used(self,time:str):
            if time == self.use_time:
                self.able_use = True
        async def function(self,interaction:Interaction,game:WereWolf,fro:WereWolf_sys.ids):
            return await interaction.response.send_message(embed = getembed(f"使用技能",f"{self.description}",PURPLE),view = View().add_item(noon_skill_select(game,self,fro)),ephemeral=True)
        async def run(self,interaction:Interaction,game:WereWolf,fro:WereWolf_sys.ids,id:WereWolf_sys.ids):
            self.able_use = False


    class prophet_skill(single_skill):
        def __init__(self) -> None:
            super().__init__()
            self.daily = True
            self.name = "預言"
            self.description = "你在每晚具有查驗能力，可以知道指定玩家的身分好壞"

    class witch_posion(single_skill):
        def __init__(self) -> None:
            super().__init__()
            self.name = "毒藥"
            self.description = "你可以於晚上下毒淘汰玩家，但只能使用一次"
    
    class witch_alive(single_skill):
        def __init__(self) -> None:
            super().__init__()
            self.name = "解藥"
            self.description = "你具有救人的能力，得知當晚被狼殺的玩家，並決定是否解救，但只能使用一次"
    
    class knight_fight(single_skill):
        def __init__(self) -> None:
            super().__init__()
            self.use_time = ["self"]
            self.name = "決鬥"
            self.description = "你可以在發言時段與他人發動決鬥，若對方為狼則狼死，若為好人則以自身之死謝罪"
        async def run(self, interaction: Interaction, game: WereWolf, fro: WereWolf_sys.ids, id: WereWolf_sys.ids):
            await interaction.response.edit_message(content="操作成功",embed = None,view = None)
            if isinstance(id.part,WereWolf_sys.wolf):

                await game.msg.channel.send(id.user.mention)
                await game.timer(
                    f"`{fro.order}號玩家` {fro.user.name} 向 `{id.order}號玩家` {id.user.name}\n"
                    f"發起了 **決鬥** ， 結果他成功殺死了 {id.part.team_name} 的一名成員",15)

                await game.msg.edit(embed = game.embed(f"{id.user.mention}，請決定你的最後一口氣"),view = lastskill_ifkilled(game,id))
            else:
                await game.timer(
                    f"`{fro.order}號玩家` {fro.user.name} 向 `{id.order}號玩家` {id.user.name}\n"
                    f"發起了 **決鬥** ， 結果他是好人，以死謝罪\n\n"
                    f"💬 即將將繼續發言"
                ,15)
                game.sys.playorder.remove(fro)
                await game.n.next()
                 
            return await super().run(interaction, game, fro, id)
            

    
    class wolf_king_show(single_skill):
        def __init__(self) -> None:
            super().__init__()
            self.use_time = ["noon","dead"]
            self.name = "自爆"
            self.description = "你可以於白天任意時間暴露身分，犧牲自己並帶走一人，亦或在被殺時(女巫的毒藥除外)使用此技能"
            self.dead = False
        async def function(self, interaction: Interaction, game: WereWolf, fro: WereWolf_sys.ids,dead:bool = False):
            self.dead = dead
            return await super().function(interaction, game, fro)
        async def run(self, interaction: Interaction, game: WereWolf, fro: WereWolf_sys.ids, id: WereWolf_sys.ids):
            await interaction.response.edit_message(content="操作成功",embed = None,view = None)

            await game.msg.channel.send(id.user.mention)
            if self.dead == True:
                await game.timer(
                        f"`{fro.order}號玩家` {fro.user.name} 使用了技能"
                        f"並帶走了 `{id.order}號玩家` {id.user.name}",15)
            else:
                await game.timer(
                    f"狼王 `{fro.order}號玩家` {fro.user.name} 自爆"
                    f"並帶走了 `{id.order}號玩家` {id.user.name}",15)
            game.sys.playorder.remove(fro)
            await game.msg.edit(embed = game.embed(f"{id.user.mention}，請決定你的最後一口氣"),view = lastskill_ifkilled(game,id))

            return await super().run(interaction, game, fro, id)


    class hunter_hunt(single_skill):
        def __init__(self) -> None:
            super().__init__()
            self.use_time = ["dead"]
            self.name = "獵槍"
            self.description = "你可以在被殺的時候瞄準一位玩家開槍，與你同歸於盡"

        async def run(self, interaction: Interaction, game: WereWolf, fro: WereWolf_sys.ids, id: WereWolf_sys.ids):
            await interaction.response.edit_message(content="操作成功",embed = None,view = None)

            await game.msg.channel.send(id.user.mention)
            await game.timer(
                    f"`{fro.order}號玩家` {fro.user.name} 使用了技能\n"
                    f"並帶走了 `{id.order}號玩家` {id.user.name}",15)
            game.sys.playorder.remove(fro)
            await game.msg.edit(embed = game.embed(f"{id.user.mention}，請決定你的最後一口氣"),view = lastskill_ifkilled(game,id))
            return await super().run(interaction, game, fro, id)




#確認區
class check_vc(View):
    def __init__(self,game:WereWolf,vc:VoiceChannel=None):
        super().__init__(timeout=0)
        self.game = game
        self.vc = vc
        if vc != None: [i for i in self.children if isinstance(i,Button) and i.custom_id=="check"][0].disabled=False


    @button(label = "確認", emoji=f'{GREEN_CHECK}',custom_id="check",disabled=True,style=ButtonStyle.green)
    async def check_the_vc(self,interaction:Interaction,button:Button):
        if interaction.user != self.game.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你並不是開發者",f"請 {self.game.author.mention} 使用本功能",RED
        ))
        await interaction.response.edit_message(embed = self.game.embed("正在更新資料"),view = None)
        self.game.vc = self.vc
        self.stop()
        return await self.game.main()

    @button(label = "更新", emoji="🔄" , custom_id="update",style=ButtonStyle.blurple)
    async def update(self,interaction:Interaction,button:Button):
        if interaction.user != self.game.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你並不是開發者",f"請 {self.game.author.mention} 使用本功能",RED
        ))
        await interaction.response.edit_message(embed = self.game.embed("正在更新資料"),view=None)
        return await self.game.main()

    @button(label = "取消", emoji=f"{BACK}",custom_id="cancel",style=ButtonStyle.danger)
    async def cancel(self,interaction:Interaction,button:Button):
        if interaction.user != self.game.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你並不是開發者",f"請 {self.game.author.mention} 使用本功能",RED
        ))
        self.stop()
        return await interaction.response.edit_message(embed = CONCIAL,view = None)



#確認區
class check_p(View):
    def __init__(self,game:WereWolf):
        super().__init__(timeout=0)
        self.game = game
        self.player = [self.game.author]

    async def v_update(self,interaction:Interaction=None):
        player = "、".join([i.mention for i in self.player])
        if interaction==None:return await self.game.msg.edit(embed=self.game.embed(f"正在等待其他玩家加入：\n{player}"),view=self)
        else:return await interaction.response.edit_message(embed=self.game.embed(f"正在等待其他玩家加入：\n{player}"),view=self)

    @button(label = "加入戰局", emoji='⚔',custom_id="join",style=ButtonStyle.green)
    async def check_the_vc(self,interaction:Interaction,button:Button):
        if interaction.user in self.player:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你已經在遊戲內了","",RED))
        elif interaction.user.voice == None or interaction.user.voice.channel!=self.game.vc:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 錯誤",f"你不在遊戲設定的語音頻道，為了您的遊戲體驗，請加入 {self.game.vc.mention} 中",RED))
        elif len(self.player)>=12:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 錯誤",f"本遊戲仍在測試階段，目前上限人數為 12 人",RED))
        self.player.append(interaction.user)
        if len(self.player)>= 4:[i for i in self.children if isinstance(i,Button) and i.custom_id=="gogo"][0].disabled = False
        return await self.v_update(interaction)

    @button(label = "退出戰局", emoji="🚪" , custom_id="leave",style=ButtonStyle.gray)
    async def update(self,interaction:Interaction,button:Button):
        if interaction.user not in self.player:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你並不在遊戲內喔","",RED))
        elif interaction.user == self.game.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 錯誤",f"為了資料運行正確，遊戲發起者不得離開遊戲",RED))
        self.player.remove(interaction.user)
        if len(self.player) < 4:[i for i in self.children if isinstance(i,Button) and i.custom_id=="gogo"][0].disabled = True
        return await self.v_update(interaction)
    

    @button(label = "確認遊戲", emoji="🔮" , custom_id="gogo",style=ButtonStyle.blurple,        disabled=True)
    async def check_to_play(self,interaction:Interaction,button:Button):
        if interaction.user != self.game.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你並不是遊戲發起者",f"請 {self.game.author.mention} 使用本功能",RED
        ))
        self.game.sys.playerList = self.player
        self.game.cp = True
        await interaction.response.edit_message(embed = self.game.embed("正在更新資料"),view=None)
        self.stop()
        return await self.game.main()


    @button(label = "關閉遊戲", emoji=f"{BACK}",custom_id="cancel",style=ButtonStyle.danger)
    async def cancel(self,interaction:Interaction,button:Button):
        if interaction.user != self.game.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你並不是遊戲發起者",f"請 {self.game.author.mention} 使用本功能",RED
        ))
        self.stop()
        return await interaction.response.edit_message(embed = CONCIAL,view = None)


class choose_order(View):
    def __init__(self,game:WereWolf):
        self.game = game
        self.part = PART_DEFAULT[len(self.game.sys.playerList)]
        self.des = "\n".join([f"{PART_DEFAULT[0][i]}：{self.part[i]}人" for i in range(len(PART_DEFAULT[0]))])
        super().__init__(timeout=0)
        for i in range(1,len(self.game.sys.playerList)+1):
            self.add_item(intro_number(i,self.game))
    
    async def v_update(self,interaction:Interaction=None):
        if interaction==None:return await self.game.msg.edit(embed=self.game.embed(f"角色配置：\n{self.des}\n\n請各位玩家選擇發言順序"),view=self)
        else:return await interaction.response.edit_message(embed=self.game.embed(f"角色配置：\n{self.des}\n\n請各位玩家選擇發言順序"),view=self)
    

    @button(label = "開始", emoji="🔮" , custom_id="gogo",style=ButtonStyle.blurple,disabled=True)
    async def check_to_play(self,interaction:Interaction,button:Button):
        if interaction.user != self.game.author:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你並不是遊戲發起者",f"請 {self.game.author.mention} 使用本功能",RED))
        await interaction.response.edit_message(embed = self.game.embed("正在更新資料"),view=None)
        self.game.sys.playorder = [self.game.sys.ids(i.custom_id,i.player) for i in self.children if isinstance(i,intro_number)]
        self.stop()
        return await self.game.main()


class intro_number(Button):
    def __init__(self,id:int,game:WereWolf):
        super().__init__(
            style=ButtonStyle.gray,
            label=f"{id}",
            disabled = False,
            custom_id = f"{id}"
        )
        self.player = None
        self.game = game
    async def callback(self, interaction: Interaction):
        if not isinstance(self.view,choose_order):return
        if interaction.user not in self.game.sys.playerList:
            return await interaction.response.send_message(embed = getembed(f"{BACK} | 你不在遊戲中","",RED),ephemeral=True)
        if self.player ==None:
            for i in [u for u in self.view.children if isinstance(u,intro_number) if u.player==interaction.user]:
                i.style = ButtonStyle.gray
                i.label = i.custom_id
                i.player = None
            self.style = ButtonStyle.green
            self.label = interaction.user.name[:3]
            self.player = interaction.user
            if len([u for u in self.view.children if isinstance(u,intro_number) and u.player!=None])>=len(self.game.sys.playerList):
                [k for k in self.view.children if isinstance(k,Button) and k.custom_id=="gogo"][0].disabled = False
            return await self.view.v_update(interaction)
        elif self.player == interaction.user:
            self.style = ButtonStyle.gray
            self.label = self.custom_id
            self.player = None
            [k for k in self.view.children if isinstance(k,Button) and k.custom_id=="gogo"][0].disabled = True
            return await self.view.v_update(interaction)
        else:return await interaction.response.send_message(embed = getembed(f"{BACK} | 無法入座","挖！有人搶走了位子，換個順序吧！",RED),ephemeral=True)


class check_self_part(View):
    def __init__(self,game:WereWolf):
        super().__init__(timeout=0)
        self.game = game
        self.player = []
    
    @button(label = "領取卡片", emoji="🃏" , custom_id="get_card",style=ButtonStyle.blurple,disabled=False)
    async def check_card(self,interaction:Interaction,button:Button):
        if interaction.user not in self.game.sys.playerList:return await interaction.response.send_message(ephemeral=True,embed = getembed(
            f"{BACK} | 你並不是遊戲玩家",f"挖！你晚了一步加入遊戲QQ",RED
        ))
        if interaction.user not in self.player:
            self.player.append(interaction.user)
        
        l1 = len(self.player)
        l2 = len(self.game.sys.playerList)

        part = [u.part for u in self.game.sys.playorder if u.user==interaction.user][0]
        skill_doc = "\n\n".join([f"{BLUE_STAR} **{i.name}**\n{i.description}" for i in part.skill if isinstance(i,skill.single_skill)])
        doc = f"{PINK_STAR} {part.description}"
        if skill_doc != "":doc+=f"\n\n以下為你的技能：\n{skill_doc}"

        embed = getembed("🃏｜取得身分",f"{doc}",PURPLE)
        embed.set_image(url="attachment://image.jpg")
        file = File(fp=part.photo,filename="image.jpg")

        await interaction.response.send_message(embed=embed,file=file,ephemeral=True)
        await interaction.message.edit(embed = self.game.embed(f"{BLUE_STAR} 請領取自己的角色卡，並確認身分\n{len(self.player)} / {len(self.game.sys.playerList)} 已確認"))

        if l1>=l2:return await self.game.night()


        

class night_borad(View):
    def __init__(self,game:WereWolf):
        super().__init__()
        self.game = game
        self.done = False
        self.am = 0
        self.killed_by_wolf:WereWolf_sys.ids = None
        self.killed = []
        self.select = [wolf_select(self.game)]
        if "prophet" in self.game.sys.tmppart:self.select.append(prophet_select(self.game))
        
    async def next(self):
        if self.am <= 0:await self.game.timer("🌙 天黑請閉眼 👀",10)
        else:await self.game.timer(self.select[self.am-1].close_eye,8)

        if self.am>=len(self.select):
            self.stop()
            return await self.game.noon(self.killed)

        self.clear_items()
        s = self.select[self.am]
        self.add_item(s)

        await self.game.timer(s.open_eye,8)
        await self.game.msg.edit(embed=self.game.embed(f"{s.doc}"),view=self)




class night_select(Select):
    def __init__(self,game:WereWolf,doc:str,open_eye:str,close_eye:str,custom_id,placeholder,options) -> None:
        super().__init__(custom_id=custom_id,placeholder=placeholder,options=options)
        self.game = game
        self.doc = doc
        self.open_eye = open_eye
        self.close_eye = close_eye


class wolf_select(night_select):
    def __init__(self,game:WereWolf) -> None:
        super().__init__(
            game=game,
            custom_id="wolf_select",
            placeholder="🔪 選擇你想殺的人",
            doc = f"{WHITE_STAR} 今晚你想來點？請狼人方選擇想殺的人，將強制選出一人",
            open_eye = "**🐺 狼人請睜眼**",
            close_eye = "**🐺 狼人請閉眼**",
            options = [
                SelectOption(label = f"{i.order} 號",description=f"{i.user.name}",emoji=f"{WHITE_STAR}",value=i.order) 
                for i in game.sys.playorder
            ]
        )
        self.len = [i for i in self.game.sys.playorder if isinstance(i.part,WereWolf_sys.wolf)]
        self.voted = []
        self.have_vote = []

    def return_count(self):
        count = len(self.len)
        v_count = len(self.have_vote)
        txt = "".join(["●" for i in range(v_count)]+["○" for i in range(count-v_count)])
        return "\n"+txt

    async def callback(self, interaction: Interaction) -> None:
        if not isinstance(self.view,night_borad):return print("Error on night_board")
        if interaction.user not in self.game.sys.playerList:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你不在遊戲內","你似乎慢了一點，沒關係，下一局就有你了！",RED
            ))
        elif interaction.user not in [i.user for i in self.game.sys.playorder]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你已經死了","你似乎已經不在場上，無法使用技能",RED))
        elif interaction.user not in [k.user for k in self.len]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你不是狼","這遊戲似乎沒有間諜，**只有狼可以操作本系統**，請稍後再試",RED
            ))
        elif interaction.user in self.have_vote:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你已經投過票了","",RED
            ))


        self.have_vote.append(interaction.user)
        self.voted.append(self.values[0])

        await interaction.response.edit_message(embed = self.game.embed(f"{self.doc}"+self.return_count()))

        if len(self.have_vote) >= len(self.len):
            data = Counter(self.voted)
            v = data.most_common(1)[0][0]
            ids = [i for i in self.game.sys.playorder if i.order==v][0]
            self.view.killed_by_wolf= ids
            self.view.killed.append(ids)
            self.view.am  += 1
            if "witch" in self.game.sys.tmppart:self.view.select.insert(1,witch_select(self.game,self.view))
            return await self.view.next()


class witch_select(night_select):
    def __init__(self,game:WereWolf,view:night_borad) -> None:
        super().__init__(
            game=game,
            custom_id="witch_select",
            placeholder="🧪選擇你想使用的藥水",
            doc = f"{WHITE_STAR} 女巫阿女巫，你要救人還是殺人？",
            open_eye = "**🧪 女巫請睜眼**",
            close_eye = "**🧪 女巫請閉眼**",
            options = [
                SelectOption(label = f"解藥",description=f"解救 {view.killed_by_wolf.order} 號玩家 {view.killed_by_wolf.user.name}",emoji=f"❤",value="use_alive"),
                SelectOption(label = f"毒藥",description=f"使用毒藥 | 點擊後將選擇玩家",emoji=f"💀",value="use_posion"),
                SelectOption(label = f"沒事",description=f"甚麼都不用",emoji=f"💬",value="nothing")
            ]
        )
        for i in [k.part for k in self.game.sys.playorder if isinstance(k.part,WereWolf_sys.witch)]:i.used = False
        self.len = [i for i in self.game.sys.playorder if isinstance(i.part,WereWolf_sys.witch)]
        self.vi = view
    
    async def update(self):
        p = [i.part for i in self.game.sys.playorder if isinstance(i.part,WereWolf_sys.witch)]
        txt = "\n" + "".join(["●" for i in p if i.used==True]+["○" for i in p if i.used==False])
        await self.game.msg.edit(embed = self.game.embed(f"{self.doc}"+txt))
        self.vi.am += 1
        return await self.vi.next()

    async def callback(self, interaction: Interaction) -> None:
        if interaction.user not in self.game.sys.playerList:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你不在遊戲內","你似乎慢了一點，沒關係，下一局就有你了！",RED))
        elif interaction.user not in [i.user for i in self.game.sys.playorder]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你已經死了","你似乎已經不在場上，無法使用技能",RED))
        elif interaction.user not in [k.user for k in self.len]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你不是女巫","這遊戲似乎沒有間諜，只有女巫可以操作本系統，請稍後再試",RED))
        part = [i.part for i in self.game.sys.playorder if isinstance(i.part,WereWolf_sys.witch) and i.user==interaction.user][0]
        if part.used == True:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你沒有多餘的力氣","你已經選擇今天要做甚麼了",RED))


        elif self.values[0] == "use_posion":
            askill = [i for i in part.skill if isinstance(i,skill.witch_posion)][0]
            if askill.able_use== False:
                return await interaction.response.send_message(ephemeral=True,embed=getembed(f"{BACK}｜你沒有毒藥了","祖宗八代不給力啊！！",RED))
            return await interaction.response.send_message(ephemeral=True,embed=getembed("💀 請選擇","看來你有深仇大恨了！",PURPLE),view = View().add_item(witch_posion_select(self,part)))    

        elif self.values[0] == "use_alive":
            askill = [i for i in part.skill if isinstance(i,skill.witch_alive)][0]
            if askill.able_use== False:
                return await interaction.response.send_message(ephemeral=True,embed=getembed(f"{BACK}｜你沒有毒藥了","祖宗八代不給力啊！！",RED))
            askill.able_use = False
            if self.vi.killed_by_wolf in self.vi.killed:self.vi.killed.remove(self.vi.killed_by_wolf)
            await interaction.response.send_message(ephemeral=True,embed=getembed("❤ 使用解藥",f"你選擇救活了 `{self.vi.killed_by_wolf.order} 號玩家`",PURPLE))

        elif self.values[0] == "nothing":
            await interaction.response.send_message(embed = getembed("💬 沉默",f"你選擇不做事",PURPLE),ephemeral=True)

        part.used = True
        await self.update()

class witch_posion_select(Select):
    def __init__(self,v:witch_select,part:WereWolf_sys.witch):
        self.v = v
        self.part = part
        super().__init__(
            custom_id="choose_to_posion",
            placeholder = "💀選擇使用毒藥的玩家",
            options = [
                SelectOption(label = f"{i.order} 號",description=f"{i.user.name}",emoji=f"{WHITE_STAR}",value=i.order) 
                for i in v.game.sys.playorder
            ]
        )
    async def callback(self, interaction: Interaction):
        posion = [i for i in self.v.game.sys.playorder if i.order == self.values[0]][0]
        [i for i in self.part.skill if isinstance(i,skill.witch_posion)][0].able_use = False
        self.v.vi.killed.append(posion)
        self.part.used = True
        await interaction.response.send_message(embed = getembed("💀 使用毒藥",f"成功毒死了 `{posion.order}號玩家` {posion.user.mention}",GREEN),ephemeral=True)
        for i in posion.part.skill:
            if isinstance(i,skill.single_skill):i.able_use = False
        posion.alive = False
        return await self.v.update()


class prophet_select(night_select):
    def __init__(self,game:WereWolf) -> None:
        super().__init__(
            game=game,
            custom_id="prophet_select",
            placeholder="🔮 選擇你想查驗的對象",
            doc = f"{WHITE_STAR} 魔鏡啊魔鏡，請讓我知道...的身分，請預言家選擇查驗玩家",
            open_eye = "**🔮 預言家請睜眼**",
            close_eye = "**🔮 預言家請閉眼**",
            options = [
                SelectOption(label = f"{i.order} 號",description=f"{i.user.name}",emoji=f"{WHITE_STAR}",value=i.order) 
                for i in game.sys.playorder
            ]
        )
        for i in [k.part for k in self.game.sys.playorder if isinstance(k.part,WereWolf_sys.prophet)]:i.reset()
        self.len = [i for i in self.game.sys.playorder if isinstance(i.part,WereWolf_sys.prophet)]
    
    async def update(self):
        p = [i.part.skill[0] for i in self.game.sys.playorder if isinstance(i.part,WereWolf_sys.prophet)]
        txt = "\n" + "".join(["●" for i in p if i.able_use==False]+["○" for i in p if i.able_use==True])
        await self.game.msg.edit(embed = self.game.embed(f"{self.doc}"+txt))
        if len(["0" for i in p if i.able_use==True])==0:
            if not isinstance(self.view,night_borad):return
            self.view.am +=1
            await self.view.next()

        

    async def callback(self, interaction: Interaction) -> None:
        if interaction.user not in self.game.sys.playerList:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你不在遊戲內","你似乎慢了一點，沒關係，下一局就有你了！",RED))
        elif interaction.user not in [i.user for i in self.game.sys.playorder]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你已經死了","你似乎已經不在場上，無法使用技能",RED))
        elif interaction.user not in [k.user for k in self.len]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你不是預言家","這遊戲似乎沒有間諜，只有預言家可以操作本系統，請稍後再試",RED))

        part = [i.part for i in self.game.sys.playorder if isinstance(i.part,WereWolf_sys.prophet) and i.user==interaction.user][0]

        if part.skill[0].able_use == False:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你已經預言過了","魔鏡似乎在睡覺，你懷念起了去年剛過世的貓",RED))
        else:
            p = [i for i in self.game.sys.playorder if i.order == self.values[0]][0]
            if isinstance(p.part,WereWolf_sys.wolf) and not isinstance(p.part,WereWolf_sys.invisible_wolf):
                text = p.part.team_name
            else:text = "好人方"
            await interaction.response.send_message(ephemeral=True,embed = getembed(f"🔮｜查驗 {p.order}號 玩家",f"`{p.order}號玩家 {p.user.name}` 是 **{text}**",PURPLE))
            part.skill[0].able_use = False

        await self.update()




class noon_board(View):
    def __init__(self,game:WereWolf,killed):
        super().__init__(timeout=0)
        self.game = game
        self.last_killed = [i for i in killed if isinstance(i,WereWolf_sys.ids)]
        self.order = 0
        self.txt = "發生錯誤"
    async def run(self):
        self.game.sys.time = "12:00"
        self.game.sys.day += 1
        if len(self.last_killed)==0:
            await self.game.timer("🎐 **天亮了**",5)
            await self.game.timer("🎐 **昨晚是平安夜**",5)
        else:
            kt = "\n".join([f"`{i.order}號` {i.user.name} 死了" for i in self.last_killed])
            await self.game.timer(f"🎐 **昨晚有人翹辮子了** \n{kt}",5)
            if self.game.sys.day == 1:
                self.game.sys.playorder = [i for i in self.game.sys.playorder if i in self.last_killed and i.alive==True] + [i for i in self.game.sys.playorder if i not in self.last_killed]
            else:self.game.sys.playorder = [i for i in self.game.sys.playorder if i not in self.last_killed]
        return await self.words()
    
    async def words(self,interaction:Interaction=None):

        if self.order>=len(self.game.sys.playorder):
            if interaction != None:await interaction.response.edit_message(embed = self.game.embed("資料處理中"))
            await self.game.timer("投票時間",5)
            return await self.game.msg.edit(embed=self.game.embed("🚩 請所有玩家投出自己所認為的壞人"),view = vote_board(self.game))


        id = self.game.sys.playorder[self.order]
        if id in self.last_killed:self.txt = f"`{id.order}號玩家` {id.user.mention}，請發表遺言！\n\n🧩點擊 過 即代表放棄技能"
        else:self.txt = f"`{id.order}號玩家` {id.user.mention}，請開始發言！"
        if interaction != None:
            await interaction.response.edit_message(embed = self.game.embed(self.txt),view = self)
        else:await self.game.msg.edit(embed = self.game.embed(self.txt),view = self)
        await self.game.msg.channel.send(f"{id.user.mention}",delete_after=5)
    
    async def next(self,interaction:Interaction=None):
        id = self.game.sys.playorder[self.order]
        if id in self.last_killed:self.game.sys.playorder.remove(id)
        else:self.order +=1
        return await self.words(interaction)


    async def error(self,interaction:Interaction):
        if interaction.user not in self.game.sys.playerList:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你不在遊戲內","你似乎慢了一點，沒關係，下一局就有你了！",RED))
        elif interaction.user not in [i.user for i in self.game.sys.playorder]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你已經死了","你似乎已經不在場上。",RED))
        else:return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜還沒輪到你","請稍後再試",RED))


    @button(label = "過", emoji=f"👍🏻" , custom_id="next",style=ButtonStyle.green)
    async def next_player(self,interaction:Interaction,button:Button):
        id = self.game.sys.playorder[self.order]
        if id.user==interaction.user:
            return await self.next(interaction)
        else:return await self.error(interaction)
    @button(label = "刷新", emoji=f"🔄" , custom_id="resend",style=ButtonStyle.blurple)
    async def resend(self,interaction:Interaction,button:Button):
        await self.game.msg.delete()
        self.game.msg = await interaction.channel.send(embed = self.game.embed(self.txt),view = self)
    @select(placeholder="👁‍🗨其他功能",custom_id="other_function",options=[
        SelectOption(label="使用技能",value="use_skill",emoji="🧩",description="使用自己角色技能"),
        SelectOption(label="個人日誌",value="log",emoji=f"📜",description="查看自己的技能說明 | 尚未開放"),
        SelectOption(label="跳過",value="force_skip",emoji="⚰",description="強制跳過此人發言｜僅限版主"),
        SelectOption(label="場外觀察",value="view_game",emoji="⚰",description="得知場上所有人的身分｜限場外人(包含遭淘汰者)"),
        # SelectOption(label="強制結束",value="force_stop",emoji=f"{BACK}",description="刪除資料並停止遊戲進行｜僅限版主")
    ])
    async def other_callback(self,interaction:Interaction,select:Select):
        if select.values[0]=="log":await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK} | 開發中",f"本功能尚無法使用",RED))
        elif select.values[0]=="use_skill":
            ids =[i for i in self.game.sys.playorder if i.user == interaction.user]

            if len(ids)==1:id = ids[0]
            else:return await self.error(interaction)

            skills = [i for i in id.part.skill if isinstance(i,skill.single_skill)]
            if len(skills)==0:
                return await interaction.response.send_message(ephemeral=True, embed=getembed(
                    f"{BACK}｜你沒有可用技能","你確定你你小時候很認真學習技能嗎",RED))
            s = skills[0]

            if s.able_use==False:
                return await interaction.response.send_message(ephemeral=True, embed=getembed(
                    f"{BACK}｜你已經用過技能了","",RED))
            elif "noon" in s.use_time:
                if isinstance(s,skill.wolf_king_show) and id in self.last_killed:
                    return await s.function(interaction,self.game,id,True)
                return await s.function(interaction,self.game,id)
            elif "self" in s.use_time:
                if interaction.user != id.user:return await interaction.response.send_message(ephemeral=True, embed=getembed(
                    f"{BACK}｜無法使用","你只能在自己發言時段使用",RED))
                else:return await s.function(interaction,self.game,id)
            elif "dead" in s.use_time:
                if id in self.last_killed:return await interaction.response.send_message(ephemeral=True, embed=getembed(
                    f"{BACK}｜無法使用","你只能在自己臨終前使用",RED))
                else:return await s.function(interaction,self.game,id)

            else:return await self.error(interaction)


        elif select.values[0]=="force_skip":
            if interaction.user==self.game.author:return await self.next(interaction)
            else:await interaction.response.send_message(ephemeral=True,embed=getembed(
                    f"{BACK} | 你並不是遊戲發起者",f"請 {self.game.author.mention} 使用本功能",RED))
        
        elif select.values[0]=="view_game":
            if interaction.user in [i.user for i in self.game.sys.playorder if i.user == interaction.user]:
                return await interaction.response.send_message(embed = getembed(
                    f"{BACK}｜你還在場上","當局著迷，旁觀者清",RED
                ))
            else:
                text = "\n\n".join([f"`{u.order}號玩家 {u.user.name}\n角色：{u.user}`" for u in self.game.sys.playorder])
                return await interaction.response.send_message(ephemeral=True,embed=self.game.embed(text))


        # elif select.values[0]=="force_stop":
        #     if interaction.user==self.game.author:
        #         await interaction.response.s
        #         self.stop()
        #         await self.
        #     else:await interaction.response.send_message(ephemeral=True,embed=getembed(
        #             f"{BACK} | 你並不是遊戲發起者",f"請 {self.game.author.mention} 使用本功能",RED))


        else:return await interaction.response.send_message(embed = getembed(f"{BACK} WOW，你抓到蟲蟲了","似乎是腦誤的開發者引導你到這",RED),ephemeral=True)
class noon_skill_select(Select):
    def __init__(self,game:WereWolf,skill:skill.single_skill,fro:WereWolf_sys.ids):
        super().__init__(
            custom_id="choose_to_skill",
            placeholder = skill.name,
            options = [
                SelectOption(label = f"{i.order} 號",description=f"{i.user.name}",emoji=f"{WHITE_STAR}",value=i.order) 
                for i in game.sys.playorder if i.alive==True and i!=fro
            ]
        )
        self.fro = fro
        self.skill = skill
        self.game =game
    async def callback(self, interaction: Interaction):
        id = [i for i in self.game.sys.playorder if i.order==self.values[0]][0]
        return await self.skill.run(interaction,self.game,self.fro,id)



class vote_board(View):
    def __init__(self,game:WereWolf):
        super().__init__(timeout=None)
        self.add_item(vote_select(game))




class vote_select(Select):
    class avote:
        def __init__(self,ids:WereWolf_sys.ids,vt:WereWolf_sys.ids) -> None:
            self.fro = ids
            self.vote = vt


    def __init__(self,game:WereWolf) -> None:
        super().__init__(
            custom_id="vote_select",
            placeholder="🔖 投票",
            options = [
                SelectOption(label = f"{i.order} 號",description=f"{i.user.name}",emoji=f"{WHITE_STAR}",value=i.order) 
                for i in game.sys.playorder
            ]
        )
        self.game = game
        self.len = game.sys.playorder
        self.voted = []

    def return_count(self):
        count = len(self.len)
        v_count = len(self.voted)
        txt = "".join(["●" for i in range(v_count)]+["○" for i in range(count-v_count)])
        return "\n"+txt
    
    async def update(self):
        await self.game.msg.edit(embed = self.game.embed(f"🚩 請所有玩家投出自己所認為的壞人\n{self.return_count()}"))
        if len(self.voted) >= len(self.len):
            data = Counter([i.vote.order for i in self.voted if isinstance(i,self.avote)])

            doc = f"\n\n{PINK_STAR}投票紀錄：\n"+"\n".join([f"{BLUE_STAR} `{i.fro.order}號玩家{i.fro.user.name}` 投給了 `{i.vote.order}號玩家`" for i in self.voted if isinstance(i,self.avote)])

            v = data.most_common()
            ids = [i.vote for i in self.voted if isinstance(i,self.avote) and i.vote.order==v[0][0]][0]


            if len(v)>=2:
                if v[0][1] == v[1][1]:ids=None
            if ids!= None:
                count = v[0][1]
                await self.game.timer(f"`{ids.order}號玩家 {ids.user.name}` 被眾人以 **{count}** 票被放逐了{doc}",15)
                return await self.game.msg.edit(embed = self.game.embed(f"{ids.user.mention}，請決定你的最後一口氣"),view = lastskill_ifkilled(self.game,ids))
            else:
                await self.game.timer(f"**{WHITE_STAR} 平票，無人出局**",15)
                return await self.game.night()

    async def callback(self, interaction: Interaction) -> None:
        if interaction.user not in self.game.sys.playerList:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你不在遊戲內","你似乎慢了一點，沒關係，下一局就有你了！",RED
            ))
        elif interaction.user not in [i.user for i in self.game.sys.playorder]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你已經死了","你似乎已經不在場上，無法投票",RED))
        elif interaction.user in [i.fro.user for i in self.voted if isinstance(i,self.avote)]:
            return await interaction.response.send_message(ephemeral=True,embed=getembed(
                f"{BACK}｜你已經投過票了","",RED
            ))
        self.voted.append(self.avote([i for i in self.len if i.user==interaction.user][0],[i for i in self.game.sys.playorder if i.order == self.values[0]][0]))
        await interaction.response.send_message(embed = getembed("🔖投票成功",f"你投給了 `{self.values[0]}號玩家`",BLUE),ephemeral=True)
        return await self.update()





class lastskill_ifkilled(View):
    def __init__(self,game:WereWolf,ids:WereWolf_sys.ids):
        super().__init__(timeout=None)
        self.game = game
        self.ids = ids
    @button(label = "略過", emoji=f"💬" , custom_id="skip_skill",style=ButtonStyle.gray)
    async def skip(self,interaction:Interaction,button:Button):
        if self.ids.user!=interaction.user:
            return await interaction.response.send_message(ephemeral=True,embed =getembed(f"你並不是本人","",BLUE))
        await interaction.response.send_message(ephemeral=True,embed =getembed(f"你選擇了沉默，並被淘汰了","",BLUE))
        await self.game.timer(f"`{self.ids.order}號玩家{self.ids.user.name}` 除了死亡，沒有留下任何東西",10)
        self.game.sys.playorder.remove(self.ids)
        await self.game.night()
    @button(label = "技能", emoji=f"🧩" , custom_id="use_skill",style=ButtonStyle.blurple)
    async def use(self,interaction:Interaction,button:Button):
        id = [i for i in self.game.sys.playorder if i.user == interaction.user][0]
        skills = [i for i in id.part.skill if isinstance(i,skill.single_skill)]
        if len(skills)==0:
            return await interaction.response.send_message(ephemeral=True, embed=getembed(
                f"{BACK}｜你沒有可用技能","你確定你小時候很認真學習技能嗎？",RED))
        s = skills[0]
        if s.able_use==False:
            return await interaction.response.send_message(ephemeral=True, embed=getembed(
                f"{BACK}｜你已經用過技能了","",RED))
        elif "dead" in s.use_time:
            if isinstance(s,skill.wolf_king_show):
                return await s.function(interaction,self.game,id,True)
            else:return await s.function(interaction,self.game,id)
        else:return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK}｜無法使用","你這時候無法施展技能",RED))
    @button(label = "跳過", emoji=f"🕐" , custom_id="force_skip",style=ButtonStyle.red)
    async def force_skip(self,interaction:Interaction,button:Button):
        if self.game.author !=interaction.user:
            return await interaction.response.send_message(ephemeral=True,embed =getembed(f"版主專用",f"請 {self.game.author.mention} 使用本功能來跳過",BLUE))
        await interaction.response.send_message(ephemeral=True,embed =getembed(f"強制跳過",f"成功使用指令，已跳過 `{self.ids.order}號玩家{self.ids.user.name}` 的發言",BLUE))
        await self.game.timer(f"`{self.ids.order}號玩家{self.ids.user.name}` 除了死亡，沒有留下任何東西",10)
        self.game.sys.playorder.remove(self.ids)
        await self.game.night()