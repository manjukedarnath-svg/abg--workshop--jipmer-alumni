import os

def patch_file(path, replacements, label):
    if not os.path.exists(path):
        print(f"SKIP {label}: {path} not found")
        return
    with open(path,"r",encoding="utf-8") as f:
        content = f.read()
    applied = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)
            applied += 1
            print(f"  OK - {old[:55]}...")
        else:
            print(f"  MISS - {old[:55]}...")
    if applied:
        with open(path,"w",encoding="utf-8") as f:
            f.write(content)
    print(f"{label}: {applied}/{len(replacements)} applied\n")

# ── 1. PDF generator ──
patch_file("abg_workshop_generator.py", [
    ('"Participant Question Booklet - 13 Cases"',
     '"Participant Question Booklet - 13 cases, 8 drawn live"'),
    ('"Participant Discussion and Answer Booklet - 13 Cases"',
     '"Participant Discussion and Answer Booklet - 13 cases, 8 drawn live"'),
], "PDF generator")

# ── 2. Slide deck generator ──
patch_file("make_deck.py", [
    ('"13 cases · 15 min per case · ~3.25 hours total"',
     '"13 cases in the booklet  ·  8 drawn live at the start  ·  15 min per case"'),
], "PPTX generator")

# ── 3. Live app ──
patch_file("index.html", [
    ('Live participant app - 13 cases - interpret, intervene, re-evaluate',
     'Live participant app - 13 cases - 8 drawn live'),
    ('<strong>Faculty view.</strong> 3 min interpret',
     '<strong>Faculty view.</strong> 13 cases in the booklet &middot; 8 drawn live &middot; 3 min interpret'),
    ('Unlock codes, case walkthroughs, and quick reference - all in one place.',
     'Unlock codes, case walkthroughs, and quick reference - all in one place.<br><span style="font-size:12.5px">13 cases in the booklet. Draw 8 at the start of the session for the live run.</span>'),
], "Live app")
