import random
HAPPY_FACE = [
    "ヾ(•ω•`)o",
    "o(*°▽°*)o",
    "( •̀ ω •́ )y",
    "(・∀・(・∀・(・∀・*)",
    "◉‿◉",
    "٩(ˊᗜˋ )و",
    "┬┴┬┴┤･ω･)ﾉ",
    "ρ(・ω・、)",
    "(｡◕∀◕｡)",
    "(⁎⁍̴̛ᴗ⁍̴̛⁎)",
    "ಠ౪ಠ"
]
SAD_FACE = [
    "（；´д｀）ゞ",
    "o(TヘTo)",
    "(；′⌒`)",
    "ಠ_ಠ"
]

def Face(kind:str):
    if kind == "happy":
        return random.choice(HAPPY_FACE)
    elif kind == "sad":
        return random.choice(SAD_FACE)
    else:
        return ""