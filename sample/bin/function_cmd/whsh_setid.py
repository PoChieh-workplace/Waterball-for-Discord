import asyncio
from sample.bin.function_cmd.whsh import whsh_check_setid
from sample.bin.message import embed
from sample.bin.sql import check_whsh_id
from core import BACK, BLUE_STAR, CYAN_HEART, WHITE_STAR, WHSH_ICON,Color
from discord import Embed, Interaction,Message



async def set_whsh_id(i:Interaction,name:str,classroom:int,school_id:str):
    a = check_whsh_id(i.user,school_id)
    if isinstance(a,Embed):
        return await i.response.send_message(ephemeral=True,embed = a)
    bot = i.client
    user = i.user
    await i.response.send_message(embed = embed(f"{WHITE_STAR} | 步驟尚未完成","請檢視私人訊息！",Color.PURPLE),ephemeral=True)
    msg = await i.user.send(embed= embed(
        f"{WHITE_STAR} | 身分檢驗",
        f"為了確定你為當事人，請在這邊傳送一張可證明為 {WHSH_ICON}文華學生之圖片\n，需帶有文華學號(可為校服之學號、學生證等)，若有疑慮，其餘個資可先行裁切掉，等待管理員幫你審理，本照片不會儲存，審理完後將會自動刪除\n\n"
        f"{WHITE_STAR}注意！使用此功能代表你同意 [📜隱私權政策](http://waterball.ddns.net:6001/privacy.html)",
        Color.PURPLE
    ))
    photo=None
    while photo==None:
        try:u :Message = await bot.wait_for('message',check=lambda a:a.author==user and len(a.attachments)!=0,timeout=300)
        except asyncio.TimeoutError:return await msg.edit(embed= embed())
        if u.attachments[0].content_type.startswith('image'):
            photo = u.attachments[0].url
            msg = await u.channel.send(embed = embed(f"{CYAN_HEART} | 成功傳送圖片","狀態：`審核中`",Color.ORANGE))
        else:await u.channel.send(embed = embed(f"{BACK} | 這格式不正確(非圖片檔)","",Color.RED))
    channel = bot.get_channel(978125238363619388)
    embeds=embed(f"{WHSH_ICON} 學號綁定審核",f"{user.name} 想進行學號綁定，\n{BLUE_STAR}姓名：{name},班級座號：{classroom}\n{WHITE_STAR}學號：{school_id}",Color.PURPLE)
    embeds.set_image(url=photo)
    await channel.send(
        embed=embeds,
        view = whsh_check_setid(
            msg,i.user,
            name,
            classroom,
            school_id
        )
    )
