import discord
import os
import requests
import json
from keep_alive import keep_alive

client = discord.Client()
def get_quote():
  response = requests.get("https://michael-scott-quotes.herokuapp.com/quote")
  json_data = json.loads(response.text)
  quote = json_data['quote'] + ' -' + json_data['author']
  return(quote)



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('!quote'):
    quote = get_quote()
    await message.channel.send(quote)
  if message.content.startswith('!purge'):
    wholestring = message.content
    string = wholestring.split(' ')
    lenofinput = len(string)
    if lenofinput == 1:
      await message.channel.send('I can only delete message count b/w 1-99')
    else:
      number = int(string[1])
      if number > 99 or number < 1:
        await message.channel.send('I can only delete message count b/w 1-99')
      else:
        deleted = await message.channel.purge(limit=number)
        await message.channel.send('Deleted {} message(s)'.format(len(deleted)))

keep_alive()
client.run(os.getenv('TOKEN'))