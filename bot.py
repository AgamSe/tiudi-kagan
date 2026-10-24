import discord
from discord.ext import commands
from bot_token import BOT_TOKEN
import status_cmds
import done_cmds

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

@bot.command(name="status")
async def status(ctx):
    await status_cmds.task_status(ctx)

@bot.command(name="done")
async def done(ctx):
    await done_cmds.task_done(ctx)

@bot.event
async def on_message(message):
    # 1. Ignore messages from the bot itself to prevent infinite loops
    if message.author == bot.user:
        return

    # 2. Check if the message contains any channel mentions
    if message.channel_mentions:
        for target_channel in message.channel_mentions:
            # Prevent forwarding a message to the same channel it was sent in
            if target_channel != message.channel:
                try:
                    # Forward the message content with the original author's name
                    await target_channel.send(
                        f"**הודעה מאת {message.author.display_name} בערוץ {message.channel.mention}:**\n{message.content}"
                    )
                except discord.errors.Forbidden:
                    print(f"Missing permissions to send messages in {target_channel.name}")

    # 3. Essential: Process normal commands (like !ping) after handling the message
    await bot.process_commands(message)

# 5. Run the bot
bot.run(BOT_TOKEN)