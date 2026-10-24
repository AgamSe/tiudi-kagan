
async def task_done(ctx):
    finished_tasks = []
    
    # Emojis that mark a task as completed or canceled/ignored
    done_emojis = {'👍'}

    async for msg in ctx.channel.history(limit=10):
        # 1. Ignore bots and commands
        if msg.author.bot or msg.content.startswith(ctx.prefix):
            continue

        # 2. Skip if the message has a thumbs up OR an X reaction
        if not any(str(reaction.emoji) in done_emojis for reaction in msg.reactions):
            continue

        # 3. Clean up the message text (replace line breaks with spaces)
        clean_content = msg.content.replace("\n", " ").strip()
        if not clean_content:
            clean_content = "[Attachment / No text]"
            
        preview = clean_content[:50] + "..." if len(clean_content) > 50 else clean_content

        # Put the link on static text (or paste msg.jump_url directly) so user text never breaks it
        task_entry = f"• **[Jump to finished task]({msg.jump_url})** — {preview} (Requested by {msg.author.mention})"
        finished_tasks.append(task_entry)

    if finished_tasks:
        finished_tasks.reverse()
        response = "**📋 finished Tasks:**\n" + "\n".join(finished_tasks)
        await ctx.send(response)
    else:
        await ctx.send("🎉 All tasks in the last 100 messages are complete!")