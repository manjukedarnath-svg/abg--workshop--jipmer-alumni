import re
with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

# ---- 1. Add new JS functions just before the closing </script> ----
NEW_JS = '''
/* ===== MODERATOR ENHANCEMENTS ===== */

function getParticipantUrl(){
  return window.location.origin + window.location.pathname;
}

function buildQRCode(){
  var url = getParticipantUrl();
  var el = document.getElementById("participantUrl");
  if (el) el.textContent = url;
  var img = document.getElementById("qrImg");
  if (img){
    img.src = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&margin=8&data=" + encodeURIComponent(url);
  }
}

function switchModTab(tabName){
  var tabs = document.querySelectorAll(".mod-tab");
  var panels = document.querySelectorAll(".mod-panel");
  tabs.forEach(function(t){
    t.classList.toggle("active", t.dataset.tab === tabName);
  });
  panels.forEach(function(p){
    p.classList.toggle("active", p.id === "panel-" + tabName);
  });
}

function buildCaseWalkthroughs(){
  var host = document.getElementById("caseWalkthroughs");
  if (!host) return;
  if (host.dataset.built === "1") return;
  host.dataset.built = "1";
  host.innerHTML = CASES.map(function(c){
    var html = '<div class="walkthrough-case" data-id="' + c.id + '">';
    html += '<button class="wt-head" type="button">'
      + '<span class="wt-num">' + c.id + '</span>'
      + '<span class="wt-title">' + esc(c.title) + '</span>'
      + '<span class="wt-arrow">&#9654;</span></button>';
    html += '<div class="wt-body">';
    html += '<div class="vignette" style="margin-bottom:14px"><b>Vignette.</b> ' + esc(c.vignette) + '</div>';
    html += '<div class="section-head" style="border-color:var(--teal);margin-top:16px"><h2 style="color:var(--teal-dark)">Initial gas</h2></div>';
    html += gasGrid(c.gas_in);
    html += '<div class="section-head" style="border-color:var(--teal);margin-top:20px"><h2 style="color:var(--teal-dark)">Interpretation</h2></div>';
    html += '<div class="steps">';
    c.steps_in.forEach(function(p){
      html += '<div class="step"><div class="lbl">' + esc(p[0]) + '</div><div class="model-answer">' + esc(p[1]) + '</div></div>';
    });
    html += '</div>';
    html += '<div class="section-head" style="border-color:var(--teal);margin-top:20px"><h2 style="color:var(--teal-dark)">SID / Stewart</h2></div>';
    html += '<table class="sid-table"><thead><tr><th>Tool</th><th>Value</th><th>Interpretation</th></tr></thead><tbody>';
    c.sid_in.forEach(function(r){
      html += '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td></tr>';
    });
    html += '</tbody></table>';
    html += '<div class="section-head" style="border-color:var(--teal);margin-top:20px"><h2 style="color:var(--teal-dark)">Case-specific Q&amp;A</h2></div>';
    c.qs.forEach(function(q, i){
      html += '<div class="qa" style="margin-bottom:12px"><div class="q"><span class="n">Q' + (i+1) + '.</span><span>' + esc(q) + '</span></div>'
        + '<div class="model-answer">' + esc(c.ans[i]) + '</div></div>';
    });
    if (c.gas_post){
      html += '<div class="section-head gold" style="margin-top:20px"><h2>Post-intervention</h2></div>';
      html += '<div class="post-card"><div class="ph">Intervention</div>'
        + '<div class="intervention">' + esc(c.intervention) + '</div>'
        + '<div class="ph">Repeat gas</div>' + gasGrid(c.gas_post) + '</div>';
      html += '<div class="steps" style="margin-top:12px">';
      c.steps_post.forEach(function(p){
        html += '<div class="step"><div class="lbl">' + esc(p[0]) + '</div><div class="model-answer">' + esc(p[1]) + '</div></div>';
      });
      html += '</div>';
      if (c.qs_post && c.ans_post){
        html += '<div style="margin-top:14px">';
        c.qs_post.forEach(function(q, i){
          html += '<div class="qa" style="margin-bottom:12px"><div class="q"><span class="n">Q' + (i+1) + '.</span><span>' + esc(q) + '</span></div>'
            + '<div class="model-answer">' + esc(c.ans_post[i]) + '</div></div>';
        });
        html += '</div>';
      }
    }
    if (c.pitfalls && c.pitfalls.length){
      html += '<div class="section-head" style="border-color:var(--warn);margin-top:20px"><h2 style="color:var(--warn)">Where groups go wrong</h2></div>';
      c.pitfalls.forEach(function(p){
        html += '<div class="pitfall"><span class="bullet">*</span><span>' + esc(p) + '</span></div>';
      });
    }
    if (c.synthesis){
      html += '<div class="callout" style="margin-top:16px"><div class="lbl">Faculty synthesis</div>'
        + '<div class="txt">' + esc(c.synthesis) + '</div></div>';
    }
    html += '<div class="callout" style="margin-top:10px"><div class="lbl">Take-home</div>'
      + '<div class="txt">' + esc(c.take) + '</div></div>';
    html += '</div></div>';
    return html;
  }).join("");

  host.querySelectorAll(".walkthrough-case .wt-head").forEach(function(btn){
    btn.addEventListener("click", function(){
      btn.parentElement.classList.toggle("open");
    });
  });
}
'''

# Insert NEW_JS before the closing </script> (just before "(function boot()")
marker = "(function boot(){"
if marker not in html:
    print("ERROR: could not find boot marker")
else:
    html = html.replace(marker, NEW_JS + "\n" + marker, 1)

# ---- 2. Replace initModerator with enhanced version ----
new_init = '''function initModerator(){
  document.getElementById("landing").style.display = "none";
  document.getElementById("app").style.display = "none";
  document.getElementById("moderator").classList.add("on");

  var seedInput = $("#seed");
  seedInput.value = STATE.seed;

  function renderCodes(){
    var seed = seedInput.value.trim() || SEED_DEFAULT;
    STATE.seed = seed;
    save(LS.seed, seed);
    $("#codeGrid").innerHTML = CASES.map(function(c){
      return '<button class="code-card" data-id="' + c.id + '">'
        + '<div class="cid">Case ' + c.id + '</div>'
        + '<div class="ct">' + esc(c.title) + '</div>'
        + '<div class="cc">' + unlockCode(c.id, seed) + '</div></button>';
    }).join("");
    $$("#codeGrid .code-card").forEach(function(b){
      b.addEventListener("click", function(){
        $$("#codeGrid .code-card").forEach(function(x){ x.classList.remove("active"); });
        b.classList.add("active");
        var id = parseInt(b.dataset.id, 10);
        var c = caseById(id);
        $("#bigCode").textContent = unlockCode(id, seed);
        $("#bigCodeLabel").textContent = "Case " + id + " - " + c.title;
      });
    });
  }

  seedInput.addEventListener("input", renderCodes);
  renderCodes();

  var first = document.querySelector('#codeGrid .code-card[data-id="1"]');
  if (first) first.click();

  // Copy link
  $("#copyLink").addEventListener("click", function(){
    var url = getParticipantUrl();
    if (navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(url).then(function(){ toast("Link copied"); }, function(){ toast(url); });
    } else {
      toast(url);
    }
  });

  // Refresh QR
  var refreshBtn = $("#refreshQR");
  if (refreshBtn){
    refreshBtn.addEventListener("click", function(){
      buildQRCode();
      toast("QR refreshed");
    });
  }

  // Tab switching
  $$(".mod-tab").forEach(function(t){
    t.addEventListener("click", function(){ switchModTab(t.dataset.tab); });
  });

  // Build QR and case walkthroughs
  buildQRCode();
  buildCaseWalkthroughs();
}
'''

# Find and replace existing initModerator
pattern = re.compile(r'function initModerator\(\)\{.*?\n\}\n', re.DOTALL)
new_html, n = pattern.subn(new_init + "\n", html, count=1)
if n == 0:
    print("ERROR: could not find initModerator to replace")
else:
    html = new_html
    with open("index.html","w",encoding="utf-8") as f:
        f.write(html)
    print("PATCH 3 OK - tabs, QR, case walkthroughs added")
