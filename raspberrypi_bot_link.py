import discord
from discord.commands.context import ApplicationContext
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from secrets import secrets

# Initialize Bluetooth-related objects
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

# Set up Bluetooth connection
ble.start_advertising(advertisement)

# Define variables used throughout Discord bot
MY_NAME = "Tekktrik"

# Prepare Discord bot
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def cheer(ctx: ApplicationContext, message: str):
    """Sends the gamer a message"""
    # TODO: send message to PyBadge
    await ctx.respond("Sending your message to {0}!".format(MY_NAME))

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def hype(ctx: ApplicationContext, message: str):
    """Cheers on the gamer with an exciting message!"""
    # TODO: send message to PyBadge
    await ctx.respond("Sending your hype to {0}!".format(MY_NAME))

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def ping(ctx: ApplicationContext, message: str):
    """Pings the gamer with the given message"""
    # TODO: send message to PyBadge
    await ctx.respond("Pinging {0} with your message!".format(MY_NAME))

# Run blocking event code
bot.run(secrets["login-token"])
