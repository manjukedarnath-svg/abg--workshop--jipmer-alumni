with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

# ---- 1. CSS for faculty mode ----
CSS = """
.faculty-mode .mod-tab[data-tab="codes"]{display:none}
.faculty-mode #panel-codes{display:none}
.faculty-banner{
  background:var(--gold-soft);border-left:4px solid var(--gold);
  border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:18px;
  font-size:13.5px;color:var(--navy);line-height:1.55;
}
.faculty-banner strong{color:var(--gold)}
"""
if "faculty-mode" not in html:
    html = html.replace("</style>", CSS + "\n</style>", 1)

# ---- 2. Faculty banner right before the tabs ----
if "facultyBanner" not in html:
    html = html.replace(
        '<div class="mod-tabs">',
        '<div class="faculty-banner" id="facultyBanner" style="display:none"><strong>Faculty view.</strong> 3 min interpret &middot; 3 min discuss &middot; 2 min synthesise. Tap any case below to expand the full walkthrough.</div>\n      <div class="mod-tabs">',
        1
    )

# ---- 3. initModerator accepts a mode ----
old_sig = 'function initModerator(){\n  document.getElementById("landing").style.display = "none";\n  document.getElementById("app").style.display = "none";\n  document.getElementById("moderator").classList.add("on");'
new_sig = '''function initModerator(mode){
  mode = mode || "moderator";
  document.getElementById("landing").style.display = "none";
  document.getElementById("app").style.display = "none";
  var modEl = document.getElementById("moderator");
  modEl.classList.add("on");
  if (mode === "faculty"){
    modEl.classList.add("faculty-mode");
    var banner = document.getElementById("facultyBanner");
    if (banner) banner.style.display = "block";
  }'''
if old_sig in html:
    html = html.replace(old_sig, new_sig, 1)

# ---- 4. Faculty defaults to Cases tab ----
old_after = '''  var first = document.querySelector('#codeGrid .code-card[data-id="1"]');
  if (first) first.click();'''
new_after = '''  var first = document.querySelector('#codeGrid .code-card[data-id="1"]');
  if (first) first.click();

  if (mode === "faculty"){
    switchModTab("cases");
  }'''
if old_after in html:
    html = html.replace(old_after, new_after, 1)

# ---- 5. Boot routes faculty ----
old_boot = '''(function boot(){
  var params = new URLSearchParams(location.search);
  if (params.get("mod") === "1" || location.hash === "#moderator"){
    initModerator();
    return;
  }'''
new_boot = '''(function boot(){
  var params = new URLSearchParams(location.search);
  if (params.get("mod") === "1" || location.hash === "#moderator"){
    initModerator("moderator");
    return;
  }
  if (params.get("faculty") === "1" || location.hash === "#faculty"){
    initModerator("faculty");
    return;
  }'''
if old_boot in html:
    html = html.replace(old_boot, new_boot, 1)

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
print("PATCH 5 OK - faculty view added (no codes)")
