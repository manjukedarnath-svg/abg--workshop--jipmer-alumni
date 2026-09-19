with open("abg_workshop_generator.py","r",encoding="utf-8") as f:
    src = f.read()

# 1. Faculty mapping — insert near the top (after CASES definition ends)
mapping = '''
# Group -> Faculty facilitator allocation
GROUP_FACULTY = [
    ("1","Manju Kedarnath"),
    ("2","Shilpa"),
    ("3","Namitha"),
    ("4","Sivamurukan"),
    ("5","Nikhil"),
    ("6","Rohit"),
    ("7","Balachandar"),
    ("8","Dipu / Sreedeep"),
]
'''
if "GROUP_FACULTY" not in src:
    # insert right before "def qblk("
    src = src.replace("def qblk(", mapping + "\ndef qblk(", 1)

# 2. Insert a faculty allocation table into build_f, right after the intro paragraph
old_block = '''    s.append(Paragraph("<b>Case 1 twist:</b> small-group phase works presenting gas only; moderator reveals the 14-hour repeat gas in plenary.",ST["b"]))
    s.append(PageBreak())'''
new_block = '''    s.append(Paragraph("<b>Case 1 twist:</b> small-group phase works presenting gas only; moderator reveals the 14-hour repeat gas in plenary.",ST["b"]))

    s.append(Paragraph("Faculty allocation by group",ST["h1"]))
    fac_rows = [[Paragraph("Group",ST["cl"]), Paragraph("Faculty facilitator",ST["cl"])]]
    for g, n in GROUP_FACULTY:
        fac_rows.append([Paragraph(g, ST["cb"]), Paragraph(n, ST["c"])])
    fac_t = Table(fac_rows, colWidths=[30*mm, 140*mm], repeatRows=1)
    fac_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), TEAL),
        ("TEXTCOLOR",(0,0),(-1,0), colors.white),
        ("BACKGROUND",(0,1),(0,-1), GREY_L),
        ("BOX",(0,0),(-1,-1),0.6, GREY_M),
        ("INNERGRID",(0,0),(-1,-1),0.4, GREY_M),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    s.append(fac_t)

    s.append(PageBreak())'''
if "Faculty allocation by group" not in src:
    src = src.replace(old_block, new_block, 1)

with open("abg_workshop_generator.py","w",encoding="utf-8") as f:
    f.write(src)
print("PATCH OK - faculty names added to Faculty Guide")
