def detect_bias(user_prefs: dict, recommendations: list) -> dict:
    """Analyze recommendation results for known bias patterns and return a confidence report."""

    top_song, top_score, top_reasons = recommendations[0]
    bottom_song, bottom_score, bottom_reasons = recommendations[-1]

    # Check 1: How many results have a genre match
    genre_matches = sum(
        1 for song, score, reasons in recommendations
        if song["genre"] == user_prefs["preferred_genre"]
    )

    # Check 2: How many results have a mood match
    mood_matches = sum(
        1 for song, score, reasons in recommendations
        if song["mood"] == user_prefs["preferred_mood"]
    )

    # Check 3: Score gap between 1st and last result
    score_gap = top_score - bottom_score

    # Check 4: Genre dominance — top result has genre match but no mood match
    top_has_genre = any("genre match" in r for r in top_reasons)
    top_has_mood = any("mood match" in r for r in top_reasons)
    genre_dominance = top_has_genre and not top_has_mood

    # Check 5: No categorical matches at all
    no_matches = genre_matches == 0 and mood_matches == 0

    # Check 6: Contradictory preferences — energy and acousticness both above 0.8
    contradictory = (
        user_prefs.get("target_energy", 0) > 0.8 and
        user_prefs.get("target_acousticness", 0) > 0.8
    )

    # Confidence score: start at 1.0, deduct for each issue
    confidence_score = 1.0
    flags = []

    if no_matches:
        confidence_score -= 0.4
        flags.append("No genre or mood matches found — results may not reflect user taste.")

    if genre_dominance:
        confidence_score -= 0.2
        flags.append("Genre weight dominance detected — top result matched genre but not mood.")

    if score_gap < 1.0:
        confidence_score -= 0.1
        flags.append("Low score gap — results are closely ranked, meaning no strong match exists.")

    if contradictory:
        confidence_score -= 0.2
        flags.append("Contradictory preferences detected — high energy and high acousticness conflict.")

    if genre_matches == 0:
        confidence_score -= 0.1
        flags.append("No songs matched preferred genre in top results.")

    if mood_matches == 0:
        confidence_score -= 0.1
        flags.append("No songs matched preferred mood in top results.")

    confidence_score = max(0.0, round(confidence_score, 2))

    return {
        "confidence_score": confidence_score,
        "genre_matches": genre_matches,
        "mood_matches": mood_matches,
        "score_gap": round(score_gap, 2),
        "genre_dominance": genre_dominance,
        "contradictory_prefs": contradictory,
        "no_categorical_matches": no_matches,
        "flags": flags
    }