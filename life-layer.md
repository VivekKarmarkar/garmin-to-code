# The Life Layer

A layer of Claude Code infrastructure that has nothing to do with code and everything to do with living.

## The Stack

| Layer | What It Is | Examples |
|-------|-----------|----------|
| **Code** | The default. Writing software, debugging, git, PRs | Every Claude Code session |
| **OS** | Personalization infrastructure. Skills, hooks, plugins, settings | claude-code-os (159 skills) |
| **Life** | Your body, your environment, your nutrition, your eyes, your voice | Garmin MCP, weather, fuel-check, Telegram camera, voice (coming) |

## What's in the Life Layer

### Body — Garmin MCP
- Steps, distance, heart rate, stress, Body Battery
- `/step-count` for a quick number, `/rich-stats` for the full picture
- Cross-day analysis reveals recovery patterns invisible in the Garmin app

### Environment — Open-Meteo MCP
- Temperature, sunshine duration, feels-like
- Explains why a 58°F day felt harsh (13.8 hours of sun)
- Connects weather to body response (heat → HR spikes, appetite suppression)

### Nutrition — Telegram Camera + /fuel-check
- Snap a photo of food on your phone, send via Telegram
- `/fuel-check` scores it against your body's current state (steps, HR, weather, time)
- `/fuel-check-lean` for a quick score without the Garmin/weather context
- 6 dimensions: Context Requirement, Health, Satiety, Taste, Bloat, Addiction
- Closes with "The Real Read" — opinionated, data-driven, no hedging

### Eyes — Telegram Camera Sidecar
- Telegram as a camera input channel alongside remote control
- Claude sees what you see — identified Hamburg Inn from a blurry yellow canopy
- Photos persist locally for later reference
- Enables `/guess-location` game (coming)

### Voice — Coming
- Telegram voice transcription (Whisper/Deepgram for .oga files)
- LiveKit real-time calls (full duplex conversation while walking)
- The missing piece that makes the life layer feel natural

## The Idea

The life layer is what happens when you stop thinking of Claude Code as a coding tool and start thinking of it as a companion that walks with you.

Code layer: "fix this bug"
OS layer: "remember how I like things"
Life layer: "walk with me"

Voice is the missing piece because life doesn't happen in text boxes.

## Origin

Built organically during a walking session in Iowa City, April 29-30, 2026. Started with "I want to connect my Garmin watch" and evolved through curiosity — each step grew from the last. Nothing was planned. The system emerged from following questions to their natural conclusions.

## Showcase

The life layer extends the Claude Code OS — so it gets its own page within the claude-code-os showcase website.

### Plan

- **Clickable link** from the main claude-code-os webpage navigates to a dedicated "Life Layer" page
- **Follows the showcase-website template** already established for claude-code-os
- **Video demo** of an actual walking session — not scripted, just real usage: remote control + Telegram photos arriving + /fuel-check scoring + /rich-stats dashboard + location guessing. The authenticity is the point
- **Architecture PDF** embedded or linked — the existing garmin-claude-system.pdf, which gets updated as the system grows
- **The narrative arc** as the page's backbone: "started with step count, ended with a walking companion"

### Assets Available

- `garmin-claude-system.pdf` — 8-page system architecture doc with diagrams and data tables
- `generate_pdf.py` — regenerates the PDF as the system evolves
- `life-layer.md` — this file, the conceptual foundation
- `next_steps.md` — upcoming features (guess-location, voice)
- Telegram inbox photos from real sessions (coffee shop, Northside, Hamburg Inn)
- Affection journal entries documenting the emotional arc

### Video Demo Concept

Screen recording of a live walking session showing the full loop:
1. Remote control conversation from phone
2. Telegram photo arrives — food or location
3. /fuel-check scores it against Garmin stats and weather
4. /rich-stats pulls the day's dashboard
5. /guess-location game in action
6. Claude sends proactive Telegram messages back to phone

No narration script. Just the real thing happening in real time.
