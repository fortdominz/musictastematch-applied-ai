"""
MusicTasteMatch — FastAPI backend
Wraps the full pipeline and exposes /api/recommend
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure logs directory exists before any logger import
os.makedirs("logs", exist_ok=True)

from src.profile_builder import build_profile_from_text
from src.spotify_catalog import build_catalog
from src.recommender import recommend_songs
from src.bias_detector import detect_bias
from src.critique import critique_recommendations, refine_preferences_from_critique
from src.logger import log_session


app = FastAPI(title="MusicTasteMatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Request / Response models ----------

class RecommendRequest(BaseModel):
    description: str
    count: int = Field(default=5, ge=3, le=10)


class ProfileOut(BaseModel):
    genre: str
    mood: str
    energy: float
    valence: float
    tempo_bpm: float


class SongOut(BaseModel):
    title: str
    artist: str
    genre: str
    mood: str
    score: float
    reasons: list[str]


class ConfidenceOut(BaseModel):
    confidence_score: float
    genre_matches: int
    mood_matches: int
    flags: list[str]


class RecommendResponse(BaseModel):
    profile: ProfileOut
    songs_fetched: int
    recommendations: list[SongOut]
    confidence: ConfidenceOut
    critique: str


# ---------- Routes ----------

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/recommend")
def recommend(req: RecommendRequest):
    try:
        # Step 1: Build user profile
        user_prefs = build_profile_from_text(req.description)

        # Step 2: Fetch catalog
        songs = build_catalog(user_prefs["preferred_genre"], user_prefs["preferred_mood"])

        if not songs:
            return {"error": "No songs found for that description. Try something different."}, 404

        # Step 3: Recommend
        raw_recs = recommend_songs(user_prefs, songs, k=req.count)

        # Step 4: Bias detection
        confidence_raw = detect_bias(user_prefs, raw_recs)

        # Step 5: Critique
        critique = critique_recommendations(req.description, user_prefs, raw_recs, confidence_raw)

        # Step 5b: Refine preferences based on critique and re-score
        refined_prefs = refine_preferences_from_critique(req.description, user_prefs, critique)
        if refined_prefs != user_prefs:
            raw_recs = recommend_songs(refined_prefs, songs, k=req.count)
            confidence_raw = detect_bias(refined_prefs, raw_recs)

        # Step 6: Log
        log_session(req.description, user_prefs, raw_recs, confidence_raw, critique)

        # Build response
        profile_out = ProfileOut(
            genre=user_prefs["preferred_genre"],
            mood=user_prefs["preferred_mood"],
            energy=float(user_prefs.get("target_energy", 0.5)),
            valence=float(user_prefs.get("target_valence", 0.5)),
            tempo_bpm=float(user_prefs.get("target_tempo_bpm", 120)),
        )

        recs_out = [
            SongOut(
                title=song["title"],
                artist=song["artist"],
                genre=song.get("genre", ""),
                mood=song.get("mood", ""),
                score=round(float(score), 3),
                reasons=list(reasons),
            )
            for song, score, reasons in raw_recs
        ]

        confidence_out = ConfidenceOut(
            confidence_score=float(confidence_raw["confidence_score"]),
            genre_matches=int(confidence_raw["genre_matches"]),
            mood_matches=int(confidence_raw["mood_matches"]),
            flags=list(confidence_raw["flags"]),
        )

        return RecommendResponse(
            profile=profile_out,
            songs_fetched=len(songs),
            recommendations=recs_out,
            confidence=confidence_out,
            critique=critique,
        )

    except Exception as exc:
        return {"error": str(exc)}


# ---------- Dev entry point ----------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
