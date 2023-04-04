from discord import Embed
from core import Color,OFFLINE,ONLINE
from sample.bin.message.times import timemethod
#discord 嵌入式訊息腳本

class embed(Embed):
    def __init__(self,title = None,description = None,color = Color.BLACK,image_type:str = None,thumbnail_type:str = None):
        super().__init__(color=color, title=title, description=description)
        self.set_footer(text="Code by WB")
        if image_type!=None:self.set_image(url=f'attachment://image.{image_type}')
        if thumbnail_type!=None:self.set_thumbnail(url=f'attachment://thumbnail.{thumbnail_type}')
    
    def delafter(self,d=0,h=0,min=0,s=0):
        self.description+=f"\n\n將於 <t:{timemethod.after(d=d,h=h,min=min,s=s)}:R> 關閉本訊息"
        return self
    def disable(self,d=0,h=0,min=0,s=0):
        self.description+=f"\n\n將於 <t:{timemethod.after(d=d,h=h,min=min,s=s)}:R> 失效"
        return self
        
    @classmethod
    def cancel(cls,mention:str = ""):
        return cls(f"{OFFLINE} | 操作取消",f"{mention} 取消了操作",Color.BLACK).delafter(s=5)
    
    @classmethod
    def load(cls,mention:str = ""):
        return cls(f"{ONLINE} | 初始化系統","",Color.BLACK)
    