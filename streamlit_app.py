import streamlit as st
from src.recommender import recommend_songs
from src.profile_builder import build_profile_from_text
from src.spotify_catalog import build_catalog
from src.bias_detector import detect_bias
from src.critique import critique_recommendations
from src.logger import log_session

st.set_page_config(
    page_title="MusicTasteMatch 2.0",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 MusicTasteMatch 2.0")
st.caption("Describe your music mood and get personalized recommendations powered by AI.")

st.divider()

user_input = st.text_input(
    "What kind of music are you in the mood for?",
    placeholder="e.g. something chill to study to late at night..."
)

k = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)

if st.button("Find My Music", type="primary"):
    if not user_input.strip():
        st.warning("Please describe what you're in the mood for.")
    else:
        # Step 1: Build profile
        with st.spinner("🤖 Building your taste profile..."):
            try:
                user_prefs = build_profile_from_text(user_input)
            except Exception as e:
                st.error(f"Failed to build profile: {e}")
                st.stop()

        col1, col2, col3 = st.columns(3)
        col1.metric("Genre", user_prefs["preferred_genre"].title())
        col2.metric("Mood", user_prefs["preferred_mood"].title())
        col3.metric("Energy", f"{user_prefs['target_energy']:.1f}")

        st.divider()

        # Step 2: Fetch catalog
        with st.spinner("🎧 Fetching songs from Spotify..."):
            try:
                songs = build_catalog(
                    user_prefs["preferred_genre"],
                    user_prefs["preferred_mood"]
                )
            except Exception as e:
                st.error(f"Failed to fetch songs: {e}")
                st.stop()

        if not songs:
            st.error("No songs found. Try a different description.")
            st.stop()

        st.caption(f"Found {len(songs)} songs — scoring them now...")

        # Step 3: Score and rank
        recommendations = recommend_songs(user_prefs, songs, k=k)

        st.subheader("🎵 Your Recommendations")
        for i, (song, score, reasons) in enumerate(recommendations, 1):
            with st.expander(f"{i}. {song['title']} by {song['artist']} — Score: {score:.2f}"):
                cols = st.columns(2)
                reason_pairs = [(reasons[j], reasons[j+1]) if j+1 < len(reasons)
                               else (reasons[j], "") for j in range(0, len(reasons), 2)]
                for left, right in reason_pairs:
                    cols[0].write(f"• {left}")
                    if right:
                        cols[1].write(f"• {right}")

        st.divider()

        # Step 4: Bias detection
        with st.spinner("🔎 Analyzing recommendations..."):
            confidence = detect_bias(user_prefs, recommendations)

        col1, col2, col3 = st.columns(3)
        col1.metric("Confidence Score", f"{confidence['confidence_score']} / 1.0")
        col2.metric("Genre Matches", f"{confidence['genre_matches']} / {k}")
        col3.metric("Mood Matches", f"{confidence['mood_matches']} / {k}")

        if confidence["flags"]:
            st.warning("⚠️ " + " | ".join(confidence["flags"]))
        else:
            st.success("✅ No bias flags detected.")

        st.divider()

        # Step 5: AI critique
        with st.spinner("💬 Generating AI critique..."):
            critique = critique_recommendations(
                user_input, user_prefs, recommendations, confidence
            )

        st.subheader("💬 AI Critique")
        st.info(critique)

        # Step 6: Log session
        log_session(user_input, user_prefs, recommendations, confidence, critique)
        st.caption("📝 Session logged.")