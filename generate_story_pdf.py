from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

doc = SimpleDocTemplate(
    "/home/vivekkarmarkar/Python Files/garmin-to-code/garmin-claude-story.pdf",
    pagesize=letter,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch,
    leftMargin=0.85*inch,
    rightMargin=0.85*inch,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Title'],
    fontSize=24, spaceAfter=6, textColor=HexColor('#1a1a2e'),
    fontName='Helvetica-Bold'
)
subtitle_style = ParagraphStyle(
    'Subtitle', parent=styles['Normal'],
    fontSize=12, spaceAfter=20, textColor=HexColor('#555555'),
    alignment=TA_CENTER, fontName='Helvetica-Oblique'
)
h1_style = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontSize=18, spaceBefore=20, spaceAfter=10,
    textColor=HexColor('#2d3436'), fontName='Helvetica-Bold'
)
h2_style = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontSize=14, spaceBefore=14, spaceAfter=8,
    textColor=HexColor('#636e72'), fontName='Helvetica-Bold'
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontSize=11, spaceAfter=8, leading=15,
    fontName='Helvetica'
)
code_style = ParagraphStyle(
    'Code', parent=styles['Code'],
    fontSize=9, spaceAfter=10, leading=12,
    backColor=HexColor('#f5f5f5'),
    borderColor=HexColor('#dddddd'),
    borderWidth=0.5,
    borderPadding=8,
    fontName='Courier'
)
bullet_style = ParagraphStyle(
    'Bullet', parent=body_style,
    leftIndent=20, bulletIndent=8, spaceAfter=4
)
insight_style = ParagraphStyle(
    'Insight', parent=body_style,
    fontSize=10, leftIndent=15, rightIndent=15,
    backColor=HexColor('#fff9e6'),
    borderColor=HexColor('#f0c040'),
    borderWidth=1,
    borderPadding=10,
    spaceAfter=12, spaceBefore=8,
    fontName='Helvetica-Oblique'
)

story = []

# ──────────────────────────────────────────────
# Title page
# ──────────────────────────────────────────────
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("The Life Layer", title_style))
story.append(Paragraph("Building a Walking Companion with Claude Code", subtitle_style))
story.append(Spacer(1, 0.3*inch))
story.append(HRFlowable(width="60%", thickness=1, color=HexColor('#cccccc')))
story.append(Spacer(1, 0.3*inch))

overview_items = [
    "From a Garmin watch connection to a six-layer life-aware system",
    "Detection, enforcement, and observability for multi-modal channel input",
    "Human-AI collaboration: taste, smell, and steering",
    "Built during walking sessions in Iowa City, April–May 2026",
]
for item in overview_items:
    story.append(Paragraph(f"•  {item}", bullet_style))

story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("Vivek Karmarkar &amp; Claude", ParagraphStyle(
    'DateLine', parent=body_style, alignment=TA_CENTER, textColor=HexColor('#888888')
)))

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 0: Life Layer — Motivation
# ──────────────────────────────────────────────
story.append(Paragraph("0. Life Layer — Motivation", h1_style))
story.append(Paragraph(
    "Claude Code has a code layer (writing software) and an OS layer (skills, hooks, plugins "
    "that personalize it). The life layer is a third layer on top: making Claude aware of your "
    "body, your environment, your nutrition, what you see, and what you say — the physical "
    "reality of the person using it. Life doesn’t happen in text boxes. If you’re walking all "
    "day with only a phone, Claude should know your steps, your heart rate, the weather, what "
    "you ate, what you’re looking at, and what you said out loud — not just what you typed.",
    body_style
))

story.append(Spacer(1, 10))
layer_data = [
    ['Layer', 'What It Is', 'Examples'],
    ['Code', 'The default — writing software,\ndebugging, git, PRs', 'Every Claude Code\nsession'],
    ['OS', 'Personalization infrastructure —\nskills, hooks, plugins, settings', 'claude-code-os\n(160+ skills)'],
    ['Life', 'Your body, your environment,\nyour nutrition, your eyes, your voice', 'Garmin, weather,\nfuel-check, camera, voice'],
]
layer_table = Table(layer_data, colWidths=[0.8*inch, 2.3*inch, 2.0*inch])
layer_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f8f9fa')),
    ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fff3e0')),
    ('BACKGROUND', (0, 3), (-1, 3), HexColor('#e8f5e9')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(layer_table)

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 0.1: Connecting Garmin to Claude Code
# ──────────────────────────────────────────────
story.append(Paragraph("0.1. Connecting Garmin to Claude Code", h1_style))
story.append(Paragraph(
    "The first concrete step: connecting a Garmin wearable to Claude Code through a lightweight "
    "pipeline. Data flows from the watch via Bluetooth to the Garmin Connect app, then through "
    "the cloud API to a local MCP server, and finally into Claude Code as callable tools.",
    body_style
))

story.append(Spacer(1, 10))
flow_data = [
    ['Garmin Watch', '→', 'Garmin Connect App', '→', 'Garmin Cloud API'],
    ['', '', '', '', '↓'],
    ['Claude Code', '←', 'MCP Tools', '←', 'FastMCP Server'],
]
flow_table = Table(flow_data, colWidths=[1.3*inch, 0.4*inch, 1.5*inch, 0.4*inch, 1.3*inch])
flow_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2d3436')),
    ('BACKGROUND', (0, 0), (0, 0), HexColor('#e8f5e9')),
    ('BACKGROUND', (2, 0), (2, 0), HexColor('#e3f2fd')),
    ('BACKGROUND', (4, 0), (4, 0), HexColor('#fce4ec')),
    ('BACKGROUND', (0, 2), (0, 2), HexColor('#f3e5f5')),
    ('BACKGROUND', (2, 2), (2, 2), HexColor('#fff3e0')),
    ('BACKGROUND', (4, 2), (4, 2), HexColor('#fce4ec')),
    ('BOX', (0, 0), (0, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 0), (2, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (4, 0), (4, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (0, 2), (0, 2), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 2), (2, 2), 0.5, HexColor('#aaaaaa')),
    ('BOX', (4, 2), (4, 2), 0.5, HexColor('#aaaaaa')),
]))
story.append(Spacer(1, 10))
story.append(flow_table)

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 0.2: Garmin Architecture
# ──────────────────────────────────────────────
story.append(Paragraph("0.2. Garmin Architecture", h1_style))
story.append(Paragraph(
    "A single Python file (server.py) using FastMCP exposes three tools. "
    "It authenticates via garminconnect and caches tokens at ~/.garmin-tokens.",
    body_style
))

tools_data = [
    ['Tool', 'Description', 'Parameters'],
    ['get_daily_stats', 'Rich daily summary: steps, distance,\ncalories, stress, Body Battery', 'target_date\n(YYYY-MM-DD)'],
    ['get_steps_in_range', 'Step counts + distance for a\ndate range (up to 30 days)', 'start_date,\nend_date'],
    ['get_heart_rate', 'Resting, min, max, avg HR\nfor a specific date', 'target_date\n(YYYY-MM-DD)'],
]
tools_table = Table(tools_data, colWidths=[1.5*inch, 2.8*inch, 1.2*inch])
tools_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
]))
story.append(Spacer(1, 6))
story.append(tools_table)

story.append(Spacer(1, 15))
story.append(Paragraph("Three Lean Skills", h2_style))
story.append(Paragraph(
    "Three global skills wrap the MCP tools for quick conversational access:",
    body_style
))
skills_items = [
    "<b>/step-count</b> — one-line step count for any date",
    "<b>/rich-stats</b> — full daily dashboard with all metrics and an opinionated summary",
    "<b>/fuel-check</b> — context-aware food photo scoring using Garmin stats + weather + time of day",
]
for s in skills_items:
    story.append(Paragraph(f"•  {s}", bullet_style))

story.append(Spacer(1, 15))
story.append(Paragraph("Open-Meteo Weather MCP", h2_style))
story.append(Paragraph(
    "A pre-built MCP server providing global weather data — current conditions, forecasts, "
    "and historical archives. No API key required.",
    body_style
))

weather_data = [
    ['Capability', 'What It Provides'],
    ['Current / Forecast', 'Temperature, humidity, wind,\nprecipitation, UV index'],
    ['Historical Archive', 'ERA5 reanalysis data back to 1940\nfor any coordinates and date range'],
    ['Apparent Temperature', '“Feels like” factoring in wind chill\nand humidity'],
]
weather_table = Table(weather_data, colWidths=[1.8*inch, 3.5*inch])
weather_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(weather_table)

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 0.2.1: HR Recovery Discovery
# ──────────────────────────────────────────────
story.append(Paragraph("0.2.1. Discovery: HR Recovery Patterns", h1_style))
story.append(Paragraph(
    "The Garmin data wasn’t just numbers on a dashboard. By cross-referencing data across "
    "multiple days conversationally — asking Claude questions, getting answers, following up — "
    "the data came alive in a way that static graphs in Garmin Connect never could.",
    body_style
))

story.append(Spacer(1, 8))
hr_data = [
    ['Date', 'Steps', 'Body Battery', 'Resting HR'],
    ['Apr 6', '30,799', '55 → 34', '—'],
    ['Apr 7', '31,120', '51 → 4', '—'],
    ['Apr 8', '11,375', '36 → 3', '63 bpm (worst)'],
    ['', '', '', ''],
    ['Apr 20', '41,107', '59 → 9', '—'],
    ['Apr 21', '14,943', '30 → 20', '—'],
    ['Apr 22', '6,316', '59 → 34', '54 bpm (best)'],
]
hr_table = Table(hr_data, colWidths=[1.1*inch, 1.2*inch, 1.4*inch, 1.6*inch])
hr_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('BACKGROUND', (3, 3), (3, 3), HexColor('#ffebee')),
    ('BACKGROUND', (3, 7), (3, 7), HexColor('#e8f5e9')),
    ('TEXTCOLOR', (3, 3), (3, 3), HexColor('#c62828')),
    ('TEXTCOLOR', (3, 7), (3, 7), HexColor('#2e7d32')),
    ('FONTNAME', (3, 3), (3, 3), 'Helvetica-Bold'),
    ('FONTNAME', (3, 7), (3, 7), 'Helvetica-Bold'),
    ('LINEBELOW', (0, 3), (-1, 3), 1, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, 3), [HexColor('#fff8f8'), HexColor('#fff8f8')]),
    ('ROWBACKGROUNDS', (0, 5), (-1, 7), [HexColor('#f8fff8'), HexColor('#f8fff8')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(hr_table)

story.append(Spacer(1, 10))
story.append(Paragraph(
    "Both sequences had a massive effort day. The difference was what happened <b>after</b>:",
    body_style
))
story.append(Paragraph("•  <b>Apr 6–8:</b>  Big → Big → Crash. No recovery. HR spiked to 63.", bullet_style))
story.append(Paragraph("•  <b>Apr 20–22:</b>  Big → Easy → Easier. Proper taper. HR dropped to 54.", bullet_style))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "This finding emerged from conversation, not computation. The data was always there in "
    "Garmin Connect — but it took asking Claude “why was my HR so high on the 8th?” to "
    "connect the dots across days. That’s the life layer difference: data brought to life "
    "through interaction, not static graphs.",
    insight_style
))

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 0.3: The Camera Problem and the Telegram Idea
# ──────────────────────────────────────────────
story.append(Paragraph("0.3. The Camera Problem and the Telegram Idea", h1_style))
story.append(Paragraph(
    "After Garmin was working, the next goal was a richer snapshot — Garmin plus nutrition. "
    "But the Claude Code app camera was broken for remote control, so there was no way to "
    "send food photos while walking. Claude suggested Telegram as the camera layer. Vivek "
    "tried it on a cappuccino — Claude immediately recognized it and ran /fuel-check-lean. "
    "It worked.",
    body_style
))

story.append(Spacer(1, 8))
story.append(Paragraph(
    "Two threads opened in parallel. First: what if a hook could detect a Telegram food image "
    "and auto-trigger the skill? Second: Vivek was just exploring, playing. He showed Claude "
    "a photo of the neighborhood, then a blurry yellow canopy — Claude guessed Hamburg Inn. "
    "That turned into the /guess-location skill idea, born from curiosity, not planning.",
    body_style
))

story.append(Spacer(1, 10))
sol_data = [
    ['Channel', 'Purpose', 'Strength'],
    ['Remote Control', 'Conversation, commands,\nanalysis, coding', 'Text interaction'],
    ['Telegram', 'Photos, voice notes,\nvisual input', 'Camera + voice\nfrom anywhere'],
]
sol_table = Table(sol_data, colWidths=[1.5*inch, 2.2*inch, 1.5*inch])
sol_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#e8f5e9'), HexColor('#e3f2fd')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(sol_table)

story.append(Spacer(1, 10))
story.append(Paragraph(
    "At that point the vision started forming. Garmin was body. The camera brought nutrition. "
    "Telegram also had voice notes, but what Anthropic shipped was broken — the channel "
    "infrastructure was missing pieces. So it boiled down to one concrete question: can we "
    "build a hook that recognizes a Telegram input, classifies its mode (text, image, or "
    "audio), and figures out what action to take?",
    body_style
))

story.append(Spacer(1, 10))
story.append(Paragraph(
    "The camera layer wasn’t planned — it emerged. A channel designed to send food photos "
    "became a spatial reasoning interface when curiosity met capability. The /guess-location "
    "skill was born from play, not planning. That’s the life layer pattern: infrastructure "
    "designed for one purpose finds its real purpose through use.",
    insight_style
))

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 1: The Unified Problem
# ──────────────────────────────────────────────
story.append(Paragraph("1. The Unified Problem", h1_style))
story.append(Paragraph(
    "A Telegram message can arrive as text, an image, or a voice note. The system needs to: "
    "detect that a Telegram message arrived, classify which of the three modes it is, take "
    "the correct action for that mode, do this reliably across every session and every repo, "
    "and provide visibility into whether it’s actually working. There is no built-in support "
    "for any of this — Claude Code doesn’t distinguish channel message modes, doesn’t enforce "
    "behavior on them, and doesn’t let you observe what happened.",
    body_style
))

story.append(Spacer(1, 10))
problem_data = [
    ['Input Mode', 'Correct Action', 'Challenge'],
    ['Text', 'Reply normally\non Telegram', 'No enforcement that Claude\nactually uses the reply tool'],
    ['Image', 'View image — if food,\nrun /fuel-check-lean', 'No hook fires for\nchannel messages'],
    ['Voice', 'Download .oga, transcribe\nvia Whisper, respond', 'No built-in voice\npipeline exists'],
]
problem_table = Table(problem_data, colWidths=[1.2*inch, 1.8*inch, 2.2*inch])
problem_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(problem_table)

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 2: The Black Box Solution
# ──────────────────────────────────────────────
story.append(Paragraph("2. The Black Box Solution", h1_style))
story.append(Paragraph(
    "The black box solution is behavioral enforcement via a global instruction file. Instead "
    "of building infrastructure (hooks, plugins, custom code) to make Claude act correctly on "
    "channel messages, you write two plain-English rules in ~/.claude/CLAUDE.md and Claude "
    "just follows them. It works — but you can’t see inside it. You have no way to verify "
    "it’s actually following the rules until it doesn’t.",
    body_style
))

story.append(Spacer(1, 10))
blackbox_flow = [
    ['Input', '→', 'CLAUDE.md', '→', 'Output'],
    ['Three modes:\ntext, image, voice', '', 'Two plain-English\nrules', '', 'Correct behavior\n(no visibility)'],
]
blackbox_table = Table(blackbox_flow, colWidths=[1.3*inch, 0.4*inch, 1.5*inch, 0.4*inch, 1.3*inch])
blackbox_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2d3436')),
    ('BACKGROUND', (0, 0), (0, 1), HexColor('#e3f2fd')),
    ('BACKGROUND', (2, 0), (2, 1), HexColor('#424242')),
    ('TEXTCOLOR', (2, 0), (2, 1), HexColor('#ffffff')),
    ('BACKGROUND', (4, 0), (4, 1), HexColor('#e8f5e9')),
    ('BOX', (0, 0), (0, 1), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 0), (2, 1), 0.5, HexColor('#aaaaaa')),
    ('BOX', (4, 0), (4, 1), 0.5, HexColor('#aaaaaa')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
]))
story.append(Spacer(1, 10))
story.append(blackbox_table)

story.append(Spacer(1, 12))
story.append(Paragraph("The Two Rules", h2_style))

rules_data = [
    ['Rule', 'Trigger', 'Action'],
    ['Voice\nTranscription', 'Telegram message with\nattachment_kind="voice"', 'Download .oga → transcribe.py\n(Whisper API) → respond.\nNo hooks. No permissions.'],
    ['Food Image\nDetection', 'Any image (Telegram or\nterminal) containing food', 'Auto-invoke /fuel-check-lean\nas baseline analysis.\nRespect explicit skill choice.'],
]
rules_table = Table(rules_data, colWidths=[1.2*inch, 1.8*inch, 2.2*inch])
rules_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(rules_table)

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 3: The Hallucination Incident
# ──────────────────────────────────────────────
story.append(Paragraph("3. The Hallucination Incident", h1_style))
story.append(Paragraph(
    "CLAUDE.md solved the problem — Claude follows the two rules and acts correctly on "
    "Telegram messages. But it’s a black box. You can’t see whether it’s working. This was "
    "proven when Claude hallucinated that a terminal message came from Telegram — it "
    "misidentified the source and acted on the wrong rules. The black box had no dashboard, "
    "no logs, no flash. It just silently did the wrong thing. That’s when it became clear: "
    "a solution that works isn’t enough. You need to be able to see it working.",
    body_style
))

story.append(Spacer(1, 10))
story.append(Paragraph("The Enforcement Gap", h2_style))

gap_data = [
    ['What Exists', 'What’s Missing'],
    ['<channel> XML tag marks\nsource in prompt', 'No programmatic validation\nof source identity'],
    ['MCP server instructions\ntell Claude how to act', 'No hook event fires\nfor channel messages'],
    ['UserPromptSubmit fires\nfor terminal input', 'No ChannelMessageReceived\nor equivalent event'],
    ['PreToolUse/PostToolUse\nfire for tool calls', 'No per-channel tool\nscoping or routing'],
]
gap_table = Table(gap_data, colWidths=[2.5*inch, 2.5*inch])
gap_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('BACKGROUND', (0, 1), (0, -1), HexColor('#e8f5e9')),
    ('BACKGROUND', (1, 1), (1, -1), HexColor('#ffebee')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(gap_table)

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 4: The Measurement Operator
# ──────────────────────────────────────────────
story.append(Paragraph("4. The Measurement Operator", h1_style))
story.append(Paragraph(
    "The fix for the black box: a shell script that runs automatically every time Claude is "
    "about to send a Telegram reply. Before the reply goes out, the script looks backwards at "
    "what triggered it — was the incoming message text, an image, or a voice note? It flashes "
    "the answer to the terminal so you see it in real time, and writes everything to an audit "
    "log — when it happened, what mode it was, what the reply said, and the exact input that "
    "started it. Every Telegram reply now leaves a trace you can inspect. The same pattern "
    "was then built for photos taken through the terminal camera. Two scripts, two audit logs, "
    "full visibility into a system that was previously invisible.",
    body_style
))

story.append(Spacer(1, 10))
detect_flow = [
    ['Telegram message\narrives', '→', 'Claude decides\nto reply', '→', 'Script fires\nbefore reply'],
    ['', '', '', '', '↓'],
    ['', '', 'Reply\nproceeds', '←', 'Classify mode +\nflash + log'],
]
detect_table = Table(detect_flow, colWidths=[1.3*inch, 0.4*inch, 1.3*inch, 0.4*inch, 1.4*inch])
detect_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2d3436')),
    ('BACKGROUND', (0, 0), (0, 0), HexColor('#e3f2fd')),
    ('BACKGROUND', (2, 0), (2, 0), HexColor('#f3e5f5')),
    ('BACKGROUND', (4, 0), (4, 0), HexColor('#fff3e0')),
    ('BACKGROUND', (2, 2), (2, 2), HexColor('#e8f5e9')),
    ('BACKGROUND', (4, 2), (4, 2), HexColor('#fce4ec')),
    ('BOX', (0, 0), (0, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 0), (2, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (4, 0), (4, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 2), (2, 2), 0.5, HexColor('#aaaaaa')),
    ('BOX', (4, 2), (4, 2), 0.5, HexColor('#aaaaaa')),
]))
story.append(Spacer(1, 10))
story.append(detect_table)

story.append(Spacer(1, 12))
story.append(Paragraph("Mode Classification", h2_style))

mode_data = [
    ['Mode', 'Detection Signal', 'Action Taken'],
    ['text', 'No attachment attributes\nin the input message', 'Reply normally'],
    ['image', 'image_path= attribute\npresent', 'View image — if food,\ntrigger /fuel-check-lean'],
    ['audio', 'attachment_kind="voice"\npresent', 'Download .oga → transcribe\nvia Whisper → respond'],
]
mode_table = Table(mode_data, colWidths=[0.8*inch, 2.0*inch, 2.5*inch])
mode_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(mode_table)

story.append(Spacer(1, 12))
story.append(Paragraph("Audit Trail", h2_style))

output_data = [
    ['Output', 'Where', 'Purpose'],
    ['Terminal flash', '/dev/tty', 'Immediate visual confirmation\nthat a reply is firing'],
    ['Audit log', 'Telegram_calls.md\nor Terminal_image_calls.md', 'Persistent record with timestamp,\nmode, reply text, verbatim input'],
]
output_table = Table(output_data, colWidths=[1.4*inch, 1.8*inch, 2.0*inch])
output_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(output_table)

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 5: Human-AI Collaboration
# ──────────────────────────────────────────────
story.append(Paragraph("5. Human-AI Collaboration", h1_style))
story.append(Paragraph(
    "This project wasn’t one person’s work. Claude built the engine — the MCP server, the "
    "transcription script, the Telegram integration, the detection hooks, the global CLAUDE.md "
    "rules. All the code came from Claude. Vivek provided three things that code can’t provide: "
    "taste, smell, and steering.",
    body_style
))

story.append(Spacer(1, 10))
story.append(Paragraph("Taste", h2_style))
story.append(Paragraph(
    "Pushing for Telegram voice notes when it wasn’t obvious, seeing how separate threads "
    "(camera, food, voice, location) were converging into one unified problem, bringing "
    "frameworks of thinking — Unix philosophy, verify globally, step by step.",
    body_style
))

story.append(Spacer(1, 8))
story.append(Paragraph("Smell", h2_style))
story.append(Paragraph(
    "Designing the observability architecture. CLAUDE.md works but is invisible — you can’t "
    "tell if Claude is following the rules. The hooks, the terminal flash, the audit logs — "
    "that’s the layer that lets you see the system operating. Without it, the black box "
    "stays black.",
    body_style
))

story.append(Spacer(1, 8))
story.append(Paragraph("Steering", h2_style))
story.append(Paragraph(
    "Catching errors, correcting course, validating what worked. The extended dialogue — "
    "dozens of voice notes, corrections, redirections — was the mechanism through which "
    "the right solution emerged.",
    body_style
))

story.append(Spacer(1, 12))
collab_data = [
    ['Contribution', 'Who', 'Parallel'],
    ['Code — MCP server, transcribe.py,\nhooks, CLAUDE.md rules', 'Claude', '—'],
    ['Taste — vision, convergence\nof threads, frameworks', 'Vivek', 'Tao: “penumbra” and\n“softer aspects”'],
    ['Smell — observability\narchitecture, audit logs', 'Vivek', 'Tao: “smell test”'],
    ['Steering — corrections,\nvalidation, dialogue', 'Vivek', 'Schwartz: “guided\nand validated”'],
]
collab_table = Table(collab_data, colWidths=[2.2*inch, 0.8*inch, 2.0*inch])
collab_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('BACKGROUND', (1, 1), (1, 1), HexColor('#e3f2fd')),
    ('BACKGROUND', (1, 2), (1, 4), HexColor('#e8f5e9')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(collab_table)

story.append(Spacer(1, 10))
story.append(Paragraph(
    "There are soft parallels to two recent papers. Tao’s work on AI in mathematics describes "
    "“penumbra” and “softer aspects” — the heuristic reasoning, motivation, and strategy "
    "surrounding a formal core. That maps to Vivek’s taste. Tao’s “smell test” — the "
    "intuitive signal that something is correct or wrong — maps to the observability layer. "
    "Schwartz’s QCD paper credits the human author with having “guided and validated” the "
    "AI’s calculations. Those two words compress the entire steering process into a phrase "
    "that sounds simple but isn’t.",
    insight_style
))

story.append(PageBreak())

# ──────────────────────────────────────────────
# Section 6: The Telephone Layer
# ──────────────────────────────────────────────
story.append(Paragraph("6. The Telephone Layer", h1_style))
story.append(Paragraph(
    "Six layers make up the life layer. Garmin gave Claude the body. Weather gave it the "
    "environment. Nutrition combined camera with Garmin and weather to score food in context. "
    "The camera gave it eyes. Voice notes gave it ears — async, one-way, transcribed through "
    "Whisper.",
    body_style
))

story.append(Spacer(1, 10))
senses_data = [
    ['Layer', 'Infrastructure', 'Status'],
    ['Body', 'Garmin MCP — steps, HR,\nstress, Body Battery', 'Live'],
    ['Environment', 'Open-Meteo MCP — temperature,\nsunshine, feels-like', 'Live'],
    ['Nutrition', 'Camera + /fuel-check\n+ Garmin + weather context', 'Live'],
    ['Eyes', 'Telegram camera → CC app\nnative camera', 'Live'],
    ['Voice', 'transcribe.py (Whisper API)\nfor Telegram .oga files', 'Live'],
    ['Telephone', 'Real-time bidirectional\nvoice — phone call', '?'],
]
senses_table = Table(senses_data, colWidths=[1.2*inch, 2.3*inch, 1.5*inch])
senses_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('TEXTCOLOR', (2, 1), (2, 5), HexColor('#2e7d32')),
    ('FONTNAME', (2, 1), (2, 5), 'Helvetica-Bold'),
    ('TEXTCOLOR', (2, 6), (2, 6), HexColor('#e67e22')),
    ('FONTNAME', (2, 6), (2, 6), 'Helvetica-Bold'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('BACKGROUND', (0, 6), (-1, 6), HexColor('#fff3e0')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(senses_table)

story.append(Spacer(1, 12))
story.append(Paragraph(
    "Five of six are built. The sixth is the logical next step in the progression: a real-time "
    "phone call — going from “Claude reads what you said” to “Claude talks with you.”",
    body_style
))

story.append(Spacer(1, 8))
story.append(Paragraph(
    "But logical doesn’t mean practical. Voice is a spectrum — telephone calls, laptop calls, "
    "voice notes — and each point on the spectrum carries different latency, effort, and feel. "
    "Claude isn’t fast at real-time responses. Latency that’s invisible in a text exchange "
    "becomes unnatural in a live call. And there’s the social weight: a phone call locks you "
    "in, while a voice note lets you keep walking, say what you need at your own pace, and "
    "move on. Voice notes hit a sweet spot that a phone call might not.",
    body_style
))

story.append(Spacer(1, 8))
story.append(Paragraph(
    "The telephone layer is the obvious abstract progression but an open question in practice. "
    "It might work. It might feel worse than what’s already there. It might require setup and "
    "API work that breaks the walking-only constraint. The answer is: try it and find out.",
    insight_style
))

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
story.append(Spacer(1, 20))
story.append(HRFlowable(width="40%", thickness=0.5, color=HexColor('#cccccc')))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Built during walking sessions in Iowa City, April 29 – May 1, 2026.<br/>"
    "The system was tested on the same walks that built it.",
    ParagraphStyle('Footer', parent=body_style, alignment=TA_CENTER,
                   textColor=HexColor('#888888'), fontSize=9, fontName='Helvetica-Oblique')
))

doc.build(story)
print("PDF generated: garmin-claude-story.pdf")
