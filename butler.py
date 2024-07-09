# bot.py
import os
import discord
import subprocess
from discord import option
from dotenv import load_dotenv
from watchlist import (
    list_watchlist_function,
    check_watchlist_function,
    add_to_watchlist_function,
    remove_from_watchlist_function)

repo_path = '/home/butler/butler'
version_script = '/home/butler/butler/version.sh'

load_dotenv()   # load .env file
bot = discord.Bot()
intents = discord.Intents.none()
intents.reactions = True
intents.members = True
intents.guilds = True


# Logging
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    channel = bot.get_channel(1257840623596208309)
    await channel.send(f"_ _\n:white_check_mark: Butler updated to {os.getenv('BOT_VERSION')}.")


def get_updates(repo_path):
    try:
        result = subprocess.run(
            ["git", "pull"],
            cwd=repo_path,
            check=True,
            text=True,
            capture_output=True
        )

        output = result.stdout.strip()

        if "Already up to date." in output:
            return False
        else:
            return True

    except subprocess.CalledProcessError as e:
        print(e)


# Slash Commands ========================================

# Hello
@bot.slash_command(
    name="hello",
    description="Say hi to Butler."
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond
    ("_ _\n:wave: Hello! "
     "I am Butler, a bot created by the one and only @sammothxc. "
     "I am here to help you with your Hitman needs.")


# Ping
@bot.slash_command(
    name="ping",
    description="Sends the bot's latency."
)
async def ping(ctx: discord.ApplicationContext):
    latency_ms = round(bot.latency * 1000, 2)
    await ctx.respond(f"_ _\n:white_check_mark: Pong! Latency is {latency_ms}ms.")


# Butler Help
@bot.slash_command(
    name="butler_help",
    description="List Butler's commands."
)
async def help(ctx: discord.ApplicationContext):
    await ctx.respond("_ _\n:white_check_mark: [TODO: Butler Help]\n\n")


# Update Butler
@bot.slash_command(
    name="update_butler",
    description="Update Butler's code."
)
async def update_butler(ctx: discord.ApplicationContext):
    await ctx.respond("_ _\n:warning: Checking for updates...")
    updates = get_updates(repo_path)
    if not updates:
        await ctx.respond("_ _\n:white_check_mark: Butler software is already up to date.")
        return
    await ctx.respond("_ _\n:white_check_mark: Updates available.\n:warning: Updating Butler software...")
    os.system("bash /home/butler/butler/version.sh")
    os.system("sudo systemctl restart butler")


# List Watchlist
@bot.slash_command(
    name="list_watchlist",
    description="List accounts on Watchlist."
)
async def list_watchlist(ctx: discord.ApplicationContext):
    watchlist = list_watchlist_function()
    if not watchlist:
        await ctx.respond("_ _\n:x: Watchlist error.")
        return
    await ctx.respond(f"_ _\n:white_check_mark: Watchlist accounts:\n{watchlist}")
    await ctx.edit(suppress=True)


# Check Watchlist
@bot.slash_command(
    name="check_watchlist",
    description="Run status check on Watchlist accounts."
)
async def check_watchlist(ctx: discord.ApplicationContext):
    await ctx.respond("_ _\n:warning: Checking Watchlist accounts...")
    try:
        chk = check_watchlist_function()
    except Exception as e:
        print(e)

        await ctx.respond("_ _\n:x: Watchlist check error: " + str(e))
        return
    result = "\n".join([f"{key} {('still up, ID: 'if not chk[key][2] else 'suppressed, ID: ') + chk[key][1] if chk[key][0] else 'was eliminated'}" for key in chk.keys()])
    result = "\n".join([f"{key} {chk[key][1]} {chk[key][0]}" for key in chk.keys()])         # for debugging purposes, delete later
    await ctx.respond(f"_ _\n:white_check_mark: Done checking Watchlist accounts.\nHere are my findings:\n{result}")


# Add to Watchlist
@bot.slash_command(
    name="add_to_watchlist",
    description="Add an account to Watchlist."
)
@option("username")
async def add_to_watchlist(ctx: discord.ApplicationContext, account:str):

    if add_to_watchlist_function(account):
        await ctx.respond(f"_ _\n:white_check_mark: Added {account} to Watchlist.")
    else:
        await ctx.respond(f"_ _\n:x: {account} is already in Watchlist.")


# Remove from Watchlist
@bot.slash_command(
    name="remove_from_watchlist",
    description="Remove an account from Watchlist."
)
@option("username")
async def remove_from_watchlist(ctx: discord.ApplicationContext, account:str):

    if remove_from_watchlist_function(account):
        await ctx.respond(f"_ _\n:white_check_mark: Removed {account} from Watchlist.")
    else:
        await ctx.respond(f"_ _\n:x: {account} is not in Watchlist.")


# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))