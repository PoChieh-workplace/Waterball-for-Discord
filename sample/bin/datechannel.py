from datetime import date, timedelta, datetime
from discord.ui import Button,Modal,TextInput,button,Select
from discord import ButtonStyle,Interaction,TextStyle,SelectOption,User
from sample.Slash_permission import classic_error
from sample.bin.message import embed,V,define_inter_error
from sample.bin.sql import datechannelSQL
from core import Color,BACK, LIGHT_BLUE_CHECK, PENCIL, ERROR, ONLINE

class Value_Error(classic_error):
    """YEE"""

class V_Error(define_inter_error):
    """操作介面發生未知問題"""



class datechannel(V):

# dates = None content = None
    def __init__(self,user:User,channel_id:int,dates:tuple=None,content:str=None):
        super().__init__(timeout=0)
        self.add_item(c_select(self))
        self.channel = channel_id
        self.mode = [('狀態：關閉',ButtonStyle.danger,'close',ERROR),('狀態：啟動',ButtonStyle.green,'open',ONLINE)]
        self.user = user

        data = datechannelSQL().get_from_channelID(channel_id) # (id,date,context)

        self.date = date.today()
        self.context = "範例：脫單倒數{}天"

        if data!=None:
            self.date = data[1]
            self.context = data[2]
            self.mode.append(self.mode.pop(0))
        elif content!=None:
            try:self.date = date(dates[0],dates[1],dates[2])
            except ValueError:raise Value_Error("似乎沒有這個日期")
            self.context = content
            
        if dates!=None:
            try:self.date = date(dates[0],dates[1],dates[2])
            except ValueError:raise Value_Error("似乎沒有這個日期")

        self.retype()

    def retype(self):
        c = [i for i in self.children if isinstance(i,Button)]
        c[0].label = self.mode[0][0]
        c[0].style = self.mode[0][1]
        c[0].custom_id = self.mode[0][2]
        c[0].emoji = self.mode[0][3]

    def embed(self):
        time:timedelta = self.date-date.today()
        t = self.context.format(time.days)
        return embed(
            '🎨 設定頻道倒數介面',
            f'預覽：\n> {t}\n\n倒數至 `{self.date}`',
            Color.WHITE
        )
    
    async def update(self,interaction:Interaction):
        self.retype()
        return await interaction.response.edit_message(embed=self.embed(),view=self)

    
    @button(label='狀態：關閉',emoji=ERROR,style=ButtonStyle.danger,row=0,custom_id='close')
    async def tcallback(self, interaction: Interaction,button:Button):
        self.mode.append(self.mode.pop(0))
        return await self.update(interaction)

    @button(label='關閉提醒',row=0,emoji=ERROR,disabled=True,style=ButtonStyle.danger)
    async def remindcallback(self,interaction:Interaction,button:Button):
        pass


    @button(label='單次',row=0,emoji='1️⃣',disabled=True)
    async def tycallback(self,interaction:Interaction,button:Button):
        pass


class edit_date_model(Modal):

        def __init__(self,c:datechannel) -> None:
            ids = c.date
            self.c = c
            super().__init__(title='📆 設定倒數日期', timeout=0)
            self.add_item(TextInput(label='年份',default=f'{ids.strftime("%Y")}',style=TextStyle.short,placeholder='請輸入年份'))
            self.add_item(TextInput(label='月份',default=f'{ids.strftime("%m")}',style=TextStyle.short,placeholder='請輸入月份'))
            self.add_item(TextInput(label='日期',default=f'{ids.strftime("%d")}',style=TextStyle.short,placeholder='請輸入日子'))

        async def on_submit(self, interaction: Interaction) -> None:

            if interaction.user.id != self.c.user.id:return await interaction.response.send_message(ephemeral=True,embed=embed(f"{BACK} | ㄟ！妳無法干預別人操作！","",Color.RED))

            try:v = [int(i.value) for i in self.children if isinstance(i,TextInput)]
            except:return await interaction.response.send_message(ephemeral=True,embed=embed(f"{BACK} | 喂！你所輸入的資料似乎不是數字","",Color.RED))
            try:self.c.date=date(v[0],v[1],v[2])
            except ValueError:return await interaction.response.send_message(ephemeral=True,embed=embed(f"{BACK} | 挖！你所輸入的日期似乎不存在","",Color.RED))
            except:
                return await interaction.response.send_message(
                    ephemeral=True,
                    embed=embed(
                        f"{BACK} | Sorrrry！系統似乎發生了問題....，如果重複發生請告知開發者","",Color.RED
                    )
                )
            return await self.c.update(interaction)


class edit_title_model(Modal):

        def __init__(self,c:datechannel) -> None:
            super().__init__(title='🍡編輯頻道名稱', timeout=0)
            self.add_item(
                TextInput(
                    label='名稱',
                    default=c.context,
                    style=TextStyle.short,
                    placeholder='請輸入名稱，使用{}插入倒數日期數字'
                )
            )
            self.c = c

        async def on_submit(self, interaction: Interaction) -> None:

            if interaction.user.id != self.c.user.id:return await interaction.response.send_message(ephemeral=True,embed=embed(f"{BACK} | ㄟ！妳無法干預別人操作！","",Color.RED))

            a = [i.value for i in self.children if isinstance(i,TextInput)][0]
            if '{}' in a:
                self.c.context = a
                return await self.c.update(interaction)
            return await interaction.response.send_message(ephemeral=True,embed=embed(f"{BACK} | YEE！你所輸入的資料似乎沒有加入 {'{}'} 呢！","加入 {} 以嵌入倒數數字",Color.RED))

class c_select(Select):

        def __init__(self,c:datechannel) -> None:
            super().__init__(
                custom_id='select', placeholder='🎀 編輯',
                options = [
                SelectOption(label='名稱',value='name',description='編輯想要顯示的頻道名稱',emoji=PENCIL),
                SelectOption(label='日期',value='date',description='設定倒數日期',emoji='📆'),
                SelectOption(label='儲存',value='done',description='完成所有設定並儲存',emoji=LIGHT_BLUE_CHECK),
                SelectOption(label='取消',value='cancel',description='取消操作並關閉編輯器',emoji=BACK)
                ], row=1)
            self.c = c
        
        async def callback(self, interaction: Interaction):

            if interaction.user.id != self.c.user.id:return await interaction.response.send_message(ephemeral=True,embed=embed(f"{BACK} | ㄟ！你無法干預別人操作！","",Color.RED))

            s = self.values[0]
            if s=='name':return await interaction.response.send_modal(edit_title_model(self.c))
            elif s=='date':return await interaction.response.send_modal(edit_date_model(self.c))
            elif s=='done':
                if [i for i in self.c.children if isinstance(i,Button)][0].custom_id=='close':
                    datechannelSQL().remove(self.c.channel)
                    return await interaction.response.edit_message(embed = embed("",f"{interaction.user.mention} 於 <t:{int(datetime.now().timestamp())}:R> 關閉了頻道倒數器",Color.BLACK),view=None)
            
                else:
                    datechannelSQL().insert(self.c.channel,self.c.date,self.c.context)
                    time = self.c.date-date.today()
                    text = self.c.context.format(time.days)
                    await interaction.client.get_channel(self.c.channel).edit(name=text)
                    return await interaction.response.edit_message(
                        embed = embed(
                            "",
                            f"{interaction.user.mention} 於 <t:{int(datetime.now().timestamp())}:R> 開啟了頻道倒數器，並設定名稱為 {text}",
                            Color.WHITE),
                            view=None
                        )
            
            elif s=='cancel':
                self.c.stop()
                await interaction.response.defer()
                return await interaction.message.edit(embed = embed.cancel(interaction.user.mention),view=None,delete_after=5)
            else:raise V_Error(f"{BACK} | Sorrrry！系統似乎發生了問題....，如果重複發生請告知開發者")
