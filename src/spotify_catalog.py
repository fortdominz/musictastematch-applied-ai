import os
import json
import re
import ollama
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))


def estimate_features(title: str, artist: str, genre: str, mood: str) -> dict:
    """Use Llama 3.2 to estimate audio features for a song based on its metadata."""

    prompt = f"""You are a music analyst. Estimate the audio features for this song based on its title, artist, genre, and mood.

Song: "{title}" by {artist}
Genre: {genre}
Mood: {mood}

Return ONLY a valid JSON object with exactly these keys and float values between 0.0 and 1.0 (tempo_bpm between 60 and 200):
{{
    "energy": 0.0 to 1.0,
    "tempo_bpm": 60 to 200,
    "valence": 0.0 to 1.0,
    "danceability": 0.0 to 1.0,
    "acousticness": 0.0 to 1.0,
    "instrumentalness": 0.0 to 1.0,
    "speechiness": 0.0 to 1.0,
    "liveness": 0.0 to 1.0
}}

Do not include any explanation, markdown, or code blocks. Return only the raw JSON object."""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response["message"]["content"].strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    return json.loads(raw)


def fetch_songs(query: str, genre: str, mood: str, limit: int = 10) -> list:
    """Search Spotify for songs and estimate their audio features using Llama."""

    results = sp.search(q=query, type="track", limit=limit)
    tracks = results["tracks"]["items"]

    if not tracks:
        return []

    songs = []
    for track in tracks:
        title = track["name"]
        artist = track["artists"][0]["name"]

        try:
            features = estimate_features(title, artist, genre, mood)
        except Exception as e:
            print(f"   ⚠️ Could not estimate features for {title}: {e}")
            continue

        song = {
            "id": track["id"],
            "title": title,
            "artist": artist,
            "genre": genre,
            "mood": mood,
            "energy": features["energy"],
            "tempo_bpm": features["tempo_bpm"],
            "valence": features["valence"],
            "danceability": features["danceability"],
            "acousticness": features["acousticness"],
            "instrumentalness": features["instrumentalness"],
            "speechiness": features["speechiness"],
            "liveness": features["liveness"],
        }
        songs.append(song)

    return songs


def build_catalog(user_genre: str, user_mood: str) -> list:
    """Build a live catalog of songs from Spotify with AI-estimated audio features."""

    print(f"   Searching Spotify for {user_genre} {user_mood} songs...")
    primary = fetch_songs(
        query=f"{user_genre} {user_mood}",
        genre=user_genre,
        mood=user_mood,
        limit=8
    )

    print(f"   Searching for related {user_genre} songs...")
    secondary = fetch_songs(
        query=f"{user_genre} music",
        genre=user_genre,
        mood=user_mood,
        limit=5
    )

    # Combine and deduplicate by track ID
    all_songs = primary + secondary
    seen = set()
    unique_songs = []
    for song in all_songs:
        if song["id"] not in seen:
            seen.add(song["id"])
            unique_songs.append(song)

    return unique_songs