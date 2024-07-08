# bot.py
import os
import discord
from discord import option
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
    if not watchlist:
        await ctx.respond(":x: Watchlist error.")
        return
    await ctx.respond(f":white_check_mark: Watchlist accounts:\n{watchlist}")
    await ctx.edit(suppress=True)

## Check Watchlist
@bot.slash_command(
    name="check_watchlist",
    description="Run status check on Watchlist accounts."
)
async def check_watchlist(ctx: discord.ApplicationContext):
    await ctx.respond(":warning: Checking Watchlist accounts...")
    try:
        chk = check_watchlist_function()
    except Exception as e:
        print(e)
        
        await ctx.respond(":x: Watchlist check error: " + str(e))
        return
    result = "\n".join([f"{key} {('still up, ID: 'if not chk[key][2] else 'suppressed, ID: ') + chk[key][1] if chk[key][0] else 'was eliminated'}" for key in chk.keys()])
    await ctx.respond(f":white_check_mark: Done checking Watchlist accounts.\nHere are my findings:\n{result}")

## Add to Watchlist
@bot.slash_command(
    name="add_to_watchlist",
    description="Add an account to Watchlist."
)
@option("username")
async def add_to_watchlist(ctx: discord.ApplicationContext, account:str):
    if add_to_watchlist_function(account):
            await ctx.respond(f":white_check_mark: Added {account} to Watchlist.")
    else:
        await ctx.respond(f":x: {account} is already in Watchlist.")

## Remove from Watchlist
@bot.slash_command(
    name="remove_from_watchlist",
    description="Remove an account from Watchlist."
)
@option("username")
async def remove_from_watchlist(ctx: discord.ApplicationContext, account:str):
    if remove_from_watchlist_function(account):
        await ctx.respond(f":white_check_mark: Removed {account} from Watchlist.")
    else:
        await ctx.respond(f":x: {account} is not in Watchlist.")
    
## Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))