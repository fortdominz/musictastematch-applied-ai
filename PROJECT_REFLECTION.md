# Project Reflection — MusicTasteMatch AI

**Author:** Dominion Eze  
**Project lifespan:** 2025 – 2026  
**Final form:** Live web app at [musictastematchai.dominioneze.dev](https://musictastematchai.dominioneze.dev)  
**Repo:** [github.com/fortdominz/musictastematch-applied-ai](https://github.com/fortdominz/musictastematch-applied-ai)

---

## The Full Journey

This project did not start as what it became. It started as a CSV file and a Python loop.

**v1.0 — Module 3 of Applied AI class.** The assignment was to build a music recommender. I had 18 hardcoded songs in a spreadsheet, a cosine similarity function I barely understood, and no real user interface. It worked in the sense that it returned songs. It did not work in any other sense.

**v2.0 — The real version.** After the module ended, I kept going. I replaced the CSV with the live Spotify API catalog. I added Llama 3.2 running locally through Ollama to convert plain English descriptions into structured preference profiles. I built a 6-stage pipeline: profile builder → Spotify catalog search → audio feature scoring → bias detector → AI critique → session logger. All of it was CLI-based — you ran it in the terminal and read the output. I wrote nine automated tests. I wrote a model card. I treated it like a real system.

Then Gemini replaced Ollama. The local inference was too slow — 30–60 seconds per call on CPU. The Gemini API cut that to under 2 seconds. Same pipeline, faster engine.

**v3.0 — The web app.** The CLI was good for me. It was not good for anyone else. In 2026, the full app got rebuilt as a FastAPI backend + React frontend, containerized in a single service, and deployed to Render with a custom subdomain on my personal domain. Anyone can now open a browser, describe their mood, and get recommendations — no terminal required.

That arc — from hardcoded CSV to production web app — is what this reflection is about.

---

## What I Learned About Recommender Systems

The hardest part of a recommender is not the algorithm. It is the data.

I thought scoring logic was the hard problem. It is not. The hard problem is getting clean, relevant data into your system before the algorithm ever runs. Spotify deprecated audio features for new developers in 2024, which means I could not get actual energy, valence, or tempo values for songs from the API. I had to build a rule-based lookup table that assigns estimated audio feature values by genre and mood combination. Every lofi/relaxed song gets the same energy estimate. Every pop/happy song gets the same valence estimate. That is a real limitation and I knew it while building it.

What it taught me is that system design is mostly about constraints. You do not design the ideal system. You design the best system possible given what you actually have access to — and you document the gaps honestly.

The model card has a full limitations section. That was not required. I wrote it anyway because a system that does not know its own weaknesses is dangerous to trust.

---

## AI Collaboration — One Instance Where It Worked Well

Llama 3.2's zero-shot generalization surprised me.

When a user types "gaming music," there is no explicit rule that maps gaming to electronic/intense. I never wrote that. But Llama consistently returned `genre: electronic`, `mood: intense`, `energy: 0.85` for that prompt. It made a conceptual leap I did not program. That is genuinely impressive for a 2GB model running locally on CPU.

The profile builder worked well for any vibe with cultural context — "late night driving," "Afrobeats pre-game," "coding at 2am." Llama understood the emotional register of those descriptions and mapped them to real audio feature targets with reasonable accuracy. That is the correct place to use an LLM: fuzzy natural language → structured output. It is not the right tool for precise calculation, but for that specific translation task, it performed.

---

## AI Collaboration — One Instance Where It Fell Short

Batch JSON output was unreliable.

When I asked Llama to estimate audio features for a list of 8 songs and return them as a JSON array, it would sometimes return 7 items. Sometimes it would include an explanation sentence inside the array. Sometimes it would close the JSON bracket one entry early. Every one of these broke the downstream parser.

I had to build a fallback system: if the output does not parse cleanly, extract whatever songs did parse, fill the rest with defaults, and continue. That was not in the original design. I added it after the third broken run.

The lesson is not that LLMs are unreliable. The lesson is that LLM outputs always need a validation layer between the model and the rest of your system. You do not trust raw LLM output the same way you do not trust raw user input. You sanitize it, validate it, and build graceful handling for when it is wrong.

---

## What Surprised Me About Building and Testing This

Two things.

**First: the bias detector caught things I did not anticipate.** When searching Spotify for "lofi relaxed," it returned "Loft Music" by The Weeknd. The word "loft" matched the search query. The Weeknd is not lofi. Without the bias detector flagging that as a genre mismatch, the system would have returned it with a straight face. Having an automated layer that says "wait, this does not look right" made the system feel more honest than confident. That is what I wanted.

**Second: the Spotify search is non-deterministic.** The same query returns different songs on different runs. I expected a consistent catalog lookup. What I got was a live search that varies by session, time of day, and factors I cannot control. That is a fundamentally different reliability model than working with a static dataset. Automated tests that depend on specific song titles in the results are fragile. I learned to test the pipeline behavior — does the scorer rank higher-matching songs higher? — rather than testing specific outputs.

---

## Could This System Be Misused? How Would You Prevent It?

Yes. If a bad actor had access to how the profile builder works and how Spotify's search ranking operates, they could craft prompts that consistently surface specific artists — effectively using the system as a manipulation tool to boost streams or skew recommendations toward commercial interests.

Two preventions:

**Transparency.** The profile output is shown to the user before recommendations are generated. You see exactly what the system inferred from your description. If the system got your vibe wrong, you see it immediately. No hidden state.

**Weighted diversity.** A guardrail that caps any single artist at one appearance per recommendation set prevents one act from dominating the output regardless of how the scoring falls. I noted this in the model card as future work. In a production system, it would be a hard requirement.

---

## What Would I Do Differently If I Rebuilt This From Scratch?

**Start with real audio features.** The rule-based lookup table was a workaround for Spotify's API deprecation. If I rebuilt today, I would find a licensed source of actual audio feature data — AcousticBrainz, a scraped dataset, or a local model trained on audio — and use real values instead of estimates by genre/mood bucket. The scoring logic would be the same. The inputs would be far more accurate.

**Design the API layer from day one.** The v2 FastAPI layer was retrofitted onto code that was written to run as a CLI script. The module imports, the file paths, the logger — all of it assumed a specific working directory and runtime context. When uvicorn tried to load the app, it broke in ways that took time to trace. If I had designed for the API from the beginning, the modules would have been stateless functions with clear inputs and outputs, not scripts with side effects. Good system architecture considers deployment from the first commit, not the last.

**Write the model card before the code.** The model card for this project was written after the system was built. Writing it first — forcing myself to document intended use, limitations, and evaluation criteria before writing a single line of code — would have shaped better design decisions. It is harder to cut a feature that already exists than to never build the wrong thing.

---

## What This Project Taught Me That a Tutorial Never Would

That the gap between "it works in the terminal" and "it works for someone who is not me" is enormous — and most of that gap is invisible until you try to close it.

Every tutorial shows you a working demo. The demo runs in a controlled environment, with known inputs, on the author's machine, with no edge cases. Nobody's tutorial covers what happens when Llama returns malformed JSON at 2am, or when Spotify changes what a search query returns between your test run and production, or when you deploy to a platform that uses a different Python path than your local environment.

Real systems fail in ways tutorials do not cover. Building this project end-to-end — from a blank `.py` file to a deployed web app with a custom domain — forced me to encounter and solve real failures. That is what the version number means. v1.0 was a tutorial project. v3.0 is a real one.

---

## The System Architect Angle

When I look at MusicTasteMatch as an architect, I see a 6-stage pipeline where each stage has a single job:

1. **Profile Builder** — natural language → structured data
2. **Catalog Search** — structured query → candidate songs
3. **Feature Assignment** — candidates → scored attributes
4. **Recommender** — attributes → ranked songs
5. **Bias Detector** — ranked output → confidence + flags
6. **Critique** — full context → honest evaluation

Each stage is independent. You can swap Llama for Gemini (I did), swap the CSV for Spotify (I did), or swap the Streamlit interface for a FastAPI + React frontend (I did) — without touching the other stages. That is the whole point of designing in stages. The system is modular by construction, not by accident.

The deployment architecture is equally deliberate: FastAPI serves the React build as static files in production, meaning the entire app — frontend and backend — runs as one service on one Render instance. No separate CDN deployment, no CORS complexity in production, no multiple services to monitor. For a project at this scale, simplicity is the right architecture. A more complex deployment would have more failure points and no real benefit.

---

## The AI Engineer Angle

What makes this an AI engineering project rather than just a Python project is the intentional design of the human-AI boundary.

The AI does two jobs: translate natural language into structured data, and generate a critique of the output. Everything else — scoring, ranking, bias detection, logging — is deterministic code. That split is intentional. Deterministic code is predictable, testable, and auditable. AI is used only where determinism would fail — understanding vague human language, and generating human-readable commentary.

A common mistake in AI engineering is using AI for everything because it feels more impressive. This project uses AI for exactly two tasks. That discipline is what makes the system reliable enough to test, audit, and trust.

---

## Wins

- Built a working AI-powered recommendation system in a class module and kept going when the module ended
- Shipped a live web app with a custom domain — accessible to anyone, no setup required
- Nine automated tests, all passing
- A model card that documents limitations honestly, not just strengths
- Learned FastAPI, Vite, React component architecture, Render deployment, and custom domain DNS — all on this one project

## Hiccups Along the Way

- Spotify deprecated audio features for new developers mid-build, forcing a pivot to rule-based feature estimation
- Llama 3.2's batch JSON output was unreliable and required a validation/fallback layer
- Local inference (Ollama + Llama 3.2) was too slow for interactive use — replaced with Gemini API
- The v2 CLI architecture did not translate cleanly to a FastAPI context — required refactoring module imports and file paths
- Vite proxy configuration only applies in dev mode — API base URL had to be updated to use relative paths for production

---

*This project represents the full arc of what I try to do: start with something real, build it until it works, then ship it so others can use it too.*
