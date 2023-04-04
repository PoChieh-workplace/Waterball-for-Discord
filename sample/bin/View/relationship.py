from sample.bin.message import embed,V,define_inter_error
from sample.bin.image.friendship import friend_exp_img
from sample.bin.rpg.friendship.config import *
from sample.bin.rpg.rpgsql import limit, make_friend,get_money_info,cost_money,get_friend_level,get_friend_exp,edit_friend_exp
from core import BACK,PENCIL,GREEN_HEART,PRE,Color
from discord.ui import View,button,Button,Select,select
from discord import Interaction,ButtonStyle,User,SelectOption
from random import choice,randint


class confession_check_button(V):
    def __init__(self):
        super().__init__(timeout=0)

    @button(label="告白誓言", emoji="🔖", custom_id="mate_confession", disabled=True, style=ButtonStyle.blurple)
    async def mate_button_callback(self, interaction: Interaction, button: Button):
        pass

    @button(label="婚姻誓言", emoji="📜", custom_id="spouse_confession", disabled=True, style=ButtonStyle.red)
    async def spouse_button_callback(self, interaction: Interaction, button: Button):
        pass



### 交友是否同意

class make_friendship(V):
    def __init__(self, author: User, to: User):
        self.author = author
        self.to = to
        super().__init__(timeout=0)

    @button(label="同意", emoji=f"{PENCIL}", custom_id="accept_friend", style=ButtonStyle.green)
    async def accept_friend_callback(self, interaction: Interaction, button: Button):
        if interaction.user.id == self.author.id:return await interaction.response.send_message(ephemeral=True, embed=embed(f"{BACK} | 強行交友不好喔！", "", RED))
        elif interaction.user.id == self.to.id:
            await interaction.response.edit_message(embed=embed(f"{GREEN_HEART} | {self.author.name} 與 {self.to.name} 成為了朋友", "", GREEN), view=None)
            return make_friend(self.author.id, self.to.id)
        else:raise define_inter_error("怎麼可以去干涉別人感情呢")

    @button(label="拒絕", emoji=f"{BACK}", custom_id="refuse", style=ButtonStyle.red)
    async def refuse_friend_callback(self, interaction: Interaction, buttin: Button):
        if interaction.user.id == self.author.id:return await interaction.response.send_message(ephemeral=True, embed=embed(f"{BACK} | 問心酸的？", "", RED))
        elif interaction.user.id == self.to.id:
            return await interaction.response.edit_message(embed=embed(f"{ERROR} | {self.to.name} 拒絕當 {self.author.name} 的朋友", "", Color.BLACK), view=None)
        else:raise define_inter_error("怎麼可以去干涉別人感情呢")





### 贈禮

class feed_friend(View):
    def __init__(self, author: User, to: User, level: int):
        super().__init__(timeout=0)
        self.author = author
        self.to = to
        if level == 0:
            for i in [k for k in self.children if isinstance(k, Button) and k.custom_id in ['mate_interaction', 'spouse_interaction']]:i.disabled = True
        if level == 1:
            for i in [k for k in self.children if isinstance(k, Button) and k.custom_id in ['spouse_interaction']]:i.disabled = True
    def find_gift_select (self):
        return next(
            child for child in self.children
                if isinstance(child, Select) and child.custom_id == "gift_select"
        )
    @button(label="朋友交流", emoji=f"🎈", custom_id="friend_interaction", style=ButtonStyle.gray)
    async def friend_interaction_callback(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.author.id:return await interaction.response.send_message(ephemeral=True, embed=getembed(f"{BACK} | 還敢亂啊", "", RED))
        options = [SelectOption(emoji=f"{j[2]}", label=f"{j[0]}{j[3]}", value=f"{j[4]}",description=f"親密度 {j[5]}～{j[6]:+d}、價格 {j[7]} 元") for j in friend_options]
        select = self.find_gift_select()
        select.disabled = False
        select.options = options
        return await interaction.response.edit_message(embed=getembed(f"🎈 | 朋友交流 - {interaction.user.name}", "、".join([f"`{v[3]}`" for v in friend_options]), BLUE), view=self)

    @button(label="親密贈與", emoji=f"🎀", custom_id="mate_interaction", style=ButtonStyle.blurple)
    async def mate_interaction_callback(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message(ephemeral=True, embed=getembed(f"{BACK} | 還敢亂啊", "", RED))
        options = [SelectOption(emoji=f"{j[2]}", label=f"{j[0]}{j[3]}", value=f"{j[4]}",description=f"親密度 {j[5]}～{j[6]:+d}、價格 {j[7]} 元") for j in mate_options]
        select = self.find_gift_select()
        select.disabled = False
        select.options = options
        return await interaction.response.edit_message(embed=getembed(f"🎀 | 親密贈與 - {interaction.user.name}", "、".join([f"`{v[3]}`" for v in mate_options]), YELLOW), view=self)

    @button(label="愛的施捨", emoji=f"💍", custom_id="spouse_interaction", style=ButtonStyle.danger)
    async def spouse_interaction_callback(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.author.id:return await interaction.response.send_message(ephemeral=True, embed=getembed(f"{BACK} | 還敢亂啊", "", RED))
        options = [SelectOption(emoji=f"{j[2]}", label=f"{j[0]}{j[3]}", value=f"{j[4]}",description=f"親密度 {j[5]}～{j[6]:+d}、價格 {j[7]} 元") for j in marriage_options]
        select = self.find_gift_select()
        select.disabled = False
        select.options = options
        return await interaction.response.edit_message(embed=getembed(f"💍 | 愛的施捨 - {interaction.user.name}", "、".join([f"`{v[3]}`" for v in marriage_options]), RED), view=self)

    @select(placeholder="🍡請先選擇交流方式", custom_id="gift_select", disabled=True, options=[SelectOption(label="錯誤", value="0")])
    async def select_callback(self, interaction: Interaction, select: Select):
        #確認回覆者
        if interaction.user.id != self.author.id:return await interaction.response.send_message(ephemeral=True, embed=getembed(f"{BACK} | 還敢亂啊 (你不是指令發起者)", "", RED))
        v = select.values[0]

        #確認資料
        # [0類別名,1類別 SQL,2 emoji,3中文,4英文,5親密度下限,6親密度上限,7金錢花費,8間隔時間]

        if v in [u[4] for u in friend_options]:
            c = [i for i in friend_options if v in i[4]][0]
            color = GREEN
        elif v in [u[4] for u in mate_options]:
            c = [i for i in mate_options if v in i[4]][0]
            color = YELLOW
        elif v in [u[4] for u in marriage_options]:
            c = [i for i in marriage_options if v in i[4]][0]
            color = RED
        else:return await interaction.response.send_message("發生錯誤")

        #確認錢錢
        money = get_money_info(self.author.id)
        if money < c[7]:return await interaction.response.send_message(embed=getembed(f"{BACK} | 你似乎缺錢呢！", "但....親密度不一定只能用錢換喔！", RED))

        #冷卻設置與偵測

        if len(c)==9:
            limit.check_data(interaction.user.id)
            cool = limit.edit_data(interaction.user.id,c[1],c[8])
            # cool = True
            if isinstance(cool,str):
                return await interaction.response.send_message(
                    embed = getembed(f"{BACK} | 冷卻中",f"{c[0]} 剩餘冷卻時間：`{cool}`",RED
                ))

        #確認條件通過後

        ran_xp = randint(c[5], c[6])
        if ran_xp > 0:msg = choice(like_or_unlike.like(c[1]))
        else:msg = choice(like_or_unlike.unlike(c[1]))
        money_left = cost_money(self.author.id, c[7])
        xp = get_friend_exp(self.author.id,self.to.id)
        level = get_friend_level(self.author.id,self.to.id)


        #親密度是否達上限
        if xp + ran_xp > RELATION_LIMIT[level]:
            ran_xp = RELATION_LIMIT[level]-xp
            await interaction.channel.send(
                embed = getembed(
                    "⚠ | 親密度已達上限",
                    f"恭喜你們又更親密了！！\n可以使用 `{PRE}confession` 或 `{PRE}proposal` 來突破關係喔",
                    BLUE
                ))
        xp_left = edit_friend_exp(self.author.id, self.to.id, ran_xp)
        embed =getembed(
            f"{c[2]} | 來自 {self.author.name} 的 {c[3]}",
            f"{msg.format(self.to.name,c[3])}\n\n親密度：{ran_xp:+d} ( {xp_left} ) \n金錢剩餘：{money_left}元",color
        )
        file = friend_exp_img(xp,ran_xp,RELATION_LIMIT[level])
        embed.set_image(url='attachment://image.png')
        return await interaction.response.send_message(embed = embed,file=file)
