from datetime import timedelta

from core import C_DUMPLINGS, FRENCH_FRIES, MONEY_PAPER
from discord import Embed, User
from discord.ext import commands

# 新增親密度

friend_options = [  # ["類別名","類別 SQL","emoji","中文","英文",親密度下限,親密度上限,金錢花費,間隔時間]
    ["飲料 - ", "drink", "🧃",                  "穀香紅茶",                 "black_tea",            -4, 4, 20,      timedelta(minutes=1)],
    ["飲料 - ", "drink", "🥤",                  "迷客冬黑糖鮮奶",           "brownsuger_milk",      -1, 8, 60,      timedelta(minutes=3)],
    ["飲料 - ", "drink", "🥤",                  "媽股芝芝奶蓋雙Q",          "cheese_tea",           -3, 10, 90,       timedelta(minutes=3)],
    ["飲料 - ", "drink", "🍷",                   "夏火堂珍珠奶茶",           "bubble_milk_tea",      -5, 15, 170,     timedelta(minutes=3)],
    ["甜點 - ", "dessert", "🍬",                "九天玄女糖",               "candy",                -1, 2, 10,     timedelta(minutes=1)],
    ["甜點 - ", "dessert", "🥧",                "海綿大叔蛋糕",             "bob_cake",             -1, 10, 80,     timedelta(minutes=15)],
    ["食物 - ", "food", "🍜",                   "偽力麻醬麵",               "insent_noodles",       -2, 3, 15,       timedelta(minutes=30)],
    ["食物 - ", "food", "🍜",                   "三寶巧福-紹辣乾麵",        "spicy_noodles",        -3, 8, 60,       timedelta(hours=1)],
    ["食物 - ", "food", "🍝",                   "鵝仔麵線",                 "ocie_noodle",          0, 5, 60,       timedelta(hours=1)],
    ["食物 - ", "food", "🥟",                   "五洋遊龍-水餃",            "dumpling",             -3, 10, 80,      timedelta(hours=1)],
    ["食物 - ", "food", f"{FRENCH_FRIES}",      "胖老媽薯條",               "french_fried",         -3, 15, 90,      timedelta(hours=1)],
    ["食物 - ", "food", "🍖",                   "蘿莉牛排",                 "steak",                -10, 30, 120,     timedelta(hours=2)],
    ["其他 - ", "other", "💌",                  "Dcard nitro",              "dcard_nitro",         0, 10, 500,        timedelta(weeks=1)]
]
mate_options = [  # ["類別名","類別 SQL","emoji","英文",親密度下限,親密度上限,金錢花費]
    ["飲料 - ", "drink", "🥤",                  "腥巴克腥冰樂",             "blood_ice",            -1, 2,  1,     timedelta(minutes=3)],
    ["食物 - ", "food", "🍗",                   "啃雞肌炸雞",               "fried_chicken",        -1, 8, 60,      timedelta(hours=1)],
    ["食物 - ", "food", f"{C_DUMPLINGS}",       "頂太原小籠包",             "chinese_dumplings",    -5, 10, 105,    timedelta(hours=1)],
    ["甜點 - ", "dessert", "🍬",                "QQㄡㄡ好油到Peko糖",       "Peko_candy",          -1, 1,  1,     timedelta(minutes=1)],
    ["甜點 - ", "dessert", "🍨",                "薏仁黑糖冰",               "brownsuger_ice",       -2, 5, 90,       timedelta(hours=5)],
    ["甜點 - ", "dessert", "🎂",                "月九客提拉米蘇",           "tiramisu",             -2, 6, 95,      timedelta(hours=5)],
    ["餐廳 - ", "restaurant", "🐟",             "魚次方",                   "fish",                 -5, 20, 798,     timedelta(hours=12)],
    ["餐廳 - ", "restaurant", "🔥",             "烤探花",                   "barbecue",             -20, 40, 1332,  timedelta(hours=12)],
    ["餐廳 - ", "restaurant", "🍣",             "賊壽司",                   "susi",                 0, 20, 1500,    timedelta(hours=12)],
    ["其他 - ", "other", f"{MONEY_PAPER}",      "錢錢",                     "money",                0, 20, 3888],
    ["其他 - ", "other", "🚿",                  "洗澡卡",                   "shampoo_card",         -50, 100, 5203,   timedelta(weeks=1)]
]
marriage_options = [  # ["類別名","類別 SQL","emoji","英文",親密度下限,親密度上限,金錢花費]
    ["餐廳 - ", "restaurant", "🍲",             "饗食地獄",                 "underworld",           -5, 30, 1600,   timedelta(days=3)],
    ["餐廳 - ", "restaurant", "🍢",             "鳥馬",                     "fish_horse",            -15, 20, 2388,  timedelta(days=3)],
    ["餐廳 - ", "restaurant", "🥘",             "牛爸爸羊肉爐",             "lamb_stove",            10, 25, 2772,  timedelta(days=3)],
    ["餐廳 - ", "restaurant", "🥩",             "教皇牛排",                 "s_steak",              -20, 40, 3330,  timedelta(days=3)],
    ["餐廳 - ", "restaurant", "🍧",             "分子料理",                 "molecular",             20, 30, 4200,   timedelta(days=3)],
    ["其他 - ", "other",      "💎",             "1克拉鑽石",                "diamond",               100, 150, 88888]
]



# 禮物回話


LIKE_FOOD = [
    "**{}** ：**{}** 真香",
    "**{}** 有點餓， **{}** 來填填肚子剛剛好",
    "**{}** 雖然不餓，但 **{}** 讓他食慾大增"
]
UNLIKE_FOOD = [
    "**{}** 覺得 **{}** 味道怪怪的",
    "**{}** 不喜歡 **{}** 有香菜",
    "**{}** 對 **{}** 挑食",
    "**{}** 發現 **{}** 發霉了"
]


LIKE_DRINK = [
    "**{}** 喝了 **{}**，沁涼無比",
    "**{}** 渴了，**{}**，解渴剛剛好",
    "**{}** 發現 **{}** 是全糖！"
]
UNLIKE_DRINK = [
    "**{}** ：為什麼 **{}** 不是全糖！！",
    "**{}** ：為什麼給我點無糖的 **{}** ！！",
    "**{}** ：人家水球給我錢錢，你呢？給我 **{}** ！！"
]

LIKE_DESSERT = [
    "**{}** 把 **{}** 吃的精光，體重上升 1 kg",
    "**{}** 似乎對 **{}** 的包裝很感興趣"
]

UNLIKE_DESSERT = [
    "**{}** 今天想減肥，把 **{}** 丟到一旁了",
    "**{}** 覺得很膩，**{}** 臭掉了"
]

LIKE_RESTAURANT = [
    "**{}** 似乎喜歡你請的 **{}**",
    "**{}** 很愛玩 **{}** 裡的水族箱",
    "**{}** 在 **{}** 抽到了鉛筆小新鑰匙環限定款",
    "**{}** 在 **{}** 吃飯時得到 九九折折價卷，開心無比"
]

UNLIKE_RESTAURANT = [
    "**{}** 不在預期的約會地點，**{}** 的計畫被放鴿子了",
    "**{}** 與你在 **{}** 時看著隔壁桌的帥哥，沒心情吃飯了",
    "**{}** 在 **{}** 吃飯時不小心燙傷了",
    "**{}** 發現你在 **{}** 只顧著吃飯，都不理他",
    "老闆發現 **{}** 在 **{}** 睡著了，被趕出去"
]

LIKE_OTHER = [
    "**{}** 默默收下了你給的 **{}**，暗中竊喜",
    "**{}** 想要一起使用這份 **{}**",
    "**{}** 恨不得想立即把 **{}** 用掉"
]

UNLIKE_OTHER = [
    "**{}** 對 **{}** 不感興趣",
    "**{}** 不想要你給的 **{}**",
    "**{}** 已經擁有了 **{}**"
]

class msg_type_error(commands.CommandError):
    """ """


class like_or_unlike:
    @staticmethod
    def like(type:str):
        if type == "food":return LIKE_FOOD
        elif type == "drink":return LIKE_DRINK
        elif type == "dessert":return LIKE_DESSERT
        elif type == "restaurant":return LIKE_RESTAURANT
        elif type == "other":return LIKE_OTHER
        else: raise msg_type_error("型態錯誤，請告知開發者")
    @staticmethod
    def unlike(type:str):
        if type == "food":return UNLIKE_FOOD
        elif type == "drink":return UNLIKE_DRINK
        elif type == "dessert":return UNLIKE_DESSERT
        elif type == "restaurant":return UNLIKE_RESTAURANT
        elif type == "other":return UNLIKE_OTHER
        else: raise msg_type_error("型態錯誤，請告知開發者")





# 親密度上限 [伴侶、結婚、婚後]

RELATION_LIMIT = [100, 600,9999999]

