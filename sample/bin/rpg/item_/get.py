import sys
from .item_library import (
    money,
    magic_stone,
    bread,
    hamburgur
)
from .treasure_library import (
    daily_chest,
    epic_chest
)

def get_item(id:str):
    return getattr(sys.modules[__name__], id)