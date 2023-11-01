import requests
import random
import asyncio
import discord
from datetime import datetime
import os
from time import time, sleep
import time
from discord.ext import commands
from discord.ext.commands import Bot 
import pytz
import keep_alive
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle


intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents = intents)
token = os.getenv("TOKEN")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    quote.start()




@tasks.loop(minutes = 10)
async def quote():
    await client.wait_until_ready()
    channeld = filter(lambda c: c.name == 'daily-quotes', client.get_all_channels())
    
    for channelb in channeld:
      listmessage = await channelb.history(limit=1).flatten()
      if not listmessage:
        data = requests.get("https://type.fit/api/quotes").json()
        number = random.randint(0, 1643)
        
        await channelb.send('"' + str(data[number]["text"]) + '" -' + str(data[number]["author"]))
      else:
        async for message in channelb.history(limit=1):
          central = pytz.timezone("America/Los_Angeles")
          timer = message.created_at.astimezone(central)
          timer = timer.strftime("%H%M%S")
          timer = timer[:-4]
          tz_NY = pytz.timezone('America/Los_Angeles') 
          datetime_NY = datetime.now(tz_NY)
          timenow = datetime_NY.strftime("%H%M%S")
          timenow = timenow[:-4]
          
          if timenow == "23" or timenow == "11":
            if timenow != timer:
                data = requests.get("https://type.fit/api/quotes").json()
          
                number = random.randint(0, 1643)
                await channelb.purge(limit = 1)
                await channelb.send('"' + str(data[number]["text"]) + '" -' + str(data[number]["author"]))


@client.event
async def on_message(message):
    if str(message.content).lower() == "!quote":
        
          await client.wait_until_ready()
          data = requests.get("https://type.fit/api/quotes").json()
          numbe = random.randint(0, 1643)
          await message.channel.send('"' + str(data[numbe]["text"]) + '" -' + str(data[numbe]["author"]))
      


keep_alive.keep_alive()    

client.run(token)
