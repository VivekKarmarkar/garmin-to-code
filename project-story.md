# Project Story

> **Diagram rule:** All new architectural diagrams use the aesthetic from the existing generate_pdf.py — colored boxes with arrows, Table + TableStyle, matching color palette (greens, blues, pinks, oranges), 9pt Helvetica, HexColor scheme.

---

## 0. Life Layer — Motivation

Claude Code has a code layer (writing software) and an OS layer (skills, hooks, plugins that personalize it). The life layer is a third layer on top: making Claude aware of your body, your environment, your nutrition, what you see, and what you say — the physical reality of the person using it. Life doesn't happen in text boxes. If you're walking all day with only a phone, Claude should know your steps, your heart rate, the weather, what you ate, what you're looking at, and what you said out loud — not just what you typed.

[D] — Life layer stack diagram (Code → OS → Life)

---

## 0.1. Connecting Garmin to Claude Code

The first concrete step — connecting the Garmin watch to Claude Code.

*(Keep existing: System Architecture flow diagram from PDF section 1)*

---

## 0.2. Garmin Architecture

*(Keep existing from PDF: MCP server, tools table, skills (/step-count, /rich-stats, /fuel-check), Open-Meteo weather table, walking workstation stack table.)*

---

## 0.2.1. Discovery: HR Recovery Patterns

*(Keep existing from PDF section 5: HR data table, the finding — stacked big days vs. proper taper, resting HR 63 vs 54. The point: Garmin data brought to life through conversational interaction, not static graphs.)*

---

## 0.3. The Camera Problem and the Telegram Idea

After Garmin was working, the next goal was a richer snapshot — Garmin plus nutrition. But the Claude Code app camera was broken for remote control, so there was no way to send food photos while walking. Claude suggested Telegram as the camera layer. Vivek tried it on a cappuccino — Claude immediately recognized it and ran /fuel-check-lean. It worked.

Two threads opened in parallel. First: what if a hook could detect a Telegram food image and auto-trigger the skill? Second: Vivek was just exploring, playing. He showed Claude a photo of the neighborhood, then a blurry yellow canopy — Claude guessed Hamburg Inn. That turned into the /guess-location skill idea, born from curiosity, not planning.

At that point the vision started forming. Garmin was body. The camera brought nutrition. Telegram also had voice notes, but what Anthropic shipped was broken — the channel infrastructure was missing pieces. So it boiled down to one concrete question: can we build a hook that recognizes a Telegram input, classifies its mode (text, image, or audio), and figures out what action to take?

[D] — Telegram as camera sidecar: two-channel diagram (Remote Control for text, Telegram for photos/voice)

---

## 1. The Unified Problem

A Telegram message can arrive as text, an image, or a voice note. The system needs to: detect that a Telegram message arrived, classify which of the three modes it is, take the correct action for that mode, do this reliably across every session and every repo, and provide visibility into whether it's actually working. There is no built-in support for any of this — Claude Code doesn't distinguish channel message modes, doesn't enforce behavior on them, and doesn't let you observe what happened.

[D] — Three-mode input diagram (text / image / voice → ? → correct action)

---

## 2. The Black Box Solution

The black box solution is behavioral enforcement via a global instruction file. Instead of building infrastructure (hooks, plugins, custom code) to make Claude act correctly on channel messages, you write two plain-English rules in ~/.claude/CLAUDE.md and Claude just follows them. It works — but you can't see inside it. You have no way to verify it's actually following the rules until it doesn't.

[D] — Black box diagram (input → CLAUDE.md [opaque] → correct output... but no visibility)

---

## 3. The Hallucination Incident

CLAUDE.md solved the problem — Claude follows the two rules and acts correctly on Telegram messages. But it's a black box. You can't see whether it's working. This was proven when Claude hallucinated that a terminal message came from Telegram — it misidentified the source and acted on the wrong rules. The black box had no dashboard, no logs, no flash. It just silently did the wrong thing. That's when it became clear: a solution that works isn't enough. You need to be able to see it working.

*(Keep existing from PDF section 9: the enforcement gap table — What Exists vs What's Missing)*

---

## 4. The Measurement Operator

The fix for the black box: a shell script that runs automatically every time Claude is about to send a Telegram reply. Before the reply goes out, the script looks backwards at what triggered it — was the incoming message text, an image, or a voice note? It flashes the answer to the terminal so you see it in real time, and writes everything to an audit log — when it happened, what mode it was, what the reply said, and the exact input that started it. Every Telegram reply now leaves a trace you can inspect. The same pattern was then built for photos taken through the terminal camera. Two scripts, two audit logs, full visibility into a system that was previously invisible.

[D] — Detection flow diagram (message arrives → Claude decides to reply → script fires → classification + flash + log → reply proceeds)
[D] — Mode classification table (text / image / audio — detection signal, action taken)

---

## 5. Human-AI Collaboration

This project wasn't one person's work. Claude built the engine — the MCP server, the transcription script, the Telegram integration, the detection hooks, the global CLAUDE.md rules. All the code came from Claude. Vivek provided three things that code can't provide: taste, smell, and steering.

Taste: pushing for Telegram voice notes when it wasn't obvious, seeing how separate threads (camera, food, voice, location) were converging into one unified problem, bringing frameworks of thinking — Unix philosophy, verify globally, step by step.

Smell: designing the observability architecture. CLAUDE.md works but is invisible — you can't tell if Claude is following the rules. The hooks, the terminal flash, the audit logs — that's the layer that lets you see the system operating. Without it, the black box stays black.

Steering: catching errors, correcting course, validating what worked. The extended dialogue — dozens of voice notes, corrections, redirections — was the mechanism through which the right solution emerged.

There are soft parallels to two recent papers. Tao's work on AI in mathematics describes "penumbra" and "softer aspects" — the heuristic reasoning, motivation, and strategy surrounding a formal core. That maps to Vivek's taste. Tao's "smell test" — the intuitive signal that something is correct or wrong — maps to the observability layer. Schwartz's QCD paper credits the human author with having "guided and validated" the AI's calculations. Those two words compress the entire steering process into a phrase that sounds simple but isn't.

[D] — Contribution map table (What / Who Built It / Parallel)

---

## 6. The Telephone Layer

Six layers make up the life layer. Garmin gave Claude the body. Weather gave it the environment. Nutrition combined camera with Garmin and weather to score food in context. The camera gave it eyes. Voice notes gave it ears — async, one-way, transcribed through Whisper.

Five of six are built. The sixth is the logical next step in the progression: a real-time phone call — going from "Claude reads what you said" to "Claude talks with you."

But logical doesn't mean practical. Voice is a spectrum — telephone calls, laptop calls, voice notes — and each point on the spectrum carries different latency, effort, and feel. Claude isn't fast at real-time responses. Latency that's invisible in a text exchange becomes unnatural in a live call. And there's the social weight: a phone call locks you in, while a voice note lets you keep walking, say what you need at your own pace, and move on. Voice notes hit a sweet spot that a phone call might not.

The telephone layer is the obvious abstract progression but an open question in practice. It might work. It might feel worse than what's already there. It might require setup and API work that breaks the walking-only constraint. The answer is: try it and find out.

[D] — Six layers table (Body / Environment / Nutrition / Eyes / Voice / Telephone — infrastructure, status)

---
