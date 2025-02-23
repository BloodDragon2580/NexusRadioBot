import nextcord
from nextcord.ext import commands
import asyncio

TOKEN = "DEIN_BOT_TOKEN"
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
STREAM_URL = "https://streams.bigfm.de/bigfm-deutschland-128-mp3"

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot ist eingeloggt als {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        vc.play(nextcord.FFmpegPCMAudio(FFMPEG_PATH, options=f"-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -i {STREAM_URL}"))
        await ctx.send("🎵 **BigFM wird jetzt abgespielt!**")
    else:
        await ctx.send("❌ **Du musst in einem Sprachkanal sein!**")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("👋 **Bot hat den Kanal verlassen!**")
    else:
        await ctx.send("❌ **Ich bin in keinem Sprachkanal!**")

bot.run(TOKEN)
