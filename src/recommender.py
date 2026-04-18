from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score all songs for a user and return the top k sorted by score."""
        scored = []
        for song in self.songs:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 2.0
            if song.mood == user.favorite_mood:
                score += 1.0
            score += 1 - abs(user.target_energy - song.energy)
            if user.likes_acoustic:
                score += song.acousticness
            else:
                score += 1 - song.acousticness
            scored.append((song, score))

        scored = sorted(scored, key=lambda x: x[1], reverse=True)
        return [song for song, score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation for why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("genre match")
        if song.mood == user.favorite_mood:
            reasons.append("mood match")
        energy_sim = 1 - abs(user.target_energy - song.energy)
        reasons.append(f"energy similarity ({energy_sim:.2f})")
        if not reasons:
            return "General similarity to your taste profile."
        return "Recommended because: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file and return a list of dictionaries with numeric values converted.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["instrumentalness"] = float(row["instrumentalness"])
            row["speechiness"] = float(row["speechiness"])
            row["liveness"] = float(row["liveness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences and return the score and list of reasons.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["preferred_genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs["preferred_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    numerical_features = [
        ("energy", "target_energy"),
        ("valence", "target_valence"),
        ("danceability", "target_danceability"),
        ("acousticness", "target_acousticness"),
        ("instrumentalness", "target_instrumentalness"),
        ("speechiness", "target_speechiness"),
        ("liveness", "target_liveness"),
    ]

    for song_key, pref_key in numerical_features:
        similarity = 1 - abs(user_prefs[pref_key] - song[song_key])
        score += similarity
        reasons.append(f"{song_key} similarity ({similarity:.2f})")

    tempo_similarity = 1 - abs(user_prefs["target_tempo_bpm"] - song["tempo_bpm"]) / 200
    score += tempo_similarity
    reasons.append(f"tempo similarity ({tempo_similarity:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored[:k]

