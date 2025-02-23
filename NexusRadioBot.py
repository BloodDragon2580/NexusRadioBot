import nextcord
from nextcord.ext import commands
import asyncio

# Bot-Token und IDs
TOKEN = ""  # Dein Bot Token
GUILD_ID = 123456789  # Deine Server-ID
VOICE_CHANNEL_ID = 123456789  # Sprachkanal-ID
RADIO_STREAM_URL = "http://streams.bigfm.de/bigfm-deutschland-128-mp3"  # Stream-URL
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # Pfad zu ffmpeg.exe

# Nextcord-Intents
intents = nextcord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    """Wird ausgeführt, wenn der Bot online geht."""
    print(f"Eingeloggt als {client.user}")

    # Server abrufen
    guild = nextcord.utils.get(client.guilds, id=GUILD_ID)
    if not guild:
        print("Fehler: Server nicht gefunden!")
        return

    # Sprachkanal abrufen
    channel = guild.get_channel(VOICE_CHANNEL_ID)
    if not channel:
        print("Fehler: Sprachkanal nicht gefunden!")
        return

    # Prüfen, ob der Bot die Berechtigungen hat
    if not channel.permissions_for(guild.me).connect or not channel.permissions_for(guild.me).speak:
        print("Fehler: Der Bot hat keine Berechtigung, dem Sprachkanal beizutreten oder zu sprechen!")
        return

    # Automatisch verbinden
    await connect_and_stream(channel)

async def connect_and_stream(channel):
    """Verbindet den Bot mit dem Sprachkanal und spielt den Stream."""
    while True:
        try:
            if channel and not client.voice_clients:
                vc = await channel.connect()
                vc.play(nextcord.FFmpegPCMAudio(RADIO_STREAM_URL, executable=FFMPEG_PATH, options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
                print(f"Bot spielt jetzt {RADIO_STREAM_URL} in {channel.name}")
            await asyncio.sleep(600)  # Alle 10 Minuten prüfen, ob der Bot noch verbunden ist
        except Exception as e:
            print(f"Fehler: {e}")
            await asyncio.sleep(10)  # 10 Sekunden warten, dann erneut versuchen

@client.command()
async def radioon(ctx):
    """Befehl zum Starten des Streams, ohne dass der Nutzer in einem Kanal sein muss."""
    guild = ctx.guild
    channel = guild.get_channel(VOICE_CHANNEL_ID)

    if not channel:
        await ctx.send("Fehler: Sprachkanal nicht gefunden!")
        return

    if not channel.permissions_for(guild.me).connect or not channel.permissions_for(guild.me).speak:
        await ctx.send("Fehler: Ich habe keine Berechtigung, dem Sprachkanal beizutreten!")
        return

    await connect_and_stream(channel)
    await ctx.send("BigFM wird jetzt abgespielt.")

@client.command()
async def radiooff(ctx):
    """Befehl zum Stoppen des Streams und Verlassen des Sprachkanals."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bot hat den Kanal verlassen.")
    else:
        await ctx.send("Ich bin in keinem Sprachkanal.")

client.run(TOKEN)
