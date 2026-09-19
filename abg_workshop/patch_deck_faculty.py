with open("make_deck.py","r",encoding="utf-8") as f:
    src = f.read()

if "Slide 5: Faculty allocation" in src:
    print("Already patched")
else:
    faculty_slide = '''
# ── Slide 5: Faculty allocation ──
s = new_slide()
header(s, "Faculty allocation", "Group \u2192 Faculty facilitator", "")
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

'''
    src = src.replace("# ── Case slides ──",
                      faculty_slide + "# ── Case slides ──", 1)
    with open("make_deck.py","w",encoding="utf-8") as f:
        f.write(src)
    print("PATCH A OK - faculty allocation slide added")
