import discord
from discord.commands.context import ApplicationContext
import asyncio
import requests
from shared.messages import CommandType
from raspberrypi.rpi_messages import RPiDiscordMessage
from shared.uart import UARTManager
from shared.secrets import secrets

# Define variables used throughout Discord bot
MY_NAME = "Tekktrik"
MY_NUMBER = "0458"


# Prepare Discord bot
bot = discord.Bot()

def send_message_post(message: str, user: str, command_type: int) -> None:
    new_message = RPiDiscordMessage(message, user, command_type)
    requests.post("URL", json=new_message.to_json()) # TODO: Add ability to use IP address here

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def cheer(ctx: ApplicationContext, message: str):
    """Sends the gamer a message"""

    await ctx.respond("Sending your message to {0}!".format(MY_NAME))
    send_message_post(message, ctx.user, CommandType.CHEER)

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def hype(ctx: ApplicationContext, message: str):
    """Cheers on the gamer with an exciting message!"""

    await ctx.respond("Sending your hype to {0}!".format(MY_NAME))
    send_message_post(message, ctx.user, CommandType.HYPE)

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def ping(ctx: ApplicationContext, message: str):
    """Pings the gamer with the given message"""

    await ctx.respond("Pinging {0} with your message!".format(MY_NAME))
    send_message_post(message, ctx.user, CommandType.PING)

# Run blocking event code
loop = asyncio.new_event_loop()
bluetooth_task = loop.create_task(bluetooth_functionality())
discord_task = loop.create_task(bot.start(secrets["login-token"]))
loop.run_forever()
