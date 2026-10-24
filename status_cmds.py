
async def task_status(ctx):
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
        clean_content = msg.content[1:].replace("\n", " ").strip()
        if not clean_content:
            clean_content = "[Attachment / No text]"
            
        preview = clean_content[:50] + "..." if len(clean_content) > 50 else clean_content

        # Put the link on static text (or paste msg.jump_url directly) so user text never breaks it
        task_entry = f"• **[Jump to Task]({msg.jump_url})** — {preview} (Requested by {msg.author.mention})"
        pending_tasks.append(task_entry)

    if pending_tasks:
        pending_tasks.reverse()
        response = "**📋 Pending Tasks:**\n" + "\n".join(pending_tasks)
        await ctx.send(response)
    else:
        await ctx.send("🎉 All tasks in the last 100 messages are complete!")