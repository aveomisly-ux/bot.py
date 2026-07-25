import discord
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_TOKEN')
MY_USER_ID = int(os.getenv('MY_USER_ID', '0'))

# Validate required environment variables
if not BOT_TOKEN or MY_USER_ID == 0:
    raise ValueError("DISCORD_TOKEN and MY_USER_ID must be set in .env file")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)

# Comprehensive keyword filtering arrays
FLAG_CATEGORIES = {
    "NSFW / Gore": [
        "nsfw", "porn", "xxx", "hentai", "erotic", "nudity", "leaked",
        "gore", "bloody", "mutilate", "behead", "decapitation", "corpse",
        "dismember", "slaughter", "torture", "suicide", "self-harm"
    ],
    "Politics / War": [
        "election", "democrat", "republican", "biden", "trump", "harris",
        "senate", "congress", "parliament", "libertarian", "socialist",
        "war", "military", "invasion", "missile", "bombing", "casualty",
        "geopolitics", "propaganda", "sanctions", "ceasefire", "nato"
    ],
    "Discrimination": [
        "slur", "racist", "sexist", "xenophobe", "hate speech", "bigot",
        "misogyny", "homophobia", "transphobia", "antisemitism", "supremacist"
    ],
    "Debated / Controversial": [
        "abortion", "pro-life", "pro-choice", "fetus", "planned parenthood",
        "immigration", "border wall", "deportation", "asylum seeker", "refugee",
        "religion", "atheist", "god", "jesus", "allah", "prophet", "church", 
        "mosque", "bible", "quran", "cult"
    ]
}

@client.event
async def on_ready():
    print(f"✅ Flagged Message Alert Bot successfully connected as {client.user}")
    print(f"📍 Monitoring for flagged messages...")

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    content_lower = message.content.lower()
    triggered_categories = []

    # Check text against categories using word boundaries
    for category, keywords in FLAG_CATEGORIES.items():
        for word in keywords:
            pattern = rf"\b{re.escape(word)}\b"
            if re.search(pattern, content_lower):
                triggered_categories.append(category)
                break

    # Send alert to your DMs if triggers were found
    if triggered_categories:
        try:
            # Fetch your user profile
            target_user = await client.fetch_user(MY_USER_ID)
            
            if target_user:
                embed = discord.Embed(
                    title="⚠️ Flagged Message Alert",
                    color=discord.Color.red()
                )
                embed.add_field(name="User", value=message.author.mention, inline=True)
                embed.add_field(name="Channel", value=message.channel.mention, inline=True)
                embed.add_field(name="Categories", value=", ".join(triggered_categories), inline=False)
                embed.add_field(name="Content", value=message.content[:1024], inline=False)  # Truncate long messages
                
                # Send DM
                await target_user.send(embed=embed)
                print(f"📧 Alert sent for message from {message.author} in {message.channel}")
        except discord.Forbidden:
            print(f"❌ Error: The bot cannot DM user ID {MY_USER_ID}. Check privacy settings.")
        except discord.HTTPException as e:
            print(f"❌ Failed to send DM due to an HTTP error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

# Launch the bot
if __name__ == "__main__":
    try:
        client.run(BOT_TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
