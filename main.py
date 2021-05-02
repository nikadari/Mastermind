import discord
from discord.ext import commands, tasks
from itertools import cycle
import discord.client
import os
import requests
import json
import googletrans

client = discord.Client()
client = commands.Bot(command_prefix='$')

#status = cycle(['French', 'English', 'Math', 'Science', 'Geography', 'Art', 'Computer Science', 'History'])

todo = ["homework", "project 1", "project 2"]


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  #no action is message is from bot (itself)
  if message.author == client.user:
    return
  
  msg = message.content

  #return inspirational message
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  #Todo: Update this help menu
  if msg.startswith('$help'):
    commands = "Commands:\n$inpsire - request an inspirational quote to motivate you\n$oracle - request an answer for your question (for fact checking and math calculations)"
    await message.channel.send(commands)

  await client.process_commands(message)    

#using Wolfram Alpha API for calculations and Wiki Search
@client.command()
async def oracle(ctx,*args):
  query = '+'.join(args)
  url = f"https://api.wolframalpha.com/v1/result?appid={os.environ['AppID']}&i={query}%3F"
  response = requests.get(url)

  #answer not found
  if response.status_code == 501:
    await ctx.send("Seems like we couldn't find an answer to that. Try again!")
    return
  
  await ctx.send(response.text)

#using Google Translate API to translate text
@client.command()
async def translate(ctx, lang_to, *args):
  lang_to = lang_to.lower()
  if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
    raise commands.BadArgument("Invalid language to translate to.")

  text = ' '.join(args)
  translator = googletrans.Translator()
  text_translated = translator.translate(text, dest=lang_to).text
  await ctx.send(text_translated)

#keeps track of to do list (action items)
#  @client.command()
#  async def todo(ctx, action, *args):
#    if action == 'clear':
#      todo.clear()
#    elif action == 'show':
#      for i in range(len(todo)):
#        await ctx.send(i)
    #elif action == 'add':
    #elif action == 'delete':



#Todo: shows what subject you are working on (background task)
#@tasks.loop(seconds=10)
#async def change_status():
  #await client.change_presence(activity=discord.Game(next(status)))
  #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.studying, name="a movie")))

client.run(os.environ['TOKEN'])
