import asyncio
from discord import Intents,Game,Status
from discord.ext import commands
from sample.bin.help import CustomHelpCommand
from core.config import PRE,BOT_ONLINE_INF,BOT_ONLINE_SET, TOKEN
import os


intents = Intents.all()
bot = commands.Bot(command_prefix=PRE,intents=intents,help_command=CustomHelpCommand())


@bot.event
async def on_ready():
    print(BOT_ONLINE_INF)
    game = Game(BOT_ONLINE_SET)
    await bot.change_presence(status=Status.idle, activity=game)
    await bot.tree.sync()


async def to_extensions():
    for i in ['cmd','slash','listener']:
        for filename in os.listdir(f'./sample/{i}/'):
            if filename.endswith('.py'):
                await bot.load_extension(f'sample.{i}.{filename[:-3]}')



async def main():
    async with bot:
        await to_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())