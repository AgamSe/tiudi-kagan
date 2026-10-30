from load_students import load_students
import discord

SKIP_EMOJIS = {'👍', '❌', '✖️'}

async def default_status(ctx):
    pending_tasks = []

    async for msg in ctx.channel.history(limit=100):
        # 1. Ignore bots and commands
        if msg.author.bot or msg.content.startswith(ctx.prefix):
            continue

        # 2. Skip if the message has a thumbs up OR an X reaction
        if any(str(reaction.emoji) in SKIP_EMOJIS for reaction in msg.reactions):
            continue

        # if msg is empty or if msg doesn't start with $
        if (not msg.content) or (msg.content[0] != '$'):
            continue

        # 3. Clean up the message text (replace line breaks with spaces)
        first_line = msg.content[1:].split("\n")[0].strip()
        if not first_line:
            first_line = "[Attachment / No text]"
            
        preview = first_line[:50] + "..." if len(first_line) > 50 else first_line

        # Put the link on static text (or paste msg.jump_url directly) so user text never breaks it
        task_entry = f"• **[Jump to Task]({msg.jump_url})** — {preview} (Requested by {msg.author.mention})"
        pending_tasks.append(task_entry)

    if pending_tasks:
        pending_tasks.reverse()
        response = "**📋 Pending Tasks:**\n" + "\n".join(pending_tasks)
        await ctx.send(response)
    else:
        await ctx.send("🎉 All tasks in the last 100 messages are complete!")

async def presentation_status(ctx):
    students_that_didnt_present = load_students()

    async for msg in ctx.channel.history(limit=500):
        # 1. Ignore bots and commands
        if msg.author.bot or msg.content.startswith(ctx.prefix):
            continue

        # if msg is empty or if msg doesn't start with $
        if (not msg.content) or (msg.content[0] != '$'):
            continue

        mentioned_channel_names = [channel.name for channel in msg.channel_mentions]

        # loops over a snapshot of the list 
        for student in students_that_didnt_present[:]:
            for mentioned_channel_name in mentioned_channel_names:
                if student in mentioned_channel_name.replace('-', ' '):
                    students_that_didnt_present.remove(student)

    if len(students_that_didnt_present) != 0:
        output = "חניכים שלא הציגו:\n"
        output += '\n'.join(students_that_didnt_present)
        await ctx.send(output)
    else:
        await ctx.send("🎉 All students have presented!")


async def status_all(ctx):
    
    status_msg = await ctx.send(f"🔍 Scanning all tasks... (This may take a few seconds)")

    # List non-task channels here so normal chat isn't flagged as pending tasks
    ignored_channels = ['הרצאות-חניכים-30-דקות👨🏽🏫', 'הרצאות-חניכים-5-דקות']
    
    report_sections = []

    # Loop through every text channel in the server
    for channel in ctx.guild.text_channels:
        if channel.name in ignored_channels:
            continue

        channel_tasks = []
        try:
            async for msg in channel.history(limit=50):
                # 1. Ignore bots and commands
                if msg.author.bot or msg.content.startswith(ctx.prefix):
                    continue

                # 2. Skip completed or canceled tasks
                if any(str(reaction.emoji) in SKIP_EMOJIS for reaction in msg.reactions):
                    continue

                # if msg is empty or if msg doesn't start with $
                if (not msg.content) or (msg.content[0] != '$'):
                    continue

                # 3. Clean and format the task preview
                first_line = msg.content[1:].split("\n")[0].strip()
                if not first_line:
                    first_line = "[Attachment / No text]"
                preview = first_line[:50] + "..." if len(first_line) > 50 else first_line

                task_entry = f"• **[Jump to Task]({msg.jump_url})** — {preview} ({msg.author.display_name})"
                channel_tasks.append(task_entry)

        except discord.errors.Forbidden:
            # Skip private channels the bot doesn't have permission to read
            continue

        # Only add the channel to the report if it actually has pending tasks
        if channel_tasks:
            channel_tasks.reverse()
            section = f"**📂 {channel.mention}**\n" + "\n".join(channel_tasks)
            report_sections.append(section)

    await status_msg.delete()

    # If no channels had pending tasks
    if not report_sections:
        await ctx.send("🎉 All tasks across all channels are complete!")
        return

    # Send the report (automatically splits into multiple messages if it exceeds Discord's 2000-character limit)
    current_message = "**📋 All Pending Tasks by Channel**\n\n"
    for section in report_sections:
        if len(current_message) + len(section) + 2 > 2000:
            await ctx.send(current_message)
            current_message = section + "\n\n"
        else:
            current_message += section + "\n\n"

    if current_message:
        await ctx.send(current_message)