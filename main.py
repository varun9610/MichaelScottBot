import discord
import os
import requests
import json
import logging
from keep_alive import keep_alive

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

QUOTE_API_TIMEOUT = 5  # seconds


def get_quote():
    try:
        response = requests.get(
            "https://michael-scott-quotes.herokuapp.com/quote",
            timeout=QUOTE_API_TIMEOUT
        )
        response.raise_for_status()
        json_data = response.json()
        quote = json_data['quote'] + ' -' + json_data['author']
        return quote
    except requests.exceptions.Timeout:
        logger.error("Quote API request timed out")
        return "That's what she said! (API timed out) - Michael Scott"
    except requests.exceptions.RequestException as e:
        logger.error(f"Quote API request failed: {e}")
        return "I'm not superstitious, but I am a little stitious. (API error) - Michael Scott"
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Failed to parse quote response: {e}")
        return "Would I rather be feared or loved? Both. (Parse error) - Michael Scott"


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
        # Check if user has manage_messages permission
        if not message.author.guild_permissions.manage_messages:
            await message.channel.send(
                "You don't have permission to delete messages.")
            return

        # Check if bot has required permissions
        if not message.guild.me.guild_permissions.manage_messages:
            await message.channel.send(
                "I don't have permission to delete messages in this channel.")
            return

        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send(
                'Usage: !purge <number> (1-99)')
            return

        try:
            number = int(parts[1])
        except ValueError:
            await message.channel.send(
                'Please provide a valid number. Usage: !purge <number>')
            return

        if number < 1 or number > 99:
            await message.channel.send(
                'I can only delete between 1-99 messages.')
            return

        try:
            deleted = await message.channel.purge(limit=number)
            await message.channel.send(
                f'Deleted {len(deleted)} message(s).',
                delete_after=5)
        except discord.Forbidden:
            await message.channel.send(
                "I don't have permission to delete messages here.")
        except discord.HTTPException as e:
            logger.error(f"Failed to purge messages: {e}")
            await message.channel.send(
                "Failed to delete messages. Please try again.")


keep_alive()
client.run(os.getenv('TOKEN'))
