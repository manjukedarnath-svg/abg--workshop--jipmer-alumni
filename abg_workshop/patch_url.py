import re
with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

# 1. Add participant URL field to the Codes & QR panel
html = html.replace(
    '<div class="field" style="margin-bottom:14px">\n          <label for="seed">Session seed</label>\n          <input id="seed" type="text" value="JIPMER-PCCM-26">\n        </div>',
    '''<div class="field" style="margin-bottom:14px">
          <label for="seed">Session seed</label>
          <input id="seed" type="text" value="JIPMER-PCCM-26">
        </div>
        <div class="field" style="margin-bottom:14px">
          <label for="baseUrl">Participant base URL <span style="text-transform:none;color:var(--grey-t);font-weight:400">(edit if auto-detect is wrong)</span></label>
          <input id="baseUrl" type="text" placeholder="http://192.168.1.42:8000/">
        </div>''',
    1
)

# 2. Replace getParticipantUrl to use stored value
old_url = '''function getParticipantUrl(){
  return window.location.origin + window.location.pathname;
}'''
new_url = '''function detectLanIP(){
  return new Promise(function(resolve){
    try{
      var pc = new RTCPeerConnection({iceServers:[]});
      pc.createDataChannel("");
      var ips = {};
      pc.onicecandidate = function(e){
        if (!e || !e.candidate) { resolve(Object.keys(ips)[0] || null); return; }
        var m = /([0-9]{1,3}(\\.[0-9]{1,3}){3})/.exec(e.candidate.candidate);
        if (m && !m[1].startsWith("127.") && !m[1].startsWith("169.254.")) ips[m[1]] = true;
      };
      pc.createOffer().then(function(o){ return pc.setLocalDescription(o); });
      setTimeout(function(){ resolve(Object.keys(ips)[0] || null); }, 1200);
    }catch(e){ resolve(null); }
  });
}

function getParticipantUrl(){
  var stored = localStorage.getItem("abg:baseUrl");
  if (stored) return stored;
  var el = document.getElementById("baseUrl");
  if (el && el.value.trim()) return el.value.trim();
  return window.location.origin + window.location.pathname;
}

function setParticipantUrl(url){
  localStorage.setItem("abg:baseUrl", url);
  var el = document.getElementById("baseUrl");
  if (el) el.value = url;
}'''
if old_url in html:
    html = html.replace(old_url, new_url, 1)

# 3. In initModerator, add baseUrl handling
old_init_block = '''  var seedInput = $("#seed");
  seedInput.value = STATE.seed;'''
new_init_block = '''  var seedInput = $("#seed");
  seedInput.value = STATE.seed;

  var baseUrlInput = $("#baseUrl");
  var stored = localStorage.getItem("abg:baseUrl");
  if (stored){
    baseUrlInput.value = stored;
  } else {
    // Smart default: if we're on localhost, try to detect LAN IP
    var host = window.location.hostname;
    if (host === "localhost" || host === "127.0.0.1" || host === "::1"){
      detectLanIP().then(function(ip){
        if (ip){
          var url = "http://" + ip + ":" + (window.location.port || "8000") + "/";
          baseUrlInput.value = url;
          setParticipantUrl(url);
          buildQRCode();
          toast("Detected LAN IP: " + ip);
        } else {
          baseUrlInput.value = "http://YOUR-MAC-IP:8000/";
          baseUrlInput.placeholder = "Enter http://YOUR-MAC-IP:8000/";
        }
      });
    } else {
      baseUrlInput.value = window.location.origin + window.location.pathname;
    }
  }
  baseUrlInput.addEventListener("input", function(){
    setParticipantUrl(baseUrlInput.value.trim());
    buildQRCode();
  });'''
if old_init_block in html:
    html = html.replace(old_init_block, new_init_block, 1)

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
print("PATCH 4 OK - participant URL field + LAN IP auto-detect")
