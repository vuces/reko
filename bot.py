import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
from discord.ext.commands import has_permissions
from discord import emoji
import time
from discord import embeds
import youtube_dl
from discord import voice_client
import youtube_dl
import os
import shutil
import asyncio
from discord.utils import get
from discord.ext import commands
from helper import *

bot = discord.Client()

players = {}

client = commands.Bot(command_prefix = ',')
status = cycle(['On The Moon!', 'With A Monster!'])

@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('In Space!'))
    print("I'm ready.")

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity==discord.Game(next(status)))


@client.command()
async def commandz(ctx):
    await ctx.send("`🔧Moderation: clear, kick, ban.\n🏆Fun: askme, dice, pplength.\n💍Other: Work in Progress...\n🔥Music: leave, join, play.`")

@client.command()
async def dice(ctx):
    bigresponses = ["`🎲: 1`",
                    "`🎲: 2`",
                    "`🎲: 3`",
                    "`🎲: 4`",
                    "`🎲: 5`",
                    "`🎲: 6`",
                    "`🎲: 7`",
                    "`🎲: 8`",
                    "`🎲: 9`",
                    "`🎲: 10`"]
    await ctx.send(random.choice(bigresponses))

@client.command(aliases=['bigbrain'])
async def askme(ctx, *, question):
    responses = ["idk you tell me",
    "It is decidedly so.",
    "Without a doubt.",
    "uh, sure!",
    "no",
    "not rlly",
    "Most likely.",
    "Outlook good.",
    "yes!",
    "Signs point to yes.",
    "do I look like an 8ball to you",
    "I'm hungry ask later",
    "I can't answer that, I'm not big brain..",
    "Cannot predict now.",
    "uh what",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."]
    await ctx.send(f'Question: `{question}`\nAnswer: {random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)

@client.command()
async def pplength(ctx):
    pps = ["`🍆: 8=D`",
          "`🍆: 8==D`",
          "`🍆: 8=====D`",
          "`🍆: 8===D`",
          "You don't have a dick at all...",
          "`🍆: 8=====D`",
          "`🍆: 8===========D`",
          "`🍆: 8=====D`",
          "`🍆: 8D`",
          "`🍆: 0=D, you got one ball, you ok?`"]
    await ctx.send(random.choice(pps))

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client


@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return
    await ctx.send("Getting everything ready, playing audio soon")
    print("Someone wants to play music let me get that ready for them...")
    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()





def setup(client):
    client.add_cog(Audio(client))









client.run('process.env.BOT_TOKEN');
