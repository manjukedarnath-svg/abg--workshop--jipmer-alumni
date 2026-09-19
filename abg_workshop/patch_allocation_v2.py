import re

# ══════════════════════════════════════════════════════════════════════
# 1 · PDF generator
# ══════════════════════════════════════════════════════════════════════
with open("abg_workshop_generator.py","r",encoding="utf-8") as f:
    src = f.read()

# Replace GROUP_FACULTY data block
new_data = '''GROUP_FACULTY = [
    ("1", "Manju",           3, "AGE (Gastroenteritis)"),
    ("2", "Shilpa",          6, "Hanging (Post-arrest)"),
    ("3", "Namitha",         9, "Encephalopathy (Two neonates)"),
    ("4", "Sivamurukan",     8, "Methaemoglobinaemia"),
    ("5", "Nikhil",          5, "Salicylate poisoning"),
    ("6", "Rohit",           7, "Septic shock + severe anaemia"),
    ("7", "Balachandar",     4, "Suspected IEM"),
    ("8", "Dipu / Sreedeep", 2, "Pyloric stenosis"),
]
'''
src = re.sub(r'GROUP_FACULTY\s*=\s*\[.*?\n\]\n', new_data, src, count=1, flags=re.DOTALL)

# Replace the table render block
old_render = re.compile(
    r's\.append\(Paragraph\("Faculty allocation by group",ST\["h1"\]\)\).*?s\.append\(fac_t\)',
    re.DOTALL
)
new_render = '''s.append(Paragraph("Faculty allocation by group",ST["h1"]))
    s.append(Paragraph("<b>Moderator:</b> Dr Narayanan and Dr Manju Kedarnath",ST["b"]))
    fac_rows = [[Paragraph("Group",ST["cl"]), Paragraph("Faculty facilitator",ST["cl"]),
                 Paragraph("Case",ST["cl"]), Paragraph("Diagnosis",ST["cl"])]]
    for g, n, cn, dx in GROUP_FACULTY:
        fac_rows.append([Paragraph(g, ST["cb"]),
                         Paragraph(n, ST["c"]),
                         Paragraph(str(cn), ST["cb"]),
                         Paragraph(dx, ST["c"])])
    fac_t = Table(fac_rows, colWidths=[18*mm, 48*mm, 18*mm, 86*mm], repeatRows=1)
    fac_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), TEAL),
        ("TEXTCOLOR",(0,0),(-1,0), colors.white),
        ("BACKGROUND",(0,1),(0,-1), GREY_L),
        ("BACKGROUND",(2,1),(2,-1), GREY_L),
        ("BOX",(0,0),(-1,-1),0.6, GREY_M),
        ("INNERGRID",(0,0),(-1,-1),0.4, GREY_M),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    s.append(fac_t)'''
src, n1 = old_render.subn(new_render, src, count=1)

with open("abg_workshop_generator.py","w",encoding="utf-8") as f:
    f.write(src)
print(f"PDF generator: {n1} render block replaced")

# ══════════════════════════════════════════════════════════════════════
# 2 · Teaching deck
# ══════════════════════════════════════════════════════════════════════
with open("make_deck_rich.py","r",encoding="utf-8") as f:
    src = f.read()

# Replace FACULTY_ALLOC list
new_alloc = '''FACULTY_ALLOC = [
    ("1","Manju",            "3", "AGE (Gastroenteritis)"),
    ("2","Shilpa",           "6", "Hanging (Post-arrest)"),
    ("3","Namitha",          "9", "Encephalopathy (Two neonates)"),
    ("4","Sivamurukan",      "8", "Methaemoglobinaemia"),
    ("5","Nikhil",           "5", "Salicylate poisoning"),
    ("6","Rohit",            "7", "Septic shock + severe anaemia"),
    ("7","Balachandar",      "4", "Suspected IEM"),
    ("8","Dipu / Sreedeep",  "2", "Pyloric stenosis"),
]
'''
src = re.sub(r'FACULTY_ALLOC\s*=\s*\[.*?\n\]\n', new_alloc, src, count=1, flags=re.DOTALL)

# Replace the render loop (from "y0 = Inches(2.2)" to end of loop)
old_loop = re.compile(
    r'y0 = Inches\(2\.2\).*?anchor=MSO_ANCHOR\.MIDDLE\)\n(?:.*?anchor=MSO_ANCHOR\.MIDDLE\)\n){0,4}',
    re.DOTALL
)
new_loop = '''y0 = Inches(2.2)
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
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)'''
src, n2 = old_loop.subn(new_loop, src, count=1)

# Update moderator line on the faculty allocation slide
src = src.replace(
    'header(s, "Faculty allocation", "Group \u2192 Faculty facilitator")',
    'header(s, "Faculty allocation", "Moderator: Dr Narayanan and Dr Manju Kedarnath")'
)
src = src.replace(
    'header(s, "Faculty allocation", "Group → Faculty facilitator")',
    'header(s, "Faculty allocation", "Moderator: Dr Narayanan and Dr Manju Kedarnath")'
)

with open("make_deck_rich.py","w",encoding="utf-8") as f:
    f.write(src)
print(f"Teaching deck: {n2} render block replaced")

# ══════════════════════════════════════════════════════════════════════
# 3 · Live app
# ══════════════════════════════════════════════════════════════════════
with open("index.html","r",encoding="utf-8") as f:
    src = f.read()

# Replace FACULTY_ALLOCATION data
new_js = '''var FACULTY_ALLOCATION = [
  {group:"1", name:"Manju",           caseNum:3, dx:"AGE (Gastroenteritis)"},
  {group:"2", name:"Shilpa",          caseNum:6, dx:"Hanging (Post-arrest)"},
  {group:"3", name:"Namitha",         caseNum:9, dx:"Encephalopathy (Two neonates)"},
  {group:"4", name:"Sivamurukan",     caseNum:8, dx:"Methaemoglobinaemia"},
  {group:"5", name:"Nikhil",          caseNum:5, dx:"Salicylate poisoning"},
  {group:"6", name:"Rohit",           caseNum:7, dx:"Septic shock + severe anaemia"},
  {group:"7", name:"Balachandar",     caseNum:4, dx:"Suspected IEM"},
  {group:"8", name:"Dipu / Sreedeep", caseNum:2, dx:"Pyloric stenosis"}
];'''
src = re.sub(r'var FACULTY_ALLOCATION = \[.*?\];', new_js, src, count=1, flags=re.DOTALL)

# Replace renderFacultyBlock
old_render = re.compile(r'function renderFacultyBlock\(\)\{.*?\n\}', re.DOTALL)
new_render = '''function renderFacultyBlock(){
  var host = document.getElementById("facultyAllocationBlock");
  if (!host) return;
  var html = '<div class="cheat-section" style="margin-bottom:24px">';
  html += '<h3>Faculty allocation by group</h3>';
  html += '<p style="color:var(--grey-t);font-size:12.5px;margin:0 0 10px"><b>Moderator:</b> Dr Narayanan and Dr Manju Kedarnath</p>';
  html += '<table><thead><tr>'
        + '<th style="width:12%">Group</th>'
        + '<th style="width:26%">Faculty</th>'
        + '<th style="width:14%">Case</th>'
        + '<th>Diagnosis</th></tr></thead><tbody>';
  FACULTY_ALLOCATION.forEach(function(f){
    html += '<tr><td>Group ' + f.group + '</td>'
          + '<td>' + f.name + '</td>'
          + '<td><b>Case ' + f.caseNum + '</b></td>'
          + '<td>' + f.dx + '</td></tr>';
  });
  html += '</tbody></table></div>';
  host.innerHTML = html;
}'''
src, n3 = old_render.subn(new_render, src, count=1)

with open("index.html","w",encoding="utf-8") as f:
    f.write(src)
print(f"Live app: {n3} render function replaced")

print()
print("All three files patched. Now run:")
print("  python abg_workshop_generator.py")
print("  python make_deck_rich.py")
