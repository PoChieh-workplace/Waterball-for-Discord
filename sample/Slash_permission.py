from discord import Interaction
from discord.app_commands import check,commands

from sample.bin.sql import check_if_whsh


class classic_error(commands.CheckFailure):
    pass

class NotOwner(classic_error):
    pass

class PermissionRequire(classic_error):
    pass

PERMISSION:dict = {
    "owner":[561731559493861398,948247739752394852], # 我、小葉子
    "book_editor":[561731559493861398,948247739752394852,603520807976828947] # 我、小葉子、Tekui
}

def is_owner_slash():
    def p(interaction: Interaction):
        if interaction.user.id not in PERMISSION["owner"]:
            raise NotOwner("開發者限定，你無法使用此指令")
        else:return True
    return check(p)

def is_book_editor():
    def p(interaction:Interaction):
        if interaction.user.id not in PERMISSION["book_editor"]: 
            raise NotOwner("你不是作家")
        else:return True
    return check(p)

def is_admin():
    def p(interaction:Interaction):
        if interaction.user.guild_permissions.administrator:return True
        else:raise PermissionRequire("你沒有管理員權限使用此指令！")
    return check(p)

def have_registered():
    def p(interaction:Interaction):
        if check_if_whsh(interaction.user):return True
        else:raise PermissionRequire("你尚未於機器人註冊學生帳號，無法辨識""\n請使用 *f - 學號註冊 功能後再試一次！")
    return check(p)