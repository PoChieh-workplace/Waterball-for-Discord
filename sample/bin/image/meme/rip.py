from discord import User,Member,File
from core import Union
from PIL import Image,ImageDraw
import io

async def make_rip_with_user(user:Union[User,Member]):
    v = user.avatar
    if isinstance(user,Member):
        if user.guild_avatar!=None:
            v = user.guild_avatar

    image_li = io.BytesIO()
    await v.save(fp=image_li)

    rip = Image.open("docs/image/meme/rip.png")
    u = Image.open(image_li).rotate(angle=350.0).resize(size = (125,125)).convert('1')

    #圓形切割
    e = Image.new("L", u.size, 0)
    draw = ImageDraw.Draw(e)
    draw.ellipse((5, 5, 120, 120), fill=255)


    rip.paste(u,(145,145),e)

    with io.BytesIO() as file:
        rip.save(file,format='png')
        file.seek(0)
        return File(fp=file,filename=f"RIP-{user.name}.png",description=f"{user.name} 被 RIP 了")