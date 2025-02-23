import nextcord  # Nextcord-Bibliothek für Discord-Bots
from nextcord.ext import commands  # Befehle aus der Nextcord-Erweiterung
import asyncio  # Für asynchrone Prozesse

# Bot-Token (Ersetze mit deinem echten Token!)
TOKEN = ""

# IDs für Server (Guild) und Sprachkanal
GUILD_ID = 123456789  # Deine Server-ID
VOICE_CHANNEL_ID = 123456789  # Sprachkanal-ID

# Stream-URL (Hier: BigFM)
RADIO_STREAM_URL = "http://streams.bigfm.de/bigfm-deutschland-128-mp3"  # Stream-URL

# Pfad zur ffmpeg.exe (Falls nicht im Systempfad, hier anpassen)
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # Pfad zu ffmpeg.exe

# Nextcord-Intents (Erlaubt dem Bot, Nachrichteninhalte zu lesen)
intents = nextcord.Intents.default()
intents.message_content = True

# Erstellen des Bot-Clients mit einem Befehlspräfix (wird bei Slash-Commands nicht benötigt)
client = commands.Bot(command_prefix="!", intents=intents)

# Funktion zum Verbinden des Bots mit dem Sprachkanal und Starten des Streams
async def connect_and_stream():
    """Verbindet den Bot mit dem angegebenen Sprachkanal und startet den Stream."""
    guild = client.get_guild(GUILD_ID)  # Server abrufen
    if not guild:
        print("Fehler: Server nicht gefunden!")
        return

    channel = guild.get_channel(VOICE_CHANNEL_ID)  # Sprachkanal abrufen
    if not channel:
        print("Fehler: Sprachkanal nicht gefunden!")
        return

    try:
        if not client.voice_clients:  # Prüft, ob der Bot nicht bereits verbunden ist
            vc = await channel.connect()  # Verbindet mit dem Sprachkanal
            vc.play(nextcord.FFmpegPCMAudio(RADIO_STREAM_URL, executable=FFMPEG_PATH, 
                   options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
            print(f"Bot spielt jetzt {RADIO_STREAM_URL} in {channel.name}")  # Debug-Info
    except Exception as e:
        print(f"Fehler beim Verbinden mit dem Sprachkanal: {e}")

# Event: Wird ausgeführt, wenn der Bot gestartet ist
@client.event
async def on_ready():
    print(f"Eingeloggt als {client.user}")  # Zeigt den Bot-Namen in der Konsole
    
    # Slash-Commands automatisch synchronisieren
    await client.sync_all_application_commands()
    print("Slash-Commands synchronisiert!")

    # Bot beim Start automatisch verbinden
    await connect_and_stream()

# Slash-Command: Startet den Radio-Stream manuell
@client.slash_command(guild_ids=[GUILD_ID], description="Starte den Radio-Stream")
async def radioon(interaction: nextcord.Interaction):
    """Befehl zum Verbinden des Bots mit einem bestimmten Sprachkanal und Starten des Streams."""
    await connect_and_stream()
    await interaction.response.send_message("BigFM wird jetzt abgespielt.")

# Slash-Command: Stoppt den Stream und verlässt den Sprachkanal
@client.slash_command(guild_ids=[GUILD_ID], description="Stoppe den Radio-Stream")
async def radiooff(interaction: nextcord.Interaction):
    """Befehl zum Stoppen des Streams und Verlassen des Sprachkanals."""
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Bot hat den Kanal verlassen.")
    else:
        await interaction.response.send_message("Ich bin in keinem Sprachkanal.")

# Startet den Bot mit dem Token
client.run(TOKEN)
