with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

# ── 1. CSS for the instruction card ──
CSS = """
.landing-instructions{
  margin:22px 0 26px;
  border:1px solid var(--grey-m);
  border-radius:12px;
  padding:16px 18px 14px;
  background:var(--grey-l);
}
.landing-instructions .li-title{
  font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:var(--teal-dark);margin:0 0 10px;
}
.landing-steps{display:flex;flex-direction:column;gap:10px}
.landing-step{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.45;color:var(--navy)}
.landing-step .n{
  min-width:22px;height:22px;border-radius:50%;background:var(--teal);color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;
  flex-shrink:0;margin-top:1px;
}
.landing-step b{color:var(--navy)}
.landing-step .hint{color:var(--grey-t)}
@media(max-width:640px){
  .landing-instructions{padding:14px 14px 12px}
  .landing-step{font-size:12.5px}
  .landing-step .n{min-width:20px;height:20px;font-size:10.5px}
}
"""
if "landing-instructions" not in html:
    html = html.replace("</style>", CSS + "\n</style>", 1)

# ── 2. Insert the instruction block before the name field ──
old_block = '''<div class="field">
      <label for="pname">Your name</label>'''
new_block = '''<div class="landing-instructions">
      <p class="li-title">How this works &mdash; 5 steps</p>
      <div class="landing-steps">
        <div class="landing-step"><span class="n">1</span><div><b>Enter your name and pick your group.</b> <span class="hint">Choose the same group as the faculty at your table.</span></div></div>
        <div class="landing-step"><span class="n">2</span><div><b>Tap &ldquo;Start the workshop&rdquo;</b> to open the case list. You&rsquo;ll land on Case 1.</div></div>
        <div class="landing-step"><span class="n">3</span><div><b>Work each case as we go.</b> <span class="hint">Fill in the interpretation grid, SID analysis, and case-specific questions in your own words.</span></div></div>
        <div class="landing-step"><span class="n">4</span><div><b>Wait for the moderator&rsquo;s 4-character code</b> at the end of each case. Type it into the unlock bar and tap <b>Unlock answers</b>.</div></div>
        <div class="landing-step"><span class="n">5</span><div><b>Compare your answers with the model interpretation</b>, then move to the next case. <span class="hint">Answers autosave on this device &mdash; you can leave and come back any time.</span></div></div>
      </div>
    </div>

    <div class="field">
      <label for="pname">Your name</label>'''

if "landing-instructions" not in html or old_block in html:
    if "landing-steps" not in html:
        html = html.replace(old_block, new_block, 1)
        print("  inserted instruction block")
    else:
        print("  instruction block already present")
else:
    print("  WARNING: could not find name field placeholder")

# ── 3. Soften the autosave footer note (avoid duplicate messaging) ──
html = html.replace(
    'Answers autosave on this device. You can return any time.',
    'Your answers stay on your phone. No login required.'
)

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
print("PATCH OK - landing instructions added")
