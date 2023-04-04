
from core.color import Color
from core.emoji import *

"""機器人Token"""
TOKEN="Token"


"""指令用prefix"""
PRE = '*'

"""時區"""

TIME_ZONE = 'Asia/Taipei'

"""機器人上線狀態"""
BOT_ONLINE_INF="WaterBall 上線"
BOT_ONLINE_SET=f"文華工具人 | {PRE}help"



"""顏文字與顏色設定"""

#請前往 color.py 修改


"""指令系統"""
#勿動
ADD_LIST = ["add","set","connect"]
DELETE_LIST = ["delete","remove","disconnect"]





"""Help 指令"""
class Helpcommand:
    TITLE = ":book: 指 令 使 用 說 明"
    DESCRIPTION = "\n".join([
        "{} 感 謝 使 用 全 中 文 Uto 2.0 機器人，",
        "如果有指令上的使用問題 ❓",
        "**歡迎查看以下文件**",
        "[📜說明文件](http://waterball.ddns.net:6001/)",
        "[⭐更新頻道](https://discord.gg/whsh)",
        "[📎作者github](https://github.com/PoChieh-workplace/)"
    ])
    color = Color.RED
HELPFOOTER = "Discord bot name : Uto , Code by：Po-Chieh"
HELP_COMMAND_TITLE="{} 指令說明"




"""伺服器指令 joinconnect leaveconnect"""

JOIN_CONNECT="✅| 已連接 歡迎訊息 至 {}"
LEAVE_CONNECT="✅| 已連接 離開訊息 至 {}"
GUILD_DESCRPTION = "\n".join([
    "**伺服器基本資訊：**\n",
    "👉🏻伺服器id：{}，",
    "👉🏻人數🙋🏻‍♀️🙋🏻‍♂️：{}人(上限{}人)\n",
    "**其他：**\n",
    "👉🏻伺服器語言💬：{}",
    "👉🏻伺服器加成等級⚜：{}\n"
])



"""音樂機器人"""
MUSIC_SONG_ADD_ERROR = (
    '❌| 載入您的歌曲時出錯。\n'
    '```錯誤代碼：\n[{}]\n```'
)

MUSIC_NOW_PLAYING_TITLE = "🎶 | 正在播放"
MUSIC_NOW_PLAYING_DESCRIPTION = "[{}]({}) \n由 {} 點播"
MUSIC_NOW_PLAYING_COLOR = Color.GREEN
MUSIC_NOPRIVATE_ERROR = "❌| 本命令不能用於私聊"
MUSIC_ADD_LIST = "🎶 | 成功加入清單 [{}]({}) \n由 {} 點播"
MUSIC_MEMBER_NOT_JOIN = "❌| 你沒有加入語音頻道"
MUSIC_MEMBER_HAVENT_JOIN = "❌| 無法進入語音頻道，請確認您在一個語音頻道"
MUSIC_MOVE_CHANNEL_TICK = "❌| 移動至 <{}> 頻道時超時"
MUSIC_ADD_CHANNEL_TICK = "❌| 連接至 <{}> 頻道時超時"
MUSIC_JOIN_REACTION = "🎶"
MUSIC_JOIN_SUCCESS = "**🎶| 成功加入 `{}` 頻道**"
MUSIC_NO_PLAYING = "❌| 沒有音樂在播放"
MUSIC_PAUSE = "已暫停 ⏸️"
MUSIC_SKIP = "🤟🏻 | 跳過音樂"
MUSIC_BOT_NOT_JOINED = "❌| 我不在一個語音頻道"
MUSIC_REMOVED = "⏏️ | 從清單中移除： [{}]({}) \n由 {} 請求"
MUSIC_SONG_NOT_FOUND = "❌ | 無法找到音樂編號 **{}**"
MUSIC_QUERE_CLEAN = "🎶 | **清除清單**"
MUSIC_QUERE_EMPTY = "❓ | 清單是空的"
MUSIC_QUERE_TITLE = "在 {} 中的音樂清單"
MUSIC_NOW_IS_PLAYING = "[{}]({}) {}點的歌\n時長：`{}`"
MUSIC_NOW_PLAYING_CONFIG = "正在撥放 🎶"
MUSIC_VOLUME = "🔊 | 目前音量 **{}%**"
MUSIC_VOL_VOL_ERROR = "❌ | 請輸入範圍為 1 至 100 的值"
MUSIC_VOLUME_CHANGE = "**`{}`** 將音量更改為 **{}%**"
MUSIC_DISCONNECT_EMOJI = "👋🏻"
MUSIC_DISCONNECT = "**{}慢走不送下次再連絡**"
MUSIC_RESTARTING = "**重啟中ψ(｀∇´)ψ，小小惡魔即將復甦**"
MUSIC_RESTART_SUCCESS = "**成功回到 `{}` 頻道**"


"""數學"""
MATH_ERROR = "❌ | 計算錯誤"
ARC_LOCATE_ERROR = "`❌ | 括弧放置錯誤`"
MAX_ERROR = "`❌ | 極端值(錯誤)`"
FAKE_NUMBER_ERROR = "`❌|無法計算虛數`"
MATH_INFO_ERROR = "`❌ | 對數給予資料錯誤`"






"""貼文"""
WHSHEMBED_TITLE = "{}"
WHSHEMBED_DESCRIPTION = "\n".join([
    "{} \n",
    "發布時間：{}"
])
WHSHEMBED_COLOR = Color.LIGHT_ORANGE

WHSHANNOUNCE_TITLE = "📜文華日報 Daily NEWS - {} Beta"
WHSHANNOUNCE_DESCRIPTION = "\n **{}**\n[🔍前往公告連結]({})  發布日期：{} \n"
WHSHANNOUNCE_END = "\n\n[💒前往校網](https://whsh.tc.edu.tw/) **此版面為 Beta 版**"
WHSHANNOUNCE_COLOR = Color.PURPLE_LIGHT

WHSH_POST_GET_ERROR = "❌ | 找不到 {}，請見 {}help fbpost"
POST_CONNECT_KEY_ERROR = "❌ | 找不到 {}，請見 {}help post"
POST_CONNECT_SUCCESS = "\n".join([
    "✅ | 成功訂閱 `{}` 到 `{}` 頻道，",
    "如果想要取消訂閱， 請使用 {}{} delete {}"
])
POST_DISCONNECT_SUCCESS = "✅ | 成功取消訂閱 `{}` 頻道的 `{}`"
POST_HAVE_CONNECT = "❌ | 你已經在訂閱 `{}` 了"
POST_REMOVE_KEY_ERROR = "❌ | 你沒有在 `{}` 頻道中訂閱 `{}` o(TヘTo)"


"""權限設置"""
NO_PERMISSION = "❌ | 你沒有權限使用此指令"
PERMISSION_DEVOLOPER_ERROR = "❌ | devoloper 只能手動更改"
PERMISSION_LOWER = "❌ | 無法設定比你更高的權限"
PERMISSION_HAVE_HIGHER = "❌ | `{}` 已經有比 `{}` 更高的權限了"
PERMISSION_HAVED = "❌ | `{}` 已經擁有 `{}` 權限了"
PERMISSION_KEY_ERROR = "❌ | 錯誤的參數設置，請見 `{}help permission`"
PERMISSION_EDIT_SUCCESS = "✅ | 成功{} `{}` 的 `{}` 權限"
PERMISSION_GET = "🔎 | 查詢到 `{}` 權限為 `{}`"


"""匿名"""
NICKNAME_SET_SUCCESS = "✅ | 成功將你的匿稱設為 **{}**"
NICK_SEND_SUCCESS_REACTION = "💬"
NICK_CHANNEL_HAD_SET = "❌ | 此頻道已設置為匿名頻道"
NICK_CHANNEL_SET_SUCCESS = "✅ | 成功設置 **{}** 為公共匿名頻道"
NICK_CHANNEL_HADDNT_SET = "❌ | 此頻道不是匿名頻道"
NICK_CHANNEL_DELETE_SUCCESS = "✅ | 成功移除 **{}** 的匿名功能"



"""錯誤"""
ERROR_KEY_NOT_FOUND = "❌|指令所輸入資料並不完全，可輸入 {}help 了解更多"
ERROR_CHANNEL_LIMIT = "❌|本頻道無法使用此指令"
ERROR_TIME_TICK = "❌|指令時間限制，請稍後再試"


"""倒數頻道系統"""
DATE_KEY_ERROR = "❌ | 錯誤的參數設置，請見 `{}help datechannel`"
DATE_CHANNEL_EDIT_SUCCESS = "✅ | 成功設置 **{}** 為倒數日頻道"
DATE_CHANNEL_NOT_FOUND = "❌ | 此頻道沒有設置倒數系統"
DATE_CHANNEL_DELETE_SUCCESS = "✅ | 已取消設置 **{}** 的倒數系統"


"""抽籤系統"""
DICE_NUMBER_KEY_ERROR = "❌ | 錯誤的參數設置，請見 `{}help number`"
DICE_NUMBER_MAX_ERROR = "❌ | 最大值不可小於 {}"
DICE_COUUNT_ERROR = "❌ | 骰子數量不可大於最大值與最小值的間隔"

class DICE_NUMBER_SUCCESS:
    title = "🎲 | 擲骰成功"
    description = "`{}` "
    color = Color.BLUE_CYAN




WHSH_KB = [f"{KB_WHSH} 前往 靠北文華FB 連結","https://www.facebook.com/FOURKBWHSH"]
WHSH_LOVE = [f"{LOVE_WHSH} 前往 暈船文華FB 連結","https://www.facebook.com/107210948520480/"]
WHSH_CLASS_LINK = [f"{ROLE_BOOK} 前往查詢文華課表","https://class.whsh.tc.edu.tw/110-2/classTable.asp"]
WHSH_INVITED = [f"{LINK} 顯示文華 Discord 連結","https://discord.gg/whsh"]
CDC_WEB = [f"🌱 前往衛福部","https://www.cdc.gov.tw/"]




"""遊戲"""
WAIT_FOR_PLAYER_TITLE = "{} 發起了遊戲"


