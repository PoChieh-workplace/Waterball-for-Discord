from .item_.model import item_,unlimit,treasure_chest
from typing import List
from .item_.get import get_item

__all__ = (
    'backpack'
)

class backpack:
    def __init__(self,**k) -> None:
        self.version = 1.0
        self.player_id = k['uuid']
        self.level:int = k['bp_level']

        tmp = load_item(k['item'],k['unlimit'],k['treasure_chest'])
        self.item:List[item_] = tmp[0]
        self.unlimit_items:List[unlimit] = tmp[1]
        self.treasure:List[treasure_chest] = tmp[2]
        
        # money&1$$magic_stone&2
    def add_item(self,it:item_):

        #物件堆疊
        for i in self.item+self.unlimit_items+self.treasure:
            if type(i) is type(it):
                it.count = i.add(it.count)
        #背包空間確認
        if it.count!=0:
            if isinstance(it,unlimit):
                if isinstance(it,treasure_chest):
                    self.treasure.append(type(it)(count=it.count))
                else:
                    self.unlimit_items.append(type(it)(count=it.count))

            elif len(self.item)<= 2+self.level*3:
                self.item.append(type(it)(count=it.count))
            else:return
            it.count = 0
    
    # 資料轉換成字串
    def dump(self):
        self.check()
        return [
            '$$'.join(
                [f'{j.id_}&{j.count}' for j in i if isinstance(j,item_)]
            ) for i in [self.item,self.unlimit_items,self.treasure]
        ]
    
    def all(self):
        return self.item+self.unlimit_items+self.treasure
    
    def check(self):
        self.item = [i for i in self.item if i.count>0]
        self.unlimit_items = [i for i in self.unlimit_items if i.count>0]
        self.treasure = [i for i in self.treasure if i.count>0]
        
    
def load_item(*arg:str):
    ret = []
    for i in arg:
        if i in [None,""]:
            ret.append([])
            continue

        lists = []
        k = i.split("$$")

        for j in k:
            tmp = j.split('&')
            lists.append(
                get_item(tmp[0])(count=int(tmp[1]))
            )
        ret.append(lists)
    return ret
