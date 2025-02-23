# 📌 NexusRadioBot - Komplette Installationsanleitung  

## 🛠️ Voraussetzungen  
- 💻 **Windows-Server oder PC**  
- 🐍 **Python** (mindestens Version 3.10) → [Download](https://www.python.org/downloads/)  
- 🎵 **FFmpeg** für Audio-Streaming → [Download](https://ffmpeg.org/download.html)  
- 🔄 **NSSM** (Non-Sucking Service Manager) für Autostart als Windows-Dienst → [Download](https://nssm.cc/download)  

---

## 🔧 1️⃣ Bot im Discord Developer Portal erstellen  
1. Gehe zum [Discord Developer Portal](https://discord.com/developers/applications).  
2. Klicke auf **"New Application"** und gib einen Namen ein.  
3. Navigiere zu **"Bot"** → **"Add Bot"**.  
4. Klicke auf **"Reset Token"**, kopiere ihn und speichere ihn sicher.  

### ➤ **Berechtigungen setzen**  
1. Gehe zu **OAuth2 > URL Generator**.  
2. Aktiviere **"bot"** unter **Scopes**.  
3. Setze folgende **Bot Permissions**:  
   - ✅ **Connect**  
   - ✅ **Speak**  
   - ✅ **Use Voice Activity**  
4. Kopiere die generierte URL und lade den Bot auf deinen Server ein.  

### ➤ **Intents aktivieren**  
1. Gehe zu **"Bot"** im Developer Portal.  
2. Aktiviere unter **Privileged Gateway Intents**:  
   - ✅ **Presence Intent**  
   - ✅ **Server Members Intent**  
   - ✅ **Message Content Intent**  
3. Klicke auf **"Save Changes"**.  

---

## 💾 2️⃣ Installation der Abhängigkeiten  
### **Python-Pakete installieren**  
Öffne die **Eingabeaufforderung (cmd)** und gib folgendes ein:  
```sh
pip install nextcord nextcord[voice]
```  

### **FFmpeg installieren & konfigurieren**  
1. Lade FFmpeg von [hier](https://ffmpeg.org/download.html) herunter.  
2. Entpacke es in ein Verzeichnis (z. B. `C:\ffmpeg`).  
3. Kopiere den Pfad zu `ffmpeg.exe` (z. B. `C:\ffmpeg\bin\ffmpeg.exe`).  

---

## 🚀 3️⃣ Bot-Code (`NexusRadioBot.py`) erstellen  
Erstelle eine Datei **`NexusRadioBot.py`** und füge folgenden Code ein:  
```python
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
```  

✏️ **Ersetze `DEIN_BOT_TOKEN` mit deinem Token** und **stelle sicher, dass `FFMPEG_PATH` korrekt ist!**  

---

## 🖥️ 4️⃣ Start-/Stop-Skript (`NexusRadioBot.bat`)  
Erstelle eine Datei **`NexusRadioBot.bat`** und füge folgenden Code ein:  
```bat
@echo off
title Nexus Radio Bot
chcp 65001 >nul
cd /d %~dp0
set BOT_SCRIPT=NexusRadioBot.py

:MENU
cls
echo ============================
echo      Nexus Radio Bot
echo ============================
echo [1] Starten
echo [2] Stoppen
echo [3] Beenden
echo ============================
set /p choice=Bitte eine Option waehlen: 

if "%choice%"=="1" (
    echo Starte den Bot...
    start "NexusRadioBot" cmd /c python %BOT_SCRIPT%
    echo Bot läuft nun.
    timeout /t 3 >nul
    goto MENU
)

if "%choice%"=="2" (
    echo Stoppe den Bot...
    for /f "tokens=2 delims= " %%A in ('tasklist ^| findstr /i "python.exe"') do taskkill /PID %%A /F
    echo Bot wurde gestoppt.
    timeout /t 2 >nul
    goto MENU
)

if "%choice%"=="3" (
    echo Beende das Programm...
    exit
)

echo Ungültige Eingabe, bitte erneut versuchen.
timeout /t 2 >nul
goto MENU
```  

📌 **Speichere die Datei als `NexusRadioBot.bat`** und führe sie aus, um den Bot zu starten oder zu stoppen.  

---

## 🔄 5️⃣ Bot als Windows-Dienst mit NSSM einrichten  
### **📥 NSSM herunterladen & installieren**  
1. Lade NSSM von [hier](https://nssm.cc/download) herunter.  
2. Entpacke es in einen Ordner, z. B. `C:\nssm`.  

### **📌 Bot als Dienst einrichten**  
Öffne **CMD als Administrator** und gib folgendes ein:  
```sh
C:\nssm\nssm.exe install NexusRadioBot
```
Ein Fenster öffnet sich:  
1. **Application** → Bei **Path** den Pfad zur `python.exe` eingeben (z. B. `C:\Python311\python.exe`).  
2. **Arguments** → `NexusRadioBot.py` eintragen.  
3. **Startup Type** auf **"Automatic"** setzen.  
4. Auf **"Install Service"** klicken.  

### **✅ Dienst starten/stoppen**  
Um den Bot zu starten:  
```sh
net start NexusRadioBot
```
Um den Bot zu stoppen:  
```sh
net stop NexusRadioBot
```
Um den Dienst zu entfernen:  
```sh
C:\nssm\nssm.exe remove NexusRadioBot confirm
```

---

## ❓ 6️⃣ Wo müssen die Befehle eingegeben werden?  
- **Die Befehle `!join` und `!leave` müssen in einem Discord-Textkanal eingegeben werden!**  
- Der Bot **muss auf dem Server sein** und **die Berechtigungen haben**, um Sprachnachrichten zu senden.  

---

## ✅ 7️⃣ Bot starten  
1️⃣ **Doppelklicke** `NexusRadioBot.bat` oder starte den Dienst mit `net start NexusRadioBot`.  
2️⃣ Schreibe `!join` in einen **Textkanal**, um den Bot in den Sprachkanal zu holen.  
3️⃣ Der Bot spielt **bigFM** ab.  
4️⃣ Schreibe `!leave`, damit der Bot den Kanal verlässt.  

Falls Probleme auftreten, überprüfe die **Fehlermeldungen** oder frage im Support!  
 
