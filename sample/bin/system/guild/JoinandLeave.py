from discord import Client
from bin.embed import getembed
from bin.json import open_json_JoinAndLeave, write_json_JoinAndLeave

from cmds.Permission import HavePermission
from config.color import RED
from config.zh_tw import JOIN_CONNECT, LEAVE_CONNECT, NO_PERMISSION


async def set_guild_join_message(client:Client,ctx,msg):
    if not HavePermission(ctx.author.id,ctx.guild.id,3):
        await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
        return
    Js = open_json_JoinAndLeave()
    channels = client.get_channel(ctx.channel.id)
    data = {"channel":int(ctx.channel.id),"txt":msg}
    Js['{}.join'.format(ctx.guild.id)] = data
    write_json_JoinAndLeave(Js)
    await ctx.send(JOIN_CONNECT.format(channels))


async def set_guild_leave_message(client:Client,ctx,msg):
    if not HavePermission(ctx.author.id,ctx.guild.id,3):
        await ctx.channel.send(embed=getembed("",NO_PERMISSION,RED))
        return
    Js = open_json_JoinAndLeave()
    channels = client.get_channel(ctx.channel.id)
    data = {"channel":int(ctx.channel.id),"txt":msg}
    Js['{}.leave'.format(ctx.guild.id)] = data
    write_json_JoinAndLeave(Js)
    await ctx.send(LEAVE_CONNECT.format(channels))