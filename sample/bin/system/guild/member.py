



from bin.button import member_information_edit_view
from bin.embed import getembed
from bin.json import open_json_member_inf, write_json_member_inf
from config.color import BLUE
from config.emoji import BLUE_STAR, GREEN_CHECK, PINK_STAR, WHITE_STAR


async def search_member_inf(ctx,arg,ids):
    if arg!=None:member = ctx.guild.get_member(arg.id)
    elif ids!=None:member = ctx.guild.get_member(ids)
    else:member = ctx.author

    if member.joined_at !=None:time = member.joined_at.strftime("%Y年%m月%d日 %H:%M:%S")
    role ="無"
    if len(member.roles)!=0:
        role_list = []
        for i in member.roles:role_list.append(i.mention)
        role = "、".join(role_list)
    data = open_json_member_inf()
    if not data.get("{}".format(member.id)):
        data["{}".format(member.id)] = {
            "mate":"單身",
            "birthday":"未填寫",
            "information":"未填寫"
        }
        write_json_member_inf(data)
    mate = data["{}".format(member.id)]["mate"]
    birthday = data["{}".format(member.id)]["birthday"]
    inf =  data["{}".format(member.id)]["information"]
    embed = getembed(
        f"{GREEN_CHECK} | 查詢到本地資料",
        "\n".join([
            f"{BLUE_STAR} **稱號**",
            f"\t   名稱：{member.name}",
            f"\t   ID：`{member.id}`",
            f"\t   加入{ctx.guild.name}：{time}",
            "",
            f"{WHITE_STAR} **身分**",
            f"\t   身分組：{role}",
            "",
            f"{PINK_STAR} **狀態**",
            f"\t   目前狀態：{member.web_status}",
            f"\t   配偶：`{mate}`  生日：`{birthday}`",
            f"\t   簡介：",
            f"\t   `{inf}`"
        ]),
        BLUE
    )
    embed.set_thumbnail(url=f"{member.avatar}")
    embed.set_footer(text="Code by Po-Chieh")
    if member == ctx.author: return await ctx.channel.send(embed = embed,view = member_information_edit_view())
    else:return await ctx.channel.send(embed = embed)