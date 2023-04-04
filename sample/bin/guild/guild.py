
from core import PEOPLE ,LEVEL, DISCORD, GREEN_CHECK, IMAGE,Color
from discord.ui import Button
from discord import Guild,ButtonStyle,Interaction
from sample.bin.message import embed,IC,V

class invite_button(Button):
    def __init__(self,guild:Guild):
        super().__init__(
            style=ButtonStyle.blurple,
            label = "邀請連結",
            emoji = PEOPLE)
        self.g = guild
    async def callback(self, interaction: Interaction):
        return await interaction.response.send_message(embed=embed(f"{PEOPLE} | {self.g.name}",f"連結：{self.g.vanity_url}",Color.KHAKI),ephemeral=True)


class guild_view(V):
    def __init__(self,guild:Guild, timeout: int = 0):
        super().__init__(timeout)
        self.add_item(Button(emoji=IMAGE,label="頭像",url=guild.icon.url))
        if guild.banner!=None:
            self.add_item(Button(emoji=IMAGE,label="旗幟",url=guild.banner.url))
        if "VANITY_URL" in guild.features:
            self.add_item(invite_button(guild))


    async def nothing_1(self,i,b):
        pass
    


async def search_guild_inf(ctx:IC):
    g = ctx.ic.guild
    fields = [
        [
            f" {DISCORD} 稱號",
            f"名稱：{g.name}"
            f"\nID：\n`{g.id}`"
            f"\n創建時間：\n <t:{int(g.created_at.timestamp())}:D>"
        ],[
            f" {LEVEL} 等級",
            f"加成等級：\n`{g.verification_level}`"
            f"\n加成數量：\n`{g.premium_subscription_count}`"
            f"\n上傳限制：\n{int(g.filesize_limit)/1048576} MB"
        ],[
            f" {PEOPLE} 人員",
            f"伺服人數：\n`{g.member_count}/{g.max_members}人`"
            f"\n擁有者：\n{g.owner.mention}"
        ],
    ]
    d = g.description
    if d==None:d = ""
    else:d = f"> {d}"
    embeds = embed(
        f"{GREEN_CHECK} | 查詢到本地資料",
        d,Color.BLUE_ULTRAMARINE,
    )
    for i in fields:embeds.add_field(name=i[0],value=i[1],inline = True)
    embeds.set_thumbnail(url=g.icon)
    if g.banner!=None:
        embeds.set_image(url=g.banner.url)

    return await ctx.send()(
        embed = embeds, view=guild_view(guild=g)
    )