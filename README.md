# garmin-to-code

A FastMCP server that connects Garmin Connect to Claude Code, exposing watch data (steps, distance, heart rate, stress, Body Battery) as MCP tools.

## Tools

| Tool | Description |
|------|-------------|
| `get_daily_stats` | Rich daily summary — steps, distance (km + mi), calories, active minutes, stress, Body Battery |
| `get_steps_in_range` | Step counts + distance for a date range (up to 30 days) |
| `get_heart_rate` | Resting, min, max HR for a specific date |

## Setup

1. Install dependencies:
   ```bash
   pip install garminconnect fastmcp
   ```

2. Add to `~/.claude.json` under `mcpServers`:
   ```json
   {
     "garmin-connect": {
       "type": "stdio",
       "command": "python3",
       "args": ["/path/to/server.py"],
       "env": {
         "GARMIN_EMAIL": "your@email.com",
         "GARMIN_PASSWORD": "your-password"
       }
     }
   }
   ```

3. Restart Claude Code. The Garmin tools are now available globally.

## Skills

Two global skills wrap the MCP tools for quick access:

- `/step-count` — one-line step count for any date
- `/rich-stats` — full daily dashboard with all metrics

## Data Flow

```
Garmin Watch → (Bluetooth) → Garmin Connect App → (Cloud) → Garmin API → MCP Server → Claude Code
```

Data freshness depends on your last Bluetooth sync.
