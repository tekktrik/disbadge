import discord
from discord.commands.context import ApplicationContext
import asyncio
from adafruit_ble import BLERadio, BLEConnection
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from shared.messages import CommandType, DiscordMessageBase
from shared.uart import UARTManager
from secrets import secrets

# Define variables used throughout Discord bot
MY_NAME = "Tekktrik"
MY_NUMBER = "0458"

# Initialize Bluetooth-related objects
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

CURRENT_MESSAGE = DiscordMessageBase()


async def bluetooth_functionality() -> None:

    # Connect to the PyBadge if connection exists
    ble_connection = None
    if ble.connected:
        for connection in ble.connections:
            if UARTService in connection:
                ble_connection: BLEConnection = connection
            break

    asyncio.sleep(0)

    # Main loop
    while True:
        
        # Set up Bluetooth connection
        if not ble_connection or not ble_connection.connected:
            print("Scanning...")
            for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5): # Scan...
                adv: ProvideServicesAdvertisement
                if UARTService in adv.services: # If UARTService found...
                    print("Found a UARTService advertisement!")
                    ble_connection = ble.connect(adv) # Create a UART connection
                    break # No need to scan any more
                ble.stop_scan() # Stop scanning whether or not we are connected

        # Main code that only executes while Pi is connected to PyBadge
        if ble_connection and ble_connection.connected:
            with UARTManager(uart, ble) as uart_mngr:
                while uart_mngr.connected:

                    # If a message should be sent to the PyBadge
                    if CURRENT_MESSAGE:
                        uart_mngr.transmit(CURRENT_MESSAGE.to_dict())
                    asyncio.sleep(0)

        # Relinquish control
        asyncio.sleep(0)

# Prepare Discord bot
bot = discord.Bot()

def set_message_properties(message: str, user: str, command_type: int) -> None:
    CURRENT_MESSAGE.message = message
    CURRENT_MESSAGE.user = user
    CURRENT_MESSAGE.cmd_type = command_type

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def cheer(ctx: ApplicationContext, message: str):
    """Sends the gamer a message"""

    await ctx.respond("Sending your message to {0}!".format(MY_NAME))
    set_message_properties(message, ctx.user, CommandType.CHEER)

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def hype(ctx: ApplicationContext, message: str):
    """Cheers on the gamer with an exciting message!"""

    await ctx.respond("Sending your hype to {0}!".format(MY_NAME))
    set_message_properties(message, ctx.user, CommandType.HYPE)

@bot.slash_command(guild_ids=[secrets["guild-id"]])
async def ping(ctx: ApplicationContext, message: str):
    """Pings the gamer with the given message"""

    await ctx.respond("Pinging {0} with your message!".format(MY_NAME))
    set_message_properties(message, ctx.user, CommandType.PING)

# Run blocking event code
loop = asyncio.new_event_loop()
bluetooth_task = loop.create_task(bluetooth_functionality())
discord_task = loop.create_task(bot.start(secrets["login-token"]))
loop.run_forever()
