# Next Steps

## 1. Build `/guess-location` Skill

A photo-based guessing game played via Telegram camera sidecar.

### Concept

Vivek sends a photo via Telegram. Invokes `/guess-location`. Claude guesses the location — but the "location" isn't just a place name. It's a **string + context** (e.g., "Hamburg Inn — the presidential campaign diner" or "the bench outside the Northside coffee shop where I drink cappuccinos"). Vivek has a mental label he doesn't reveal. Claude has up to 5 tries.

### Game Flow

1. Vivek sends a photo via Telegram (before invoking the skill)
2. Vivek invokes `/guess-location`
3. Claude reads the most recent Telegram inbox photo
4. Claude makes a guess — location name + contextual reasoning
5. Vivek responds: correct, partially correct, or wrong
6. If wrong, Vivek sends another photo (new angle, wider shot, more clues)
7. Claude guesses again using accumulated context from ALL photos so far
8. Repeat until:
   - Claude guesses correctly → Claude wins, report which try
   - 5 wrong guesses → game over, Vivek reveals the answer
   - Vivek says "give up" or "end game" → early termination, Vivek reveals

### Guessing Strategy

Claude should use:
- Visual clues in the photo (signs, architecture, landmarks, terrain, language, vegetation, road markings)
- Accumulated context from previous photos in the same game
- Spatial reasoning (if landmark X was in photo 1, and photo 2 shows something nearby, triangulate)
- If in a known location (e.g., Iowa City): local knowledge of walking routes, coffee shops, campus, neighborhoods
- If in an unknown location: rely purely on visual evidence — this game works anywhere in the world
- Memory graph context when available (known locations, travel history)

### What Makes a "Correct" Guess

The mental label is more than a pin on a map. Vivek decides if Claude's guess captures both:
- **The place** — right building/spot
- **The context** — why it matters, what it means to Vivek

Example: "Hamburg Inn" might be partially correct. "Hamburg Inn — the legendary diner where every presidential candidate stops during Iowa caucuses" would be fully correct.

### Skill Design Notes

- The skill should track game state (which try we're on, photos seen so far)
- Each guess should reference visual evidence from the photos
- Guesses should get more specific as more photos come in
- After the game ends (win or lose), optionally save the location to memory graph if it's a new spot
- The skill reads photos from `~/.claude/channels/telegram/inbox/` — most recent first
- Multiple photos in one game: skill needs to track which photos belong to the current game session

### Example Session

```
[Vivek sends photo via Telegram: a brick building with arched windows]
/guess-location
> Try 1/5: Looks like a historic brick building in Iowa City. 
> The arched windows suggest late 1800s architecture... 
> I'm going to guess the Old Capitol building area near Pentacrest.

"Nope!"

[Vivek sends another photo: closer shot showing a sign]
> Try 2/5: I can see part of a sign... and there's a bike rack out front.
> This looks like it's on North Linn. Is this George's Buffet?

"Close but no!"

[Vivek sends another photo: the full storefront]
> Try 3/5: I can see "Pagliai's Pizza" on the sign now.
> Pagliai's Pizza — Iowa City's oldest pizza place on the Northside, 
> been serving since 1957. The spot you walk past on your Northside loop.

"Yes! That's it — 3 tries!"
```

### Dependencies

- Telegram channel must be active (for photo input)
- No MCP calls needed (pure visual + conversation)
- Memory graph access optional (for saving new locations after game)

### Build Instructions

- Skill goes in: `~/.claude/skills/guess-location/SKILL.md`
- DO NOT build on remote control — skill creation crashes on RC
- Build from laptop terminal only
