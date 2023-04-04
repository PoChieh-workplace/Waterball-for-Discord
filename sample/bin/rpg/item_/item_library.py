from .model import item_, unlimit,player_edition
from core import FOOD,BREAD,MONEY_PAPER,MAGIC_STONE

class bread(
    item_,
    id_ = 'bread',
    name = "麵包",
    useable = True,
    emoji = BREAD,
    maximum = 10
):
    pass
    def use(self):
        return player_edition(power=1)

class hamburgur(
    item_,
    id_ = 'hamburgur',
    name = "漢堡",
    useable = True,
    emoji = FOOD,
    maximum = 5
):
    pass
    def use(self):
        return player_edition(power=3)


class money(
    unlimit,
    id_ = 'money',
    name = "錢",
    useable = False,
    emoji = MONEY_PAPER
):
    pass

class magic_stone(
    unlimit,
    id_ = 'magic_stone',
    name = "魔法石",
    useable = False,
    emoji = MAGIC_STONE
):
    pass
