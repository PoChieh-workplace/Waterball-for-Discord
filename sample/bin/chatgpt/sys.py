from .ai import ai_response
from sample.bin.message import V,embed,define_inter_error as d
from discord.ui import button,Button,Modal,TextInput
from discord import ButtonStyle,Interaction,TextStyle,Message
from core import Color,CHATGPT

LANGS = [
    ('zh_tw','繁體中文','聊天'),
    ('zh_cn','简体中文','聊天'),
    ('en','English','respone'),
    ('ja','日本語','答え')
]

# gpt按鈕
class chatgpt_view(V):
    def __init__(self, timeout: int = 0):
        super().__init__(timeout)
        self.langs = 0
        self.que = []
    
    async def start(self,i:Interaction,tops,lang):
        self.langs = lang
        self.user = i.user
        self.que.append(tops)
        await i.response.defer(thinking=True)
        return await i.followup.send(
            embed=embed(
                f"{CHATGPT} Chatgpt X Waterball",
                f"問：{tops}\n{CHATGPT}：\n```{ai_response(self.que,LANGS[self.langs][0])}```",
                Color.GREEN_DARK
            ),
            view = self
        )


    @button(label='聊天',style=ButtonStyle.green,emoji="💬",custom_id='chat')
    async def chat(self,i:Interaction,b:Button):
        if i.user!=self.user:
            raise d('只有發起這項指令的人可以使用')
        return await i.response.send_modal(
            chatgpt_respond_model(
                title = LANGS[self.langs][2],
                lang = LANGS[self.langs][0],
                msg = i.message,
                v = self
            )
        )

    @button(label='繁體中文',style =ButtonStyle.blurple,emoji="🔣")
    async def lang(self,i:Interaction,b:Button):
        if i.user!=self.user:
            raise d('只有發起這項指令的人可以使用')
        
        self.langs = self.langs + 1 if self.langs + 1<len(LANGS) else 0
        [i for i in self.children if isinstance(i,Button) and i.custom_id == 'chat'][0].label = LANGS[self.langs][2]
        b.label = LANGS[self.langs][1]
        return await i.response.edit_message(view=self)

# gpt詢問表單
class chatgpt_respond_model(Modal):
    def __init__(self,**k) -> None:
        super().__init__(
            title=k['title'],
            custom_id = k['lang']
        )
        self.msg:Message = k['msg']
        self.v:chatgpt_view = k['v']
    
    res = TextInput(label=".",max_length=2048,required=True,style=TextStyle.paragraph)

    async def on_submit(self, i: Interaction) -> None:
        t = "\n\n`提醒您！為了節省資源，Waterball只會紀錄過去 10 筆紀錄來回應您！！`" if len(self.v.que)>=10 else ""
        await i.response.send_message(f'思考中...{t}',ephemeral=True,delete_after=2)
        self.v.que.append(self.res.value)
        self.v.que = self.v.que[-10:]
        return await self.msg.edit(
            embed=embed(
                f"{CHATGPT} Chatgpt X Waterball",
                f"問：{self.res.value}\n{CHATGPT}：\n```{ai_response(self.v.que,self.custom_id)}```",
                Color.GREEN_DARK
            )
        )