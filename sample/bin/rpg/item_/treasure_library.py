from .model import treasure_chest
from .item_library import *


# 寶箱配置區

class daily_chest(
    treasure_chest,
    id_ = 'daily_chest',
    name = "每日寶箱"
):
    def __init__(self,count):
        super().__init__(
            count=count,
            t = {
                bread(count=3):1,
                money(count=100):1,
                money(count=300):1,
                money(count=500):1,
                magic_stone(count = 10):1
            }
        )

class epic_chest(
    treasure_chest,
    id_ = 'epic_chest',
    name = "稀有寶箱"
):
    def __init__(self,count):
        super().__init__(
            count=count,
            t = {
                money(count=500):2,
                magic_stone(count = 20):1
            }
        )