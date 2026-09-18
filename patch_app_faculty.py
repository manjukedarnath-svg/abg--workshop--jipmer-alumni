with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

# 1. Insert allocation block placeholder in the Cases & Answers panel
old_cases = '''<div class="mod-panel" id="panel-cases">
        <p style="color:var(--grey-t);font-size:13.5px;margin:0 0 16px">
          Tap any case to expand the full walkthrough: vignette, gas, interpretation, SID analysis, case-specific Q&amp;A, post-intervention gas, pitfalls, and take-home.
        </p>
        <div id="caseWalkthroughs"></div>
      </div>'''
new_cases = '''<div class="mod-panel" id="panel-cases">
        <div id="facultyAllocationBlock"></div>
        <p style="color:var(--grey-t);font-size:13.5px;margin:0 0 16px">
          Tap any case to expand the full walkthrough: vignette, gas, interpretation, SID analysis, case-specific Q&amp;A, post-intervention gas, pitfalls, and take-home.
        </p>
        <div id="caseWalkthroughs"></div>
      </div>'''

if old_cases in html and "facultyAllocationBlock" not in html:
    html = html.replace(old_cases, new_cases, 1)
    print("  inserted #facultyAllocationBlock placeholder")
elif "facultyAllocationBlock" in html:
    print("  placeholder already present")
else:
    print("  ERROR: could not find Cases & Answers panel")

# 2. Add JS constant + renderer
if "FACULTY_ALLOCATION" not in html:
    js_block = '''
/* ===== FACULTY ALLOCATION ===== */
var FACULTY_ALLOCATION = [
  {group:"1", name:"Manju Kedarnath"},
  {group:"2", name:"Shilpa"},
  {group:"3", name:"Namitha"},
  {group:"4", name:"Sivamurukan"},
  {group:"5", name:"Nikhil"},
  {group:"6", name:"Rohit"},
  {group:"7", name:"Balachandar"},
  {group:"8", name:"Dipu / Sreedeep"}
];

function renderFacultyBlock(){
  var host = document.getElementById("facultyAllocationBlock");
  if (!host) return;
  var html = '<div class="cheat-section" style="margin-bottom:24px">';
  html += '<h3>Faculty allocation by group</h3>';
  html += '<table><thead><tr><th style="width:22%">Group</th><th>Faculty facilitator</th></tr></thead><tbody>';
  FACULTY_ALLOCATION.forEach(function(f){
    html += '<tr><td>Group ' + f.group + '</td><td>' + f.name + '</td></tr>';
  });
  html += '</tbody></table></div>';
  host.innerHTML = html;
}
'''
    html = html.replace("function buildQRCode(){", js_block + "\nfunction buildQRCode(){", 1)
    print("  inserted FACULTY_ALLOCATION + renderFacultyBlock")
else:
    print("  JS block already present")

# 3. Call renderFacultyBlock in initModerator
old_call = "  buildQRCode();\n  buildCaseWalkthroughs();"
new_call = "  buildQRCode();\n  buildCaseWalkthroughs();\n  renderFacultyBlock();"
if old_call in html and "renderFacultyBlock();" not in html.split("function initModerator")[1][:2000] if "function initModerator" in html else False:
    html = html.replace(old_call, new_call, 1)
    print("  added renderFacultyBlock() call")
elif "renderFacultyBlock();" in html:
    print("  call already present")
else:
    # fallback: replace the first occurrence
    if old_call in html:
        html = html.replace(old_call, new_call, 1)
        print("  added renderFacultyBlock() call")
    else:
        print("  WARNING: could not add renderFacultyBlock() call")

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
print("PATCH B OK - faculty allocation added to live app")
