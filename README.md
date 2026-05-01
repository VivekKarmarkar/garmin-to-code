# garmin-to-code

A FastMCP server that connects Garmin Connect to Claude Code, exposing watch data (steps, distance, heart rate, stress, Body Battery) as MCP tools. Also includes the Telegram voice transcription pipeline and the PreToolUse detection system for channel message observability.

## Tools

| Tool | Description |
|------|-------------|
| `get_daily_stats` | Rich daily summary — steps, distance (km + mi), calories, active minutes, stress, Body Battery |
| `get_steps_in_range` | Step counts + distance for a date range (up to 30 days) |
| `get_heart_rate` | Resting, min, max HR for a specific date |

## Voice Transcription

`transcribe.py` transcribes Telegram voice messages (.oga) using the OpenAI Whisper API.

```bash
python3 transcribe.py [path-to-oga-file]
```

If no file is provided, it finds the most recent `.oga` in the Telegram inbox (`~/.claude/channels/telegram/inbox/`).

Requires `OPENAI_API_KEY` in the environment.

## Telegram Detection System

A PreToolUse hook (`~/.claude/hooks/pretool-detect-telegram.sh`) provides observability for Telegram channel messages:

- **Terminal flash** — prints `Telegram Reply Detected = True` and `mode = text|image|audio` to the terminal via `/dev/tty`
- **Audit log** — appends each Telegram reply to `Telegram_calls.md` with timestamp, chat ID, reply text, mode, and the verbatim input message extracted from the session transcript
- **Food detection** — injects `additionalContext` for image-mode messages, triggering the `/fuel-check-lean` skill on food photos

## Terminal Image Detection

A UserPromptSubmit hook (`~/.claude/hooks/userprompt-detect-image.sh`) detects camera images sent via the Claude Code mobile app:

- **Terminal flash** — prints `Terminal Image Detected = True` to the terminal via `/dev/tty`
- **Audit log** — appends each detection to `Terminal_image_calls.md` with timestamp, image path, and full input
- **Food detection** — injects `additionalContext` triggering `/fuel-check-lean` on food photos

Note: The CC app requires text alongside images (image-only sends silently fail — [#55198](https://github.com/anthropics/claude-code/issues/55198)). Workaround: type `/fuel-check-lean` as the text input.

## Skills

Three global skills wrap the MCP tools for quick access:

- `/step-count` — one-line step count for any date
- `/rich-stats` — full daily dashboard with all metrics
- `/fuel-check-lean` — quick food analysis from a Telegram photo

## Data Flow

```
Garmin Watch → (Bluetooth) → Garmin Connect App → (Cloud) → Garmin API → MCP Server → Claude Code
```

```
Telegram Voice → Bot API → Channel Plugin → transcribe.py (Whisper) → Claude Code
```

```
Telegram Reply → PreToolUse Hook → Terminal Flash + Telegram_calls.md Audit Log
```

```
CC App Camera → UserPromptSubmit Hook → Terminal Flash + Terminal_image_calls.md Audit Log
```

Data freshness depends on your last Bluetooth sync.
