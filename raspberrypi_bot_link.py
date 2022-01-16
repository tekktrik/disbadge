import discord
from discord.commands.context import ApplicationContext
from secrets import secrets

MY_NAME = "Tekktrik"

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
    
# Test commit

bot.run(secrets["login-token"])