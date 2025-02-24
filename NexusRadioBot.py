import nextcord  # Nextcord-Bibliothek für Discord-Bots
from nextcord.ext import commands, tasks  # Befehle und Tasks aus der Nextcord-Erweiterung
import asyncio  # Für asynchrone Prozesse

# Bot-Token (Ersetze mit deinem echten Token!)
TOKEN = "DEIN DISCORD TOKEN"

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
    """Verbindet den Bot mit dem Sprachkanal (falls nicht schon verbunden) und startet den Stream."""
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("Fehler: Server nicht gefunden!")
        return

    channel = guild.get_channel(VOICE_CHANNEL_ID)
    if not channel:
        print("Fehler: Sprachkanal nicht gefunden!")
        return

    try:
        # Prüfen, ob der Bot bereits im Sprachkanal ist
        vc = nextcord.utils.get(client.voice_clients, guild=guild)
        
        if not vc:  # Falls nicht verbunden, dann verbinden
            vc = await channel.connect()
        
        # Falls bereits ein Stream läuft, diesen stoppen
        if vc.is_playing():
            vc.stop()

        # Neuen Stream starten
        vc.play(nextcord.FFmpegPCMAudio(RADIO_STREAM_URL, executable=FFMPEG_PATH, 
               options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
        
        # Setzt den Status des Bots auf "Hört BigFM"
        await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="BigFM"))
        
        print(f"Bot spielt jetzt {RADIO_STREAM_URL} in {channel.name}")  # Debug-Info
    except Exception as e:
        print(f"Fehler beim Starten des Streams: {e}")

# Hintergrundaufgabe für das regelmäßige Neustarten des Streams
@tasks.loop(minutes=15)
async def restart_stream():
    """Startet den Stream alle 15 Minuten neu, ohne den Bot aus dem Kanal zu werfen."""
    print("Neustart des Streams...")
    await connect_and_stream()

# Event: Wird ausgeführt, wenn der Bot gestartet ist
@client.event
async def on_ready():
    print(f"Eingeloggt als {client.user}")  # Zeigt den Bot-Namen in der Konsole
    
    # Slash-Commands automatisch synchronisieren
    await client.sync_all_application_commands()
    print("Slash-Commands synchronisiert!")

    # Bot beim Start automatisch verbinden
    await connect_and_stream()

    # Start der Hintergrundaufgabe zum regelmäßigen Neustarten des Streams
    restart_stream.start()

# Slash-Command: Startet den Radio-Stream manuell
@client.slash_command(guild_ids=[GUILD_ID], description="Starte den Radio-Stream")
async def radioon(interaction: nextcord.Interaction):
    """Befehl zum Starten des Streams."""
    await connect_and_stream()
    await interaction.response.send_message("BigFM wird jetzt abgespielt.")

# Slash-Command: Stoppt den Stream, ohne den Bot aus dem Sprachkanal zu werfen
@client.slash_command(guild_ids=[GUILD_ID], description="Stoppe den Radio-Stream")
async def radiooff(interaction: nextcord.Interaction):
    """Befehl zum Stoppen des Streams."""
    vc = nextcord.utils.get(client.voice_clients, guild=interaction.guild)
    if vc and vc.is_playing():
        vc.stop()
        await client.change_presence(activity=None)  # Entfernt den Status
        await interaction.response.send_message("Stream gestoppt.")
    else:
        await interaction.response.send_message("Es läuft gerade kein Stream.")

# Slash-Command: Erzwingt ein erneutes Laden des Streams
@client.slash_command(guild_ids=[GUILD_ID], description="Lädt den Stream neu")
async def radioreload(interaction: nextcord.Interaction):
    """Befehl zum erneuten Verbinden des Streams."""
    await connect_and_stream()
    await interaction.response.send_message("Stream wurde neu geladen.")

# Startet den Bot mit dem Token
client.run(TOKEN)
