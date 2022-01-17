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
uart_connection = None

# Connect to the PyBadge if connection exists
print(ble.connected)
if ble.connected:
    for connection in ble.connections:
        if UARTService in connection:
            uart_connection = connection
        break

# Main loop
while True:
    
    # Set up Bluetooth connection
    if not uart_connection or not uart_connection.connected:
        print("Scanning...")
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5): # Scan...
            if UARTService in adv.services: # If UARTService found...
                print("Found a UARTService advertisement!")
                uart_connection = ble.connect(adv) # Create a UART connection
                break # No need to scan any more
            ble.stop_scan() # Stop scanning whether or not we are connected

    # Main code that only executes while Pi is connected to PyBadge
    while uart_connection and uart_connection.connect:
        print("Connected!")

# Define variables used throughout Discord bot
MY_NAME = "Tekktrik"
MY_NUMBER = "0458"

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
