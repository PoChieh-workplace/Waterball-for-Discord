
from datetime import date
from sample.bin.message.embed import embed
# from sample.bin.rpg.rpgsql import check_data
from core import BACK,Color
from discord import Member, User
import mysql.connector



class db:
    db = mysql.connector.connect(
        host = "localhost",
        user = "waterball",
        passwd = "water@0724",
        database = "WaterBall",
        auth_plugin='mysql_native_password'
    )

    def connect(self) ->tuple:
        try:db.ping()
        except:
            db = mysql.connector.connect(
                host = "localhost",
                user = "waterball",
                passwd = "water@0724",
                database = "WaterBall",
                auth_plugin='mysql_native_password'
            )
        return (db.cursor(),db)

sys = db()

def check_data(member_id:int):
    mycursor,db = sys.connect()
    mycursor.execute("SELECT `user` FROM `info`")
    if member_id in [value[0] for value in mycursor.fetchall()]:return True
    else:mycursor.execute(f"INSERT INTO `info` (`user`) VALUES ({member_id});")
    db.commit()

def delete_data(id:int):
    mycursor,db = sys.connect()
    mycursor.execute(f"DELETE FROM `info` WHERE `user`= {id};")
    db.commit()

#學號註冊用
def check_whsh_id(user:User,school_id:str):
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT `discord_id` FROM `whsh_inf` WHERE `discord_id` = {user.id}")
    if len(mycursor.fetchall())!=0:return embed(f"{BACK} | 你已經註冊過了","",Color.RED)
    mycursor.execute(f"SELECT `school_uuid` FROM `whsh_inf` WHERE `school_uuid` = '{school_id}'")
    if len(mycursor.fetchall())!=0:return embed(f"{BACK} | {school_id} 學號似乎已經註冊過了","",Color.RED)
    return False


#一般查詢是否有
def check_if_whsh(user:User):
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT `discord_id` FROM `whsh_inf` WHERE `discord_id` = {user.id}")
    if len(mycursor.fetchall())!=0:return True
    return False


#回傳資料
def get_whsh_inf(user:User):
    if check_if_whsh(user)==True:
        mycursor,db = sys.connect()
        mycursor.execute(f"SELECT `discord_id`,`name`,`school_uuid`,`classroom` FROM `whsh_inf` WHERE `discord_id` = {user.id}")
        return mycursor.fetchall()[0]
    else:return None

def add_whsh_id(user:User,name:str,school_id:str,classroom:int):
    mycursor,db = sys.connect()
    a = check_whsh_id(user,school_id)
    if a==False:
        check_data(user.id)
        try:mycursor.execute(f"INSERT INTO `whsh_inf` (`discord_id`,`name`,`school_uuid`,`classroom`) VALUES({user.id},'{name}','{school_id}',{classroom})")
        except:return embed(f"{BACK} | 發生問題，如果重複發生請通知開發者","",Color.RED)
        db.commit()

#儲存暫時暱稱
def set_tmp_nickname(user:Member):
    mycursor,db = sys.connect()
    if user.nick==None:
        if get_tmp_nickname(user)!=None:return del_tmp_nickname(user)
        else:return
    if get_tmp_nickname(user)==None:mycursor.execute(f"INSERT INTO `nickname_tmp` (`id`,`nickname`) VALUES({user.id},'{user.nick}')")
    else:mycursor.execute(f"UPDATE `nickname_tmp` SET `nickname` = '{user.nick}' WHERE `id` = {user.id};")
    db.commit()

def get_tmp_nickname(user:User):
    mycursor,db = sys.connect()
    mycursor.execute(f"SELECT `nickname` FROM `nickname_tmp` WHERE `id` = {user.id}")
    a = mycursor.fetchall()
    if len(a)==0:return None
    else:return a[0][0]


def del_tmp_nickname(user:User):
    mycursor,db = sys.connect()
    try:
        mycursor.execute(f"DELETE FROM `nickname_tmp` WHERE `id` = {user.id}")
        db.commit()
        return True
    except:return False


class datechannelSQL:

    
    def get_from_channelID(self,id:int):
        mycursor,db = sys.connect()
        mycursor.execute(f"SELECT * FROM `datechannel` WHERE `channel_id` = {id}")
        a = mycursor.fetchall()
        if len(a)==0:return None
        else:return a[0]
    
    @staticmethod
    def get_all():
        mycursor,db = sys.connect()
        mycursor.execute(f"SELECT * FROM `datechannel`")
        return mycursor.fetchall()
    
    
    def insert(self,id:int,date:date,context:str):
        mycursor,db = sys.connect()
        if self.get_from_channelID(id)==None:
            mycursor.execute(f"INSERT INTO `datechannel` (`channel_id`,`date`,`context`) VALUES({id},'{date}','{context}')")
        else:mycursor.execute(f"UPDATE `datechannel` SET `date` = '{date}',`context`='{context}' WHERE `channel_id` = {id};")
        db.commit()
        return None
    
    
    def remove(self,id:int):
        mycursor,db = sys.connect()
        if self.get_from_channelID(id)==None:return
        else:mycursor.execute(f"DELETE FROM `datechannel` WHERE `channel_id` = {id};")
        db.commit()
        return
    