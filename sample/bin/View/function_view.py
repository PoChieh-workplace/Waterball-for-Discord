from bin.button import part_color
from bin.embed import getembed
from bin.modal.user import edit_member_introduce_modal
from bin.modal.whsh import bot_invite, whsh_admin_hire, whsh_advice, whsh_setid
from bin.select.part import part_chosen
from config.color import PURPLE, RED
from config.emoji import *
from discord import Interaction,SelectOption
from discord.ui import View,Select,select

from config.zh_tw import CDC_WEB, WHSH_CLASS_LINK, WHSH_INVITED, WHSH_KB, WHSH_LOVE, WHSH_PART_COLOR, WHSH_PART_EMBED, WHSH_PART_ERROR





class whsh_selection(View):
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
    async def callback(self, interaction: Interaction,select:Select):
        if select.values[0] == "edit_inf":await interaction.response.send_modal(edit_member_introduce_modal())
        elif select.values[0] == "change_part":
            select.disabled = True
            k= part_chosen(self,interaction.client,interaction.guild,interaction.user)
            k.msg = interaction.message
            self.add_item(k)
            if k.max_values==0:return await interaction.response.send_message(ephemeral=True,embed=getembed("❓ | 本伺服器沒有設定本功能喔","",RED))
            await interaction.response.edit_message(view=self,embed=getembed(f"{PENCIL} | 請選擇下方身分組","",PURPLE))
        elif select.values[0] == "intive_url":await interaction.response.edit_message(embed = WHSH_INVITED)
        elif select.values[0] == "part_color":
            if interaction.guild_id == 910150769624358914:
                await interaction.user.send(embed = WHSH_PART_EMBED,view = part_color())
                await interaction.response.edit_message(embed = WHSH_PART_COLOR)
            else: await interaction.response.edit_message(embed = getembed(WHSH_PART_ERROR.format(BACK,interaction.client.get_guild(910150769624358914).name),"",RED))
        elif select.values[0] == "whsh_bot":await interaction.response.send_modal(bot_invite())
        elif select.values[0] == "whsh_admin":await interaction.response.send_modal(whsh_admin_hire())
        elif select.values[0] == "whsh_advice":await interaction.response.send_modal(whsh_advice())
        elif select.values[0] == "whsh_setID":await interaction.response.send_modal(whsh_setid())
        elif select.values[0] == "whsh_fuck":await interaction.response.edit_message(embed = WHSH_KB)
        elif select.values[0] == "whsh_love":await interaction.response.edit_message(embed = WHSH_LOVE)
        elif select.values[0] == "whsh_class_web":await interaction.response.edit_message(embed = WHSH_CLASS_LINK)
        elif select.values[0] == "cdc_link":await interaction.response.edit_message(embed = CDC_WEB)
        else:await interaction.response.edit_message(embed = getembed(f"{BACK} | 似乎發生錯誤了？！","如果重複發生，請回報開發者",RED))
        return
