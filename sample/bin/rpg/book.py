from discord.ui import button,select,Button,Select,Modal,TextInput
from discord import ButtonStyle,Interaction,SelectOption,User,TextStyle,File
from sample.bin.message import V,define_inter_error,embed
from typing import List
from core import UP,DOWN,PENCIL,ONLINE,TRASHCAN,ADD_PAGE,ERROR,Color
from io import BytesIO
import pickle

class NotEditor(define_inter_error):
    """你不是編輯者"""
class OperateError(define_inter_error):
    """操作錯誤"""

FIRSTPAGE = (
    "║\n"
    "║\n"
    "║======**《{}》**======\n"
    "║\n"
    "║> {}\n"
    "║\n"
    "║    作者：{}\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
)
NORMAL = (
    "║=======================\n"
    "║未編輯內頁\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
    "║\n"
)



class Magic_Book:
    def __init__(self,id:str,title:str = "未命名標題",subtitle:str = "未命名副標題",author:str = "未命名作者") -> None:
        self.id = id
        self.inf = {
            "title":title,
            "subtitle":subtitle,
            "author":author
        }
        self.content:List[Pages] = [Pages(text=FIRSTPAGE.format(title,subtitle,author))]


class Pages:
    def __init__(self,text:str="未編輯頁面",image:BytesIO=None) -> None:
        self.text = text
        self.image = image
        self.image_type = None

    


def OpenPublicBook(id:str) -> Magic_Book:
    try:
        with open(f"docs/publicbook/{id}.book",'rb') as file:
            return pickle.load(file)
    except:return None
def SavePublicBook(book:Magic_Book,id:str):
    with open(f"docs/publicbook/{id}.book",'wb') as file:
        pickle.dump(book,file)
        file.close()


async def editBook(id:str,i:Interaction):
    book = OpenPublicBook(id)
    if book==None:book = Magic_Book(id)
    e = Magic_Book_Edit(book,i.user)
    await e.start(i)
    
async def readBook(id:str,i:Interaction):
    book = OpenPublicBook(id)
    if book==None:book = Magic_Book(id)
    e = Magic_Book_Read(book,i.user)
    await e.start(i)

class Magic_Book_Edit(V):
    def __init__(self, book:Magic_Book,editor:User,timeout: int = 0):
        super().__init__(timeout)
        self.book = book
        self.page = 0
        self.editor = editor

    async def start(self,i:Interaction):
        await i.response.send_message(
            embed=embed(
                description=self.book.content[self.page].text,
            ),view=self
        )


    async def update(self,i:Interaction):
        [i for i in self.children if isinstance(i,Button) and i.custom_id=="nowpage"][0].label = f"{self.page+1}/{len(self.book.content)}"
        p = self.book.content[self.page]
        if p.image != None:
            file = File(p.image,filename=f"image.{p.image_type}")
            await i.response.edit_message(
                embed=embed(
                    description=p.text,
                    image_type=p.image_type
                ),
                view=self,attachments=file
            )
        else:
            await i.response.edit_message(
                embed=embed(
                    description=p.text,
                    image_type=p.image_type
                ),
                view=self
            )
    
    async def topage(self,i:Interaction):
        if self.page==-1:self.page = len(self.book.content)-1
        elif self.page==len(self.book.content):self.page = 0
        await self.update(i)

    @button(emoji=UP,style=ButtonStyle.blurple,custom_id="lastpage",row=1)
    async def to_last_page(self,i:Interaction,b:Button):
        self.page-=1
        return await self.topage(i)
    
    @button(emoji=ADD_PAGE,style=ButtonStyle.blurple,custom_id="newpage",row=1)
    async def add_page(self,i:Interaction,b:Button):
        self.book.content.insert(self.page+1,Pages(text=NORMAL))
        self.page+=1
        return await self.topage(i)

    @button(label="1",style=ButtonStyle.gray,custom_id="nowpage",row=1,disabled=True)
    async def now_page(self,i:Interaction,b:Button):
        return await i.response.defer()
    
    @button(emoji=TRASHCAN,style=ButtonStyle.blurple,custom_id="deletepage",row=1)
    async def del_page(self,i:Interaction,b:Button):
        if len(self.book.content)<=1:
            raise OperateError("這已經是最後一頁了")
        self.book.content.pop(self.page)
        return await self.topage(i)

    @button(emoji=DOWN,style=ButtonStyle.blurple,custom_id="nextpage",row=1)
    async def next_page(self,i:Interaction,b:Button):
        self.page+=1
        return await self.topage(i)
    
    @select(placeholder="編輯",row=2,options=[
        SelectOption(label="文字",emoji=PENCIL,value="edit_context",description="編輯此頁面文字敘述"),
        SelectOption(label="小圖示",emoji=PENCIL,value="edit_Icon",description="新增或更改此頁面小圖片(右上角)"),
        SelectOption(label="大圖片",emoji=PENCIL,value="edit_picture",description="新增或更改此頁面大圖片(下方)"),
        SelectOption(label="取消",emoji=ERROR,value="nothing_happened",description="手殘按到，關閉選擇頁面"),
        SelectOption(emoji = "💾",label="完成",value="welldone",description="儲存並關閉書本編輯器")
    ])
    async def select_call(self,i:Interaction,s:Select):
        if self.editor!=i.user:raise NotEditor("你不是編輯者")
        v = s.values[0]
        if v == "edit_context":
            return await i.response.send_modal(Edit_Book_Modal(self,self.book))
        elif v in ["edit_picture","edit_Icon"]:
            raise OperateError("開發中")
        elif v=="nothing_happened":
            return await i.response.defer()
        elif v=="welldone":
            SavePublicBook(self.book,self.book.id)
            return await i.response.edit_message(embed=embed(f"{ONLINE} | 成功儲存書籍",f"書名：{self.book.id}.magicbook",Color.GREEN),view=None)

class Edit_Book_Modal(Modal):
    name = TextInput(label="編輯",style=TextStyle.paragraph,placeholder="空",max_length=1800,required=True)

    def __init__(self,v:Magic_Book_Edit,book:Magic_Book) -> None:
        self.name.default = book.content[v.page].text
        super().__init__(timeout=0,title=f"🖋編輯第 {v.page} 頁內文")
        self.book = book
        self.v = v
        
    async def on_submit(self, interaction: Interaction) -> None:
        self.book.content[self.v.page].text = self.name.value
        return await self.v.update(interaction)


class Magic_Book_Read(V):
    def __init__(self, book:Magic_Book,editor:User,timeout: int = 0):
        super().__init__(timeout)
        self.book = book
        self.page = 0
        self.editor = editor

    async def start(self,i:Interaction):
        await i.response.send_message(
            embed=embed(
                description=self.book.content[self.page].text,
            ),view=self
        )


    async def update(self,i:Interaction):
        [i for i in self.children if isinstance(i,Button) and i.custom_id=="nowpage"][0].label = f"{self.page+1}/{len(self.book.content)}"
        p = self.book.content[self.page]
        if p.image != None:
            file = File(p.image,filename=f"image.{p.image_type}")
            await i.response.edit_message(
                embed=embed(
                    description=p.text,
                    attachment_type=p.image_type
                ),
                view=self,attachments=file
            )
        else:
            await i.response.edit_message(
                embed=embed(
                    description=p.text,
                    attachment_type=p.image_type
                ),
                view=self
            )
    
    async def topage(self,i:Interaction):
        if self.page==-1:self.page = len(self.book.content)-1
        elif self.page==len(self.book.content):self.page = 0
        await self.update(i)

    @button(emoji=UP,style=ButtonStyle.blurple,custom_id="lastpage",row=1)
    async def to_last_page(self,i:Interaction,b:Button):
        self.page-=1
        return await self.topage(i)

    @button(label="1",style=ButtonStyle.gray,custom_id="nowpage",row=1,disabled=True)
    async def now_page(self,i:Interaction,b:Button):
        return await i.response.defer()

    @button(emoji=DOWN,style=ButtonStyle.blurple,custom_id="nextpage",row=1)
    async def next_page(self,i:Interaction,b:Button):
        self.page+=1
        return await self.topage(i)
    