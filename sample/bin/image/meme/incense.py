from discord import User,Member,Attachment,File
from core import Union
from PIL import Image,ImageDraw
import io
from random import randint,choice

async def make_incense_with_user(user:Union[User,Member]) ->File :
    v = user.avatar
    if isinstance(user,Member):
        if user.guild_avatar!=None:
            v = user.guild_avatar

    image_li = io.BytesIO()
    await v.save(fp=image_li)

    incense = Image.open("docs/image/meme/incense.png")
    u = Image.open(image_li).resize(size = (550,550))
    
    #圓形切割
    e = Image.new("L", u.size, 0)
    draw = ImageDraw.Draw(e)
    draw.ellipse((5, 5, u.size[0]-5, u.size[1]-5), fill=255)



    incense.paste(u,(685,230),e)

    with io.BytesIO() as file:
        incense.save(file,format='png')
        file.seek(0)
        return File(fp=file,filename=f"incense-{user.name}.png",description=f"{user.name} 被上香了")


async def add_incense(file:Attachment):

    b = io.BytesIO() 
    await file.save(fp=b)
    incense = Image.open(b)

    t = (randint(-80,80),randint(-10,10))
    if t[0]<0:a = randint(0,10)
    else:a = randint(350,359)

    stick = Image.open("docs/image/meme/incense_stick.png").rotate(angle=a)
    incense.paste(stick,(900+t[0],750+t[1]),stick) #()
    with io.BytesIO() as files:
        incense.save(files,format='png')
        files.seek(0)
        return File(fp=files,filename=file.filename,description=file.description)