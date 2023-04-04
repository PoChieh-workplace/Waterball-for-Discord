from core import (
    PENCIL,BLUE_STAR,LINK,NSFT,DC_BOT,KB_WHSH,DOG,PINK_STAR,WHITE_STAR,
    LOVE_WHSH,ROLE_BOOK,GREEN_CHECK,ONE,TWO,THREE,BACK,Color
)
from discord import Interaction,SelectOption,ButtonStyle,Message,TextStyle
from discord.ui import Select,select,button,Button,Modal,TextInput
from datetime import datetime
from sample.bin.message import embed,V,define_inter_error,Unknow_Error,IC
from sample.bin.json import open_json_member_inf,write_json_member_inf
from sample.bin.function_cmd.whsh_setid import set_whsh_id


class bot_invite(Modal,title=f"申請加入機器人"):
    url = TextInput(label="🤖邀請連結",style=TextStyle.short,placeholder="https://discord.com",max_length=200,required=True)
    pro = TextInput(label="🍡目的 (可不填)",style=TextStyle.paragraph,placeholder="新增遊戲玩法、方便管理dc、增加管管人氣",max_length=200,required=False)
    async def on_submit(self, interaction: Interaction) -> None:
        channel = interaction.client.get_channel(964153866750926858)
        await channel.send(embed = embed(
            f"{DC_BOT} | 機器人申請",
            f"連結 : {self.url.value}\n"
            f"目的 : {self.pro.value}",
            Color.BLUE_LIGHT
        ))
        await interaction.response.send_message(embed=embed(
            f"{GREEN_CHECK} | 成功提交申請資料",
            f"請稍等管理員回應，我們有決定機器人權限之權利",
            Color.LIGHT_ORANGE
        ),ephemeral=True)

class whsh_admin_hire(Modal,title=f"申請加入管理員"):
    name = TextInput(label="🙋🏻‍♂️班級座號與姓名",style=TextStyle.short,placeholder="21214 王小明",max_length=20,required=True)
    pro = TextInput(label="🍡加入目的",style=TextStyle.paragraph,placeholder="幫忙管理discord訊息、開發或維護 disocrdbot、定期舉辦大型活動",max_length=200,required=True)
    dc = TextInput(label="💻自述對 discord 的熟悉程度",style=TextStyle.paragraph,placeholder="會編輯個身分組權限、了解discord所有規範",max_length=200,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        channel = interaction.client.get_channel(910385049273245777)
        await channel.send(embed = embed(
            f"{DOG} | 申請加入管理員",
            f"{WHITE_STAR} 班級姓名：`{self.name.value}`\n\n"
            f"{BLUE_STAR} 目的：\n{self.pro.value}\n\n"
            f"{PINK_STAR} 對 discord 的熟悉程度：\n{self.dc.value}",
            Color.BLUE_LIGHT
        ))
        await interaction.response.send_message(embed=embed(
            f"{GREEN_CHECK} | 成功提交申請資料",
            f"請稍等管理員回應，感謝參與文華discord內部運作",
            Color.LIGHT_ORANGE
        ),ephemeral=True)



class whsh_advice(Modal,title=f"意見回饋"):
    name = TextInput(label="🙋🏻‍♂️原名或暱稱",style=TextStyle.short,placeholder="老乾結水球",max_length=20,required=True)
    pro = TextInput(label="🍡回報內容",style=TextStyle.paragraph,placeholder="播放音樂發生錯誤、我想舉辦電競賽",max_length=1000,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        channel = interaction.client.get_channel(910385049273245777)
        await channel.send(
            embed = embed(
                f"📜 | 意見回饋",
                f"{WHITE_STAR} 原名或暱稱：`{self.name.value}`\n\n"
                f"{BLUE_STAR} 內容：\n{self.pro.value}",
                Color.BLUE_LIGHT
            )
        )
        await interaction.response.send_message(embed=embed(
            f"{GREEN_CHECK} | 成功提交意見回饋",
            f"請稍等管理員回應，感謝參與文華discord內部運作",
            Color.LIGHT_ORANGE
        ),ephemeral=True)



class whsh_setid(Modal,title=f"學號綁定"):
    name = TextInput(label="🙋🏻‍♂️姓名(真實姓名)",style=TextStyle.short,placeholder="王小明",max_length=20,required=True)
    classroom = TextInput(label="📚目前班級與座號",style=TextStyle.short,placeholder="21214",max_length=10,required=True)
    ids = TextInput(label="🍡學號",style=TextStyle.short,placeholder="911125",max_length=10,required=True)
    async def on_submit(self, interaction: Interaction) -> None:
        if self.classroom.value.isdigit() and self.ids.value.isdigit():return await set_whsh_id(interaction,self.name.value,int(self.classroom.value),self.ids.value)
        ### set_whsh_id -> bin.system.whsh_setid
        else:return await interaction.response.send_message(ephemeral=True,embed = embed(f"{BACK} | 格式錯誤","",Color.RED))

class edit_member_introduce_modal(Modal,title="🎀修改個人資料"):
    birthday = TextInput(label="🎂生日 Birthday",style=TextStyle.short,placeholder="2000/1/1",max_length=30,required=False)
    introduce = TextInput(label="🍡個人簡介",style=TextStyle.paragraph,placeholder="我只想說管理員很帥",max_length=200,required=False)
    async def on_submit(self, interaction: Interaction) -> None:
        data = open_json_member_inf()
        if data.get(interaction.user.id) == None:
            data["{}".format(interaction.user.id)] = {
                "mate":"單身",
                "birthday":"未填寫",
                "information":"未填寫"
            }
        if self.birthday.value != "":data["{}".format(interaction.user.id)]["birthday"] = self.birthday.value
        if self.introduce.value != "":data["{}".format(interaction.user.id)]["information"] = self.introduce.value
        write_json_member_inf(data)
        await interaction.response.send_message(embed=embed(
            f"{GREEN_CHECK} | 成功編輯資料",
            f"將於<t:{datetime.now()+10}:R>",
            Color.GREEN
        ),ephemeral=True,delete_after=10)


class url_V(V):
    def __init__(self, url:str,timeout: int = 0,):
        super().__init__(timeout)
        b:Button = self.children[0]
        b.url = url

    @button(style=ButtonStyle.url,label="前往訊息處",custom_id="link",row=0)
    async def link(self,interaction:Interaction,button:Button):
        await interaction.response.defer()


# 申請可以澀澀身分組


class part_color(V):
    def __init__(self):
        super().__init__(timeout=0)

    @button(emoji = f"{PENCIL}",label="確定申請",style=ButtonStyle.blurple)
    async def green_button_callback(self,i:Interaction, button:Button):

        button.disabled = True
        guild =  i.client.get_guild(910150769624358914)
        member = guild.get_member(i.user.id)

        r = guild.get_role(913649078582272030)
        await member.add_roles(r)
        await i.response.edit_message(embed = embed(f"{GREEN_CHECK} | 成功",f"你已取得 {r.name} 身分組",Color.BLUE),view = None)

    @button(emoji = BACK,label="取消",style=ButtonStyle.danger)
    async def button_callback(self,i:Interaction,button:Button):
        self.clear_items()
        await i.response.edit_message(embed = embed.cancel(),view = None)

async def partcolor_sys(i:Interaction):
    if i.guild_id == 910150769624358914:
        msg:Message = await i.user.send(embed = embed(
            f"{NSFT} 申請 可以澀澀 身分組",
            "\n".join([
                f"{ONE} 因本身分組涉及色情 🔞",
                f"不宜兒童與青少年使用"
                f"請確保你已經年滿 18 歲",
                f" ",
                f"{TWO} 因應 discord 最新條款，",
                f"請勿出現兒童色情，例如：`正太`、`羅莉`等，",
                f"禁止裸露部位包括：露點、陰道、雞雞...等性器",
                f"管你的 1~87 次元，本項目嚴格取締",
                f" ",
                f"{THREE} 違反以上規定，將以伺服規定懲處"
            ]),Color.PURPLE
        ),view = part_color())
        await i.response.send_message(embed = embed(f"{GREEN_CHECK}",f"已傳送一則訊息給您，請至私人聊天室查看",Color.PURPLE),view = url_V(msg.jump_url))
    else: raise define_inter_error(f"此功能需於 {i.client.get_guild(910150769624358914).name} 中進行")


#總系統

class whsh_selection(V):
    def __init__(self) -> None:
        super().__init__(timeout=0)
    @select(
        placeholder="✨請選擇功能",
        options=[
            SelectOption(label="DC - 編輯個人資料",             value = "edit_inf",         emoji=f"{PENCIL}",      description="編輯生日與簡介"),
            SelectOption(label="DC - 更換身分組",               value = "change_part",      emoji=f"{BLUE_STAR}",   description="更換在所在伺服器的標籤"),
            SelectOption(label="WHSH - 邀請連結",               value = "intive_url",       emoji=f"{LINK}",        description="顯示文華discord邀請連結"),
            SelectOption(label="WHSH - 申請 `可以澀澀`",        value = "part_color",       emoji=f"{NSFT}",        description="申請身分組"),
            SelectOption(label="WHSH - 機器人申請",             value = "whsh_bot",         emoji=f"{DC_BOT}",      description="機器人申請"),
            SelectOption(label="WHSH - 加入管管",               value = "whsh_admin",       emoji=f"{DOG}",         description="管理員徵選"),
            SelectOption(label="WHSH - 綁定學號",               value = "whsh_setID",       emoji=f"💳",            description="申請身分組"),
            SelectOption(label="WHSH - 文華 Discord 意見提供",  value = "whsh_advice",      emoji=f"📜",            description="意見回饋"),
            SelectOption(label="LINK - 靠北文華 FB 連結",       value = "whsh_fuck",        emoji=f"{KB_WHSH}"),
            SelectOption(label="LINK - 暈船文華 FB 連結",       value = "whsh_love",        emoji=f"{LOVE_WHSH}"),
            SelectOption(label="LINK - 文華課表查詢",           value = "whsh_class_web",   emoji=f"{ROLE_BOOK}"),
            SelectOption(label="LINK - 衛生福利部(cdc)",        value = "cdc_link",         emoji=f"🌱")
        ]
    )
    async def callback(self, i: Interaction,select:Select):

        v = select.values[0]

        if v == "edit_inf":await i.response.send_modal(edit_member_introduce_modal())
        elif v == "change_part":
            select.disabled = True
            k = part_chosen(self,i)
            self.add_item(k)
            if k.max_values==0:return await i.response.send_message(ephemeral=True,embed=embed("❓ | 本伺服器沒有設定本功能喔","",Color.RED))
            else:await i.response.edit_message(view=self,embed=embed(f"{PENCIL} | 請選擇下方身分組","",Color.PURPLE))
        elif v == "intive_url":await i.response.edit_message(embed = embed(f"{LINK} 顯示文華 Discord 連結","https://discord.gg/whsh"))
        elif v == "part_color":await partcolor_sys(i)
        elif v == "whsh_bot":await i.response.send_modal(bot_invite())
        elif v == "whsh_admin":await i.response.send_modal(whsh_admin_hire())
        elif v == "whsh_advice":await i.response.send_modal(whsh_advice())
        elif v == "whsh_setID":await i.response.send_modal(whsh_setid())
        elif v == "whsh_fuck":await i.response.edit_message(embed = embed(f"{KB_WHSH} 前往 靠北文華FB 連結","https://www.facebook.com/FOURKBWHSH"))
        elif v == "whsh_love":await i.response.edit_message(embed = embed(f"{LOVE_WHSH} 前往 暈船文華FB 連結","https://www.facebook.com/107210948520480/"))
        elif v == "whsh_class_web":await i.response.edit_message(embed = embed(f"{ROLE_BOOK} 前往查詢文華課表","https://class.whsh.tc.edu.tw/111-2/classTable.asp"))
        elif v == "cdc_link":await i.response.edit_message(embed = embed(f"🌱 前往衛福部","https://www.cdc.gov.tw/"))
        else:raise Unknow_Error("")
        return

    async def main(self,ic:IC):
        embeds = embed(
            f"{PINK_STAR} 歡迎使用 whsh 快捷鍵",
            "使用本服務即代表你同意了 [【📜隱私權條款】](http://waterball.ddns.net:6001/privacy.html)",
            Color.WHITE
        )
        if isinstance(ic.ic,Interaction):
            self.msg = await ic.send()(
            view = self,
            embed=embeds,
            ephemeral=True
        )
        else:self.msg = await ic.send()(
            view = self,
            embed=embeds
        )
    
    async def reset(self,i:Interaction):
        await i.response.edit_message(
            view = self,
            embed = embed(
                f"{PINK_STAR} 歡迎使用 whsh 快捷鍵",
                "使用本服務即代表你同意了 [【📜隱私權條款】](http://waterball.ddns.net:6001/privacy.html)",
                Color.WHITE
            )
        )



class part_chosen(Select):
    def __init__(self,op:whsh_selection,i:Interaction) -> None:
        self.op = op
        self.bot = i.client
        self.guild = i.guild
        self.user = i.user
        super().__init__(
            custom_id="part_chosen",
            placeholder="🙋🏻‍♂️請選擇適合的身分",
            min_values = 0,
            options = [
                SelectOption(label=f"{v.name}",value = f"{v.id}",default=f"{v.id in [i.id for i in self.user.roles]}")
                for v in i.guild.get_member(i.client.application_id).roles if v.permissions.administrator==False and v.is_assignable()
            ]
        )
        self.max_values = len(self.options)

    async def callback(self, interaction: Interaction) -> None:
        if interaction.user != self.user:
            raise define_inter_error("你不是指令觸發者，無法使用本操作")
        self.op.remove_item(self)
        
        for i in [k for k in self.op.children if isinstance(k,Select)]:
            i.disabled = False
        
        await self.op.reset(interaction)
        msg = await interaction.channel.send(content="身分組作業中請稍後")
        for k in [self.guild.get_role(int(u.value)) for u in self.options if int(u.value) in [r.id for r in self.user.roles] and not (u.value in self.values)]:await self.user.remove_roles(k)
        for i in self.values:
            if int(i) not in [k.id for k in self.user.roles]:
                await msg.edit(content=f"{PENCIL} | 正在處理身分組 {self.guild.get_role(int(i)).name}")
                await self.user.add_roles(self.guild.get_role(int(i)))
        await msg.edit(content=f"{GREEN_CHECK} | 身分組更新完畢",delete_after=5)



# class part(Select):
#     def __init__(self,i:Interaction) -> None:
#         self.bot = bot
#         self.guild = guild
#         self.user = guild.get_member(user.id)
#         super().__init__(
#             custom_id="part_chosen",
#             placeholder="🙋🏻‍♂️請選擇適合的身分",
#             min_values = 0,
#             options = [
#                 SelectOption(label=f"{v.name}",value = f"{v.id}",default=f"{v.id in [i.id for i in self.user.roles]}")
#                 for v in guild.get_member(bot.application_id).roles if v.permissions.administrator==False and v.is_assignable()
#             ] 
#         )
#         self.max_values = len(self.options)
#     async def callback(self, interaction: Interaction) -> None:
#         if interaction.user.id != self.user.id:return await interaction.response.send_message(ephemeral=True,embed = getembed(f"{BACK} | 你不是指令觸發者","",RED))
#         await interaction.response.edit_message(content="")
#         msg:Message = await interaction.channel.send(content="身分組作業中請稍後")
#         for k in [self.guild.get_role(int(u.value)) for u in self.options if int(u.value) in [r.id for r in self.user.roles] and not (u.value in self.values)]:await self.user.remove_roles(k)
#         for i in self.values:
#             if int(i) not in [k.id for k in self.user.roles]:
#                 await msg.edit(content=f"{PENCIL} | 正在處理 {} 的身分組 {self.guild.get_role(int(i)).name}")
#                 await self.user.add_roles(self.guild.get_role(int(i)))
#         await msg.edit(content=f"{GREEN_CHECK} | 身分組更新完畢",delete_after=5)




