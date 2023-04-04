from datetime import date, datetime, timedelta
from discord.ext import commands
import mysql.connector
from sample.bin.sql import db,check_data


class sql_went_error(commands.CommandError):
    """發生錯誤"""
class number_error(commands.CommandError):
    """數字錯誤"""


# class db:
#     db = mysql.connector.connect(
#         host = "localhost",
#         user = "waterball",
#         passwd = "water@0724",
#         database = "WaterBall"
#     )

#     def connect(self) ->tuple:
#         try:db.ping()
#         except:
#             db = mysql.connector.connect(
#                 host = "localhost",
#                 user = "waterball",
#                 passwd = "water@0724",
#                 database = "WaterBall"
#             )
#         return (db.cursor(),db)

sys = db()


def get_money_info(user_id:int) ->int:
    mycursor,db = sys.connect()
    check_data(user_id)
    mycursor.execute(f"SELECT `money` FROM `info` WHERE `user` = {user_id}")
    return mycursor.fetchall()[0][0]

def earn_money(member_id:int,add:int) ->int:
    mycursor,db = sys.connect()
    money = get_money_info(member_id)
    mycursor.execute(f"UPDATE `info` SET `money` = {money+add} WHERE `user` = {member_id}")
    db.commit()
    return money+add

def cost_money(member_id:int,add:int) ->int:
    mycursor,db = sys.connect()
    money = get_money_info(member_id)
    mycursor.execute(f"UPDATE `info` SET `money` = {money-add} WHERE `user` = {member_id}")
    db.commit()
    return money-add
def give_money(give:int,to:int,count:int):
    earn_money(to,count)
    cost_money(give,count)

def search_stock_from_name(name:str):
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT * FROM `stock` WHERE `stock_name` LIKE '%{name}%' LIMIT 1")
    return mycursor.fetchall()




def check_relation(user1:int,user2:int):
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT * FROM `relationship` WHERE playerA IN ({user1},{user2}) AND playerB IN ({user1},{user2});")
    for i in mycursor.fetchall():return list(i)
    return -1

def friend_count(user:int,user2:int=None):
    mycursor,db = sys.connect()
    if user2==None:
        mycursor.execute(f"SELECT `playerA`,`playerB`,`level` FROM `relationship` WHERE `playerA` = {user} OR `playerB` = {user};")
        f = [v for v in mycursor.fetchall()]
        a = [list(v)[0] for v in f if list(v)[1]==user and list(v)[2]==0]+[list(v)[1] for v in f if list(v)[0]==user and list(v)[2]==0]
        b = [list(v)[0] for v in f if list(v)[1]==user and list(v)[2]==1]+[list(v)[1] for v in f if list(v)[0]==user and list(v)[2]==1]
        c = [list(v)[0] for v in f if list(v)[1]==user and list(v)[2]==2]+[list(v)[1] for v in f if list(v)[0]==user and list(v)[2]==2]
        return [a,b,c]
    else:return check_relation(user,user2)

##########################  情侶系統

def make_friend(user1:int,user2:int):
    mycursor,db = sys.connect()
    for i in [user1,user2]:check_data(i)
    check = check_relation(user1,user2)
    if check == -1:
        mycursor.execute(f"INSERT INTO `relationship` (`playerA`,`playerB`,`FriendDate`) VALUES({user1},{user2},'{date.today()}')")
        db.commit()


def get_friend_exp(user1:int,user2:int) -> int:
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT `exp` FROM `relationship` WHERE `playerA` IN ({user1},{user2}) AND `playerB` IN ({user1},{user2}) LIMIT 1;")
    return mycursor.fetchall()[0][0]


def edit_friend_exp(user1:int,user2:int,modify:int) ->int:
    mycursor,db = sys.connect()
    exp = get_friend_exp(user1,user2)
    mycursor.execute(f"UPDATE `relationship` SET `exp` = {exp+modify} WHERE `playerA` IN ({user1},{user2}) AND `playerB` IN ({user1},{user2}) LIMIT 1;")
    db.commit()
    return exp+modify


def get_friend_level(user1:int,user2:int) -> int:
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT `level` FROM `relationship` WHERE `playerA` IN ({user1},{user2}) AND `playerB` IN ({user1},{user2}) LIMIT 1;")
    return mycursor.fetchall()[0][0]

def set_Mate(user1:int,user2:int,message:str):
    mycursor,db = sys.connect()
    try:
        mycursor.execute(f'UPDATE `relationship` SET `level` = 1,`MateConfession` = "{message}" ,`MateDate` = "{date.today()}" WHERE `playerA` IN ({user1},{user2}) AND `playerB` IN ({user1},{user2}) LIMIT 1;')
        db.commit()
    except:raise sql_went_error("資料庫編輯資料時發生錯誤，如果重複發生請轉知開發者")
    return


def time_cul(d:int,s:int,t:datetime):
    if d !=0 :return f"{d} 天"
    elif s >= 3600:return t.strftime('%H 小時')
    elif s >= 60:return t.strftime('%M 分鐘')
    else:return t.strftime('%S 秒')




class limit: 
    @staticmethod
    def print_data():
        mycursor,db = sys.connect()
        mycursor.execute(f"SELECT * FROM `rpg_limit`")
        for i in mycursor.fetchall():
            print(i)


    @staticmethod
    def check_data(user:int):
        try:
            mycursor,db = sys.connect()
            mycursor.execute(f"SELECT * FROM `rpg_limit` WHERE `id` = {user}")
            if len(mycursor.fetchall()) == 0:
                check_data(user)
                t = datetime.now()
                d = date.today()-timedelta(days=1)
                mycursor.execute(
                    f"INSERT INTO `rpg_limit` (`id`,`drink`,`food`,`dessert`,`restaurant`,`gift`,`check_in`,`other`,`power`,`gift_ban`) "
                    f"VALUES({user},'{t}','{t}','{t}','{t}','{t}','{d}','{t}',100,'{t}')")
                db.commit()
        except:raise sql_went_error("新增 RPG 時效限制資料時發生錯誤，如果重複發生請轉知開發者")
        return

    @staticmethod
    def get_data(user:int,type:str) -> datetime:
        try:
            mycursor,db = sys.connect()
            mycursor.execute(f"SELECT `{type}` FROM `rpg_limit` WHERE `id` = {user}")
            return mycursor.fetchall()[0][0]
        except:raise sql_went_error("查詢 RPG 時效限制資料時發生錯誤，如果重複發生請轉知開發者")

    @staticmethod
    def edit_data(user:int,type:str,time:timedelta):
        try:
            mycursor,db = sys.connect()
            if limit.get_data(user,type) < datetime.now():
                t = datetime.now()+time
                mycursor.execute(f'UPDATE `rpg_limit` SET `{type}` = "{t}" WHERE `id` = {user}')
                db.commit()
                return True
            else:
                t = (limit.get_data(user,type) - datetime.now())
                return time_cul(t.days,t.seconds,datetime.fromtimestamp(t.seconds))
        except:raise sql_went_error("修改限制資料時發生錯誤，如果重複發生請轉知開發者")

    @staticmethod
    def get_data_from_date(user:int,type:str) -> date:
        try:
            mycursor,db = sys.connect()
            mycursor.execute(f"SELECT `{type}` FROM `rpg_limit` WHERE `id` = {user}")
            return mycursor.fetchall()[0][0]
        except:raise sql_went_error("查詢 RPG 日期資料時發生錯誤，如果重複發生請轉知開發者")
    @staticmethod
    def set_date_to_now(user:int,type:str):
        try:
            mycursor,db = sys.connect()
            mycursor.execute(f"UPDATE `rpg_limit` SET `{type}` = '{date.today()}' WHERE `id` = {user}")
            db.commit()
        except:raise sql_went_error("設置 RPG 今日限制資料時發生錯誤，如果重複發生請轉知開發者")
    

    class ban:
        @staticmethod
        def gift_check(user:int):
            limit.check_data(user)
            mycursor,db = sys.connect()
            mycursor.execute(f"SELECT `gift_ban` FROM `rpg_limit` WHERE `id` = {user}")
            t = mycursor.fetchall()[0][0]
            if t < datetime.now():return True
            else:return time_cul(t.days,t.seconds,datetime.fromtimestamp(t.seconds))
        @staticmethod
        def gift_edit(user:int,time:timedelta):
            t = limit.ban.gift_check(user)



class power:
    @staticmethod
    def set(user:int,count:int):
        try:
            if count < 0 or count > 100: return number_error("設定數字只能在 0 ~ 100")
            mycursor,db = sys.connect()
            mycursor.execute(f"UPDATE `rpg_limit` SET `power` = {count} WHERE `id` = {user}")
            db.commit()
        except:return sql_went_error("更新 RPG 體力資料時發生錯誤")
    
    @staticmethod
    def get(user:int) -> int:
        limit.check_data(user)
        mycursor,db = sys.connect()
        mycursor.execute(f"SELECT `power` FROM `rpg_limit` WHERE `id` = {user}")
        return mycursor.fetchall()[0][0]
        