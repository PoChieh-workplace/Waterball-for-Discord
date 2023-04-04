from .backpack import backpack
from .item_.sys import item_gui
from discord import User,Client,Interaction
from typing import List
from sample.bin.message import define_inter_error as d
from sample.bin.sql import db

class player:
    def __init__(self,user:User,**k) -> None:
        self.user = user
        self.uuid = k['uuid']
        self.power = k['power']
        self.name = k['name'] if 'name' in k else '未命名'
        self.backpack = backpack(**k)
    
    # 更新玩家資料
    def save(self):
        lists:List[str] = self.backpack.dump()
        my,dbs = db().connect()
        my.execute(
            f"UPDATE `rpg_player` SET `name`='{self.name}',"
            f"`item`='{lists[0]}',`unlimit`='{lists[1]}',`treasure_chest`='{lists[2]}',`power`={self.power} "
            f"WHERE `uuid`={self.uuid}"
        )
        dbs.commit()

    
    # 重載背包資料
    def reload_backpack(self):
        my,dbs = db().connect()
        my.execute(
            f"SELECT `item`,`unlimit`,`treasure_chest` FROM `rpg_player` WHERE `uuid` = {self.uuid}"
        )
        r = my.fetchall()[0]
        self.backpack = backpack(
            uuid = self.uuid,
            item = r[0],
            unlimit = r[1],
            treasure_chest = r[2],
            bp_level = 1
        )
    
    # 使用道具
    async def use_item(self,i:Interaction,string:str):
        item = [j for j in self.backpack.all() if j.id_==string]
        if len(item)==0:
            raise d("發現背包沒有這項物品，請刷新訊息後再試一次！")
        else:
            gui = item_gui(self,item[0])
            return await gui.open_gui(i)

    
    

def get_player_from_uuid(c:Client,uuid:int):
    my,dbs = db().connect()
    #取得角色資料
    my.execute(
        f"SELECT * FROM `rpg_player` WHERE `uuid` = {uuid}"
    )
    r = my.fetchall()[0]
    return player(
        user = c.get_user(r[1]),
        uuid = r[0],
        name = r[2],
        item = r[3],
        unlimit = r[4],
        treasure_chest = r[5],
        power = r[6],
        bp_level = 1
    )



def get_player_from_user(user:User) -> List[player]:
    #取得玩家列表
    my,dbs = db().connect()
    my.execute(
        f"SELECT * FROM `rpg_player` WHERE `user` = {user.id}"
    )
    return [
        player(
            uuid = i[0],
            user = i[1],
            name = i[2],
            item = i[3],
            unlimit = i[4],
            treasure_chest = i[5],
            power = i[6],
            bp_level = 1
        )
        for i in my.fetchall()
    ]


def insert_player_sql(user:User,name:str):
    my,dbs = db().connect()

    #確定數量上限
    my.execute(
        f"SELECT `uuid` FROM `rpg_player` WHERE `user` = {user.id}"
    )
    l = my.fetchall()
    if len(l)>=2:
        return False

    #創立資料
    my.execute(
        f"INSERT INTO `rpg_player`(`user`,`name`) VALUES({user.id},'{name}')"
    )
    dbs.commit()
    return True