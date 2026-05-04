import json
import re
import ollama


AVAILABLE_GENRES = [
    "pop", "lofi", "rock", "metal", "jazz", "ambient", "synthwave",
    "indie pop", "country", "electronic", "folk", "classical", "reggae",
    "dream pop", "pop rock"
]

AVAILABLE_MOODS = [
    "happy", "chill", "intense", "relaxed", "focused", "moody",
    "romantic", "energetic", "peaceful", "aggressive", "nostalgic",
    "laid-back", "hopeful", "dreamy"
]


def build_profile_from_text(user_input: str) -> dict:
    """Use Llama 3.2 to convert a plain English music description into a structured user_prefs dictionary."""

    prompt = f"""You are a music taste analyzer. Convert the following description into a structured music preference profile.

User description: "{user_input}"

Available genres: {', '.join(AVAILABLE_GENRES)}
Available moods: {', '.join(AVAILABLE_MOODS)}

Return ONLY a valid JSON object with exactly these keys:
{{
    "preferred_genre": "one genre from the available list",
    "preferred_mood": "one mood from the available list",
    "target_energy": 0.0 to 1.0,
    "target_tempo_bpm": 60 to 180,
    "target_valence": 0.0 to 1.0,
    "target_danceability": 0.0 to 1.0,
    "target_acousticness": 0.0 to 1.0,
    "target_instrumentalness": 0.0 to 1.0,
    "target_speechiness": 0.0 to 1.0,
    "target_liveness": 0.0 to 1.0
}}

Do not include any explanation, markdown, or code blocks. Return only the raw JSON object."""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response["message"]["content"].strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    profile = json.loads(raw)
    return profile