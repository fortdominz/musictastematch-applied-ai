"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label, user_prefs, songs, k=5):
    print(f"\n{'='*50}")
    print(f"Profile: {label}")
    print(f"{'='*50}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for song, score, reasons in recommendations:
        print(f"\n{song['title']} — Score: {score:.2f}")
        for reason in reasons:
            print(f"  • {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    pop_fan = {
        "preferred_genre": "pop",
        "preferred_mood": "happy",
        "target_energy": 0.80,
        "target_tempo_bpm": 118,
        "target_valence": 0.80,
        "target_danceability": 0.78,
        "target_acousticness": 0.18,
        "target_instrumentalness": 0.10,
        "target_speechiness": 0.05,
        "target_liveness": 0.14,
    }

    lofi_fan = {
        "preferred_genre": "lofi",
        "preferred_mood": "chill",
        "target_energy": 0.38,
        "target_tempo_bpm": 78,
        "target_valence": 0.58,
        "target_danceability": 0.58,
        "target_acousticness": 0.78,
        "target_instrumentalness": 0.35,
        "target_speechiness": 0.03,
        "target_liveness": 0.10,
    }

    metal_fan = {
        "preferred_genre": "metal",
        "preferred_mood": "aggressive",
        "target_energy": 0.96,
        "target_tempo_bpm": 150,
        "target_valence": 0.35,
        "target_danceability": 0.60,
        "target_acousticness": 0.05,
        "target_instrumentalness": 0.05,
        "target_speechiness": 0.03,
        "target_liveness": 0.25,
    }

    # Adversarial/Edge Case Profiles for System Evaluation
    adversarial_high_energy_sad = {
        "preferred_genre": "pop",
        "preferred_mood": "sad",
        "target_energy": 0.9,  # High energy
        "target_tempo_bpm": 140,
        "target_valence": 0.2,  # Low positivity (sad)
        "target_danceability": 0.8,
        "target_acousticness": 0.1,
        "target_instrumentalness": 0.0,
        "target_speechiness": 0.1,
        "target_liveness": 0.1,
    }

    adversarial_low_energy_happy = {
        "preferred_genre": "rock",
        "preferred_mood": "happy",
        "target_energy": 0.1,  # Low energy
        "target_tempo_bpm": 60,
        "target_valence": 0.9,  # High positivity (happy)
        "target_danceability": 0.2,
        "target_acousticness": 0.9,
        "target_instrumentalness": 0.8,
        "target_speechiness": 0.0,
        "target_liveness": 0.0,
    }

    adversarial_extreme_acoustic_energy = {
        "preferred_genre": "indie",
        "preferred_mood": "chill",
        "target_energy": 1.0,  # Maximum energy
        "target_tempo_bpm": 180,
        "target_valence": 0.5,
        "target_danceability": 0.9,
        "target_acousticness": 1.0,  # Maximum acousticness
        "target_instrumentalness": 0.9,
        "target_speechiness": 0.0,
        "target_liveness": 0.0,
    }

    adversarial_neutral_profile = {
        "preferred_genre": "jazz",
        "preferred_mood": "chill",  # Using existing mood; adjust if "neutral" exists
        "target_energy": 0.5,
        "target_tempo_bpm": 100,
        "target_valence": 0.5,
        "target_danceability": 0.5,
        "target_acousticness": 0.5,
        "target_instrumentalness": 0.5,
        "target_speechiness": 0.5,
        "target_liveness": 0.5,
    }

    adversarial_nonexistent_category = {
        "preferred_genre": "cyberpunk",  # Assuming not in dataset
        "preferred_mood": "manic",  # Assuming not in dataset
        "target_energy": 0.0,  # Minimum energy
        "target_tempo_bpm": 0,
        "target_valence": 0.0,
        "target_danceability": 0.0,
        "target_acousticness": 0.0,
        "target_instrumentalness": 0.0,
        "target_speechiness": 0.0,
        "target_liveness": 0.0,
    }

    adversarial_conflicting_valence = {
        "preferred_genre": "electronic",
        "preferred_mood": "happy",
        "target_energy": 0.7,
        "target_tempo_bpm": 130,
        "target_valence": 0.1,  # Very low positivity (sad)
        "target_danceability": 0.8,
        "target_acousticness": 0.2,
        "target_instrumentalness": 0.1,
        "target_speechiness": 0.1,
        "target_liveness": 0.2,
    }

    print_recommendations("High-Energy Pop", pop_fan, songs)
    print_recommendations("Chill Lofi", lofi_fan, songs)
    print_recommendations("Intense Metal", metal_fan, songs)
    print_recommendations("Adversarial: High-Energy Sad", adversarial_high_energy_sad, songs)
    print_recommendations("Adversarial: Low-Energy Happy", adversarial_low_energy_happy, songs)
    print_recommendations("Adversarial: Extreme Acoustic High-Energy", adversarial_extreme_acoustic_energy, songs)
    print_recommendations("Adversarial: Neutral Profile", adversarial_neutral_profile, songs)
    print_recommendations("Adversarial: Non-Existent Category", adversarial_nonexistent_category, songs)
    print_recommendations("Adversarial: Conflicting Valence", adversarial_conflicting_valence, songs)


if __name__ == "__main__":
    main()