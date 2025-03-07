import requests
import time
import os
import sys

# Deine Webhook-URL hier einfügen
WEBHOOK_URL = "Your_Discord_Webhook"

# BigFM API-Endpunkt
BIGFM_API_URL = "https://www.bigfm.de/streams/api"

def get_current_song():
    """Holt den aktuell laufenden Song von der BigFM API."""
    response = requests.get(BIGFM_API_URL)
    if response.status_code != 200:
        print("Fehler beim Abrufen der BigFM API")
        return None, None, None

    try:
        data = response.json()
        
        # API gibt nummerierte Keys zurück (z. B. "1", "2", "3"), wir holen den ersten Eintrag
        first_key = next(iter(data.keys()), None)
        first_entry = data.get(first_key, {})

        if isinstance(first_entry, dict):  # Sicherstellen, dass es ein Dictionary ist
            artist = first_entry.get("artist_name", "Unbekannt")
            title = first_entry.get("song_title", "Unbekannt")
            cover_url = first_entry.get("covers", {}).get("cover_art_url_xs", None)
            return artist, title, cover_url

    except Exception as e:
        print(f"Fehler beim Verarbeiten der API-Daten: {e}")

    print("Keine Song-Daten gefunden")
    return None, None, None

def send_to_discord(artist, title, cover_url):
    """Sendet den Song als Discord-Embed."""
    embed = {
        "title": f"🎶 Aktuell läuft: {title}",
        "description": f"🎤 **Künstler:** {artist}",
        "color": 65280  # Grün als Embed-Farbe
    }
    
    if cover_url:
        embed["thumbnail"] = {"url": cover_url}
    
    payload = {"embeds": [embed]}
    response = requests.post(WEBHOOK_URL, json=payload)
    
    if response.status_code == 204 or response.status_code == 200:
        print(f"🎵 Song gesendet: {artist} - {title}")
    else:
        print(f"❌ Fehler beim Senden: {response.status_code}")

if __name__ == "__main__":
    last_song = None
    
    while True:
        try:
            artist, title, cover_url = get_current_song()
            if artist and title:
                current_song = f"{artist} - {title}"
                if current_song != last_song:  # Nur posten, wenn sich der Song geändert hat
                    send_to_discord(artist, title, cover_url)
                    last_song = current_song
            time.sleep(60)  # Alle 60 Sekunden prüfen
        
        except Exception as e:
            print(f"Fehler im Hauptprozess: {e}")
            print("Neustart des Scripts in 5 Sekunden...")
            time.sleep(5)  # Warte 5 Sekunden, bevor das Script neu gestartet wird
            # Optional kannst du auch das Script manuell neu starten, indem du es direkt erneut ausführst:
            os.execv(sys.executable, ['python'] + sys.argv)
