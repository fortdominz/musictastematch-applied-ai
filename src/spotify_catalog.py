import random
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from google import genai

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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


def get_mood_features_from_ai(mood: str) -> dict:
    """Ask Gemini to estimate audio feature values for an unknown mood."""
    prompt = f"""You are a music audio feature estimator.

Given the mood "{mood}", return the most musically accurate audio feature values for songs with this mood.

Return ONLY a valid JSON object with exactly these keys and float values:
{{
    "valence": 0.0 to 1.0,
    "speechiness": 0.0 to 0.15,
    "liveness": 0.05 to 0.35
}}

valence = positivity/happiness (0=dark/sad, 1=bright/happy)
speechiness = how much spoken word content (most music is under 0.10)
liveness = how live/concert-like it sounds (studio recordings are under 0.20)

Return only the raw JSON object, no explanation."""
    try:
        response = gemini.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception:
        return {"valence": 0.55, "speechiness": 0.05, "liveness": 0.12}


def get_features(genre: str, mood: str) -> dict:
    """Look up audio features for a genre/mood combination with variation."""
    genre_key = genre.lower()
    mood_key = mood.lower()

    # Try exact match first, then partial match for genre
    genre_feats = GENRE_FEATURES.get(genre_key, {})
    if not genre_feats:
        for key in GENRE_FEATURES:
            if key in genre_key or genre_key in key:
                genre_feats = GENRE_FEATURES[key]
                break

    # Try exact match for mood, then partial match, then ask Gemini
    mood_feats = MOOD_FEATURES.get(mood_key, {})
    if not mood_feats:
        for key in MOOD_FEATURES:
            if key in mood_key or mood_key in key:
                mood_feats = MOOD_FEATURES[key]
                break
    if not mood_feats:
        print(f"   Unknown mood '{mood}' — asking Gemini for feature values...")
        mood_feats = get_mood_features_from_ai(mood)

    def vary(value, amount=0.18):
        return round(min(1.0, max(0.0, value + random.uniform(-amount, amount))), 3)

    def vary_tempo(value, amount=18):
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


def get_artist_seeds(genre: str, mood: str) -> list[str]:
    """Ask Gemini for 5 real artists who represent this genre and mood well."""
    prompt = f"""Name exactly 5 real, well-known music artists who are strongly associated with {genre} music and a {mood} mood/vibe.

Return ONLY a JSON array of artist name strings. Example: ["Artist One", "Artist Two", "Artist Three", "Artist Four", "Artist Five"]
No explanation, no markdown."""
    try:
        response = gemini.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception:
        return []


def validate_and_label_songs(songs: list, user_genre: str, user_mood: str) -> list:
    """Use Gemini to filter mismatched songs and assign realistic per-song genre/mood labels."""
    if not songs:
        return songs

    song_list = "\n".join([
        f"{i+1}. \"{s['title']}\" by {s['artist']}"
        for i, s in enumerate(songs)
    ])

    prompt = f"""You are a strict music catalog validator for a recommender system.

The user wants: {user_genre} music with a {user_mood} mood/vibe.

Songs fetched from Spotify:
{song_list}

For each song, evaluate strictly:
1. Is this artist genuinely known for {user_genre} music? If they are primarily a different genre, mark keep=false.
2. Does the song/artist actually fit a {user_mood} mood?
3. Assign the most accurate real genre and mood labels.

Return ONLY a valid JSON array, one object per song:
[
  {{"index": 1, "keep": true, "genre": "r&b", "mood": "sexy"}},
  {{"index": 2, "keep": false, "genre": "rap", "mood": "aggressive"}}
]

Be strict — it is better to keep fewer good matches than include mismatches.
Respond with ONLY the JSON array, no explanation."""

    try:
        response = gemini.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        labels = json.loads(text.strip())

        result = []
        for entry in labels:
            idx = entry.get("index", 0) - 1
            if 0 <= idx < len(songs):
                if entry.get("keep", True):
                    song = dict(songs[idx])
                    song["genre"] = entry.get("genre", songs[idx]["genre"])
                    song["mood"] = entry.get("mood", songs[idx]["mood"])
                    result.append(song)

        return result if result else songs

    except Exception as e:
        print(f"   ⚠️ Song validation skipped: {e}")
        return songs


def build_catalog(user_genre: str, user_mood: str) -> list:
    """Build a live catalog using artist-seed search + keyword fallback."""

    # Step 1: Ask Gemini for real artists in this genre/mood
    print(f"   Getting artist seeds for {user_genre} / {user_mood}...")
    artists = get_artist_seeds(user_genre, user_mood)
    print(f"   Seeds: {artists}")

    all_songs = []

    # Step 2: Search by artist name — much more genre-accurate than keyword search
    for artist in artists[:4]:
        songs = fetch_songs(
            query=f"artist:{artist}",
            genre=user_genre,
            mood=user_mood,
            limit=3
        )
        all_songs.extend(songs)

    # Step 3: Add a keyword search as supplemental fill
    print(f"   Supplemental search: {user_genre} {user_mood}...")
    supplemental = fetch_songs(
        query=f"{user_genre}",
        genre=user_genre,
        mood=user_mood,
        limit=5
    )
    all_songs.extend(supplemental)

    # Deduplicate by title+artist (catches same song with different IDs)
    seen = set()
    unique_songs = []
    for song in all_songs:
        key = (song["title"].lower().strip(), song["artist"].lower().strip())
        if key not in seen:
            seen.add(key)
            unique_songs.append(song)

    # Step 4: Validate and label with Gemini
    print(f"   Validating {len(unique_songs)} songs with AI...")
    validated = validate_and_label_songs(unique_songs, user_genre, user_mood)
    print(f"   ✅ {len(validated)} songs passed validation")

    return validated