# bot.py
import os
import discord
from dotenv import load_dotenv

load_dotenv() # load TOKEN
bot = discord.Bot()

## Logging
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

## Slash Commands ========================================

## Hello Command
@bot.slash_command(
    name="hello",
    description="Say hello to the bot"
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hello! I am Butler, a bot created by the one and only @sammothxc. I am here to help you with your Hitman needs.")

## Check Private Accounts Command
@bot.slash_command(
    name="chkprivate",
    description="Run a script to check if private accounts resurfaced."
)
async def chkprivate(ctx: discord.ApplicationContext):
    await ctx.respond("Checking Hitman Watchlisted accounts...")

## Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))