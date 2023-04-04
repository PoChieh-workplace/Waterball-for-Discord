from bin.embed import getembed
from bin.json import lan_data
from config.emoji import PENCIL,BACK
from config.zh_tw import CONCIAL, PRE
from discord import Interaction, TextStyle,ButtonStyle,Message
from discord.ext.commands import Context,CommandError
from discord.ui import Modal,TextInput,View,Button,button
import json
import googletrans
from googletrans.models import Translated
import translate

from config.color import BLUE, LIGHT_BLUE, RED



# Basic Translate

cut = ['，','。',' ']

trans = lan_data()
    
class LangError(CommandError):
    """123"""

def translat(txt:str,s,dest):
    k = []
    while len(txt) > 200:
        n = -1
        for i in cut:
            if txt[:200].rfind(i)> n:n=txt[:200].rfind(i)+1
        if n == -1:n=200
        k.append(txt[:n])
        txt = txt[n:]
    k.append(txt)

    t = googletrans.Translator()
    try:
        if s==None:
            req = t.translate(k,dest=dest)
        elif s in trans and dest in trans:
            req = t.translate(k,dest=dest,src=s)
    except:
        raise LangError("翻譯時發生錯誤，嘗試換個語句吧！")
    return (k,[u.text for u in req if isinstance(u,Translated)])
    

class trans_gui:
    def __init__(self,fro:str,to:str,msg:Message,req) -> None:
        self.fro = fro
        self.to = to
        self.pg = 1
        self.inf = req
        self.msg = msg
        if self.fro ==None:self.fro="自動偵測"
        else:self.fro = trans[self.fro]
    def edit_page(self,i:int):
        if self.pg+i<=0:self.pg=len(self.inf[0])
        elif self.pg+i>len(self.inf[0]):self.pg=1
        else:self.pg = self.pg+i
    @property
    def embed(self):
        return getembed(
            "📖｜翻譯",
            f"翻譯系統：google  ｜  頁數：{self.pg}/{len(self.inf[0])}\n\n"
            f"從 `{self.fro}` 語言：\n"
            f"```{self.inf[0][self.pg-1]}```\n"
            f"翻譯成 `{trans[self.to]}` 語言：\n"
            f"```{self.inf[1][self.pg-1]}```",
            BLUE
        )


class check_if_tran(View):
    def __init__(self,lan_from,lan_to):
        super().__init__(timeout=600)
        self.fro = lan_from
        self.to = lan_to

    def setembed(self,a:trans_gui):
        self.embed = a
        for u in self.children:
            if isinstance(u,Button):u.disabled = False
        [u for u in self.children if isinstance(u,Button) and u.custom_id=="cancel"][0].disabled = True


    @button(label="",emoji = '◀',style=ButtonStyle.blurple,custom_id="last",disabled=True)
    async def last_page(self,interaction:Interaction,button:Button):
        self.embed.edit_page(-1)
        return await interaction.response.edit_message(embed = self.embed.embed)

    @button(label="",emoji = PENCIL,style=ButtonStyle.green,custom_id="check")
    async def check_trans(self,interaction:Interaction,button:Button):
        return await interaction.response.send_modal(getTxt(self))
        
    @button(label="",emoji = BACK,style=ButtonStyle.danger,custom_id="cancel")
    async def cancel(self,interaction:Interaction,button:Button):
        return await interaction.response.edit_message(embed = CONCIAL,view = None)
    
    @button(label="",emoji = '▶',style=ButtonStyle.blurple,custom_id="next",disabled=True)
    async def next_page(self,interaction:Interaction,button:Button):
        self.embed.edit_page(1)
        return await interaction.response.edit_message(embed = self.embed.embed)



class getTxt(Modal,title = '翻譯'):

    def __init__(self,view:check_if_tran) -> None:
        super().__init__(timeout=300)
        self.view = view

    txt = TextInput(label="請填入想要翻譯文字",style=TextStyle.paragraph,max_length=2000,required=True)

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.edit_message(embed = getembed("🎈系統運作中","系統正在翻譯，請稍後",LIGHT_BLUE))

        try:t = translat(txt=self.txt.value,s=self.view.fro,dest=self.view.to)
        except:interaction.response.send_message(embed = getembed(f"{BACK}｜錯誤 Bug","你抓蟲蟲了，翻譯時發生錯誤，嘗試換個語句吧！"))

        if isinstance(t,LangError):raise t
        else:
            a = trans_gui(fro=self.view.fro,to=self.view.to,req=t,msg = interaction.message)
            self.view.setembed(a)
            return await interaction.message.edit(embed = a.embed,view = self.view)

async def dc_translate(ctx:Context,fro,to):
    if (fro in trans or fro==None) and to in trans:
        return await ctx.send(embed = getembed('📖｜翻譯功能',f"{ctx.author.mention}，請填入要翻譯的文字",BLUE),view = check_if_tran(fro,to))
    else:return await ctx.send(embed = getembed(f"{BACK}｜語言代碼錯誤",f"{ctx.author.mention},\n選取語言時發生錯誤，語言列表似乎沒有 `{fro}` 或 `{to}`,可使用 `{PRE}help {ctx.command.name}` 確認語言列表",RED))

