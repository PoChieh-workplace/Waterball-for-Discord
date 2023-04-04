from sample.bin.message import embed,V,IC
from discord import ButtonStyle,Interaction,Member
from discord.ui import button,Button
from sample.bin.json import open_json_member_inf, write_json_member_inf
from core import BLUE_STAR, GREEN_CHECK, PINK_STAR, WHITE_STAR,PENCIL,Color
from sample.bin.function_cmd.function import edit_member_introduce_modal





class member_information_edit_view(V):
    def __init__(self):
        super().__init__(timeout=0)
    @button(emoji = f"{PENCIL}",label="編輯個人資料",style=ButtonStyle.blurple)
    async def button_callback(self,interaction:Interaction, button:Button):
        button.disabled = True
        await interaction.response.send_modal(edit_member_introduce_modal())


async def search_member_inf(i:IC,u:Member = None):
    g = i.ic.guild
    if u==None:u=i.user()

    role ="無"
    if len(u.roles)!=0:
        role_list = []
        for l in u.roles:role_list.append(l.mention)
        role = "、".join(role_list)

    data = open_json_member_inf()
    if not data.get("{}".format(u.id)):
        data["{}".format(u.id)] = {
            "mate":"單身",
            "birthday":"未填寫",
            "information":"未填寫"
        }
        write_json_member_inf(data)
    mate = data["{}".format(u.id)]["mate"]
    birthday = data["{}".format(u.id)]["birthday"]
    inf =  data["{}".format(u.id)]["information"]

    embeds = embed(
        f"{GREEN_CHECK} | 查詢到本地資料",
        "\n".join([
            f"{BLUE_STAR} **稱號**",
            f"\t   名稱：{u.name}",
            f"\t   ID：`{u.id}`",
            f"\t   加入{g.name}： <t:{int(u.joined_at.timestamp())}:D>",
            "",
            f"{WHITE_STAR} **身分**",
            f"\t   身分組：{role}",
            "",
            f"{PINK_STAR} **狀態**",
            f"\t   目前狀態：{u.web_status}"
        ]),
        Color.BLUE
    )
    embeds.set_thumbnail(url=f"{u.avatar}")
    if u == i.user: return await i.send()(embed = embeds,view = member_information_edit_view())
    else:return await i.send()(embed = embeds)