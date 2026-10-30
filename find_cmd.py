import discord

async def find(ctx, target_channel: discord.TextChannel):
    matching_messages = []
    
    try:
        # limit=500 scans the last 500 messages. 
        # You can use limit=None to scan the entire channel, but it will be slow for large channels.
        async for msg in ctx.channel.history(limit=500):
            # Check if the target channel is present in the message's channel mentions
            if target_channel in msg.channel_mentions:
                # BAD CODE TODO fix this (don't just look for keywords)
                if msg.content.startswith(ctx.prefix) or ('Messages' in msg.content) or ('Scanning' in msg.content):
                    continue
                
                # Format the message for the list
                first_line = msg.content.split("\n")[0].strip()
                if not first_line:
                    first_line = "[Attachment / No text]"
                preview = first_line[:50] + "..." if len(first_line) > 50 else first_line
                
                entry = f"• **[Jump]({msg.jump_url})** — {preview}"
                matching_messages.append(entry)
                
    except discord.errors.Forbidden:
        await ctx.send(f"❌ I don't have permission to read the history of {ctx.channel.mention}.")
        return

    # If no matches were found
    if not matching_messages:
        await ctx.send(f"ℹ️ No messages in {ctx.channel.mention} referenced that channel.")
        return
    
    # Format and send the results, splitting if it exceeds Discord's 2,000 character limit
    matching_messages.reverse() # Oldest to newest
    current_response = f"**🔗 Messages in {ctx.channel.mention} that reference {target_channel.mention}:**\n\n"
    
    for entry in matching_messages:
        if len(current_response) + len(entry) + 1 > 2000:
            await ctx.send(current_response)
            current_response = entry + "\n"
        else:
            current_response += entry + "\n"

    if current_response:
        await ctx.send(current_response)