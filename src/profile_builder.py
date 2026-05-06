# ------- USING GOOGLE's GEMINI GENERATIVE-AI API TO INTEGRATE AI CAPABILITIES --------

import os
import json
import re
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# Commenting the AVAILABLE_GENRES to allow for a vast variety

# AVAILABLE_GENRES = [
#     "pop", "lofi", "rock", "metal", "jazz", "ambient", "synthwave",
#     "indie pop", "country", "electronic", "folk", "classical", "reggae",
#     "dream pop", "pop rock", "hip hop", "indie folk"
# ]

def build_profile_from_text(user_input: str) -> dict:
    """Use Gemini to convert a plain English music description into a structured user_prefs dictionary."""

    prompt = f"""You are a music taste analyzer. Convert the following description into a structured music preference profile.

User description: "{user_input}"

For preferred_genre: use the exact music genre the user is describing. Be specific — use terms like "afrobeats", "k-pop", "drill", "bossa nova", "gospel", "reggaeton", "trap", "blues", "r&b", "house", "techno", etc. Do not generalize to broad categories.

For preferred_mood: use the most accurate single word or short phrase that captures the emotional quality of what the user wants. Do NOT constrain yourself to a fixed list — use the actual mood the user is expressing. Examples: "sexy", "hype", "melancholic", "spiritual", "nostalgic", "grimy", "euphoric", "heartbroken", "triumphant", "tense", etc.

Return ONLY a valid JSON object with exactly these keys:
{{
    "preferred_genre": "the specific genre from the user description",
    "preferred_mood": "the actual mood the user is expressing, no constraints",
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

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw = response.text.strip()
            raw = re.sub(r"```json|```", "", raw).strip()
            profile = json.loads(raw)
            return profile
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "UNAVAILABLE" in error_str:
                if attempt < 2:
                    print(f"   ⚠️ Gemini busy, retrying in 5 seconds... (attempt {attempt + 1}/3)")
                    time.sleep(5)
                else:
                    raise Exception("Gemini unavailable after 3 attempts. Please try again.")
            elif "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                if attempt < 2:
                    print(f"   ⚠️ Rate limited, retrying in 15 seconds... (attempt {attempt + 1}/3)")
                    time.sleep(15)
                else:
                    raise Exception("API quota exceeded. Please try again later.")
            else:
                raise


# ---------------- USING LLAMA TO INTEGRATE AI CAPABILITIES -----------------

# import json
# import re
# import ollama


# AVAILABLE_GENRES = [
#     "pop", "lofi", "rock", "metal", "jazz", "ambient", "synthwave",
#     "indie pop", "country", "electronic", "folk", "classical", "reggae",
#     "dream pop", "pop rock"
# ]

# AVAILABLE_MOODS = [
#     "happy", "chill", "intense", "relaxed", "focused", "moody",
#     "romantic", "energetic", "peaceful", "aggressive", "nostalgic",
#     "laid-back", "hopeful", "dreamy"
# ]


# def build_profile_from_text(user_input: str) -> dict:
#     """Use Llama 3.2 to convert a plain English music description into a structured user_prefs dictionary."""

#     prompt = f"""You are a music taste analyzer. Convert the following description into a structured music preference profile.

# User description: "{user_input}"

# Available genres: {', '.join(AVAILABLE_GENRES)}
# Available moods: {', '.join(AVAILABLE_MOODS)}

# Return ONLY a valid JSON object with exactly these keys:
# {{
#     "preferred_genre": "one genre from the available list",
#     "preferred_mood": "one mood from the available list",
#     "target_energy": 0.0 to 1.0,
#     "target_tempo_bpm": 60 to 180,
#     "target_valence": 0.0 to 1.0,
#     "target_danceability": 0.0 to 1.0,
#     "target_acousticness": 0.0 to 1.0,
#     "target_instrumentalness": 0.0 to 1.0,
#     "target_speechiness": 0.0 to 1.0,
#     "target_liveness": 0.0 to 1.0
# }}

# Do not include any explanation, markdown, or code blocks. Return only the raw JSON object."""

#     response = ollama.chat(
#         model="llama3.2",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     raw = response["message"]["content"].strip()
#     raw = re.sub(r"```json|```", "", raw).strip()

#     profile = json.loads(raw)
#     return profile