# 🎵 NexusRadioBot - Discord Radio Bot  

Ein einfacher Discord-Radio-Bot, der automatisch **BigFM** oder einen anderen gewünschten Stream in einen Sprachkanal spielt.  
Mit Unterstützung für **Slash-Commands** und **automatischen Neustart** via NSSM.  

---

## 📌 **Features**  
✅ Spielt automatisch einen **Radio-Stream** in einen bestimmten Voice-Channel  
✅ **Slash-Commands** für einfache Steuerung (`/radioon`, `/radiooff`)  
✅ **Automatischer Neustart** des Bots mit **NSSM** (Windows-Dienst)  
✅ **FFmpeg** für stabile Audio-Wiedergabe  

---

## 🚀 **1. Bot im Discord Developer Portal erstellen**  

Bevor du den Bot starten kannst, musst du ihn bei Discord registrieren.  

### **1️⃣ Developer Portal öffnen**  
1. **Gehe zum** [Discord Developer Portal](https://discord.com/developers/applications)  
2. Klicke auf **"New Application"**  
3. Gib einen Namen ein (z. B. `NexusRadioBot`) und klicke auf **"Create"**  

---

### **2️⃣ Bot erstellen**  
1. Wähle links den Reiter **"Bot"**  
2. Klicke auf **"Add Bot"** → **Bestätige mit "Yes, do it!"**  
3. Dein Bot wurde erfolgreich erstellt! 🎉  

🔹 **Optional:** Ändere den **Bot-Avatar** und Namen, wenn gewünscht.  

---

### **3️⃣ Berechtigungen setzen & Bot-Link generieren**  
Damit der Bot richtig funktioniert, muss er bestimmte Berechtigungen haben.  

1. Gehe zu **OAuth2** → **"URL Generator"**  
2. Setze ein Häkchen bei:  
   ✅ `bot`  
   ✅ `applications.commands`  

3. Scrolle nach unten und wähle **diese Berechtigungen**:  

🔹 **Berechtigungen für den Bot:**  
- ✅ `Connect` (Erlaubt das Betreten von Sprachkanälen)  
- ✅ `Speak` (Erlaubt das Abspielen von Sound)  
- ✅ `Use Slash Commands` (Ermöglicht die Nutzung von `/radioon`)  

4. Scrolle nach unten und kopiere den **generierten Einladungslink**  
5. Öffne den Link in deinem Browser und **füge den Bot deinem Discord-Server hinzu**  

✅ **Jetzt ist dein Bot auf dem Server!** 🎉  

---

## 💾 **2. Installation der benötigten Programme**  

Damit der Bot funktioniert, müssen einige Programme installiert werden.  

### **1️⃣ Python installieren**  
1. Lade **Python 3.10+** herunter: [Download Python](https://www.python.org/downloads/)  
2. Während der Installation **"Add Python to PATH"** aktivieren  
3. Nach der Installation prüfen, ob Python installiert ist:  
   ```sh
   python --version
   ```

---

### **2️⃣ FFmpeg installieren**  
1. Lade **FFmpeg** herunter: [Download FFmpeg](https://ffmpeg.org/download.html)  
2. Entpacke die Datei nach `C:\ffmpeg`  
3. Setze den **Pfad zur `ffmpeg.exe`** im Bot-Skript:  
   ```python
   FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
   ```

---

### **3️⃣ Abhängigkeiten installieren**  
Nachdem **Python** installiert wurde, installiere die benötigten Pakete mit:  
```sh
pip install -r requirements.txt
```
Falls die Datei nicht existiert, installiere die Pakete manuell:  
```sh
pip install nextcord asyncio
```

---

## 🎮 **3. Bot konfigurieren & starten**  

### **1️⃣ `bot.py` einrichten**  
Öffne `bot.py` und trage deine Werte ein:  
```python
TOKEN = "DEIN_BOT_TOKEN"
GUILD_ID = 123456789012345678  # Deine Discord-Server-ID
VOICE_CHANNEL_ID = 987654321098765432  # Die ID des Sprachkanals
```

---

### **2️⃣ Bot starten**  
```sh
python bot.py
```
Wenn alles richtig eingestellt ist, erscheint:  
```
Eingeloggt als NexusRadioBot
Slash-Commands synchronisiert!
```

✅ **Jetzt kannst du `/radioon` eingeben, um Musik zu starten!**  

---

## 🛠 **4. Bot als Windows-Dienst mit NSSM einrichten**  
Damit der Bot **immer läuft**, richten wir ihn als **Windows-Dienst** ein.  

### **1️⃣ NSSM herunterladen**  
🔗 **[Download NSSM](https://nssm.cc/download)**  

1. Entpacke die Datei nach `C:\nssm`  
2. Öffne die **Eingabeaufforderung als Administrator**  
3. Erstelle den Dienst:  
   ```sh
   C:\nssm\win64\nssm.exe install NexusRadioBot
   ```
4. Ein **Fenster** öffnet sich:  
   - **Path**: Wähle die `python.exe` (z. B. `C:\Python39\python.exe`)  
   - **Startup Directory**: Der Pfad, in dem sich `bot.py` befindet  
   - **Arguments**: `bot.py`  
5. Klicke auf **"Install service"**  

---

### **2️⃣ Dienst starten**  
```sh
C:\nssm\win64\nssm.exe start NexusRadioBot
```
✅ **Jetzt läuft dein Bot als Windows-Dienst!** 🎉  

---

### **3️⃣ Dienst automatisch neustarten lassen**  
Falls der Bot abstürzt, kann NSSM ihn automatisch neu starten:  
```sh
C:\nssm\win64\nssm.exe set NexusRadioBot AppRestartDelay 3600000
```
Dadurch startet der Dienst alle **60 Minuten neu**.  

---

## ❌ **5. Bot stoppen & entfernen (Falls nötig)**  

### **1️⃣ Dienst stoppen**  
```sh
C:\nssm\win64\nssm.exe stop NexusRadioBot
```

### **2️⃣ Dienst entfernen**  
```sh
C:\nssm\win64\nssm.exe remove NexusRadioBot confirm
```

---

## 🆘 **6. Häufige Fehler & Lösungen**  

### **1️⃣ Bot joint nicht in den Voice-Channel**  
✅ Stelle sicher, dass der Bot **Berechtigungen** hat (`Connect`, `Speak`).  
✅ Prüfe, ob die **Channel-ID** korrekt eingetragen ist.  
✅ Starte den Bot mit `python bot.py`, um Fehler zu sehen.  

### **2️⃣ FFmpeg nicht gefunden**  
✅ Prüfe, ob `ffmpeg.exe` in `C:\ffmpeg\bin\` liegt.  
✅ Stelle sicher, dass der Pfad in `bot.py` richtig ist:  
   ```python
   FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
   ```

### **3️⃣ Slash-Commands funktionieren nicht**  
✅ Warte einige Minuten, da Discord die Befehle synchronisieren muss.  
✅ Prüfe mit `@client.event async def on_ready()`, ob `sync_all_application_commands()` aufgerufen wird.  

---

## 🔗 **7. Links & Ressourcen**  

- **GitHub Repository**: [NexusRadioBot](https://github.com/BloodDragon2580/NexusRadioBot)  
- **Python Download**: [python.org](https://www.python.org/downloads/)  
- **FFmpeg Download**: [ffmpeg.org](https://ffmpeg.org/download.html)  
- **NSSM Download**: [nssm.cc](https://nssm.cc/download)  
- **Discord Developer Portal**: [discord.com/developers](https://discord.com/developers/applications)  

---

✅ **Jetzt ist dein NexusRadioBot vollständig eingerichtet und läuft automatisch!** 🎉  
