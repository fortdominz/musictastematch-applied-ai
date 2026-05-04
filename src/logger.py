import json
import os
from datetime import datetime


LOG_FILE = "logs/sessions.json"


def log_session(user_input: str, user_prefs: dict, recommendations: list, confidence: dict, critique: str) -> None:
    """Log a recommendation session to a JSON file."""

    session = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "user_prefs": user_prefs,
        "recommendations": [
            {
                "title": song["title"],
                "artist": song["artist"],
                "score": round(score, 2),
                "reasons": reasons
            }
            for song, score, reasons in recommendations
        ],
        "confidence": confidence,
        "critique": critique
    }

    # Load existing sessions if file exists
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                sessions = json.load(f)
            except json.JSONDecodeError:
                sessions = []
    else:
        sessions = []

    sessions.append(session)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2)

    print(f"\n📝 Session logged to {LOG_FILE}")