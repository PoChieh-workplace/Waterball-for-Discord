from sample.bin.image import make_rip_with_user
from sample.bin.message import IC

async def to_rip_user(i:IC,user):
    if user==None:user = i.user()
    file = await make_rip_with_user(user=user)
    return await i.send()(file=file)