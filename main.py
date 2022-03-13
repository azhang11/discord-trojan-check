import discord
from discord.ext import commands, tasks
import sys

print(sys.version)
print("Testing")
client = commands.Bot(command_prefix=',')

client.load_extension("cogs.uscsql")

@client.event
async def on_ready():
    print("Bot is online")
    await client.change_presence(activity=discord.Game('with Tommy Trojan'))


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {client.latency}ms")


client.run("###")