# ------- USING GOOGLE's GEMINI GENERATIVE-AI API TO INTEGRATE AI CAPABILITIES --------

"""Quick connection test for Spotify and Gemini APIs."""
import os
from dotenv import load_dotenv

load_dotenv()

# Test Spotify
print("Testing Spotify connection...")
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

results = sp.search(q="lofi chill study", type="track", limit=3)
tracks = results["tracks"]["items"]
print(f"✅ Spotify connected — found {len(tracks)} tracks:")
for track in tracks:
    print(f"   • {track['name']} by {track['artists'][0]['name']}")

# Test Gemini
print("\nTesting Gemini connection...")
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say 'MusicTasteMatch connected!' and nothing else."
)
print(f"✅ Gemini connected — {response.text.strip()}")



# ---------------- USING LLAMA TO INTEGRATE AI CAPABILITIES -----------------

# """Quick connection test for Spotify and Ollama."""
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Test Spotify
# print("Testing Spotify connection...")
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
#     client_id=os.getenv("SPOTIFY_CLIENT_ID"),
#     client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
# ))

# results = sp.search(q="lofi chill study", type="track", limit=3)
# tracks = results["tracks"]["items"]
# print(f"✅ Spotify connected — found {len(tracks)} tracks:")
# for track in tracks:
#     print(f"   • {track['name']} by {track['artists'][0]['name']}")

# # Test Ollama
# print("\nTesting Ollama connection...")
# import ollama

# response = ollama.chat(
#     model="llama3.2",
#     messages=[{"role": "user", "content": "Say 'MusicTasteMatch connected!' and nothing else."}]
# )
# print(f"✅ Ollama connected — {response['message']['content'].strip()}")