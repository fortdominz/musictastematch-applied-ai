# 🎧 Model Card: MusicTasteMatch 2.0

## 1. Model Name

**MusicTasteMatch 2.0**
Extended from MusicTasteMatch 1.0 (Module 3 — Music Recommender Simulation)

---

## 2. Intended Use

MusicTasteMatch 2.0 is an AI-powered music recommendation system designed for personal use and classroom exploration. A user describes their music mood in plain English, and the system translates that into a structured taste profile, fetches live songs from Spotify, scores them using content-based filtering, detects bias in the results, and generates an AI critique. It is not intended for production deployment or commercial use.

---

## 3. How the Model Works

The system runs in six steps. First, Llama 3.2 reads the user's plain English description and extracts a structured preference profile — genre, mood, energy, valence, tempo, and other audio features. Second, the Spotify API searches its live catalog for songs matching that genre and mood. Third, a rule-based lookup table assigns audio feature values to each song based on its genre and mood. Fourth, the scoring engine compares every song to the user's profile — genre matches earn +2.0 points, mood matches earn +1.0, and numerical features are scored by closeness using 1 - |user_target - song_value|. Fifth, a bias detector analyzes the results and produces a confidence score from 0.0 to 1.0. Sixth, Llama 3.2 reviews the recommendations and writes a short honest critique flagging any mismatches.

---

## 4. Data

The system uses Spotify's live catalog of 100 million songs accessed through the Web API. Each query fetches 8-13 songs depending on availability. Audio features (energy, valence, tempo, danceability, acousticness, instrumentalness, speechiness, liveness) are assigned using a rule-based lookup table organized by genre and mood rather than Spotify's audio features API, which was deprecated for new developers in 2024. The system also retains the original 18-song CSV catalog from MusicTasteMatch 1.0 for testing purposes.

---

## 5. Strengths

The system works well for well-defined genres with strong Spotify representation — lofi, electronic, folk, and rock all return relevant results. The natural language interface removes the need for users to understand music terminology or numerical feature values. Every recommendation comes with a full scoring breakdown, making the system transparent and easy to debug. The bias detector adds a layer of honesty that most recommenders lack — it tells the user when results are weak rather than presenting everything with equal confidence.

---

## 6. Limitations and Bias

The rule-based feature lookup assigns identical numerical values to all songs of the same genre and mood, which means scoring differences within a genre depend entirely on the categorical matches rather than actual song characteristics. Spotify search results vary between runs — the same query may return different songs each time, making results non-deterministic. The genre weight (+2.0) still dominates over any single numerical feature (max 1.0), meaning genre mismatches from Spotify's search can pollute the top results. Llama 3.2 running locally on CPU is slow — approximately 30-60 seconds per inference call — making the system impractical for real-time use without a faster inference backend. The system has no memory of previous sessions or user history, so it cannot learn or improve from past interactions.

---

## 7. Evaluation

Nine automated tests were written and all passed in 0.35 seconds covering the bias detector, session logger, and scoring engine. Three end-to-end profiles were tested manually: a lofi study profile, a high-energy gym profile, and a sad acoustic rainy day profile. All three produced genre and mood matching results with confidence scores of 0.9 or 1.0. The AI critique correctly identified genre mismatches in the lofi profile (The Weeknd appearing in lofi results) and provided actionable suggestions in all three cases. A key surprise was that Spotify sometimes returns songs with titles containing the search keywords but belonging to completely different genres — for example, searching "lofi relaxed" returned "Loft Music" by The Weeknd because the word "loft" appeared in the title.

---

## 8. Future Work

First, swap Llama 3.2 for the Anthropic Claude API to reduce inference time from minutes to seconds. Second, replace the rule-based feature lookup with real audio feature data from a licensed source to give songs genuinely different numerical profiles. Third, add a diversity filter so the same artist cannot appear more than once in the top results. Fourth, implement a feedback loop where users can rate recommendations and the system adjusts weights accordingly. Fifth, add a genre mismatch guardrail that filters out Spotify results whose artist genre doesn't match the requested genre before scoring.

---

## 9. Personal Reflection

**What I learned about recommender systems:**
Building 2.0 showed me that the hardest part of a recommender isn't the scoring logic — it's getting clean, relevant data into the system in the first place. Spotify's API deprecation of audio features forced a pivot that ended up teaching me more about system design than the original plan would have.

**AI collaboration — one helpful instance:**
Llama 3.2's natural language profile building worked better than expected. When given "gaming music," it correctly mapped to electronic/intense without any explicit rules for that mapping. That kind of zero-shot generalization is genuinely impressive for a 2GB local model.

**AI collaboration — one flawed instance:**
When asked to estimate audio features for a batch of songs in JSON format, Llama occasionally returned 7 results instead of 8, or included explanatory text inside the JSON array, breaking the parser. This required building a robust fallback system and taught me that AI outputs always need validation before being used downstream.

**What surprised me about reliability testing:**
The bias detector caught things I didn't anticipate — like The Weeknd appearing in lofi search results purely because the word "loft" matched the search query. Having an automated layer that flags these mismatches made the system feel genuinely more trustworthy than one that just silently returns whatever it finds.

**Could this system be misused?**
The system could theoretically be used to manipulate music discovery by crafting profiles that consistently surface specific artists. This could be prevented by adding transparency about how profiles are built and limiting the influence of any single feature in the scoring formula.
