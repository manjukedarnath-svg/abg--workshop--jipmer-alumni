# Rich teaching deck generator for ABG Workshop
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
GOLD_L = RGBColor(0xFB,0xF7,0xEC)
GREY_L = RGBColor(0xF4,0xF6,0xF8)
GREY_M = RGBColor(0xE1,0xE6,0xEB)
GREY_T = RGBColor(0x5A,0x66,0x72)
WHITE  = RGBColor(0xFF,0xFF,0xFF)

with open("cases.json") as f:
    CASES = json.load(f)

# Per-case teaching content: physiology principle + expert pearls
ENRICH = {
 1: {
  "physiology": "Insulin deficiency drives lipolysis and hepatic ketogenesis. β-hydroxybutyrate and acetoacetate accumulate as unmeasured anions — each one is buffered by bicarbonate, dropping serum HCO3. Kussmaul respiration blows off CO2 to compensate. When insulin restores, ketones clear — but chloride from saline resuscitation fills the anion gap, so the acid changes character from HAGMA to NAGMA.",
  "pearls": [
   "Corrected Na+ = Na + 1.6 × [(glucose − 100)/100]. True Na is often higher than measured.",
   "Total body K+ is depleted even when serum K+ looks normal — expect a rapid fall once insulin starts.",
   "A persistently low HCO3 after treatment usually reflects chloride load, not ongoing ketosis. Recalculate the AG before escalating insulin."
  ]
 },
 2: {
  "physiology": "Pyloric stenosis causes loss of gastric HCl — both H+ and Cl− leave the body. The kidney compensates by exchanging Na+ for H+ (generating new HCO3) and, under aldosterone drive from volume depletion, exchanges Na+ for K+. Net result: hypochloraemic, hypokalaemic metabolic alkalosis with paradoxical aciduria.",
  "pearls": [
   "Urine Cl < 15 mmol/L = chloride-responsive alkalosis. Best single discriminator from chloride-resistant causes (Bartter, Gitelman, mineralocorticoid excess).",
   "Correct volume and K+ BEFORE surgery — anaesthesia in an alkalotic, hypokalaemic infant is dangerous.",
   "Paradoxical aciduria despite systemic alkalosis is a classic pyloric stenosis sign."
  ]
 },
 3: {
  "physiology": "Stool is rich in bicarbonate. Loss depletes HCO3; the kidney reabsorbs Cl to preserve electroneutrality, producing a hyperchloraemic NAGMA. Lactate stays normal because perfusion is maintained — dehydration alone does not cause lactic acidosis until shock develops.",
  "pearls": [
   "NAGMA + normal lactate = GI or renal bicarbonate loss, not hypoperfusion.",
   "Correct AG for albumin before excluding a HAGMA — the raw number can lie.",
   "SID = Na − Cl falls below 36 in hyperchloraemic acidosis — a rapid bedside marker of chloride-driven mechanism."
  ]
 },
 4: {
  "physiology": "The raw AG looks normal because hypoalbuminaemia removes unmeasured anions. Correct the AG for albumin to unmask the HAGMA. The unmeasured anions here are likely organic acids from an inborn error of metabolism. Recurrent episodes triggered by catabolic stress (fever, fasting) are the classic pattern.",
  "pearls": [
   "Always correct AG for albumin: AG_corrected = AG + 2.5 × (4 − albumin).",
   "Recurrent unexplained acidosis + ketosis + hypoglycaemia = IEM until proven otherwise.",
   "Draw the critical sample (ammonia on ice, urine organic acids, plasma amino acids, acylcarnitine) during the acute episode, not after."
  ]
 },
 5: {
  "physiology": "Salicylate has two opposing effects. (1) Direct stimulation of the medullary respiratory centre → respiratory alkalosis. (2) Uncoupling of oxidative phosphorylation → lactic acid and ketone production → HAGMA. Net pH is often near normal because two big derangements cancel out — never trust a 'normal' pH with abnormal component values.",
  "pearls": [
   "A near-normal pH with low PaCO2 and low HCO3 is a mixed disorder until proven otherwise.",
   "Tinnitus is the most specific early clinical clue in salicylate toxicity.",
   "Treatment is urinary alkalinisation with sodium bicarbonate; haemodialysis for severe poisoning."
  ]
 },
 6: {
  "physiology": "Hanging causes both hypoxic-ischaemic injury (lactic acidosis, HAGMA) and central respiratory depression or inadequate ventilation. Both PaCO2 and HCO3 push pH down — no compensation possible. Add ARDS from aspiration/ischaemia and you have a triple threat: metabolic acidosis, respiratory acidosis, and severe oxygenation failure.",
  "pearls": [
   "Never call a high PaCO2 'compensation' when pH is acidotic and both values are deranged — name both primary disorders.",
   "OI ≥ 16 = severe paediatric ARDS (PALICC criteria).",
   "K+ 6.2 needs urgent treatment alongside the acid-base picture — calcium gluconate first if there are ECG changes."
  ]
 },
 7: {
  "physiology": "Oxygen delivery (DO2) = cardiac output × CaO2. CaO2 ≈ 1.34 × Hb × SaO2. With Hb 4.5 g/dL, CaO2 is ~6 mL/dL vs normal 16–20. The body compensates by increasing extraction (ScvO2 falls) — but once extraction is maximal, tissues switch to anaerobic metabolism → lactate rises. A normal SpO2 is completely misleading.",
  "pearls": [
   "SpO2 says nothing about oxygen delivery. ScvO2 < 65% = increased extraction = inadequate DO2.",
   "The single most effective intervention in severe anaemia is transfusion — not more FiO2.",
   "Lactate clearance and ScvO2 are better endpoints than repeat arterial gases."
  ]
 },
 8: {
  "physiology": "Methaemoglobin has Fe3+ rather than Fe2+, so it cannot bind O2. It also shifts the O2 dissociation curve left, impairing tissue unloading. Pulse oximetry cannot distinguish MetHb from oxyhaemoglobin — it reads falsely high and pins around 82–85%. Co-oximetry directly measures true SaO2.",
  "pearls": [
   "Cyanosis + chocolate-brown blood + high PaO2 + falsely reassuring SpO2 = methaemoglobinaemia.",
   "Methylene blue 1–2 mg/kg is the antidote — check G6PD status first (can cause haemolysis).",
   "MetHb > 30% requires urgent treatment regardless of symptoms."
  ]
 },
 9: {
  "physiology": "Baby A: respiratory alkalosis with no fever or distress points away from sepsis and toward central respiratory stimulation — the classic driver is hyperammonaemia (urea cycle defect). Baby B: profound HAGMA with ketones and hypoglycaemia is the classic pattern of an organic acidaemia (methylmalonic, propionic) or a fatty acid oxidation defect.",
  "pearls": [
   "Ammonia sample: on ice, delivered within 15 minutes. Delayed samples falsely elevate.",
   "Stop protein, give dextrose, treat the acute crisis while awaiting confirmation.",
   "Lactate alone does not explain the gap — ketones and organic acids fill the rest."
  ]
 },
 10: {
  "physiology": "HUS is a triple-hit acidosis. (1) Renal failure → phosphate retention raises Atot → acidifying. (2) Volume resuscitation with saline → low SID → chloride-driven acidosis. (3) Retained urate, oxalate, and other anions → unmeasured anions → HAGMA. The three forces stack, which is why the child looks worse than the numbers suggest.",
  "pearls": [
   "Hyperkalaemia and hypocalcaemia are immediately life-threatening — treat before dialysis.",
   "Avoid bicarbonate unless pH < 7.1 — it can worsen hypocalcaemia and hyperkalaemia.",
   "SID, Atot, and unmeasured anions each tell a different part of the story."
  ]
 },
 11: {
  "physiology": "Ammonia from liver failure stimulates the respiratory centre → respiratory alkalosis. Meanwhile, hypoalbuminaemia (low Atot) masks a HAGMA from lactic acidosis and impaired lactate clearance. The SBE looks normal because the alkalinising and acidifying forces cancel. Correct the AG for albumin and the HAGMA appears.",
  "pearls": [
   "A normal SBE in a sick patient is often a lie — check the albumin-corrected AG.",
   "Hypoglycaemia in liver failure is silent and dangerous — check glucose hourly.",
   "Lactate in liver failure reflects both perfusion and hepatic clearance failure."
  ]
 },
 12: {
  "physiology": "A normal fasting child mounts ketosis — β-OHB rises to supply the brain with alternative fuel. When fatty acid oxidation or ketogenesis is impaired, β-OHB stays low despite high free fatty acids. This is the classic pattern of MCAD deficiency and other fatty acid oxidation defects. Hyperinsulinism would show low FFA and low ketones.",
  "pearls": [
   "Draw the critical sample BEFORE giving dextrose — the diagnostic window closes once glucose is corrected.",
   "Critical sample: glucose, insulin, C-peptide, cortisol, growth hormone, ketones, free fatty acids, acylcarnitine, ammonia, lactate, LFTs.",
   "A fasting child with hypoglycaemia and no ketosis needs metabolic work-up even if the gas looks normal."
  ]
 },
 13: {
  "physiology": "21-hydroxylase deficiency blocks cortisol and aldosterone synthesis. Aldosterone deficiency → renal sodium wasting, potassium retention, and acidosis. Cortisol deficiency → impaired glucose counter-regulation → hypoglycaemia. The triad of hyponatraemia + hyperkalaemia + hypoglycaemia in a shocked neonate is CAH until proven otherwise.",
  "pearls": [
   "Draw the critical sample (17-OHP, cortisol, ACTH, renin, aldosterone, electrolytes, glucose) BEFORE giving hydrocortisone.",
   "Normal-looking genitalia do not exclude CAH in a boy — 46,XY infants have no ambiguous genitalia.",
   "Treat hyperkalaemia and give stress-dose hydrocortisone immediately."
  ]
 }
}

# ══════════════════════════════════════════════════════════════════════
# DECK SETUP
# ══════════════════════════════════════════════════════════════════════
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# ══════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════
def new_slide():
    return prs.slides.add_slide(BLANK)

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

def gas_grid(slide, gas, x, y, w, h, cols=5):
    keys = list(gas.keys())
    rows = (len(keys) + cols - 1) // cols
    gap = Inches(0.1)
    cell_w = (w - gap*(cols-1)) / cols
    cell_h = (h - gap*(rows-1)) / rows if rows > 1 else h
    for i, k in enumerate(keys):
        r, c = divmod(i, cols)
        cx = x + c*(cell_w + gap)
        cy = y + r*(cell_h + gap)
        add_rect(slide, cx, cy, cell_w, cell_h, GREY_L, GREY_M, rounded=True)
        add_text(slide, cx, cy + Inches(0.06), cell_w, Inches(0.28),
                 k, size=9, color=GREY_T, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
        add_text(slide, cx, cy + Inches(0.3), cell_w, cell_h - Inches(0.36),
                 str(gas[k]), size=18, color=NAVY, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def header(slide, kicker, title, subtitle=None):
    y = Inches(0.35)
    add_text(slide, Inches(0.6), y, Inches(12), Inches(0.3),
             kicker.upper(), size=9, color=GREY_T, bold=True)
    add_text(slide, Inches(0.6), y + Inches(0.25), Inches(12), Inches(0.7),
             title, size=24, color=NAVY, bold=True)
    if subtitle:
        add_text(slide, Inches(0.6), y + Inches(0.95), Inches(12), Inches(0.4),
                 subtitle, size=11, color=GREY_T)
    add_rect(slide, Inches(0.6), y + Inches(1.42), Inches(12.1),
             Inches(0.04), TEAL)

def add_ribbon(slide, x, y, w, h, text, fill):
    add_rect(slide, x, y, w, h, fill)
    add_text(slide, x + Inches(0.2), y, w, h,
             text.upper(), size=10, color=WHITE, bold=True,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

def body_block(slide, x, y, w, h, label, body, accent=TEAL):
    add_rect(slide, x, y, w, h, GREY_L, GREY_M, rounded=True)
    add_rect(slide, x, y, Inches(0.08), h, accent)
    add_text(slide, x + Inches(0.25), y + Inches(0.12), w - Inches(0.5), Inches(0.3),
             label.upper(), size=10, color=accent, bold=True)
    add_text(slide, x + Inches(0.25), y + Inches(0.45), w - Inches(0.5),
             h - Inches(0.6), body, size=11.5, color=NAVY, spacing=1.35)

# ══════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════════
s = new_slide()
add_rect(s, 0, 0, prs.slide_width, prs.slide_height, NAVY)
add_text(s, Inches(1), Inches(2.2), Inches(11.3), Inches(0.4),
         "PAEDIATRIC ACUTE CARE TEACHING", size=12, color=TEAL, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(2.7), Inches(11.3), Inches(1.2),
         "ABG Interpretation Workshop", size=44, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(4.1), Inches(11.3), Inches(0.5),
         "Moderator Teaching Deck — 13 Cases", size=18, color=GREY_L,
         align=PP_ALIGN.CENTER)
add_rect(s, Inches(5.5), Inches(4.9), Inches(2.33), Inches(0.05), TEAL)
add_text(s, Inches(1), Inches(5.2), Inches(11.3), Inches(0.4),
         "13 cases in the booklet  ·  8 drawn live at the start  ·  15 min per case",
         size=13, color=GREY_L, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════
# SLIDE 2 — HOW TODAY RUNS
# ══════════════════════════════════════════════════════════════════════
s = new_slide()
header(s, "How today runs", "Three steps, one rhythm")
steps = [
    ("STEP 1", "All 13 cases handed out",
     "The booklet contains 13 cases. At the start the moderator draws 8 for the live run; the other 5 become self-study."),
    ("STEP 2", "8-minute settling period",
     "Participants may read ahead. Faculty do not teach yet — the facilitated cycle has not started."),
    ("STEP 3", "Each drawn case = 15 minutes",
     "8 minutes at the small-group table (3-3-2), then 7 minutes in plenary with the whole room."),
]
y = Inches(2.2)
for kicker, title, body in steps:
    add_rect(s, Inches(0.6), y, Inches(0.1), Inches(1.3), TEAL)
    add_text(s, Inches(0.9), y, Inches(3), Inches(0.3),
             kicker, size=11, color=TEAL, bold=True)
    add_text(s, Inches(0.9), y + Inches(0.3), Inches(11.5), Inches(0.4),
             title, size=17, color=NAVY, bold=True)
    add_text(s, Inches(0.9), y + Inches(0.72), Inches(11.5), Inches(0.6),
             body, size=11.5, color=GREY_T, spacing=1.3)
    y += Inches(1.55)

# ══════════════════════════════════════════════════════════════════════
# SLIDE 3 — TWO PHASES
# ══════════════════════════════════════════════════════════════════════
s = new_slide()
header(s, "For every case, every group", "One case, 15 minutes, two phases")
add_text(s, Inches(0.6), Inches(2.15), Inches(6), Inches(0.35),
         "SMALL GROUP · 8 MIN · YOUR OWN TABLE", size=10.5, color=TEAL_D, bold=True)
sg = [("3","Interpret","Team works alone, in silence"),
      ("3","Discuss","Faculty-mediated, at your table"),
      ("2","Synthesise","Faculty closes for your table")]
x = Inches(0.6); w = Inches(4.0); gap = Inches(0.15)
for num, title, body in sg:
    add_rect(s, x, Inches(2.6), w, Inches(1.4), TEAL, rounded=True)
    add_text(s, x + Inches(0.2), Inches(2.7), w, Inches(0.5),
             num, size=30, color=WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(3.25), w, Inches(0.4),
             title, size=14, color=WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(3.65), w - Inches(0.4), Inches(0.6),
             body, size=10, color=GREY_L, spacing=1.2)
    x += w + gap
add_text(s, Inches(0.6), Inches(4.25), Inches(6), Inches(0.35),
         "PLENARY · 7 MIN · WHOLE ROOM, LED BY MODERATOR", size=10.5, color=GOLD, bold=True)
pl = [("3","Random draw","One group presents to all"),
      ("3","Expert comment","Case questions, answered live"),
      ("2","Take-home","One pearl, whole room")]
x = Inches(0.6)
for num, title, body in pl:
    add_rect(s, x, Inches(4.7), w, Inches(1.4), GOLD, rounded=True)
    add_text(s, x + Inches(0.2), Inches(4.8), w, Inches(0.5),
             num, size=30, color=WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(5.35), w, Inches(0.4),
             title, size=14, color=WHITE, bold=True)
    add_text(s, x + Inches(0.2), Inches(5.75), w - Inches(0.4), Inches(0.6),
             body, size=10, color=GOLD_L, spacing=1.2)
    x += w + gap

# ══════════════════════════════════════════════════════════════════════
# SLIDE 4 — TWO FACILITATORS
# ══════════════════════════════════════════════════════════════════════
s = new_slide()
header(s, "Two phases, two facilitators", "Who does what")
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
    add_rect(s, x, Inches(2.15), Inches(6.0), Inches(4.5), GREY_L,
             GREY_M, rounded=True)
    add_rect(s, x, Inches(2.15), Inches(0.15), Inches(4.5), colour)
    add_text(s, x + Inches(0.35), Inches(2.35), Inches(5.5), Inches(0.4),
             title, size=10.5, color=colour, bold=True)
    y = Inches(2.95)
    for t, b in items:
        add_text(s, x + Inches(0.35), y, Inches(5.5), Inches(0.35),
                 t, size=13.5, color=NAVY, bold=True)
        add_text(s, x + Inches(0.35), y + Inches(0.38), Inches(5.5), Inches(0.8),
                 b, size=11, color=GREY_T, spacing=1.35)
        y += Inches(1.15)

# ══════════════════════════════════════════════════════════════════════
# SLIDE 5 — FACULTY ALLOCATION
# ══════════════════════════════════════════════════════════════════════
s = new_slide()
header(s, "Faculty allocation", "Moderator: Dr Narayanan and Dr Manju Kedarnath")
FACULTY_ALLOC = [
    ("1","Manju",            "3", "AGE (Gastroenteritis)"),
    ("2","Shilpa",           "6", "Hanging (Post-arrest)"),
    ("3","Namitha",          "9", "Encephalopathy (Two neonates)"),
    ("4","Sivamurukan",      "8", "Methaemoglobinaemia"),
    ("5","Nikhil",           "5", "Salicylate poisoning"),
    ("6","Rohit",            "7", "Septic shock + severe anaemia"),
    ("7","Balachandar",      "4", "Suspected IEM"),
    ("8","Dipu / Sreedeep",  "2", "Pyloric stenosis"),
]
y0 = Inches(2.2)
row_h = Inches(0.55)
for i, (g, n, cn, dx) in enumerate(FACULTY_ALLOC):
    y = y0 + i * row_h
    add_rect(s, Inches(0.6), y, Inches(0.85), row_h - Inches(0.06), TEAL)
    add_text(s, Inches(0.6), y, Inches(0.85), row_h - Inches(0.06),
             "G" + g, size=12, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, Inches(1.5), y, Inches(3.1), row_h - Inches(0.06), GREY_L, GREY_M)
    add_text(s, Inches(1.65), y, Inches(2.9), row_h - Inches(0.06),
             n, size=12, color=NAVY,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, Inches(4.65), y, Inches(1.0), row_h - Inches(0.06), GREY_L, GREY_M)
    add_text(s, Inches(4.65), y, Inches(1.0), row_h - Inches(0.06),
             "Case " + cn, size=11, color=TEAL_D, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, Inches(5.7), y, Inches(7.0), row_h - Inches(0.06), GREY_L, GREY_M)
    add_text(s, Inches(5.85), y, Inches(6.8), row_h - Inches(0.06),
             dx, size=11.5, color=NAVY,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
# ══════════════════════════════════════════════════════════════════════
# PER-CASE SLIDES
# ══════════════════════════════════════════════════════════════════════
for c in CASES:
    cid = c["id"]
    enrich = ENRICH.get(cid, {"physiology":"","pearls":[]})

    # ── Slide A: Case + vignette + presenting gas ──
    s = new_slide()
    add_text(s, Inches(0.6), Inches(0.4), Inches(12), Inches(0.3),
             f"CASE {cid} OF 13", size=9, color=TEAL, bold=True)
    add_text(s, Inches(0.6), Inches(0.75), Inches(12), Inches(0.8),
             c["title"], size=26, color=NAVY, bold=True)
    body_block(s, Inches(0.6), Inches(1.7), Inches(12.1), Inches(1.4),
               "Vignette", c["vignette"], accent=TEAL)
    add_ribbon(s, Inches(0.6), Inches(3.3), Inches(12.1), Inches(0.4),
               "Initial gas · presenting", TEAL)
    gas_grid(s, c["gas_in"], Inches(0.6), Inches(3.85),
             Inches(12.1), Inches(1.8), cols=5)
    if c.get("gas_post"):
        add_ribbon(s, Inches(0.6), Inches(5.85), Inches(12.1), Inches(0.4),
                   "Post-intervention · " + c.get("intervention","")[:70], GOLD)
        gas_grid(s, c["gas_post"], Inches(0.6), Inches(6.4),
                 Inches(12.1), Inches(0.85), cols=5)

    # ── Slide B: Interpretation + SID ──
    s = new_slide()
    header(s, f"Case {cid} · {c['title']}", "Interpretation & SID / Stewart analysis")
    # Left column: interpretation
    add_text(s, Inches(0.6), Inches(2.1), Inches(6), Inches(0.3),
             "SYSTEMATIC INTERPRETATION", size=10, color=TEAL_D, bold=True)
    y = Inches(2.45)
    # take key steps (skip some to keep tidy)
    key_steps = c["steps_in"][:6]
    for label, body in key_steps:
        add_text(s, Inches(0.6), y, Inches(6.0), Inches(0.28),
                 label, size=10, color=TEAL_D, bold=True)
        add_text(s, Inches(0.6), y + Inches(0.26), Inches(6.0), Inches(0.55),
                 body, size=9.5, color=NAVY, spacing=1.25)
        y += Inches(0.72)
    # Right column: SID table
    add_text(s, Inches(7.0), Inches(2.1), Inches(6), Inches(0.3),
             "SID / STEWART ANALYSIS", size=10, color=TEAL_D, bold=True)
    y = Inches(2.5)
    for row in c["sid_in"]:
        add_rect(s, Inches(7.0), y, Inches(5.7), Inches(0.85), GREY_L,
                 GREY_M, rounded=True)
        add_text(s, Inches(7.15), y + Inches(0.08), Inches(5.4), Inches(0.25),
                 row[0].upper(), size=9, color=TEAL_D, bold=True)
        add_text(s, Inches(7.15), y + Inches(0.3), Inches(1.8), Inches(0.5),
                 row[1], size=10.5, color=NAVY, bold=True)
        add_text(s, Inches(9.0), y + Inches(0.3), Inches(3.6), Inches(0.5),
                 row[2], size=9.5, color=GREY_T, spacing=1.2)
        y += Inches(0.95)

    # ── Slide C: Physiology + pearls ──
    s = new_slide()
    header(s, f"Case {cid} · {c['title']}", "Physiology principle · expert pearls")
    body_block(s, Inches(0.6), Inches(2.1), Inches(12.1), Inches(2.1),
               "Basic physiology", enrich["physiology"], accent=TEAL)
    # Pearls
    add_text(s, Inches(0.6), Inches(4.4), Inches(12), Inches(0.3),
             "EXPERT PEARLS", size=10, color=GOLD, bold=True)
    y = Inches(4.75)
    for pearl in enrich["pearls"]:
        add_rect(s, Inches(0.6), y, Inches(0.08), Inches(0.7), GOLD)
        add_text(s, Inches(0.85), y + Inches(0.05), Inches(11.7), Inches(0.65),
                 pearl, size=11, color=NAVY, spacing=1.3)
        y += Inches(0.82)

    # ── Slide D: Case Q&A + take-home ──
    s = new_slide()
    header(s, f"Case {cid} · {c['title']}", "Case-specific Q&A · take-home")
    # Left: Q&A
    add_text(s, Inches(0.6), Inches(2.1), Inches(7), Inches(0.3),
             "CASE-SPECIFIC Q&A", size=10, color=TEAL_D, bold=True)
    y = Inches(2.45)
    for i, (q, a) in enumerate(zip(c["qs"][:3], c["ans"][:3])):
        add_text(s, Inches(0.6), y, Inches(7.1), Inches(0.25),
                 f"Q{i+1}. {q}", size=10, color=NAVY, bold=True)
        add_text(s, Inches(0.6), y + Inches(0.24), Inches(7.1), Inches(0.9),
                 a, size=9.5, color=GREY_T, spacing=1.25)
        y += Inches(1.25)
    # Right: take-home
    add_rect(s, Inches(8.0), Inches(2.1), Inches(4.7), Inches(4.6),
             GOLD_L, GOLD, rounded=True)
    add_text(s, Inches(8.2), Inches(2.3), Inches(4.3), Inches(0.3),
             "TAKE-HOME MESSAGE", size=10, color=GOLD, bold=True)
    add_text(s, Inches(8.2), Inches(2.65), Inches(4.3), Inches(4.0),
             c["take"], size=12, color=NAVY, spacing=1.35)

# ══════════════════════════════════════════════════════════════════════
# CLOSING SLIDE
# ══════════════════════════════════════════════════════════════════════
s = new_slide()
add_rect(s, 0, 0, prs.slide_width, prs.slide_height, NAVY)
add_text(s, Inches(1), Inches(1.8), Inches(11.3), Inches(0.4),
         "CLOSE WITH THE ROOM", size=12, color=TEAL, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(2.4), Inches(11.3), Inches(1.0),
         "Two questions before the post-test", size=30, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
add_rect(s, Inches(5.5), Inches(3.7), Inches(2.33), Inches(0.05), TEAL)
add_text(s, Inches(1.5), Inches(4.2), Inches(10.3), Inches(0.6),
         "1. Which case changed your mind about a value you thought you understood?",
         size=16, color=GREY_L, align=PP_ALIGN.CENTER, spacing=1.3)
add_text(s, Inches(1.5), Inches(5.2), Inches(10.3), Inches(0.6),
         "2. Which correction step will you now do as a reflex, every single time?",
         size=16, color=GREY_L, align=PP_ALIGN.CENTER, spacing=1.3)

# ══════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════
prs.save("ABG_Workshop_Teaching_Deck.pptx")
print(f"OK - ABG_Workshop_Teaching_Deck.pptx ({len(prs.slides)} slides)")
