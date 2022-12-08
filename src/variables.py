import discord

# Replace variables in messages

def variables_replace_target_author(text: str, target: discord.Member, author: discord.Member) -> str:
    """Takes text and replaces variables {{target}} and {{author}} with strings mentioning the target and author members"""
    
    result = text.replace("{{target}}", target.mention)
    result = result.replace("{{author}}", author.mention)

    return result