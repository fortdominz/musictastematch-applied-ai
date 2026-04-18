"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
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

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for song, score, reasons in recommendations:
        print(f"{song['title']} — Score: {score:.2f}")
        for reason in reasons:
            print(f"  • {reason}")
        print()


if __name__ == "__main__":
    main()
