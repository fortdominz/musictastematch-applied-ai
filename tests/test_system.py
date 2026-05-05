"""
Automated tests for MusicTasteMatch 2.0 components.
Tests bias detection, confidence scoring, logging, and catalog building.
"""

import os
import json
import pytest
from src.bias_detector import detect_bias
from src.logger import log_session


# ── Sample data used across tests ──────────────────────────────────────────

def make_sample_songs():
    return [
        {"id": "1", "title": "Song A", "artist": "Artist A", "genre": "pop",
         "mood": "happy", "energy": 0.8, "tempo_bpm": 118, "valence": 0.85,
         "danceability": 0.78, "acousticness": 0.18, "instrumentalness": 0.10,
         "speechiness": 0.05, "liveness": 0.14},
        {"id": "2", "title": "Song B", "artist": "Artist B", "genre": "rock",
         "mood": "intense", "energy": 0.91, "tempo_bpm": 152, "valence": 0.48,
         "danceability": 0.66, "acousticness": 0.10, "instrumentalness": 0.04,
         "speechiness": 0.06, "liveness": 0.15},
        {"id": "3", "title": "Song C", "artist": "Artist C", "genre": "lofi",
         "mood": "chill", "energy": 0.35, "tempo_bpm": 72, "valence": 0.60,
         "danceability": 0.58, "acousticness": 0.86, "instrumentalness": 0.30,
         "speechiness": 0.03, "liveness": 0.10},
        {"id": "4", "title": "Song D", "artist": "Artist D", "genre": "pop",
         "mood": "intense", "energy": 0.93, "tempo_bpm": 132, "valence": 0.77,
         "danceability": 0.88, "acousticness": 0.05, "instrumentalness": 0.08,
         "speechiness": 0.05, "liveness": 0.18},
        {"id": "5", "title": "Song E", "artist": "Artist E", "genre": "ambient",
         "mood": "chill", "energy": 0.28, "tempo_bpm": 60, "valence": 0.65,
         "danceability": 0.41, "acousticness": 0.92, "instrumentalness": 0.85,
         "speechiness": 0.02, "liveness": 0.05},
    ]


def make_sample_recommendations(songs):
    """Wrap songs in (song, score, reasons) tuples like recommend_songs returns."""
    return [
        (songs[0], 10.5, ["genre match (+2.0)", "mood match (+1.0)", "energy similarity (0.98)"]),
        (songs[1], 8.2,  ["energy similarity (0.95)", "valence similarity (0.87)"]),
        (songs[2], 7.9,  ["energy similarity (0.90)", "acousticness similarity (0.92)"]),
        (songs[3], 7.5,  ["genre match (+2.0)", "energy similarity (0.87)"]),
        (songs[4], 6.8,  ["energy similarity (0.82)", "acousticness similarity (0.88)"]),
    ]


# ── Bias Detector Tests ─────────────────────────────────────────────────────

def test_bias_detector_returns_dict():
    songs = make_sample_songs()
    recs = make_sample_recommendations(songs)
    user_prefs = {
        "preferred_genre": "pop", "preferred_mood": "happy",
        "target_energy": 0.8, "target_tempo_bpm": 118,
        "target_valence": 0.8, "target_danceability": 0.78,
        "target_acousticness": 0.18, "target_instrumentalness": 0.10,
        "target_speechiness": 0.05, "target_liveness": 0.14,
    }
    result = detect_bias(user_prefs, recs)
    assert isinstance(result, dict)


def test_bias_detector_has_required_keys():
    songs = make_sample_songs()
    recs = make_sample_recommendations(songs)
    user_prefs = {
        "preferred_genre": "pop", "preferred_mood": "happy",
        "target_energy": 0.8, "target_tempo_bpm": 118,
        "target_valence": 0.8, "target_danceability": 0.78,
        "target_acousticness": 0.18, "target_instrumentalness": 0.10,
        "target_speechiness": 0.05, "target_liveness": 0.14,
    }
    result = detect_bias(user_prefs, recs)
    required_keys = [
        "confidence_score", "genre_matches", "mood_matches",
        "score_gap", "genre_dominance", "contradictory_prefs",
        "no_categorical_matches", "flags"
    ]
    for key in required_keys:
        assert key in result, f"Missing key: {key}"


def test_confidence_score_between_0_and_1():
    songs = make_sample_songs()
    recs = make_sample_recommendations(songs)
    user_prefs = {
        "preferred_genre": "pop", "preferred_mood": "happy",
        "target_energy": 0.8, "target_tempo_bpm": 118,
        "target_valence": 0.8, "target_danceability": 0.78,
        "target_acousticness": 0.18, "target_instrumentalness": 0.10,
        "target_speechiness": 0.05, "target_liveness": 0.14,
    }
    result = detect_bias(user_prefs, recs)
    assert 0.0 <= result["confidence_score"] <= 1.0


def test_no_categorical_matches_detected():
    """When genre and mood don't match anything, flag should be raised."""
    songs = make_sample_songs()
    recs = make_sample_recommendations(songs)
    user_prefs = {
        "preferred_genre": "cyberpunk", "preferred_mood": "manic",
        "target_energy": 0.5, "target_tempo_bpm": 100,
        "target_valence": 0.5, "target_danceability": 0.5,
        "target_acousticness": 0.5, "target_instrumentalness": 0.5,
        "target_speechiness": 0.5, "target_liveness": 0.5,
    }
    result = detect_bias(user_prefs, recs)
    assert result["no_categorical_matches"] is True
    assert result["confidence_score"] < 1.0


def test_contradictory_prefs_detected():
    """High energy + high acousticness should trigger contradictory flag."""
    songs = make_sample_songs()
    recs = make_sample_recommendations(songs)
    user_prefs = {
        "preferred_genre": "pop", "preferred_mood": "happy",
        "target_energy": 0.95, "target_tempo_bpm": 180,
        "target_valence": 0.5, "target_danceability": 0.9,
        "target_acousticness": 0.95, "target_instrumentalness": 0.5,
        "target_speechiness": 0.5, "target_liveness": 0.5,
    }
    result = detect_bias(user_prefs, recs)
    assert result["contradictory_prefs"] is True


# ── Logger Tests ────────────────────────────────────────────────────────────

def test_logger_creates_file():
    songs = make_sample_songs()
    recs = make_sample_recommendations(songs)
    user_prefs = {"preferred_genre": "pop", "preferred_mood": "happy",
                  "target_energy": 0.8, "target_tempo_bpm": 118,
                  "target_valence": 0.8, "target_danceability": 0.78,
                  "target_acousticness": 0.18, "target_instrumentalness": 0.10,
                  "target_speechiness": 0.05, "target_liveness": 0.14}
    confidence = {"confidence_score": 0.9, "flags": []}

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    log_session("test input", user_prefs, recs, confidence, "test critique")
    assert os.path.exists("logs/sessions.json")


def test_logger_writes_valid_json():
    songs = make_sample_songs()
    recs = make_sample_recommendations(songs)
    user_prefs = {"preferred_genre": "pop", "preferred_mood": "happy",
                  "target_energy": 0.8, "target_tempo_bpm": 118,
                  "target_valence": 0.8, "target_danceability": 0.78,
                  "target_acousticness": 0.18, "target_instrumentalness": 0.10,
                  "target_speechiness": 0.05, "target_liveness": 0.14}
    confidence = {"confidence_score": 0.9, "flags": []}

    os.makedirs("logs", exist_ok=True)
    log_session("test input", user_prefs, recs, confidence, "test critique")

    with open("logs/sessions.json", "r") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) > 0
    assert "user_input" in data[-1]
    assert "recommendations" in data[-1]
    assert "confidence" in data[-1]


# ── Recommender Tests (carried over from 1.0) ───────────────────────────────

def test_recommend_songs_returns_correct_count():
    from src.recommender import recommend_songs
    songs = make_sample_songs()
    user_prefs = {
        "preferred_genre": "pop", "preferred_mood": "happy",
        "target_energy": 0.8, "target_tempo_bpm": 118,
        "target_valence": 0.8, "target_danceability": 0.78,
        "target_acousticness": 0.18, "target_instrumentalness": 0.10,
        "target_speechiness": 0.05, "target_liveness": 0.14,
    }
    results = recommend_songs(user_prefs, songs, k=3)
    assert len(results) == 3


def test_recommend_songs_sorted_by_score():
    from src.recommender import recommend_songs
    songs = make_sample_songs()
    user_prefs = {
        "preferred_genre": "pop", "preferred_mood": "happy",
        "target_energy": 0.8, "target_tempo_bpm": 118,
        "target_valence": 0.8, "target_danceability": 0.78,
        "target_acousticness": 0.18, "target_instrumentalness": 0.10,
        "target_speechiness": 0.05, "target_liveness": 0.14,
    }
    results = recommend_songs(user_prefs, songs, k=5)
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)