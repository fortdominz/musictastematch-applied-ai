# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

MusicTasteMatch 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

This system suggests songs from an 18-track catalog based on a user's preferred genre, mood, energy, valence, tempo, danceability, acousticness, instrumentalness, speechiness, and liveness. It assumes the user can describe their taste numerically. It is designed for classroom exploration only, not for real users or production use.

---

## 3. How the Model Works  

Each song in the catalog gets a score by comparing it to the user's taste profile. If the song's genre matches the user's preferred genre it earns 2 points. If the mood matches it earns 1 point. For every numerical feature like energy or tempo, the system measures how close the song's value is to the user's target — the closer it is, the higher it scores. All these points add up to a total score, and the songs are ranked from highest to lowest. The top results are the recommendations.

---

## 4. Data  

The catalog contains 18 songs across genres including pop, lofi, rock, metal, jazz, ambient, synthwave, indie pop, country, electronic, folk, classical, reggae, and dream pop. Moods include happy, chill, intense, relaxed, focused, moody, romantic, energetic, peaceful, aggressive, nostalgic, laid-back, hopeful, and dreamy. The dataset was expanded from the original 10 songs. It reflects a broad but shallow range of taste — most genres have only one or two songs, which limits diversity in results.

---

## 5. Strengths  

The system works best when the user's preferred genre has multiple songs in the catalog and their numerical targets are internally consistent. The pop and lofi profiles both produced intuitive top results. The scoring is fully transparent — every recommendation comes with a breakdown of exactly why it ranked where it did, which makes the system easy to understand and debug.

---

## 6. Limitations and Bias 

The system has several clear biases discovered through testing. First, genre weight dominance: a genre match alone adds +2.0 points, which can push genre-matching songs into the top results even when their mood directly contradicts the user's preference. The High-Energy Sad profile proved this — it got happy pop songs because they matched the genre, despite the user wanting sad music. Second, catalog imbalance amplifies this problem: when only one song exists for a genre (like metal), that song dominates completely and the remaining slots fill with numerically similar but genre-mismatched songs — a metal listener receiving pop recommendations in slots 3 through 5. Third, contradictory preferences produce weak results: the Extreme Acoustic High-Energy profile had all scores below 7.0 because no song could satisfy both targets simultaneously, yet the system still returned results with no warning to the user. Fourth, nonexistent genres and moods are handled silently: the cyberpunk/manic profile got results scoring around 4.7–4.9 with zero categorical matches — the system never signals that it found nothing meaningful.

---

## 7. Evaluation  

Three main profiles were tested: High-Energy Pop, Chill Lofi, and Intense Metal. Six adversarial profiles were also tested, including conflicting preferences, nonexistent categories, and extreme values. The pop and lofi profiles produced intuitive results with clear top matches. The metal profile revealed catalog imbalance bias. A weight shift experiment was run — doubling energy weight from 1.0 to 2.0 — which widened score gaps and shifted some rankings but did not change who ranked first in any profile. The adversarial profiles revealed that the system fails silently when preferences conflict or don't exist in the catalog.

---

## 8. Future Work  

First, add a diversity filter so the same genre cannot appear more than twice in the top 5 results. Second, add a confidence warning when no categorical matches are found, so the user knows the results are weak. Third, expand the catalog significantly — at least 5 songs per genre — so numerical similarity has meaningful options to rank within each category rather than spilling across genres.

---

## 9. Personal Reflection  

My biggest learning moment was realizing that genre weight alone could override everything else in the scoring.
A part of me expected mood to be the stronger signal, like, if someone wants sad music, mood should matter most, but the numbersshowed something different. A +2.0 genre match consistently overpowered a mood mismatch, which meant the system was recommending happy pop songs to someone who explicitly wanted sad music. That gap between what I designed and what actually happened taught me more about algorithmic bias than any explanation could.
Using AI tools throughout this project saved a lot of time on boilerplate and helped me think through edge cases I wouldn't have considered alone, the adversarial profiles Copilot suggested were genuinely useful. But I had to double-check everything it wrote. At one point it left dead code after return statements and used the wrong variable name in load_songs, bugs that would have broken the program silently if I hadn't caught them. AI helped me move faster on this project, but I was always the one responsible for understanding whether the output was actually correct.
What surprised me most was how convincing the results felt for well-matched profiles. The system has zero understanding of music, it just computes distances between numbers, but for the pop and lofi profiles, the recommendations felt genuinely accurate. That made me understand why real recommenders on Spotify feel "smart" even when they're doing something fundamentally similar underneath. If I extended this project, I would add a diversity filter to prevent genre repetition in the top results, a confidence warning when no categorical matches are found, and a much larger catalog with at least five songs per genre so numerical similarity has meaningful options to choose from within each category.