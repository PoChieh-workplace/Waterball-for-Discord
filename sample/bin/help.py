
from discord.ext import commands
from sample.bin.message.embed import embed
from core.color import Color
from core.emoji import BLUE_STAR, DC_BOT, DISCORD, PINK_STAR
from core.config import PRE
from typing import List
from sample.CmdCog import Command_Cog

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__()

        
    async def send_bot_help(self, mapping:List[Command_Cog]) -> None:
        await self.get_destination().send(
            embed=embed(
                title = f"📖 指令清單",
                description="\n\n".join(
                    [f"{BLUE_STAR} {cog.qualified_name}：\n {'、'.join([f'`{PRE}{command.name}`' for command in mapping[cog]])}"
                     for cog in mapping if cog!=None and len(mapping[cog])!=0 and cog.help==True]
                     +[f"{DC_BOT} 使用 `{PRE}help <群組名/指令>` 查詢更好的指令說明"]),
                color = Color.WHITE
            )
        )
    
    async def send_cog_help(self, cog:Command_Cog) -> None:
        await self.get_destination().send(
            embed=embed(
                f"{cog.qualified_name} 的指令庫",
                "\n\n".join([f"{PINK_STAR} {PRE}{command.name}：{command.brief}" for command in cog.get_commands()]),
                Color.WHITE
            )
        )
    async def send_group_help(self, group:commands.Group) -> None:
        cmds:List[commands.Command] =group.commands
        await self.get_destination().send(
            embed = embed(
                f"{group.name} 的指令庫",
                "\n\n".join([f"{PINK_STAR} {PRE}{command.name}：{command.brief}" for command in cmds]),
                Color.WHITE
            )
        )

    async def send_command_help(self, command:commands.Command) -> None:
        await self.get_destination().send(
            embed = embed(
                f"🎀 {command.name} 指令使用說明",
                f"{DISCORD} {command.brief}\n\n"
                f"{PINK_STAR}用法： `{command.usage}`\n"
                f"{BLUE_STAR}別稱：{'、'.join([f'`{PRE}{i}`' for i in command.aliases])}\n\n"
                f"{command.description}",
                Color.WHITE
            )
        )