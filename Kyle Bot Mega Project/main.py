import discord
import json
import random
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
import json

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
       prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix, intents=discord.Intents.all())
bot.remove_command("help")

status = cycle(['Default Prefix +', '/help /invite /ping'])


@bot.event
async def on_ready():
  change_status.start()
  await bot.tree.sync()
  print("Bot Activated")

@bot.event
async def on_guild_join(guild):
   with open('prefixes.json', 'r') as f:
       prefixes = json.load(f)

   prefixes[str(guild.id)] = '+'

   with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
       prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

@bot.tree.command(name="ping", description="Check Bot Latency In ms(ping)")
async def ping(interaction: discord.Interaction):
 embed = discord.Embed(title = "Pong 🏓", description = f"Bots Ping Is: {round(bot.latency *1000)}ms", color = 0xAA336A)
 embed.set_thumbnail(url="https://i.imgur.com/Wf3IRHY.jpeg")
 await interaction.response.send_message(embed = embed)

@bot.tree.command(name="invite", description="Give Invite Link For This Bot")
async def invite(interaction: discord.Interaction):
    embed = discord.Embed(title="Invite Links", description="Heres The [Invite Link](https://discord.com/oauth2/authorize?client_id=1348955477731577866&permissions=8&integration_type=0&scope=bot)!!!", color=0xAA336A)
    embed.set_thumbnail(url="https://i.imgur.com/Wf3IRHY.jpeg")
    await interaction.response.send_message(embed = embed)

@bot.tree.command(name="help", description="Show Commands")
async def help(interaction: discord.Interaction):
 embed = discord.Embed(title="Commands", description="Prefixes is (+)", color=0xAA336A)
 embed.add_field(name= "Help", value="Open This", inline= False)
 embed.add_field(name="Invite", value="Give The Invite Link Of This Bots", inline= False)
 embed.add_field(name="Ping", value="Checks Bot Ping", inline= False)
 embed.set_thumbnail(url="https://i.imgur.com/Wf3IRHY.jpeg")
 await interaction.response.send_message(embed = embed)

   

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(next(status)))

@bot.command()
async def Ping(ctx):
  """shows bot ping"""
  embed = discord.Embed(title = "Pong 🏓", description = f"Bots Ping Is: {round(bot.latency *1000)}ms", color = 0xAA336A)
  embed.set_thumbnail(url="https://i.imgur.com/Wf3IRHY.jpeg")
  embed.set_footer(text = f'Requested By {ctx.author}', icon_url = ctx.author.avatar.url)
  await ctx.reply(embed = embed)

@bot.command()
async def Help(ctx):
    embed = discord.Embed(title="Commands", description="Prefixes is (+)", color=0xA020F0)
    embed.add_field(name="Help", value="Open This", inline=False)
    embed.add_field(name="Invite", value="Give The Invite Link Of This Bots", inline=False)
    embed.add_field(name="Ping", value="Checks Bot Ping", inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/Wf3IRHY.jpeg")
    embed.set_footer(text = f'Requested By {ctx.author}', icon_url = ctx.author.avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def Invite(ctx):
    embed = discord.Embed(title="Invite Links", description="Heres The [Invite Link](https://discord.com/oauth2/authorize?client_id=1348955477731577866&permissions=8&integration_type=0&scope=bot)!!!", color=0xA020F0)
    embed.set_thumbnail(url="https://media3.giphy.com/media/7x3PHPSMXSONHFuOK4/giphy.gif?cid=6c09b952ggts0wa1u4qo4j4ni8yqr7l7pqsx8xxd5h9ju85u&ep=v1_gifs_search&rid=giphy.gif&ct=g")
    embed.set_footer(text = f'Requested By {ctx.author}', icon_url = ctx.author.avatar.url)

    await ctx.send(embed=embed)

@bot.command()
async def prefix(ctx, prefix):
   with open('prefixes.json', 'r') as f:
       prefixes = json.load(f)

   prefixes[str(ctx.guild.id)] = prefix

   with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)
   await ctx.send(f"Succesfully Changed Bot Prefix")

bot.run("TOKEN")
