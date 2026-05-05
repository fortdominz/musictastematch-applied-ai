import random
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

# Rule-based feature lookup by genre and mood
GENRE_FEATURES = {
    "lofi":       {"energy": 0.35, "tempo_bpm": 80,  "acousticness": 0.80, "instrumentalness": 0.70, "danceability": 0.55},
    "electronic": {"energy": 0.85, "tempo_bpm": 128, "acousticness": 0.05, "instrumentalness": 0.60, "danceability": 0.85},
    "rock":       {"energy": 0.85, "tempo_bpm": 135, "acousticness": 0.15, "instrumentalness": 0.20, "danceability": 0.65},
    "metal":      {"energy": 0.95, "tempo_bpm": 155, "acousticness": 0.05, "instrumentalness": 0.30, "danceability": 0.55},
    "pop":        {"energy": 0.75, "tempo_bpm": 118, "acousticness": 0.20, "instrumentalness": 0.05, "danceability": 0.80},
    "jazz":       {"energy": 0.40, "tempo_bpm": 95,  "acousticness": 0.75, "instrumentalness": 0.50, "danceability": 0.55},
    "classical":  {"energy": 0.30, "tempo_bpm": 80,  "acousticness": 0.95, "instrumentalness": 0.90, "danceability": 0.30},
    "ambient":    {"energy": 0.25, "tempo_bpm": 70,  "acousticness": 0.85, "instrumentalness": 0.85, "danceability": 0.35},
    "folk":       {"energy": 0.40, "tempo_bpm": 95,  "acousticness": 0.80, "instrumentalness": 0.25, "danceability": 0.50},
    "country":    {"energy": 0.60, "tempo_bpm": 105, "acousticness": 0.55, "instrumentalness": 0.10, "danceability": 0.65},
    "reggae":     {"energy": 0.55, "tempo_bpm": 95,  "acousticness": 0.45, "instrumentalness": 0.20, "danceability": 0.75},
    "synthwave":  {"energy": 0.70, "tempo_bpm": 115, "acousticness": 0.05, "instrumentalness": 0.55, "danceability": 0.70},
    "indie pop":  {"energy": 0.65, "tempo_bpm": 118, "acousticness": 0.35, "instrumentalness": 0.10, "danceability": 0.70},
    "dream pop":  {"energy": 0.50, "tempo_bpm": 100, "acousticness": 0.45, "instrumentalness": 0.35, "danceability": 0.55},
    "pop rock":   {"energy": 0.78, "tempo_bpm": 120, "acousticness": 0.20, "instrumentalness": 0.10, "danceability": 0.72},
    "hip hop":    {"energy": 0.75, "tempo_bpm": 95,  "acousticness": 0.15, "instrumentalness": 0.10, "danceability": 0.85},
    "indie folk": {"energy": 0.40, "tempo_bpm": 90,  "acousticness": 0.75, "instrumentalness": 0.20, "danceability": 0.50},
}

MOOD_FEATURES = {
    "happy":     {"valence": 0.85, "speechiness": 0.06, "liveness": 0.14},
    "chill":     {"valence": 0.55, "speechiness": 0.03, "liveness": 0.10},
    "relaxed":   {"valence": 0.60, "speechiness": 0.03, "liveness": 0.10},
    "intense":   {"valence": 0.45, "speechiness": 0.07, "liveness": 0.18},
    "energetic": {"valence": 0.75, "speechiness": 0.08, "liveness": 0.20},
    "aggressive":{"valence": 0.30, "speechiness": 0.08, "liveness": 0.22},
    "moody":     {"valence": 0.35, "speechiness": 0.04, "liveness": 0.12},
    "sad":       {"valence": 0.25, "speechiness": 0.04, "liveness": 0.10},
    "romantic":  {"valence": 0.70, "speechiness": 0.04, "liveness": 0.12},
    "focused":   {"valence": 0.55, "speechiness": 0.03, "liveness": 0.09},
    "peaceful":  {"valence": 0.65, "speechiness": 0.02, "liveness": 0.08},
    "nostalgic": {"valence": 0.50, "speechiness": 0.04, "liveness": 0.14},
    "dreamy":    {"valence": 0.65, "speechiness": 0.03, "liveness": 0.10},
    "hopeful":   {"valence": 0.75, "speechiness": 0.05, "liveness": 0.13},
    "laid-back": {"valence": 0.60, "speechiness": 0.04, "liveness": 0.11},
}

DEFAULT_FEATURES = {
    "energy": 0.55, "tempo_bpm": 100, "acousticness": 0.40,
    "instrumentalness": 0.30, "danceability": 0.60,
    "valence": 0.55, "speechiness": 0.05, "liveness": 0.12
}


def get_features(genre: str, mood: str) -> dict:
    """Look up audio features for a genre/mood combination with slight variation."""
    genre_key = genre.lower()
    mood_key = mood.lower()

    # Try exact match first, then partial match
    genre_feats = GENRE_FEATURES.get(genre_key, {})
    if not genre_feats:
        for key in GENRE_FEATURES:
            if key in genre_key or genre_key in key:
                genre_feats = GENRE_FEATURES[key]
                break

    mood_feats = MOOD_FEATURES.get(mood_key, {})

    def vary(value, amount=0.08):
        return round(min(1.0, max(0.0, value + random.uniform(-amount, amount))), 3)

    def vary_tempo(value, amount=10):
        return round(min(200, max(60, value + random.uniform(-amount, amount))), 1)

    return {
        "energy": vary(genre_feats.get("energy", DEFAULT_FEATURES["energy"])),
        "tempo_bpm": vary_tempo(genre_feats.get("tempo_bpm", DEFAULT_FEATURES["tempo_bpm"])),
        "acousticness": vary(genre_feats.get("acousticness", DEFAULT_FEATURES["acousticness"])),
        "instrumentalness": vary(genre_feats.get("instrumentalness", DEFAULT_FEATURES["instrumentalness"])),
        "danceability": vary(genre_feats.get("danceability", DEFAULT_FEATURES["danceability"])),
        "valence": vary(mood_feats.get("valence", DEFAULT_FEATURES["valence"])),
        "speechiness": vary(mood_feats.get("speechiness", DEFAULT_FEATURES["speechiness"]), 0.02),
        "liveness": vary(mood_feats.get("liveness", DEFAULT_FEATURES["liveness"]), 0.04),
    }


def fetch_songs(query: str, genre: str, mood: str, limit: int = 10) -> list:
    """Search Spotify for songs and assign features instantly from lookup table."""

    results = sp.search(q=query, type="track", limit=limit)
    tracks = results["tracks"]["items"]

    if not tracks:
        return []

    songs = []
    for track in tracks:
        features = get_features(genre, mood)  # called per song now
        song = {
            "id": track["id"],
            "title": track["name"],
            "artist": track["artists"][0]["name"],
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
    """Build a live catalog of songs from Spotify with rule-based audio features."""

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