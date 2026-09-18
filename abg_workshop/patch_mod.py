with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

NEW_MOD = '''<div id="moderator">
  <div class="mod-wrap">
    <div class="mod-card">
      <div class="kick" style="text-align:left">Moderator & Faculty Console</div>
      <h1 style="margin:0 0 6px;font-size:22px">ABG Workshop Control</h1>
      <p style="color:var(--grey-t);font-size:13.5px;margin:0 0 18px">
        Unlock codes, case walkthroughs, and quick reference - all in one place.
      </p>

      <div class="mod-tabs">
        <button class="mod-tab active" data-tab="codes">Codes &amp; QR</button>
        <button class="mod-tab" data-tab="cases">Cases &amp; Answers</button>
        <button class="mod-tab" data-tab="cheat">Cheat Sheet</button>
      </div>

      <div class="mod-panel active" id="panel-codes">
        <div class="field" style="margin-bottom:14px">
          <label for="seed">Session seed</label>
          <input id="seed" type="text" value="JIPMER-PCCM-26">
        </div>

        <div class="qr-block">
          <div id="qrContainer">
            <img id="qrImg" alt="Participant QR code" src="">
          </div>
          <div class="qr-info">
            <div style="font-weight:700;color:var(--teal-dark);font-size:13px;letter-spacing:.04em;text-transform:uppercase;margin-bottom:4px">Scan to join</div>
            <p style="color:var(--grey-t);font-size:13px;margin:0 0 8px;line-height:1.5">
              Participants point their phone camera at this QR code. It opens the participant app directly.
            </p>
            <div class="url" id="participantUrl">-</div>
            <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
              <button class="btn sm" id="copyLink">Copy link</button>
              <button class="btn ghost sm" id="refreshQR">Refresh QR</button>
            </div>
          </div>
        </div>

        <div style="margin-top:24px">
          <div class="sb-title">Selected case</div>
          <div class="big-code" id="bigCode">- - - -</div>
          <div style="text-align:center;color:var(--grey-t);font-size:13px" id="bigCodeLabel">Click a case below</div>
        </div>

        <div style="margin-top:24px">
          <div class="sb-title">All unlock codes</div>
          <div class="code-grid" id="codeGrid"></div>
        </div>
      </div>

      <div class="mod-panel" id="panel-cases">
        <p style="color:var(--grey-t);font-size:13.5px;margin:0 0 16px">
          Tap any case to expand the full walkthrough: vignette, gas, interpretation, SID analysis, case-specific Q&amp;A, post-intervention gas, pitfalls, and take-home.
        </p>
        <div id="caseWalkthroughs"></div>
      </div>

      <div class="mod-panel" id="panel-cheat">
        <p style="color:var(--grey-t);font-size:13.5px;margin:0 0 16px">
          Formulas, normal ranges, and pattern-recognition at a glance.
        </p>

        <div class="cheat-section">
          <h3>Core formulas</h3>
          <table>
            <thead><tr><th>Tool</th><th>Formula</th><th>Notes</th></tr></thead>
            <tbody>
              <tr><td>[H+]</td><td>24 &times; PaCO2 / HCO3</td><td>Should match reported pH (see table below)</td></tr>
              <tr><td>Anion gap</td><td>Na &minus; (Cl + HCO3)</td><td>Normal 12 &plusmn; 2</td></tr>
              <tr><td>Albumin-corrected AG</td><td>AG + 2.5 &times; (4.0 &minus; albumin)</td><td>Add 2.5 per 1 g/dL below 4.0</td></tr>
              <tr><td>Delta ratio</td><td>(AG &minus; 12) / (24 &minus; HCO3)</td><td>&lt;0.4 NAGMA &middot; 0.4-0.8 mixed &middot; 0.8-2 HAGMA &middot; &gt;2 +met alk</td></tr>
              <tr><td>Winter's (met acidosis)</td><td>PaCO2 = 1.5 &times; HCO3 + 8 &plusmn; 2</td><td>Expected respiratory compensation</td></tr>
              <tr><td>Met alkalosis comp</td><td>PaCO2 = 0.7 &times; HCO3 + 21 &plusmn; 2</td><td>Or 40 + 0.7 &times; (HCO3 &minus; 24) &plusmn; 5</td></tr>
              <tr><td>Acute resp alkalosis</td><td>HCO3 falls ~2 per 10 mmHg PaCO2 fall</td><td>Chronic: falls ~4-5 per 10</td></tr>
              <tr><td>Acute resp acidosis</td><td>HCO3 rises ~1 per 10 mmHg PaCO2 rise</td><td>Chronic: rises ~4 per 10</td></tr>
              <tr><td>Corrected Na (DKA)</td><td>Na + 1.6 &times; [(glucose &minus; 100)/100]</td><td>True Na if glucose were 100</td></tr>
              <tr><td>P/F ratio</td><td>PaO2 / FiO2</td><td>&gt;300 normal, &lt;200 severe, &lt;100 critical</td></tr>
              <tr><td>Oxygenation index</td><td>MAP &times; FiO2 &times; 100 / PaO2</td><td>PALICC severe ARDS: OI &ge; 16</td></tr>
              <tr><td>CaO2</td><td>1.34 &times; Hb &times; SaO2 + 0.003 &times; PaO2</td><td>Normal ~16-20 mL/dL</td></tr>
              <tr><td>DO2</td><td>Cardiac output &times; CaO2</td><td>Oxygen delivery</td></tr>
            </tbody>
          </table>
        </div>

        <div class="cheat-section">
          <h3>[H+] to pH reference</h3>
          <table>
            <thead><tr><th>pH</th><th>[H+]</th><th>pH</th><th>[H+]</th><th>pH</th><th>[H+]</th></tr></thead>
            <tbody>
              <tr><td>7.80</td><td>16</td><td>7.40</td><td>40</td><td>7.00</td><td>89</td></tr>
              <tr><td>7.70</td><td>20</td><td>7.30</td><td>50</td><td>6.90</td><td>112</td></tr>
              <tr><td>7.60</td><td>25</td><td>7.20</td><td>63</td><td>6.80</td><td>159</td></tr>
              <tr><td>7.50</td><td>32</td><td>7.10</td><td>79</td><td>6.70</td><td>200</td></tr>
            </tbody>
          </table>
        </div>

        <div class="cheat-section">
          <h3>SID / Stewart framework</h3>
          <table>
            <thead><tr><th>Force</th><th>Tool</th><th>Direction</th></tr></thead>
            <tbody>
              <tr><td>SID</td><td>Na &minus; Cl (normal ~36)</td><td>Low = chloride-driven acidosis. High = chloride-loss alkalosis.</td></tr>
              <tr><td>Atot</td><td>Albumin + phosphate</td><td>High = acidifying. Low albumin = alkalinising (masks HAGMA).</td></tr>
              <tr><td>Unmeasured anions</td><td>AG &minus; (lactate + ketones)</td><td>High = organic acids, salicylate, urate, oxalate.</td></tr>
            </tbody>
          </table>
        </div>

        <div class="cheat-section">
          <h3>Common patterns &mdash; one-line answers</h3>
          <table>
            <thead><tr><th>Pattern</th><th>Think</th></tr></thead>
            <tbody>
              <tr><td>HAGMA + appropriate comp + glucose 480 + ketones</td><td>DKA (severe if pH &lt;7.1 or HCO3 &lt;5)</td></tr>
              <tr><td>Met alkalosis + hypochloraemia + hypokalaemia + urine Cl &lt;15</td><td>Pyloric stenosis (chloride-responsive)</td></tr>
              <tr><td>NAGMA + hyperchloraemia + normal lactate</td><td>GI bicarbonate loss (diarrhoea)</td></tr>
              <tr><td>Raw AG normal + low albumin + abnormal lactate</td><td>Correct AG for albumin &mdash; unmask HAGMA; suspect IEM if recurrent</td></tr>
              <tr><td>Near-normal pH + low PaCO2 + low HCO3 + tinnitus</td><td>Salicylate poisoning (mixed disorder)</td></tr>
              <tr><td>PaCO2 high + HCO3 low simultaneously</td><td>Mixed resp + metabolic acidosis &mdash; never "compensation"</td></tr>
              <tr><td>Hb &lt;5 + normal SpO2 + low ScvO2 + high lactate</td><td>Oxygen delivery failure &mdash; transfuse</td></tr>
              <tr><td>High PaO2 + low SpO2 + low SO2 + chocolate-brown blood</td><td>Methaemoglobinaemia &mdash; methylene blue</td></tr>
              <tr><td>Neonate + resp alkalosis + lethargy + afebrile</td><td>Hyperammonaemia &mdash; ammonia on ice</td></tr>
              <tr><td>Neonate + HAGMA + ketones + hypoglycaemia</td><td>IEM (organic acidaemia / FAOD) &mdash; critical sample</td></tr>
              <tr><td>HUS + K 6.8 + iCa 0.92 + phosphate 9.5</td><td>Triple-hit acidosis &mdash; dialysis, treat electrolytes</td></tr>
              <tr><td>Hep A + encephalopathy + SBE &minus;1 + low albumin</td><td>Masked HAGMA + resp alkalosis &mdash; check glucose</td></tr>
              <tr><td>Fasting hypoglycaemia + low ketones + high FFA</td><td>FAOD (e.g., MCAD) &mdash; critical sample before dextrose</td></tr>
              <tr><td>2-week-old + shock + Na 122 + K 7.8 + glucose 40</td><td>CAH salt-wasting &mdash; sample before hydrocortisone</td></tr>
            </tbody>
          </table>
        </div>

        <div class="cheat-section">
          <h3>Pitfalls to teach</h3>
          <table>
            <thead><tr><th>Pitfall</th><th>Fix</th></tr></thead>
            <tbody>
              <tr><td>Reading pH first and stopping</td><td>Check PaCO2 and HCO3 against each other &mdash; normal pH can hide mixed disorder</td></tr>
              <tr><td>Skipping albumin correction</td><td>Correct AG for albumin as a reflex &mdash; most consequential when raw AG looks normal</td></tr>
              <tr><td>Applying delta ratio to alkalosis</td><td>Delta ratio only valid when AG is raised (HAGMA)</td></tr>
              <tr><td>Calling high PaCO2 "ventilator lag"</td><td>Name it as a second primary disorder needing its own fix</td></tr>
              <tr><td>Trusting SpO2 in anaemia or MetHb</td><td>SpO2 says nothing about delivery &mdash; use ScvO2, lactate, co-oximetry</td></tr>
              <tr><td>Not checking SID on repeat gases</td><td>SID falling = chloride loading; acid has changed character</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>

'''

start = html.index('<div id="moderator">')
end = html.index('<div class="toast"')
html = html[:start] + NEW_MOD + html[end:]

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
print("PATCH 2 OK - moderator HTML replaced with tabs + QR + cases + cheat sheet")
