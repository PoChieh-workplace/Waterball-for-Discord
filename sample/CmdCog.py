from core import *
from sample.bin.message.embed import embed
from discord.ext.commands import Cog,Context,errors
from discord import Client

class Command_Cog(Cog):
    def __init__(self,bot):
        self.bot:Client = bot
        
    def __init_subclass__(cls,help:bool = True) -> None:
        cls.help = help
        return super().__init_subclass__()

    async def cog_command_error(self, ctx:Context, error: Exception) -> None:

        if hasattr(ctx.command,'on_error'):return

        if isinstance(error,errors.MissingRequiredArgument) or isinstance(error,errors.BadArgument):
            c = ctx.command
            embeds = embed(
                    f"🎀 {c.name} 指令使用說明",
                    f"{DISCORD} {c.brief}\n\n"
                    f"{BLUE_STAR}別稱：{'、'.join([f'`{PRE}{i}`' for i in c.aliases])}\n"
                    f"{PINK_STAR}用法： `{c.usage}`\n\n"
                    f"{c.description}",
                    Color.WHITE
            )
        elif isinstance(error,errors.CommandOnCooldown):
            embeds = embed(f"{BACK} | 指令冷卻中，請收後再試","",Color.RED)
        elif isinstance(error,errors.UserNotFound):
            embeds = embed(f"{BACK} | 找不到用戶",f"{ctx.author.mention}，我找不到人 ```{error.argument}```",Color.RED)
        elif isinstance(error,errors.BotMissingPermissions):
            embeds = embed(f"{BACK} | 挖，我沒有權限",f"{ctx.author.mention}，我無法使用此指令來繼續操作，請為我加上權限後再試一次",Color.RED)
        elif isinstance(error,errors.NotOwner):
            return
            # embeds = embed(f"{BACK} | 開發者限定",f"{ctx.author.mention}，你無法使用此指令",Color.RED)
        elif isinstance(error,errors.CommandNotFound):return
        else:embeds = embed(f"{BACK} | 挖，此路不通",f"```{error}```\n\n錯誤代碼：{type(error)}",Color.RED)
        return await ctx.send(embed=embeds)