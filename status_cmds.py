from load_students import load_students


async def default_status(ctx):
    pending_tasks = []
    
    # Emojis that mark a task as completed or canceled/ignored
    skip_emojis = {'👍', '❌', '✖️'}

    async for msg in ctx.channel.history(limit=100):
        # 1. Ignore bots and commands
        if msg.author.bot or msg.content.startswith(ctx.prefix):
            continue

        # 2. Skip if the message has a thumbs up OR an X reaction
        if any(str(reaction.emoji) in skip_emojis for reaction in msg.reactions):
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
