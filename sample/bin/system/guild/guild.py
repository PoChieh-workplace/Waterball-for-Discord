
from bin.embed import getembed
from config.color import CYAN
from config.emoji import BLUE_STAR, GREEN_CHECK, PINK_STAR,WHITE_STAR


async def search_guild_inf(ctx):
    time = ctx.guild.created_at.strftime("%Y年%m月%d日 %H:%M:%S")
    embed = getembed(
        f"{GREEN_CHECK} | 查詢到本地資料",
        "\n".join([
            f"{BLUE_STAR} **稱號**",
            f"\t   名稱：{ctx.guild.name}",
            f"\t   ID：`{ctx.guild.id}`",
            f"\t   創建時間：{time}",
            "",
            f"{PINK_STAR} **等級**",
            f"\t   加成等級：{ctx.guild.verification_level}",
            f"\t   加成數量：{ctx.guild.premium_subscription_count}",
            f"\t   上傳限制：{int(ctx.guild.filesize_limit)/1048576} MB",
            "",
            f"{WHITE_STAR} **人員**",
            f"\t   伺服人數：{ctx.guild.member_count}/{ctx.guild.max_members}",
            f"\t   擁有者：{ctx.guild.owner.name}"
        ]),
        CYAN
    )
    embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_footer(text="Code by Po-Chieh")
    return await ctx.channel.send(
        embed = embed
    )