# bot.py
import os
import discord
from dotenv import load_dotenv
from watchlist import list_watchlist_function, check_watchlist_function, add_to_watchlist_function, remove_from_watchlist_function

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
    description="Say hi to Butler."
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(":wave: Hello! I am Butler, a bot created by the one and only @sammothxc. I am here to help you with your Hitman needs.")

## Ping
@bot.slash_command(
    name="ping",
    description="Sends the bot's latency."
)
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f":white_check_mark: Pong! Latency is {bot.latency}ms.")

## Butler Help
@bot.slash_command(
    name="butler_help",
    description="List Butler's commands."
)
async def help(ctx: discord.ApplicationContext):
    await ctx.respond(":white_check_mark: [TODO: Butler Help]\n\n")

## List Watchlist
@bot.slash_command(
    name="list_watchlist",
    description="List accounts on Watchlist."
)
async def list_watchlist(ctx: discord.ApplicationContext):
    watchlist = list_watchlist_function()
    print(watchlist)
    await ctx.respond(f":white_check_mark: Watchlist accounts: \n {watchlist}")

## Check Watchlist
@bot.slash_command(
    name="check_watchlist",
    description="Run status check on Watchlist accounts."
)
async def check_watchlist(ctx: discord.ApplicationContext):
    await ctx.respond(":warning: Checking Watchlist accounts...")
    chk = check_watchlist_function()
    result = "\n".join([f"{key} {'still up, ID: ' + chk[key][1] if chk[key][0] else 'was eliminated'}" for key in chk.keys()])
    await ctx.respond(":white_check_mark: Done checking Watchlist accounts. \n Here are my findings: \n" + result)

## Add to Watchlist
@bot.slash_command(
    name="add_to_watchlist",
    description="Add an account to Watchlist."
)
async def add_to_watchlist(ctx: discord.ApplicationContext):
    account = "test"
    try:
        add_to_watchlist_function(account)
    except:
        await ctx.respond(":x: " + account + " is already in Watchlist.")
        return
    await ctx.respond(":white_check_mark: Added " + account + " to Watchlist.")

## Remove from Watchlist
@bot.slash_command(
    name="remove_from_watchlist",
    description="Remove an account from Watchlist."
)
async def remove_from_watchlist(ctx: discord.ApplicationContext):
    account = "test"
    try:
        remove_from_watchlist_function(account)
    except:
        await ctx.respond(":x: " + account + " is not in Watchlist.")
        return
    await ctx.respond(":white_check_mark: Removed " + account + " from Watchlist.")

## Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))