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
    "/home/vivekkarmarkar/Python Files/garmin-to-code/garmin-claude-system.pdf",
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

# Title page
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("Garmin + Claude Code", title_style))
story.append(Paragraph("A Walking Workstation System", subtitle_style))
story.append(Spacer(1, 0.3*inch))
story.append(HRFlowable(width="60%", thickness=1, color=HexColor('#cccccc')))
story.append(Spacer(1, 0.3*inch))

overview_items = [
    "FastMCP server exposing Garmin watch data as MCP tools",
    "Open-Meteo MCP for weather context — temperature, sunshine, feels-like",
    "Three lean skills: /step-count, /rich-stats, /fuel-check",
    "Telegram as a sidecar camera channel for food photo capture",
    "Built for remote-control walking sessions on a phone",
    "Three pillars: Weather + Movement + Nutrition",
]
for item in overview_items:
    story.append(Paragraph(f"•  {item}", bullet_style))

story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("April 2026  —  Built in a single walking session", ParagraphStyle(
    'DateLine', parent=body_style, alignment=TA_CENTER, textColor=HexColor('#888888')
)))

story.append(PageBreak())

# Section 1: Architecture
story.append(Paragraph("1. System Architecture", h1_style))
story.append(Paragraph(
    "The system connects a Garmin wearable to Claude Code through a lightweight pipeline. "
    "Data flows from the watch via Bluetooth to the Garmin Connect app, then through the cloud "
    "API to a local MCP server, and finally into Claude Code as callable tools.",
    body_style
))

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
story.append(Spacer(1, 10))

story.append(Paragraph(
    "Data freshness depends on the last Bluetooth sync between the watch and phone. "
    "The MCP server caches Garmin authentication tokens locally to avoid rate limiting.",
    body_style
))

# Section 2: MCP Server
story.append(Paragraph("2. Garmin MCP Server", h1_style))
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
    ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f8f9fa')),
    ('BACKGROUND', (0, 3), (-1, 3), HexColor('#f8f9fa')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
]))
story.append(Spacer(1, 6))
story.append(tools_table)

story.append(Spacer(1, 10))
story.append(Paragraph("Global MCP Configuration (~/.claude.json):", h2_style))
story.append(Paragraph(
    '"garmin-connect": {<br/>'
    '&nbsp;&nbsp;"type": "stdio",<br/>'
    '&nbsp;&nbsp;"command": "python3",<br/>'
    '&nbsp;&nbsp;"args": ["/path/to/server.py"],<br/>'
    '&nbsp;&nbsp;"env": { "GARMIN_EMAIL": "...", "GARMIN_PASSWORD": "..." }<br/>'
    '}',
    code_style
))

story.append(Spacer(1, 15))
story.append(Paragraph("Open-Meteo Weather MCP", h2_style))
story.append(Paragraph(
    "A pre-built MCP server providing global weather data — current conditions, forecasts, "
    "and historical archives. No API key required. Configured globally in ~/.claude.json.",
    body_style
))

weather_data = [
    ['Capability', 'What It Provides'],
    ['Current / Forecast', 'Temperature, humidity, wind,\nprecipitation, UV index'],
    ['Historical Archive', 'ERA5 reanalysis data back to 1940\nfor any coordinates and date range'],
    ['Apparent Temperature', '"Feels like" factoring in wind chill\nand humidity'],
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
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Weather data closes the loop on understanding daily performance. A high resting HR "
    "or irritability during a walk can be cross-referenced with temperature and sunshine "
    "duration — separating heat stress from genuine fatigue. Example: Apr 29 felt harsh "
    "despite being only 58°F because the sun was out for 13.8 hours straight.",
    insight_style
))

story.append(PageBreak())

# Section 3: Skills
story.append(Paragraph("3. Three Lean Skills", h1_style))
story.append(Paragraph(
    "Three global skills wrap the MCP tools for quick conversational access. "
    "They live in ~/.claude/skills/ and are available in every Claude Code session.",
    body_style
))

story.append(Paragraph("/step-count", h2_style))
story.append(Paragraph(
    "A one-liner. Takes an optional date argument (defaults to today). "
    "Calls get_daily_stats and outputs a single line:",
    body_style
))
story.append(Paragraph(
    "<b>2026-04-29: 42,396 steps (33.76 km / 20.98 mi)</b>",
    ParagraphStyle('Example', parent=body_style, leftIndent=20,
                   backColor=HexColor('#f0f0f0'), borderPadding=6)
))
story.append(Paragraph("No tables, no analysis, no extra commentary. One line.", body_style))

story.append(Spacer(1, 8))
story.append(Paragraph("/rich-stats", h2_style))
story.append(Paragraph(
    "Full daily dashboard. Calls both get_daily_stats and get_heart_rate in parallel, "
    "then presents a comprehensive table with an opinionated one-line summary.",
    body_style
))

rich_data = [
    ['Metric', 'Example Value'],
    ['Steps', '42,396'],
    ['Distance', '33.76 km / 20.98 mi'],
    ['Calories (total / active)', '3,112 / 1,123'],
    ['Active Minutes', '479 (7.98 hrs)'],
    ['Stress', 'Balanced (avg 28)'],
    ['Body Battery', '52 → 13'],
    ['Resting HR', '58 bpm'],
    ['Max / Min HR', '127 / 51 bpm'],
]
rich_table = Table(rich_data, colWidths=[2.5*inch, 2.5*inch])
rich_table.setStyle(TableStyle([
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
story.append(rich_table)
story.append(Spacer(1, 8))

story.append(Paragraph(
    "The one-line read at the end is opinionated and matches the tone to the data:",
    body_style
))
examples = [
    '"You ground out 42K steps on a body that started at 52% battery and drained to 13 — pure stubborn endurance on fumes."',
    '"Recovery day — calm stress, low output, your body is rebuilding."',
]
for ex in examples:
    story.append(Paragraph(f"•  {ex}", bullet_style))

story.append(Spacer(1, 8))
story.append(Paragraph("/fuel-check", h2_style))
story.append(Paragraph(
    "Context-aware food analysis. Takes a photo (from Telegram or a file path), identifies "
    "the food, then scores it against your body's current state — pulling Garmin stats, "
    "weather, and time of day in parallel.",
    body_style
))

story.append(Paragraph("How it works:", body_style))
fuel_steps = [
    "<b>1.</b>  Resolves image — uses the most recent Telegram inbox photo if no path given",
    "<b>2.</b>  Verifies it's food/drink — rejects non-food photos",
    "<b>3.</b>  Gathers context — today's steps, HR, Body Battery, weather, time of day",
    "<b>4.</b>  Identifies the item — brand, flavor, size, calories, macros",
    "<b>5.</b>  Scores on 6 dimensions with contextual justifications",
    "<b>6.</b>  Closes with \"The Real Read\" — opinionated, data-driven analysis",
]
for s in fuel_steps:
    story.append(Paragraph(s, bullet_style))

story.append(Spacer(1, 8))
score_data = [
    ['Dimension', 'What It Measures'],
    ['Context Requirement', 'Does your body need this right now?'],
    ['Health', 'Nutritional quality — whole vs processed'],
    ['Satiety', 'Will this actually make you feel full?'],
    ['Taste', 'How good does this taste given your state?'],
    ['Bloat', 'Will this sit well if you keep walking?'],
    ['Addiction', 'How engineered is this to hook you?'],
]
score_table = Table(score_data, colWidths=[1.8*inch, 3.5*inch])
score_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(score_table)
story.append(Spacer(1, 8))

story.append(Paragraph(
    "Example Real Read: \"You drained your Body Battery to 13 on 42K steps, skipped lunch "
    "for the third day in a row, and now you're reaching for sugar water at 1 AM. The "
    "Gatorade isn't the problem — it's the symptom.\"",
    insight_style
))

story.append(PageBreak())

# Section 4: Telegram
story.append(Paragraph("4. Telegram: The Camera Sidecar", h1_style))
story.append(Paragraph(
    "The food photo problem: how do you send images to Claude Code while walking with only "
    "your phone? Remote control handles text but has no camera. CCPhoto and local camera "
    "servers require same-WiFi. The solution was hiding in plain sight.",
    body_style
))

story.append(Paragraph("The Problem", h2_style))
problems = [
    "Claude Code remote control UI does not support camera or image attachment",
    "CCPhoto MCP server requires QR code scan + same WiFi as laptop",
    "Local camera servers have the same same-network constraint",
    "User is walking outdoors with only a phone — laptop is at home",
]
for p in problems:
    story.append(Paragraph(f"•  {p}", bullet_style))

story.append(Paragraph("The Solution", h2_style))
story.append(Paragraph(
    "Telegram as a sidecar channel alongside remote control. One session, two interfaces:",
    body_style
))

sol_data = [
    ['Channel', 'Purpose', 'Strength'],
    ['Remote Control', 'Conversation, commands,\nanalysis, coding', 'Text interaction'],
    ['Telegram', 'Photos, visual input', 'Camera access\nfrom anywhere'],
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
story.append(Paragraph("Launch Command:", h2_style))
story.append(Paragraph(
    "claude --channels plugin:telegram@claude-plugins-official --remote-control",
    code_style
))

story.append(Paragraph("The Food Photo Flow", h2_style))
steps = [
    "<b>1.</b>  You're walking, you grab food",
    "<b>2.</b>  Open Telegram on your phone, snap a photo, send it",
    "<b>3.</b>  Claude sees it instantly — identifies food, estimates calories, logs it",
    "<b>4.</b>  Switch to remote control: \"what was in that?\" or \"log that\"",
    "<b>5.</b>  Later: \"/rich-stats\" pairs your steps with what you ate",
]
for s in steps:
    story.append(Paragraph(s, bullet_style))

story.append(Spacer(1, 10))
story.append(Paragraph(
    "Photos are saved locally at ~/.claude/channels/telegram/inbox/ — "
    "they persist on disk, so Claude can reference them later or review all meals at end of day.",
    body_style
))

story.append(Spacer(1, 10))
story.append(Paragraph(
    "Bonus: Claude can also send messages to Telegram proactively — step count updates, "
    "lunch reminders, or end-of-day summaries arrive as push notifications on the phone.",
    insight_style
))

story.append(PageBreak())

# Section 5: HR Analysis Discovery
story.append(Paragraph("5. Discovery: HR Recovery Patterns", h1_style))
story.append(Paragraph(
    "An unexpected finding from cross-referencing Garmin data across multiple days. "
    "Resting HR isn't a fitness metric — it's a recovery metric.",
    body_style
))

story.append(Paragraph("The Data", h2_style))
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
story.append(Paragraph("The Finding", h2_style))
story.append(Paragraph(
    "Both sequences had a massive effort day. The difference was what happened <b>after</b>:",
    body_style
))
story.append(Paragraph("•  <b>Apr 6–8:</b>  Big → Big → Crash. No recovery. HR spiked to 63.", bullet_style))
story.append(Paragraph("•  <b>Apr 20–22:</b>  Big → Easy → Easier. Proper taper. HR dropped to 54.", bullet_style))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "The body can handle 40K+ step days. It can't handle them stacked without recovery. "
    "One easy day after a big effort brings resting HR back near the old ultra-running "
    "range of 40–50 bpm. This is the same principle behind training periodization — "
    "adaptation happens during recovery, not during effort.",
    insight_style
))

story.append(PageBreak())

# Section 6: The Big Picture
story.append(Paragraph("6. The Walking Workstation", h1_style))
story.append(Paragraph(
    "Everything built in this session serves one goal: enabling productive work while "
    "walking all day with nothing but a phone.",
    body_style
))

story.append(Spacer(1, 10))
stack_data = [
    ['Layer', 'Component', 'What It Does'],
    ['Data', 'Garmin MCP Server', 'Pipes watch data into Claude Code'],
    ['Data', 'Open-Meteo MCP', 'Weather context for any location/date'],
    ['Interface', '/step-count skill', 'One-line step lookup'],
    ['Interface', '/rich-stats skill', 'Full daily dashboard + analysis'],
    ['Interface', '/fuel-check skill', 'Context-aware food photo scoring'],
    ['Input', 'Remote Control', 'Text conversation from phone'],
    ['Input', 'Telegram Channel', 'Camera/photo input from phone'],
    ['Output', 'Telegram Messages', 'Push notifications to phone'],
]
stack_table = Table(stack_data, colWidths=[1*inch, 1.8*inch, 2.5*inch])
stack_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('SPAN', (0, 1), (0, 1)),
    ('SPAN', (0, 2), (0, 3)),
    ('SPAN', (0, 4), (0, 5)),
]))
story.append(stack_table)

story.append(Spacer(1, 15))
story.append(Paragraph(
    "Three pillars — weather, movement, and nutrition — captured through two MCP servers "
    "and a Telegram sidecar. Remote control handles conversation, Telegram handles camera, "
    "Garmin handles the body, Open-Meteo handles the environment. "
    "Together they cover everything a walking workstation needs.",
    insight_style
))

story.append(PageBreak())

# Section 7: The Camera Layer — From Design to Visceral
story.append(Paragraph("7. The Camera Layer", h1_style))
story.append(Paragraph(
    "Telegram was designed as a camera sidecar — a way to send food photos to Claude Code "
    "while walking. That was the architecture. But the moment it became real was when Claude "
    "identified Hamburg Inn from a blurry yellow canopy two blocks away, using nothing but "
    "spatial reasoning on Telegram photos. No GPS. No laptop. Just photos from a phone "
    "and context from conversation.",
    body_style
))

story.append(Spacer(1, 8))
story.append(Paragraph("The Evolution", h2_style))

evo_data = [
    ['Stage', 'What Happened', 'What It Meant'],
    ['Design', 'Telegram added as a channel\nfor food photo input', 'Camera sidecar\narchitecture'],
    ['First Use', 'Sent a Gatorade photo,\nClaude scored it 6 ways', '/fuel-check became\na real workflow'],
    ['Organic Shift', 'Sent coffee shop photos,\nClaude guessed the location', 'Camera became\neyes, not just input'],
    ['Skill Concept', '/guess-location designed —\nphoto-based location game', 'The camera layer\ngenerates its own skills'],
]
evo_table = Table(evo_data, colWidths=[1.2*inch, 2.0*inch, 1.8*inch])
evo_table.setStyle(TableStyle([
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
story.append(evo_table)

story.append(Spacer(1, 10))
story.append(Paragraph(
    "The camera layer wasn't planned — it emerged. A channel designed to send food photos "
    "became a spatial reasoning interface when curiosity met capability. The /guess-location "
    "skill was born from play, not planning. That's the life layer pattern: infrastructure "
    "designed for one purpose finds its real purpose through use.",
    insight_style
))

story.append(PageBreak())

# Section 8: Voice Transcription
story.append(Paragraph("8. Voice: The Missing Piece", h1_style))
story.append(Paragraph(
    "The life layer concept identified voice as the missing piece — \"life doesn't happen "
    "in text boxes.\" Telegram voice messages (.oga files) are now transcribed via OpenAI's "
    "Whisper API through a standalone Python script.",
    body_style
))

story.append(Spacer(1, 8))
story.append(Paragraph("Voice Pipeline", h2_style))

voice_flow = [
    ['User speaks', '→', 'Telegram sends\n.oga file', '→', 'Channel plugin\ndelivers to CC'],
    ['', '', '', '', '↓'],
    ['Claude responds\non Telegram', '←', 'Transcript\nas text', '←', 'transcribe.py\n(Whisper API)'],
]
voice_table = Table(voice_flow, colWidths=[1.3*inch, 0.4*inch, 1.3*inch, 0.4*inch, 1.4*inch])
voice_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2d3436')),
    ('BACKGROUND', (0, 0), (0, 0), HexColor('#e8f5e9')),
    ('BACKGROUND', (2, 0), (2, 0), HexColor('#e3f2fd')),
    ('BACKGROUND', (4, 0), (4, 0), HexColor('#fff3e0')),
    ('BACKGROUND', (0, 2), (0, 2), HexColor('#f3e5f5')),
    ('BACKGROUND', (2, 2), (2, 2), HexColor('#fce4ec')),
    ('BACKGROUND', (4, 2), (4, 2), HexColor('#fff3e0')),
    ('BOX', (0, 0), (0, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 0), (2, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (4, 0), (4, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (0, 2), (0, 2), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 2), (2, 2), 0.5, HexColor('#aaaaaa')),
    ('BOX', (4, 2), (4, 2), 0.5, HexColor('#aaaaaa')),
]))
story.append(Spacer(1, 10))
story.append(voice_table)

story.append(Spacer(1, 12))
story.append(Paragraph("Key Design Decisions", h2_style))
voice_decisions = [
    "<b>Standalone script</b> — transcribe.py does one thing (Unix philosophy), no plugin modifications",
    "<b>No hooks needed</b> — Claude recognizes attachment_kind=\"voice\" in the channel tag and acts",
    "<b>Zero permissions</b> — once allowed, voice transcription runs without prompts",
    "<b>Ogg/Opus native</b> — Telegram's .oga format is accepted directly by Whisper, no conversion",
]
for v in voice_decisions:
    story.append(Paragraph(f"•  {v}", bullet_style))

story.append(Spacer(1, 10))
story.append(Paragraph(
    "Voice was the hardest feature to ship — not because of the transcription (that worked "
    "immediately), but because of the delivery mechanism. UserPromptSubmit hooks don't fire "
    "for channel messages. Plugin forks broke working infrastructure. The solution was the "
    "simplest possible: Claude just reads the channel tag and acts. No infrastructure, "
    "just behavioral pattern recognition.",
    insight_style
))

story.append(PageBreak())

# Section 9: Channel Detection System
story.append(Paragraph("9. Channel Detection &amp; Observability", h1_style))
story.append(Paragraph(
    "Anthropic shipped the channels feature with no enforcement layer for message source "
    "identity. The &lt;channel&gt; tag that marks Telegram messages is just text in the prompt — "
    "Claude is told how to interpret it, but nothing makes it. This was proven when Claude "
    "hallucinated that a terminal message came from Telegram.",
    body_style
))

story.append(Spacer(1, 8))
story.append(Paragraph("The Enforcement Gap", h2_style))

gap_data = [
    ['What Exists', 'What\'s Missing'],
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

story.append(Spacer(1, 12))
story.append(Paragraph("The Detection System", h2_style))
story.append(Paragraph(
    "A PreToolUse hook on the Telegram reply tool provides observability without interference. "
    "It detects, classifies, and logs — but never blocks.",
    body_style
))

detect_flow = [
    ['Telegram message\narrives', '→', 'Claude decides\nto reply', '→', 'PreToolUse\nhook fires'],
    ['', '', '', '', '↓'],
    ['', '', 'Tool call\nproceeds', '←', 'Detection +\nClassification'],
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
story.append(Paragraph("Three Output Channels", h2_style))

output_data = [
    ['Output', 'Where', 'Purpose'],
    ['Terminal flash', '/dev/tty', 'Immediate visual confirmation\nthat a TG reply is firing'],
    ['Debug log', '--debug-file', 'Persistent record of every\nhook execution with metadata'],
    ['Telegram_calls.md', 'Project repo', 'Audit log with timestamp,\nmode, reply text, verbatim input'],
]
output_table = Table(output_data, colWidths=[1.4*inch, 1.2*inch, 2.5*inch])
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

story.append(Spacer(1, 12))
story.append(Paragraph("Mode Classification", h2_style))

mode_data = [
    ['Mode', 'Detection Signal', 'Additional Action'],
    ['text', 'No attachment attributes\nin channel tag', 'None'],
    ['image', 'image_path= attribute\npresent in channel tag', 'additionalContext injected:\ncheck if food → /fuel-check-lean'],
    ['audio', 'attachment_kind="voice"\nin channel tag', 'Download .oga → transcribe.py\n→ Whisper API → respond'],
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

story.append(Spacer(1, 10))
story.append(Paragraph(
    "The hook reads the session transcript to extract the verbatim input message that "
    "triggered the reply. This means Telegram_calls.md contains ground truth — not what "
    "Claude thought the message was, but what the message actually was, including the full "
    "&lt;channel&gt; tag with all attributes. The audit trail is unforgeable.",
    insight_style
))

story.append(PageBreak())

# Section 10: The Life Layer
story.append(Paragraph("10. The Life Layer", h1_style))
story.append(Paragraph(
    "The life layer is what happens when you stop thinking of Claude Code as a coding tool "
    "and start thinking of it as a companion that walks with you. It sits on top of the "
    "OS layer (skills, hooks, plugins) and beneath nothing — it's the top of the stack.",
    body_style
))

story.append(Spacer(1, 8))
layer_data = [
    ['Layer', 'What It Is', 'Examples'],
    ['Code', 'The default — writing software,\ndebugging, git, PRs', 'Every Claude Code\nsession'],
    ['OS', 'Personalization infrastructure —\nskills, hooks, plugins, settings', 'claude-code-os\n(160 skills)'],
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

story.append(Spacer(1, 12))
story.append(Paragraph("Five Senses of the Life Layer", h2_style))

senses_data = [
    ['Sense', 'Infrastructure', 'Status'],
    ['Body', 'Garmin MCP — steps, HR,\nstress, Body Battery', 'Live'],
    ['Environment', 'Open-Meteo MCP — temperature,\nsunshine, feels-like', 'Live'],
    ['Nutrition', 'Telegram camera + /fuel-check\n+ /fuel-check-lean', 'Live'],
    ['Eyes', 'Telegram camera sidecar —\nphoto input, spatial reasoning', 'Live'],
    ['Voice', 'transcribe.py (Whisper API)\nfor Telegram .oga files', 'Live'],
]
senses_table = Table(senses_data, colWidths=[1.2*inch, 2.3*inch, 1.5*inch])
senses_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3436')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
    ('TEXTCOLOR', (2, 1), (2, -1), HexColor('#2e7d32')),
    ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f9fa'), HexColor('#ffffff')]),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(Spacer(1, 6))
story.append(senses_table)

story.append(Spacer(1, 12))
story.append(Paragraph("The Full System", h2_style))

full_data = [
    ['Phone Input', '→', 'Claude Code', '→', 'Phone Output'],
    ['Remote Control\n(text)', '', '', '', 'Terminal\nresponses'],
    ['Telegram text', '', 'PreToolUse hook', '', 'Telegram replies'],
    ['Telegram photo', '', 'Mode classification', '', '/fuel-check-lean'],
    ['Telegram voice', '', 'transcribe.py', '', 'Transcribed reply'],
    ['', '', '↕', '', ''],
    ['', '', 'Garmin MCP +\nOpen-Meteo MCP', '', ''],
]
full_table = Table(full_data, colWidths=[1.3*inch, 0.4*inch, 1.5*inch, 0.4*inch, 1.3*inch])
full_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2d3436')),
    ('BACKGROUND', (0, 0), (0, 0), HexColor('#e3f2fd')),
    ('BACKGROUND', (2, 0), (2, 0), HexColor('#f3e5f5')),
    ('BACKGROUND', (4, 0), (4, 0), HexColor('#e8f5e9')),
    ('BACKGROUND', (2, 6), (2, 6), HexColor('#fff3e0')),
    ('BOX', (0, 0), (0, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 0), (2, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (4, 0), (4, 0), 0.5, HexColor('#aaaaaa')),
    ('BOX', (2, 6), (2, 6), 0.5, HexColor('#aaaaaa')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('GRID', (0, 1), (-1, 4), 0.5, HexColor('#eeeeee')),
]))
story.append(Spacer(1, 10))
story.append(full_table)

story.append(Spacer(1, 15))
story.append(Paragraph(
    "Code layer: \"fix this bug.\" OS layer: \"remember how I like things.\" "
    "Life layer: \"walk with me.\" The system was built organically during walking sessions "
    "in Iowa City, April 2026. Nothing was planned. Each piece grew from the last — "
    "from \"show me my steps\" to voice transcription to a detection system that Anthropic's "
    "channel architecture was missing. The walking workstation was tested on the same walks "
    "that built it.",
    insight_style
))

story.append(Spacer(1, 20))
story.append(HRFlowable(width="40%", thickness=0.5, color=HexColor('#cccccc')))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Built during walking sessions in Iowa City, April 29–30, 2026.<br/>"
    "42,396 steps. 20.98 miles. Body Battery 52 → 13.<br/>"
    "The system was tested on the same walks that built it.",
    ParagraphStyle('Footer', parent=body_style, alignment=TA_CENTER,
                   textColor=HexColor('#888888'), fontSize=9, fontName='Helvetica-Oblique')
))

doc.build(story)
print("PDF generated: garmin-claude-system.pdf")
