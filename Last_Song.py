import requests
import time

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

    data = response.json()
    
    # Annahme: Wir interessieren uns für den ersten Eintrag in der API-Antwort
    first_entry = next(iter(data.values()), None)
    if first_entry:
        artist = first_entry.get("artist_name")
        title = first_entry.get("song_title")
        cover_url = first_entry.get("covers", {}).get("cover_art_url_xs")
        return artist, title, cover_url

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
    
    if response.status_code == 204:
        print(f"🎵 Song gesendet: {artist} - {title}")
    else:
        print(f"❌ Fehler beim Senden: {response.status_code}")

if __name__ == "__main__":
    last_song = None
    
    while True:
        artist, title, cover_url = get_current_song()
        if artist and title:
            current_song = f"{artist} - {title}"
            if current_song != last_song:  # Nur posten, wenn sich der Song geändert hat
                send_to_discord(artist, title, cover_url)
                last_song = current_song
        
        time.sleep(60)  # Alle 60 Sekunden prüfen
