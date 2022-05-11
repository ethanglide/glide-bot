import os
from unicodedata import name
from dotenv import load_dotenv
import discord
import random

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix=';')

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    members = '\n - '.join([member.name for member in guild.members])

    print(f'{bot.user} is up and running :)\n'
          f'Connected to {guild.name} (id: {guild.id})\n'
          f'Guild Members \n - {members}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Welcome to the server {member.name}')

@bot.command(name='roll', help='generates a random number from 1 to your number')
async def roll(ctx, sides: int):
    await ctx.send(str(random.randint(1, sides)))

@bot.command(name='ping', help='for testing purposes')
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name='add', help='adds your space-separated numbers together')
async def add(ctx, nums: str):
    msg = ctx.message.clean_content[5:].split(' ')
    sum = 0
    for num in msg:
        sum += float(num)
    await ctx.send(sum)

@bot.command(name='name', help='@s you')
async def name(ctx):
    await ctx.send(f'You are {ctx.author.mention}')

@bot.command(name='spam', help='don\'t be a monster')
async def spam(ctx, person: discord.User, times: int):
    if times > 10:
        await ctx.send('alright calm down there bucko, we don\'t need to ping them *that* many times')
    else:
        for _ in range(times):
            await ctx.send(f'{person.mention}')

@bot.command(name='kill', help='gets the job done')
async def kill(ctx, person: discord.Member):
    if person.guild_permissions.administrator:
        await ctx.send('cannot kill administrators, sorry')
        return

    await person.create_dm()
    invite = await ctx.channel.create_invite(max_uses=1)
    await person.dm_channel.send(invite)
    await ctx.guild.kick(person, reason=f'{ctx.author.name} had do get the job done')

@bot.command(name='dm', help='the bot will dm the user you @')
async def dm(ctx, person: discord.User):
    await person.create_dm()
    await person.dm_channel.send('Hello!!')

@bot.command(name='echo', help='sends back the message you sent')
async def echo(ctx, msg: str):
    await ctx.send(ctx.message.clean_content[6:])


bot.run(TOKEN)