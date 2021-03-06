"""
Bot link for the DisBadge!
"""
import argparse
import discord
from discord.commands.context import ApplicationContext
import requests
from shared.messages import CommandType
from raspberrypi.rpi_messages import RPiDiscordMessage
from shared.secrets import (  # pylint: disable=ungrouped-imports,no-name-in-module
    secrets,
)

# Define variables used throughout Discord bot
MY_NAME = "Tekktrik"
MY_NUMBER = "0458"


parser = argparse.ArgumentParser(description="Set the IP address for the PyBadge")
parser.add_argument("ip", metavar="IP", type=str, help="the IP address")
parser.add_argument(
    "--mute", help="Mute DisBadge for notification sounds", action="store_true"
)
args = parser.parse_args()

IP_ADDRESS = args.ip

# Prepare Discord bot
bot = discord.Bot()


def send_message_post(message: str, user: str, command_type: int) -> None:
    """Send a message to the PyBadge

    :param str message: The message to send
    :param str user: The user sending the message
    :param int command_type: The command type being used
    """

    new_message = RPiDiscordMessage(message, str(user), command_type)
    payload = new_message.to_dict()
    print(payload)
    requests.post("/".join(["http:/", IP_ADDRESS, "message"]), data=payload, timeout=5)


@bot.event
async def on_ready():
    """Method that runs when bot is ready"""
    print(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def cheer(ctx: ApplicationContext, message: str):
    """Sends the gamer a message

    :param ApplicationContext ctx: The application context
    :param str message: The message to send
    """

    await ctx.respond("Sending your message to {0}!".format(MY_NAME))
    send_message_post(message, ctx.user, CommandType.CHEER)


@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def hype(ctx: ApplicationContext, message: str):
    """Cheers on the gamer with an exciting message!

    :param ApplicationContext ctx: The application context
    :param str message: The message to send
    """

    await ctx.respond("Sending your hype to {0}!".format(MY_NAME))
    send_message_post(message, ctx.user, CommandType.HYPE)


@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def ping(ctx: ApplicationContext, message: str):
    """Pings the gamer with the given message

    :param ApplicationContext ctx: The application context
    :param str message: The message to send
    """

    await ctx.respond("Pinging {0} with your message!".format(MY_NAME))
    send_message_post(message, ctx.user, CommandType.PING)


def activate_disbadge():
    """Send an activation POST to the PyBadge"""

    print("Activating...")
    requests.post("/".join(["http:/", IP_ADDRESS, "activate"]), timeout=5)
    if args.mute:
        requests.post("/".join(["http:/", IP_ADDRESS, "sound", "off"]), timeout=5)


# Run blocking event code

activate_disbadge()
bot.run(secrets["login-token"])
# loop = asyncio.new_event_loop()
# bluetooth_task = loop.create_task(bluetooth_functionality())
# discord_task = loop.create_task(bot.start(secrets["login-token"]))
# loop.run_forever()
