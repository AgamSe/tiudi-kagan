import discord
from discord.ext import commands
from bot_token import BOT_TOKEN

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message text

# 2. Initialize the Bot
bot = commands.Bot(command_prefix='!', intents=intents)

# 3. Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# 4. Command: A simple ping command
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

# 5. Run the bot
bot.run(BOT_TOKEN)