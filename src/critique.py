import ollama


def critique_recommendations(user_input: str, user_prefs: dict, recommendations: list, confidence: dict) -> str:
    """Use Llama 3.2 to review the recommendations and flag anything suspicious or misaligned."""

    rec_summary = "\n".join([
        f"- {song['title']} by {song['artist']} (genre: {song['genre']}, mood: {song['mood']}, score: {score:.2f})"
        for song, score, reasons in recommendations
    ])

    flags_summary = "\n".join(confidence["flags"]) if confidence["flags"] else "No flags detected."

    prompt = f"""You are a music recommendation quality reviewer for MusicTasteMatch 2.0.

A user described their music taste as: "{user_input}"

This was translated into the following preference profile:
- Preferred genre: {user_prefs['preferred_genre']}
- Preferred mood: {user_prefs['preferred_mood']}
- Target energy: {user_prefs['target_energy']}
- Target valence: {user_prefs['target_valence']}

The system recommended these songs:
{rec_summary}

The bias detector flagged the following issues:
{flags_summary}

Confidence score: {confidence['confidence_score']} out of 1.0

Please write a short 2-3 sentence critique of these recommendations. Be specific about:
1. Whether the recommendations seem aligned with what the user actually asked for
2. Any obvious mismatches you notice (wrong genre, wrong mood, wrong energy)
3. One concrete suggestion for how the results could be improved

Be direct and honest. Do not be overly positive if the results are poor."""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()