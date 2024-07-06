# bot.py
import os
import discord
from dotenv import load_dotenv
from check_watchlist import check_watchlist

load_dotenv() # load TOKEN
bot = discord.Bot()

## Logging
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

## Slash Commands ========================================

## Hello
@bot.slash_command(
    name="hello",
    description="Say hello to the bot"
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hello! I am Butler, a bot created by the one and only @sammothxc. I am here to help you with your Hitman needs.")

## Check Watchlist
@bot.slash_command(
    name="check_watchlist",
    description="Run a script to check if private accounts resurfaced."
)
async def chkprivate(ctx: discord.ApplicationContext):
    await ctx.respond("Checking Hitman Watchlisted accounts...")
    chk = check_watchlist()
    result = "\n".join([f"{key} {'still up, ID: ' + chk[key][1] if chk[key][0] else 'was eliminated'}" for key in chk.keys()])
    await ctx.respond("Done checking Hitman Watchlisted accounts: \n" + result)

## Add to Watchlist
@bot.slash_command(
    name="add_watchlist",
    description="Run a script to check if private accounts resurfaced."
)
async def chkprivate(ctx: discord.ApplicationContext):
    await ctx.respond("Checking Hitman Watchlisted accounts...")
    chk = check_watchlist()
    result = "\n".join([f"{key} {'still up, ID: ' + chk[key][1] if chk[key][0] else 'was eliminated'}" for key in chk.keys()])
    await ctx.respond("Done checking Hitman Watchlisted accounts: \n" + result)

## Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))