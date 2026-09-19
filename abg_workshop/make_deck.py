import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

TEAL   = RGBColor(0x0F,0x6E,0x6E)
TEAL_D = RGBColor(0x0A,0x4E,0x4E)
NAVY   = RGBColor(0x1B,0x2A,0x3A)
GOLD   = RGBColor(0xB8,0x89,0x2B)
GREY_L = RGBColor(0xF4,0xF6,0xF8)
GREY_M = RGBColor(0xE1,0xE6,0xEB)
GREY_T = RGBColor(0x5A,0x66,0x72)
WHITE  = RGBColor(0xFF,0xFF,0xFF)

with open("cases.json") as f:
    CASES = json.load(f)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def add_rect(slide, x, y, w, h, fill, line=None, rounded=False):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.75)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    if rounded:
        # Adjust corner radius
        try: shp.adjustments[0] = 0.08
        except: pass
    return shp

def add_text(slide, x, y, w, h, text, size=14, color=NAVY, bold=False,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False,
             spacing=None):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing: p.line_spacing = spacing
        r = p.add_run()
        r.text = line
        r.font.name = "Helvetica"
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return tb

def new_slide():
    return prs.slides.add_slide(BLANK)

def gas_grid(slide, gas, x, y, w, h, cols=5):
    """Gas cards in a grid of cols-wide."""
    keys = list(gas.keys())
    rows = (len(keys) + cols - 1) // cols
    gap = Inches(0.12)
    cell_w = (w - gap*(cols-1)) / cols
    cell_h = (h - gap*(rows-1)) / rows if rows > 1 else h
    for i, k in enumerate(keys):
        r, c = divmod(i, cols)
        cx = x + c*(cell_w + gap)
        cy = y + r*(cell_h + gap)
        # Card background
        add_rect(slide, cx, cy, cell_w, cell_h, GREY_L, GREY_M, rounded=True)
        # Label (top)
        add_text(slide, cx, cy + Inches(0.08), cell_w, Inches(0.3),
                 k, size=9, color=GREY_T, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
        # Value (big)
        add_text(slide, cx, cy + Inches(0.32), cell_w, cell_h - Inches(0.4),
                 str(gas[k]), size=20, color=NAVY, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def add_ribbon(slide, x, y, w, h, text, fill):
    add_rect(slide, x, y, w, h, fill)
    add_text(slide, x + Inches(0.2), y, w, h,
             text.upper(), size=11, color=WHITE, bold=True,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

def header(slide, kicker, title, subtitle=None, rule=True):
    y = Inches(0.4)
    add_text(slide, Inches(0.6), y, Inches(12), Inches(0.3),
             kicker.upper(), size=9, color=GREY_T, bold=True)
    add_text(slide, Inches(0.6), y + Inches(0.28), Inches(12), Inches(0.7),
             title, size=26, color=NAVY, bold=True)
    if subtitle:
        add_text(slide, Inches(0.6), y + Inches(1.0), Inches(12), Inches(0.5),
                 subtitle, size=12, color=GREY_T)
    if rule:
        add_rect(slide, Inches(0.6), y + Inches(1.55), Inches(12.1),
                 Inches(0.04), TEAL)

# ── Slide 1: Title ──
s = new_slide()
add_rect(s, 0, 0, prs.slide_width, prs.slide_height, NAVY)
add_text(s, Inches(1), Inches(2.4), Inches(11.3), Inches(0.4),
         "PAEDIATRIC ACUTE CARE TEACHING", size=12, color=TEAL, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(2.9), Inches(11.3), Inches(1.2),
         "ABG Interpretation Workshop", size=44, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(4.3), Inches(11.3), Inches(0.5),
         "Moderator Slide Deck — 13 Cases", size=18, color=GREY_L,
         align=PP_ALIGN.CENTER)
add_rect(s, Inches(5.5), Inches(5.1), Inches(2.33), Inches(0.05), TEAL)
add_text(s, Inches(1), Inches(5.4), Inches(11.3), Inches(0.4),
         "13 cases in the booklet  ·  8 drawn live at the start  ·  15 min per case",
         size=13, color=GREY_L, align=PP_ALIGN.CENTER)

# ── Slide 2: How today runs ──
s = new_slide()
header(s, "How today runs", "Three steps, one rhythm", "")
steps = [
    ("STEP 1", "All 13 cases handed out",
     "Every participant receives the full case booklet at once — not one case per group."),
    ("STEP 2", "8-minute settling period",
     "Participants may read ahead. Faculty do not teach yet — the facilitated cycle has not started."),
    ("STEP 3", "13 cases × 15 minutes each",
     "Each case runs as one 15-minute unit: 8 minutes at the small-group table, then 7 minutes in plenary with the whole room."),
]
y = Inches(2.3)
for kicker, title, body in steps:
    add_rect(s, Inches(0.6), y, Inches(0.1), Inches(1.3), TEAL)
    add_text(s, Inches(0.9), y, Inches(3), Inches(0.3),
             kicker, size=11, color=TEAL, bold=True)
    add_text(s, Inches(0.9), y + Inches(0.3), Inches(11.5), Inches(0.4),
             title, size=18, color=NAVY, bold=True)
    add_text(s, Inches(0.9), y + Inches(0.75), Inches(11.5), Inches(0.6),
             body, size=12, color=GREY_T, spacing=1.3)
    y += Inches(1.6)

# ── Slide 3: Two phases ──
s = new_slide()
header(s, "For every case, every group", "One case, 15 minutes, two phases", "")
# Small group block
add_text(s, Inches(0.6), Inches(2.3), Inches(6), Inches(0.4),
         "SMALL GROUP · 8 MIN · YOUR OWN TABLE", size=11, color=TEAL_D, bold=True)
sg = [("3","Interpret","Team works alone, in silence"),
      ("3","Discuss","Faculty-mediated, at your table"),
      ("2","Synthesise","Faculty closes for your table")]
x = Inches(0.6); w = Inches(4.0); gap = Inches(0.15)
for num, title, body in sg:
    add_rect(s, x, Inches(2.8), w, Inches(1.5), TEAL, rounded=True)
    add_text(s, x + Inches(0.2), Inches(2.9), w, Inches(0.5),
             num, size=32, color=WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(3.5), w, Inches(0.4),
             title, size=14, color=WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(3.9), w - Inches(0.4), Inches(0.6),
             body, size=10, color=GREY_L, spacing=1.2)
    x += w + gap
# Plenary block
add_text(s, Inches(0.6), Inches(4.6), Inches(6), Inches(0.4),
         "PLENARY · 7 MIN · WHOLE ROOM, LED BY MODERATOR", size=11, color=GOLD, bold=True)
pl = [("3","Random draw","One group presents to all"),
      ("3","Expert comment","Case questions, answered live"),
      ("2","Take-home","One pearl, whole room")]
x = Inches(0.6)
for num, title, body in pl:
    add_rect(s, x, Inches(5.1), w, Inches(1.5), GOLD, rounded=True)
    add_text(s, x + Inches(0.2), Inches(5.2), w, Inches(0.5),
             num, size=32, color=WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(5.8), w, Inches(0.4),
             title, size=14, color=WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(6.2), w - Inches(0.4), Inches(0.6),
             body, size=10, color=RGBColor(0xFB,0xF7,0xEC), spacing=1.2)
    x += w + gap

# ── Slide 4: Two facilitators ──
s = new_slide()
header(s, "Two phases, two facilitators", "Who does what", "")
left_items = [
    ("During interpret", "Say nothing. Circulate silently and note where the group is stuck."),
    ("During discuss", 'Ask before telling — "what did you get, and why" comes first.'),
    ("During synthesis", "One tight paragraph: the diagnosis and the one teaching point for your table."),
]
right_items = [
    ("Random draw", "Pick one group, at random, to present to the whole room."),
    ("Expert comment", "Walk the case-specific questions with the authoritative answer."),
    ("Take-home", "Close with one pearl for everyone before the next case."),
]
for col, (title, items, colour) in enumerate([
        ("GROUP FACULTY · SMALL-GROUP PHASE", left_items, TEAL),
        ("MODERATOR · PLENARY PHASE", right_items, GOLD)]):
    x = Inches(0.6) + col * Inches(6.4)
    add_rect(s, x, Inches(2.3), Inches(6.0), Inches(4.6), GREY_L,
             GREY_M, rounded=True)
    add_rect(s, x, Inches(2.3), Inches(0.15), Inches(4.6), colour)
    add_text(s, x + Inches(0.35), Inches(2.5), Inches(5.5), Inches(0.4),
             title, size=11, color=colour, bold=True)
    y = Inches(3.1)
    for t, b in items:
        add_text(s, x + Inches(0.35), y, Inches(5.5), Inches(0.35),
                 t, size=14, color=NAVY, bold=True)
        add_text(s, x + Inches(0.35), y + Inches(0.4), Inches(5.5), Inches(0.8),
                 b, size=11, color=GREY_T, spacing=1.35)
        y += Inches(1.2)


# ── Slide 5: Faculty allocation ──
s = new_slide()
header(s, "Faculty allocation", "Group → Faculty facilitator", "")
FACULTY_ALLOC = [
    ("1","Manju Kedarnath"),("2","Shilpa"),("3","Namitha"),("4","Sivamurukan"),
    ("5","Nikhil"),("6","Rohit"),("7","Balachandar"),("8","Dipu / Sreedeep"),
]
y0 = Inches(2.4)
row_h = Inches(0.62)
col_w = Inches(5.9)
gap = Inches(0.2)
for i, (g, n) in enumerate(FACULTY_ALLOC):
    col = i // 4
    row = i % 4
    x = Inches(0.6) + col * (col_w + gap)
    y = y0 + row * row_h
    add_rect(s, x, y, Inches(1.3), row_h - Inches(0.08), TEAL)
    add_text(s, x, y, Inches(1.3), row_h - Inches(0.08),
             "GROUP " + g, size=12, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, x + Inches(1.3), y, col_w - Inches(1.3), row_h - Inches(0.08),
             GREY_L, GREY_M)
    add_text(s, x + Inches(1.5), y, col_w - Inches(1.6), row_h - Inches(0.08),
             n, size=14, color=NAVY,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

# ── Case slides ──
for c in CASES:
    s = new_slide()
    # Vignette
    add_text(s, Inches(0.6), Inches(0.5), Inches(12), Inches(0.3),
             f"CASE {c['id']}", size=10, color=TEAL, bold=True)
    add_text(s, Inches(0.6), Inches(0.85), Inches(12), Inches(0.9),
             c["title"], size=22, color=NAVY, bold=True)
    add_text(s, Inches(0.6), Inches(1.75), Inches(12.1), Inches(1.0),
             c["vignette"], size=12, color=GREY_T, spacing=1.3)

    if c.get("gas_post"):
        # Case has repeat gas
        add_ribbon(s, Inches(0.6), Inches(2.8), Inches(12.1), Inches(0.4),
                   "Small group · 8 min · Presenting gas", TEAL)
        gas_grid(s, c["gas_in"], Inches(0.6), Inches(3.35),
                 Inches(12.1), Inches(1.55), cols=5)
        add_ribbon(s, Inches(0.6), Inches(5.1), Inches(12.1), Inches(0.4),
                   "Plenary reveal · 7 min · Repeat gas", NAVY)
        gas_grid(s, c["gas_post"], Inches(0.6), Inches(5.65),
                 Inches(12.1), Inches(1.55), cols=5)
    else:
        # Single gas
        add_text(s, Inches(0.6), Inches(2.8), Inches(4), Inches(0.3),
                 "BLOOD GAS", size=10, color=GREY_T, bold=True)
        gas_grid(s, c["gas_in"], Inches(0.6), Inches(3.2),
                 Inches(12.1), Inches(3.9), cols=5)

# ── Closing slide ──
s = new_slide()
add_rect(s, 0, 0, prs.slide_width, prs.slide_height, NAVY)
add_text(s, Inches(1), Inches(1.8), Inches(11.3), Inches(0.4),
         "CLOSE WITH THE ROOM", size=12, color=TEAL, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(2.4), Inches(11.3), Inches(1.0),
         "Two questions before the post-test", size=32, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
add_rect(s, Inches(5.5), Inches(3.7), Inches(2.33), Inches(0.05), TEAL)
add_text(s, Inches(1.5), Inches(4.2), Inches(10.3), Inches(0.6),
         "1. Which case changed your mind about a value you thought you understood?",
         size=16, color=GREY_L, align=PP_ALIGN.CENTER, spacing=1.3)
add_text(s, Inches(1.5), Inches(5.2), Inches(10.3), Inches(0.6),
         "2. Which correction step will you now do as a reflex, every single time?",
         size=16, color=GREY_L, align=PP_ALIGN.CENTER, spacing=1.3)

prs.save("ABG_Workshop_Slide_Deck.pptx")
print(f"OK - ABG_Workshop_Slide_Deck.pptx ({len(prs.slides)} slides)")
