import re
with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

CSS = """
/* ===== MOBILE-FIRST PATCH ===== */
@media(max-width:640px){
  body{font-size:15px}
  .card{padding:24px 20px;border-radius:14px}
  .card h1{font-size:22px}
  .kick{font-size:10px}
  .topbar{padding:8px 12px;gap:8px}
  .brand{font-size:13px}
  .topbar .who{gap:6px;font-size:11.5px}
  .topbar .who .chip{padding:3px 8px;font-size:10.5px}
  .autosave{font-size:10.5px}
  .main{padding:16px 14px 110px;max-width:100%}
  .case-head h1{font-size:21px;letter-spacing:-.02em}
  .case-head .eyebrow{font-size:10px}
  .vignette{font-size:14px;padding:12px 14px;line-height:1.5}
  .section{margin-top:22px}
  .section-head{padding-bottom:5px;margin-bottom:10px}
  .section-head h2{font-size:12px;letter-spacing:.06em}
  .section-head .tag{font-size:10px}
  .gas-grid{grid-template-columns:repeat(3,1fr);gap:6px}
  .gas-card{padding:7px 4px 8px;border-radius:6px}
  .gas-card .l{font-size:9.5px;letter-spacing:0;line-height:1.15}
  .gas-card .v{font-size:17px;margin-top:2px}
  .steps{gap:10px}
  .step{grid-template-columns:1fr;gap:6px;padding:11px 12px;border-radius:7px}
  .step .lbl{font-size:12.5px;padding-top:0;line-height:1.35}
  .step textarea{font-size:16px;min-height:64px;padding:11px 12px;border-radius:7px;line-height:1.45}
  .model-answer{font-size:14px;padding:11px 12px;line-height:1.55}
  .sid-table{font-size:13px;border-radius:7px}
  .sid-table th{padding:8px 8px;font-size:10px;letter-spacing:.03em}
  .sid-table td{padding:9px 8px;font-size:13px}
  .sid-table td:first-child{width:auto;font-size:12.5px;display:table-cell}
  .sid-table td:nth-child(2){width:auto;font-size:12.5px;display:table-cell}
  .sid-table textarea{font-size:15px;padding:9px 10px;min-height:44px}
  .qa{margin-bottom:14px}
  .qa .q{font-size:14px;line-height:1.45}
  .qa .q .n{font-size:14px}
  .qa textarea{font-size:16px;min-height:80px;padding:12px;border-radius:7px;line-height:1.45}
  .unlock-bar{padding:16px 14px;border-radius:10px;margin-top:24px}
  .unlock-bar h3{font-size:14px}
  .unlock-bar p{font-size:12.5px}
  .unlock-row{flex-direction:column;align-items:stretch;gap:8px}
  .unlock-row input{width:100%;font-size:24px;letter-spacing:.3em;padding:14px;border-radius:9px}
  .unlock-row .btn{width:100%;padding:13px;font-size:15px}
  .btn{padding:12px 16px;font-size:15px;border-radius:8px}
  .btn.sm{padding:9px 12px;font-size:13.5px}
  .answer-banner{padding:12px 14px;border-radius:0 9px 9px 0}
  .answer-banner .icon{width:30px;height:30px;font-size:12px}
  .answer-banner h3{font-size:14px}
  .answer-banner p{font-size:12px}
  .callout{padding:12px 14px;border-radius:0 7px 7px 0}
  .callout .lbl{font-size:10px}
  .callout .txt{font-size:14px;line-height:1.5}
  .pitfall{font-size:13.5px;padding:5px 0}
  .post-card{padding:14px 14px;border-radius:9px}
  .post-card .ph{font-size:10.5px}
  .post-card .intervention{font-size:13px}
  .mod-card{padding:18px 16px;border-radius:12px}
  .mod-tabs{padding:3px;border-radius:9px;gap:3px}
  .mod-tab{padding:9px 12px;font-size:13px}
  .big-code{font-size:48px;padding:20px 0;letter-spacing:.18em;border-radius:12px}
  .code-grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px}
  .code-card{padding:10px}
  .code-card .cc{font-size:22px;padding:5px 0;letter-spacing:.15em}
  .qr-block{flex-direction:column;text-align:center;padding:16px}
  .qr-block img{width:200px;height:200px}
  .walkthrough-case .wt-head{padding:12px 14px;gap:10px}
  .walkthrough-case .wt-head .wt-num{width:28px;height:28px;font-size:12px}
  .walkthrough-case .wt-head .wt-title{font-size:13.5px}
  .walkthrough-case .wt-body{padding:14px}
  .cheat-section h3{font-size:14px}
  .cheat-section table{font-size:12.5px;border-radius:7px}
  .cheat-section th{padding:8px;font-size:10px;letter-spacing:.03em}
  .cheat-section td{padding:8px;font-size:12.5px}
}
@media(max-width:900px){
  .sidebar{
    position:fixed;left:0;right:0;bottom:0;top:auto;max-height:78dvh;
    transform:translateY(100%);border-radius:16px 16px 0 0;
    box-shadow:0 -8px 30px rgba(15,30,40,.15);border-right:none;
    border-top:1px solid var(--grey-m);
    padding:14px 14px 36px;transition:transform .25s cubic-bezier(.2,.9,.3,1);
    z-index:50;
  }
  .sidebar.open{transform:translateY(0)}
  .sidebar::before{
    content:'';display:block;width:40px;height:4px;border-radius:2px;
    background:var(--grey-m);margin:0 auto 12px;
  }
  .case-item{padding:11px 12px;border-radius:8px}
  .case-item .num{min-width:28px;height:28px;font-size:12.5px}
  .case-item .t{font-size:14px}
  .case-item .s{font-size:11.5px}
}
.mod-tabs{display:flex;gap:4px;background:var(--grey-l);padding:4px;border-radius:10px;margin-bottom:20px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.mod-tab{flex:1;min-width:max-content;padding:10px 16px;border-radius:7px;font-weight:600;font-size:13.5px;color:var(--grey-t);transition:all .15s;white-space:nowrap}
.mod-tab.active{background:#fff;color:var(--teal-dark);box-shadow:0 1px 3px rgba(15,30,40,.08)}
.mod-panel{display:none}
.mod-panel.active{display:block}
.qr-block{display:flex;gap:20px;align-items:center;flex-wrap:wrap;padding:18px;background:var(--grey-l);border-radius:12px;border:1px solid var(--grey-m);margin-top:16px}
.qr-block img{width:200px;height:200px;background:#fff;border-radius:8px;padding:8px;border:1px solid var(--grey-m)}
.qr-block .qr-info{flex:1;min-width:200px}
.qr-block .qr-info .url{font-family:ui-monospace,Menlo,monospace;font-size:13px;background:#fff;padding:10px 12px;border-radius:8px;border:1px solid var(--grey-m);word-break:break-all;margin-top:6px}
.walkthrough-case{border:1px solid var(--grey-m);border-radius:12px;margin-bottom:14px;overflow:hidden;background:#fff}
.walkthrough-case .wt-head{padding:14px 18px;background:var(--grey-l);cursor:pointer;display:flex;align-items:center;gap:12px;border:none;width:100%;text-align:left;font-family:inherit}
.walkthrough-case .wt-head .wt-num{width:32px;height:32px;border-radius:50%;background:var(--teal);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0;font-size:13px}
.walkthrough-case .wt-head .wt-title{flex:1;font-weight:600;font-size:14.5px;color:var(--navy)}
.walkthrough-case .wt-head .wt-arrow{color:var(--grey-t);transition:transform .2s;font-size:12px}
.walkthrough-case.open .wt-head .wt-arrow{transform:rotate(90deg)}
.walkthrough-case .wt-body{display:none;padding:18px;border-top:1px solid var(--grey-m)}
.walkthrough-case.open .wt-body{display:block}
.cheat-section{margin-bottom:24px}
.cheat-section h3{font-size:15px;color:var(--teal-dark);margin:0 0 10px;font-weight:700}
.cheat-section table{width:100%;border-collapse:separate;border-spacing:0;border:1px solid var(--grey-m);border-radius:8px;overflow:hidden;font-size:13.5px}
.cheat-section th{background:var(--teal-dark);color:#fff;text-align:left;padding:9px 12px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:600}
.cheat-section td{padding:10px 12px;border-top:1px solid var(--grey-m);vertical-align:top;color:var(--navy)}
.cheat-section tr:nth-child(even) td{background:#FBFCFD}
.cheat-section td:first-child{font-weight:700;color:var(--teal-dark)}
"""

if "MOBILE-FIRST PATCH" not in html:
    html = html.replace("</style>", CSS + "\n</style>", 1)

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
print("PATCH 1 OK - mobile CSS applied")
