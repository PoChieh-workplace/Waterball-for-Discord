
from random import choices
from typing import List,Optional
from core import TREASURE,QUESTION


__all__ = (
    'player_edition'
    'item_',
    'unlimit',
    'treasure_chest',
)


class item_:
    """
    單一物體，存放於背包 :class:`backpack` 中

    子項目
    -----------
    name:Optional[:class:`str`]
        顯示名稱用
    maximum:Optional[:class:`int`]
        物件堆疊最大值
    count:Optional[:class:`int`]
        現有數量，當數量大於最大值，會直接丟棄
    """
    def __init__(
        self,
        count:int
    ):
        self.count = count
    def __init_subclass__(
        cls,
        name:str,
        maximum:int,
        id_:Optional[str],
        useable:bool,
        emoji:Optional[str] = QUESTION
    ):
        cls.name = name
        cls.maximum = maximum
        cls.id_ = id_
        cls.useable = useable
        cls.emoji = emoji
    
    def add(self,count:int):
        self.count = self.count+count
        if self.count>self.maximum:
            c = self.count - self.maximum
            self.count = self.maximum
            return c
        return 0
    
    def use(self):
       return player_edition() 
    

class player_edition:
    def __init__(self,power:int = 0,item:List[item_] = []) -> None:
        self.power = power
        self.item = item


class unlimit(
    item_,
    name = "未定義物品",
    maximum = 0,id_ = 40401,
    useable = False,
):
    """
    單一物體，無限存放於背包 :class:`backpack` 中

    子項目
    -----------
    name:Optional[:class:`str`]
        顯示名稱用
    maximum:0
        物件堆疊最大值設定為0
    count:Optional[:class:`int`]
        現有數量，可無限堆疊
    """
    def __init_subclass__(
        cls,
        name: str,
        id_: Optional[str],
        useable: bool,
        emoji: Optional[str] = QUESTION
    ):
        return super().__init_subclass__(
            name=name,
            maximum=0,
            id_=id_,
            useable=useable,
            emoji=emoji
        )
    def add(self, count: int):
        self.count += count
        return 0


class treasure_chest(
    unlimit,
    name = "未定義寶箱",
    id_= 40402,
    useable = False
):
    """
    寶藏箱，無限存放於背包 :class:`backpack` 中
    """
    def __init__(self, *, count: int,t:dict):
        super().__init__(count)
        self.level = 1
        self.treasure = t
    
    def __init_subclass__(
        cls,
        name: Optional[str],
        id_: Optional[str],
        useable: bool = True,
        emoji = TREASURE
    ):
        return super().__init_subclass__(
            name=name,
            id_=id_,
            useable=useable,
            emoji=emoji
        )

    def use(self,c:int=1):
        return player_edition(
            item = choices(
                population=[i for i in self.treasure.keys()],
                weights=[j for j in self.treasure.values()],
                k=c
            )
        )