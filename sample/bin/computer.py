from core import Color
from sample.bin.message import embed
from discord.ext.commands import Context
from psutil import *
import os


def byte_to_MB(i:int):
    return round(i/1024**2,2)

async def Ram(ctx:Context):
    def my_ram():
        process = Process(os.getpid())
        return (byte_to_MB(Process(os.getpid()).memory_info().rss))
    memoryEmbed = embed(
        "🔧 | 記憶體使用量",
        f"> 本程序記憶體使用量：{my_ram()}MB\n",
        Color.BLUE_LIGHT
    )
    c = virtual_memory()
    p = round((c.total - c.available)/c.total * 100,2)
    l = [
        ['總容量',f'`{byte_to_MB(c.total)}` MB'],
        ['已使用量',f'`{byte_to_MB(c.total-c.available)}` MB | `{p}%`']
    ]
    for i in l:
        memoryEmbed.add_field(name=i[0],value=i[1],inline=True)
    if p>80:memoryEmbed.color = Color.RED
    elif p>30:memoryEmbed.color = Color.ORANGE
    await ctx.send(embed=memoryEmbed)



async def CPU(ctx:Context):
    memoryEmbed = embed(
        "🔧 | CPU 使用量",
        f"> cpu 核心數量：{cpu_count()}\n",
        Color.BLUE_LIGHT
    )
    c = cpu_percent()
    memoryEmbed.add_field(name=f"核心數據",
        value=f"當前時脈：`{cpu_freq().current}MHz`\n使用量：`{c}%`",
        inline=True
    )
    if c>80:memoryEmbed.color = Color.RED
    elif c>30:memoryEmbed.color = Color.ORANGE
    await ctx.send(embed=memoryEmbed)