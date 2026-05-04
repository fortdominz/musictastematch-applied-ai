"""
MusicTasteMatch 2.0 — Main Application Entry Point

Extended from MusicTasteMatch 1.0 with:
- Natural language profile building (Llama 3.2 via Ollama)
- Live music catalog from Spotify API
- Bias detection and confidence scoring
- AI self-critique (Llama 3.2 via Ollama)
- Session logging
"""

from src.recommender import recommend_songs
from src.profile_builder import build_profile_from_text
from src.spotify_catalog import build_catalog
from src.bias_detector import detect_bias
from src.critique import critique_recommendations
from src.logger import log_session


def run(user_input: str, k: int = 5) -> None:
    """Run the full MusicTasteMatch 2.0 pipeline for a given user input."""

    print("\n" + "="*60)
    print("🎵 MusicTasteMatch 2.0")
    print("="*60)
    print(f"\n📝 User input: \"{user_input}\"")

    # Step 1: Build user profile from natural language
    print("\n⚙️  Building taste profile with AI...")
    user_prefs = build_profile_from_text(user_input)
    print(f"✅ Profile built:")
    print(f"   Genre:   {user_prefs['preferred_genre']}")
    print(f"   Mood:    {user_prefs['preferred_mood']}")
    print(f"   Energy:  {user_prefs['target_energy']}")
    print(f"   Valence: {user_prefs['target_valence']}")
    print(f"   Tempo:   {user_prefs['target_tempo_bpm']} BPM")

    # Step 2: Fetch live catalog from Spotify
    print("\n🎧 Fetching live songs from Spotify...")
    songs = build_catalog(user_prefs["preferred_genre"], user_prefs["preferred_mood"])
    print(f"✅ Catalog built — {len(songs)} songs fetched")

    if not songs:
        print("❌ No songs found. Try a different description.")
        return

    # Step 3: Generate recommendations
    print("\n🔍 Scoring songs...")
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n🎵 Top {k} Recommendations:\n")
    for song, score, reasons in recommendations:
        print(f"  {song['title']} by {song['artist']} — Score: {score:.2f}")
        for reason in reasons:
            print(f"    • {reason}")
        print()

    # Step 4: Detect bias and calculate confidence
    print("🔎 Running bias detection...")
    confidence = detect_bias(user_prefs, recommendations)
    print(f"   Confidence Score: {confidence['confidence_score']} / 1.0")
    print(f"   Genre matches in top {k}: {confidence['genre_matches']}")
    print(f"   Mood matches in top {k}: {confidence['mood_matches']}")

    if confidence["flags"]:
        print("\n⚠️  Bias Flags:")
        for flag in confidence["flags"]:
            print(f"   • {flag}")
    else:
        print("   ✅ No bias flags detected.")

    # Step 5: AI self-critique
    print("\n🤖 Generating AI critique...")
    critique = critique_recommendations(user_input, user_prefs, recommendations, confidence)
    print(f"\n💬 Critique:\n   {critique}")

    # Step 6: Log session
    log_session(user_input, user_prefs, recommendations, confidence, critique)

    print("\n" + "="*60)


if __name__ == "__main__":
    inputs = [
        "I want something to study to late at night",
        "Give me high energy songs for the gym",
        "Something sad and acoustic for a rainy day"
    ]

    for user_input in inputs:
        run(user_input)