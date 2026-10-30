import discord
from discord.ext import commands
from bot_token import BOT_TOKEN
import status_cmds
import done_cmds
from load_students import load_students
import find_cmd

# 1. Setup Intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message text

# 2. Initialize the Bot
bot = commands.Bot(command_prefix="!", intents=intents)


# 3. Event: When the bot is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


# 4. Command: A simple ping command
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")


@bot.command(name="status")
async def status(ctx):
    if ctx.channel.name in ["הרצאות-חניכים-30-דקות👨🏽🏫", "הרצאות-חניכים-5-דקות"]:
        await status_cmds.presentation_status(ctx)
    else:
        await status_cmds.default_status(ctx)


@bot.command(name="statusall")
async def statusall(ctx):
    if ctx.channel.name in ["כללי🦉"]:
        await status_cmds.status_all(ctx)


@bot.command(name="done")
async def done(ctx):
    if ctx.channel.name in ["הרצאות-חניכים-30-דקות👨🏽🏫", "הרצאות-חניכים-5-דקות"]:
        await done_cmds.presentation_done(ctx)
    else:
        await done_cmds.default_done(ctx)


@bot.command(name="students")
async def students(ctx):

    students_str = "כל חניכי הקורס:\n"
    students_str += "\n".join(load_students())

    await ctx.send(students_str)


@bot.command(name="find")
async def find(ctx, target_channel: discord.TextChannel):
    await find_cmd.find(ctx, target_channel)


@bot.event
async def on_command_error(ctx, error):
    # Check if the error is specifically a "CommandNotFound" error
    if isinstance(error, commands.CommandNotFound):
        # ctx.invoked_with contains the name of the command they tried to use
        await ctx.send(
            f"❓ The command `!{ctx.invoked_with}` does not exist. Type `!help` to see available commands."
        )
        return

    if isinstance(error, commands.BadArgument):
        # ctx.invoked_with contains the name of the command they tried to use
        await ctx.send(f"❓ The command `!{ctx.invoked_with}` includes a bad argument.")
        return

    # Crucial: Let the bot raise other errors normally (like missing permissions)
    # Otherwise, this event will swallow all errors and make debugging impossible
    raise error


@bot.event
async def on_message(message):
    # 1. Ignore messages from the bot itself to prevent infinite loops
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    # 2. Check if the message contains any channel mentions
    if message.channel_mentions:
        for target_channel in message.channel_mentions:
            # Prevent forwarding a message to the same channel it was sent in
            if target_channel != message.channel:
                try:
                    # Forward the message content with the original author's name
                    await target_channel.send(
                        f"{message.content}\n**(הודעה מאת {message.author.display_name} בערוץ {message.channel.mention})**\n"
                    )
                except discord.errors.Forbidden:
                    print(
                        f"Missing permissions to send messages in {target_channel.name}"
                    )

    if message.content.startswith("$"):
        try:
            await message.add_reaction("✍️")
        except discord.errors.Forbidden:
            # Failsafe in case the bot lacks "Add Reactions" permission in this channel
            pass

    # 3. Essential: Process normal commands (like !ping) after handling the message
    await bot.process_commands(message)


# 5. Run the bot
bot.run(BOT_TOKEN)
