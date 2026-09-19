with open("abg_workshop_generator.py","r",encoding="utf-8") as f:
    src = f.read()

# Replace the "How this session runs" intro paragraph in build_f
old = 's.append(Paragraph("All 13 cases handed out. 8-minute settling period. Each case = 15-minute unit.",ST["b"]))'
new = '''s.append(Paragraph("The booklet contains <b>13 cases</b>. At the start of the session the moderator randomly draws <b>8 cases</b> for the live run — every group works all 8; the other 5 become self-study cases sent after the workshop.",ST["b"]))
    s.append(Paragraph("All cases are handed out at once. 8-minute settling period. Each drawn case = one 15-minute unit (or 10 minutes in the compressed 90-minute format).",ST["b"]))'''

if old in src:
    src = src.replace(old, new, 1)
    with open("abg_workshop_generator.py","w",encoding="utf-8") as f:
        f.write(src)
    print("PATCH OK - faculty guide now states 13 cases, 8 drawn")
else:
    print("ERROR: could not find the target paragraph. Send me this output.")
