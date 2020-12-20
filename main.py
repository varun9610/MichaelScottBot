import discord
import os
import requests
import json

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

client.run(os.getenv('TOKEN'))