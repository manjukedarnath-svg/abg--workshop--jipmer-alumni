import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, Table, TableStyle, PageBreak)

TEAL=colors.HexColor("#0F6E6E"); TEAL_D=colors.HexColor("#0A4E4E")
NAVY=colors.HexColor("#1B2A3A"); GOLD=colors.HexColor("#B8892B")
GREY_L=colors.HexColor("#F4F6F8"); GREY_M=colors.HexColor("#E1E6EB")
GREY_T=colors.HexColor("#5A6672")
OUT="output"; os.makedirs(OUT,exist_ok=True)

def S(n,**k): return ParagraphStyle(n,**k)
ST={"kick":S("k",fontName="Helvetica",fontSize=8,textColor=GREY_T,alignment=TA_CENTER,spaceAfter=2),
 "title":S("t",fontName="Helvetica-Bold",fontSize=24,textColor=NAVY,alignment=TA_CENTER,leading=28,spaceAfter=4),
 "sub":S("s",fontName="Helvetica",fontSize=11,textColor=GREY_T,alignment=TA_CENTER,leading=14,spaceAfter=12),
 "h1":S("h1",fontName="Helvetica-Bold",fontSize=15,textColor=TEAL,leading=19,spaceBefore=8,spaceAfter=5),
 "h2":S("h2",fontName="Helvetica-Bold",fontSize=11.5,textColor=TEAL_D,leading=15,spaceBefore=6,spaceAfter=4),
 "h3":S("h3",fontName="Helvetica-Bold",fontSize=10,textColor=NAVY,leading=13,spaceBefore=5,spaceAfter=3),
 "b":S("b",fontName="Helvetica",fontSize=9,textColor=NAVY,leading=12.5,alignment=TA_JUSTIFY,spaceAfter=3),
 "bs":S("bs",fontName="Helvetica",fontSize=8.5,textColor=NAVY,leading=11,spaceAfter=2),
 "bul":S("bu",fontName="Helvetica",fontSize=9,textColor=NAVY,leading=12.5,leftIndent=10,spaceAfter=2),
 "cb":S("cb",fontName="Helvetica-Bold",fontSize=8.3,textColor=NAVY,leading=10.5),
 "c":S("c",fontName="Helvetica",fontSize=8.3,textColor=NAVY,leading=10.5),
 "cl":S("cl",fontName="Helvetica-Bold",fontSize=8,textColor=TEAL_D,leading=10),
 "gl":S("gl",fontName="Helvetica-Bold",fontSize=7.5,textColor=GREY_T,alignment=TA_CENTER,leading=9),
 "gv":S("gv",fontName="Helvetica-Bold",fontSize=14,textColor=NAVY,alignment=TA_CENTER,leading=17)}

def foot(c,d,l):
    c.saveState(); c.setStrokeColor(GREY_M); c.setLineWidth(0.5)
    c.line(15*mm,15*mm,A4[0]-15*mm,15*mm)
    c.setFont("Helvetica",7.5); c.setFillColor(GREY_T)
    c.drawString(15*mm,10*mm,"2nd JIPMER Paediatric Critical Care Meet - ABG Workshop")
    c.drawRightString(A4[0]-15*mm,10*mm,f"{l} . Page {c.getPageNumber()}")
    c.restoreState()

def doc(path,label):
    d=BaseDocTemplate(path,pagesize=A4,leftMargin=15*mm,rightMargin=15*mm,topMargin=15*mm,bottomMargin=20*mm,title=label)
    f=Frame(d.leftMargin,d.bottomMargin,d.width,d.height,id="m")
    d.addPageTemplates([PageTemplate(id="m",frames=[f],onPage=lambda c,d:foot(c,d,label))])
    return d

def hdr(k,t,s):
    r=[Paragraph(k,ST["kick"]),Paragraph(t,ST["title"]),Paragraph(s,ST["sub"])]
    tb=Table([[""]],colWidths=[170*mm],rowHeights=[1.2])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),TEAL)]))
    r+=[tb,Spacer(1,8)]; return r

def gas(dt,cw=17*mm,cpr=5):
    rows=[]; r=[]
    for k,v in dt.items():
        cell=Table([[Paragraph(k,ST["gl"])],[Paragraph(str(v),ST["gv"])]],colWidths=[cw],rowHeights=[5*mm,8*mm])
        cell.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREY_L),("BOX",(0,0),(-1,-1),0.5,GREY_M),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),2),("RIGHTPADDING",(0,0),(-1,-1),2),("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2)]))
        r.append(cell)
        if len(r)==cpr: rows.append(r); r=[]
    if r:
        while len(r)<cpr: r.append("")
        rows.append(r)
    t=Table(rows,colWidths=[cw]*cpr)
    t.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),1.5),("RIGHTPADDING",(0,0),(-1,-1),1.5),("TOPPADDING",(0,0),(-1,-1),1.5),("BOTTOMPADDING",(0,0),(-1,-1),1.5)]))
    return t

def stbl(rows,hdr_=("Step","Answer"),cw=None):
    if cw is None: cw=[45*mm,125*mm]
    d=[[Paragraph(hdr_[0],ST["cl"]),Paragraph(hdr_[1],ST["cl"])]]
    for a,b in rows: d.append([Paragraph(a,ST["cb"]),Paragraph(b or "",ST["c"])])
    t=Table(d,colWidths=cw,repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),TEAL),("TEXTCOLOR",(0,0),(-1,0),colors.white),("BACKGROUND",(0,1),(0,-1),GREY_L),("BOX",(0,0),(-1,-1),0.6,GREY_M),("INNERGRID",(0,0),(-1,-1),0.4,GREY_M),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),3.5),("BOTTOMPADDING",(0,0),(-1,-1),3.5)]))
    return t

def sidt(rows):
    d=[["Tool","Value","Interpretation"]]
    for a,b,c in rows: d.append([Paragraph(a,ST["cb"]),Paragraph(b,ST["c"]),Paragraph(c,ST["c"])])
    t=Table(d,colWidths=[38*mm,30*mm,102*mm],repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),TEAL_D),("TEXTCOLOR",(0,0),(-1,0),colors.white),("BACKGROUND",(0,1),(0,-1),GREY_L),("BOX",(0,0),(-1,-1),0.6,GREY_M),("INNERGRID",(0,0),(-1,-1),0.4,GREY_M),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),3.5),("BOTTOMPADDING",(0,0),(-1,-1),3.5)]))
    return t

def call(t,b):
    inner=[[Paragraph("<b>"+t+"</b>",ST["b"])],[Paragraph(b,ST["b"])]]
    tb=Table(inner,colWidths=[168*mm])
    tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#FBF7EC")),("LINEBEFORE",(0,0),(0,-1),3,GOLD),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("VALIGN",(0,0),(-1,-1),"TOP")]))
    return tb

CASES=[]
CASES.append({"id":1,"title":"DKA",
 "vignette":"10-year-old girl, 2 weeks of polyuria and 3 days of vomiting and abdominal pain. Acidotic breathing present, haemodynamically stable, GCS 11.",
 "gas_in":{"pH":"7.08","PaCO2":"14","HCO3":"4","PaO2":"36","Na":"132","K":"4.5","Cl":"98","Albumin":"4.0","Glucose":"480","b-OHB":"5.8"},
 "steps_in":[("1. Clinical history","2 weeks of polyuria (osmotic diuresis) with vomiting and abdominal pain, Kussmaul breathing, GCS 11 - classical new-onset DKA with early obtundation."),
  ("2. Internal validity","[H+] = 24 x 14 / 4 = 84 nmol/L -> pH 7.08 - matches. PaO2 36 suggests a venous sample."),
  ("3. pH","7.08 - severe acidaemia."),("4. Primary disorder","HCO3 4 (low) with acidaemia -> metabolic acidosis."),
  ("5. Expected compensation","Winter's: PaCO2 = 1.5 x 4 + 8 = 14 +/-2. Actual 14 - appropriate."),
  ("6. Anion gap","AG = 132 - (98 + 4) = 30 (markedly raised). Albumin normal - no correction needed."),
  ("7. Delta ratio","(30 - 12)/(24 - 4) = 0.9 -> pure HAGMA."),
  ("8. Oxygenation & integration","Severe HAGMA with maximal appropriate respiratory compensation; AG 30 fully explained by ketoacids (b-OHB 5.8). Severe DKA.")],
 "sid_in":[("SID","132 - 98 = 34","Low-normal - mild chloride-driven component already present."),
  ("Atot","Albumin 4.0","Normal."),("Unmeasured anions","30 - 5.8 = 24.2","Markedly raised - ketoacids dominate."),
  ("Mechanism","-","Unmeasured anions, with mild chloride-driven component.")],
 "intervention":"10 mL/kg NS bolus, insulin infusion, NS + KCl.",
 "gas_post":{"pH":"7.25","PaCO2":"26","HCO3":"11","PaO2":"34","Na":"142","K":"3.4","Cl":"119","Albumin":"4.0","Glucose":"230","b-OHB":"0.6"},
 "steps_post":[("2. Internal validity","[H+] ~56 nmol/L - internally valid."),("3. pH","7.25 - improving."),
  ("4. Primary disorder","HCO3 11 -> metabolic acidosis."),
  ("5. Expected compensation","Winter's: PaCO2 = 1.5 x 11 + 8 = 24.5 +/-2. Actual 26 - appropriate."),
  ("6. Anion gap","AG = 142 - (119 + 11) = 12 (normal - HAGMA resolved)."),
  ("7. Delta ratio","(12 - 12)/(24 - 11) = 0 -> pure NAGMA."),
  ("9. SID / Stewart","SID = 142 - 119 = 23 (markedly low - chloride-driven). Unmeasured anions = 12 - 0.6 = 11.4 (normal). Mechanism changed: ketoacids cleared, chloride load now driving.")],
 "qs":["Calculate the corrected serum sodium.","What do the glucose and b-OHB values suggest?"],
 "ans":["Na+ + 1.6 x [(480 - 100)/100] ~138. True hyponatraemia is dilutional from hyperglycaemia.",
  "Hyperglycaemic ketosis driving the gap - severe DKA."],
 "qs_post":["Compare this ABG with the initial ABG. What has changed?",
  "Why is acidosis persisting despite improvement in glucose and b-OHB?",
  "Calculate the corrected serum sodium."],
 "ans_post":["pH improved (7.08->7.25); PaCO2 rose (14->26); HCO3 rose modestly (4->11); glucose fell (480->230); b-OHB fell (5.8->0.6); Na rose (132->142); K fell (4.5->3.4); Cl rose sharply (98->119); AG normalised (30->12). The acid has changed character.",
  "Ketoacidosis resolved. Persisting low HCO3 is now hyperchloraemic NAGMA from saline chloride load - expected, not treatment failure.",
  "142 + 1.6 x [(230 - 100)/100] ~144."],
 "pitfalls":["Calling this respiratory alkalosis from the low PaCO2 alone.",
  "Missing that the low PaO2 (venous sample) is itself a validity teaching point.",
  "Forgetting to correct the anion gap for albumin as a reflex step."],
 "synthesis":"Severe DKA, appropriately compensated, pure HAGMA. Plan: fluid resuscitation, insulin infusion with potassium replacement anticipated.",
 "take":"Recalculate the anion gap on every repeat gas - a persistently low HCO3 after treatment can mean the acid has changed character."})

CASES.append({"id":2,"title":"Pyloric stenosis",
 "vignette":"6-week-old first-born boy with 10 days of progressively forceful, non-bilious vomiting after every feed. Sunken eyes, lethargic but arousable, still hungry after vomiting.",
 "gas_in":{"pH":"7.52","PaCO2":"48","HCO3":"38","PaO2":"34","Na":"132","K":"3.0","Cl":"82","Albumin":"4.0","Glucose":"90","Urine Cl":"<15"},
 "steps_in":[("1. Clinical history","Classic for hypertrophic pyloric stenosis: forceful non-bilious vomiting after every feed, still hungry, with dehydration."),
  ("2. Internal validity","[H+] = 24 x 48 / 38 = 30 -> pH 7.52 - matches. PaO2 34 suggests venous."),
  ("3. pH","7.52 - alkalaemia."),("4. Primary disorder","HCO3 38 (raised) with alkalaemia -> metabolic alkalosis."),
  ("5. Expected compensation","PaCO2 = 0.7 x 38 + 21 = 47.6 +/-2 (45.6-49.6). Actual 48 - appropriate."),
  ("6. Anion gap","AG = 132 - (82 + 38) = 12 (normal)."),("7. Delta ratio","Not applicable - no HAGMA."),
  ("8. Oxygenation & integration","Hypochloraemic, hypokalaemic metabolic alkalosis with appropriate respiratory compensation; low urine Cl confirms chloride-responsive process.")],
 "sid_in":[("SID","132 - 82 = 50","Markedly high - chloride-loss alkalosis."),
  ("Atot","Albumin 4.0","Normal."),("Unmeasured anions","AG 12 - 0 = 12","Normal."),
  ("Mechanism","-","Loss of gastric HCl has removed chloride, raising SID.")],
 "intervention":"IV 0.9% saline + KCl, correct dehydration and hypokalaemia, then pyloromyotomy.",
 "gas_post":{"pH":"7.45","PaCO2":"40","HCO3":"27","Na":"138","K":"4.0","Cl":"100","Albumin":"4.0","Urine Cl":">20"},
 "steps_post":[("9. SID / Stewart","SID = 138 - 100 = 38 (normalising - chloride repletion working). Urine Cl now >20 confirms kidney no longer conserving chloride.")],
 "qs":["What is the significance of the low urine chloride?","What is the likely clinical diagnosis?"],
 "ans":["Urine Cl < 15-20 mmol/L confirms chloride-responsive metabolic alkalosis: kidney appropriately conserving chloride. Alkalosis will correct with chloride-rich fluid. Contrast with chloride-resistant causes (Bartter/Gitelman) where urine Cl is inappropriately high.",
  "Hypertrophic pyloric stenosis - persistent vomiting of gastric HCl and volume depletion produce hypochloraemic, hypokalaemic metabolic alkalosis; secondary hyperaldosteronism drives further renal H+ and K+ loss."],
 "pitfalls":["Trying to apply the delta ratio or AG framework to an alkalosis.",
  "Overlooking K 3.0 as an urgent, actionable finding."],
 "synthesis":"A textbook gas: use it to drill the metabolic-alkalosis compensation formula and the urine-chloride distinction.",
 "take":"A urine chloride confirms whether a metabolic alkalosis will respond to chloride repletion. SID tracks the response."})

CASES.append({"id":3,"title":"Gastroenteritis",
 "vignette":"8-month-old girl with 2 days of fever and large-volume loose stools. Sunken eyes, delayed skin turgor, prolonged capillary refill time.",
 "gas_in":{"pH":"7.22","PaCO2":"27","HCO3":"11","PaO2":"34","Na":"129","K":"3.2","Cl":"112","Albumin":"3.5","Glucose":"85","Lactate":"1"},
 "steps_in":[("1. Clinical history","Acute gastroenteritis with large-volume diarrhoea and significant dehydration."),
  ("2. Internal validity","[H+] = 24 x 27 / 11 = 59 -> pH 7.23 - matches. PaO2 34 suggests venous."),
  ("3. pH","7.22 - acidaemia."),("4. Primary disorder","HCO3 11 (low) -> metabolic acidosis."),
  ("5. Expected compensation","Winter's: PaCO2 = 1.5 x 11 + 8 = 24.5 +/-2 (22.5-26.5). Actual 27 is at upper edge - borderline compensation."),
  ("6. Anion gap","AG = 129 - (112 + 11) = 6 (low/normal). Corrected AG = 6 + 2.5 x (4 - 3.5) = 7.25 - still normal."),
  ("7. Delta ratio","Not applicable - no raised AG."),
  ("8. Oxygenation & integration","NAGMA (hyperchloraemic) from stool bicarbonate loss; normal lactate argues against hypoperfusion.")],
 "sid_in":[("SID","129 - 112 = 17","Markedly low - severe chloride-driven acidosis."),
  ("Atot","Albumin 3.5","Mildly low - slightly alkalinising."),
  ("Unmeasured anions","AG 6 - 1 = 5","Normal."),("Mechanism","-","Chloride-driven NAGMA.")],
 "intervention":"IV isotonic fluids, correct dehydration.",
 "gas_post":{"pH":"7.35","PaCO2":"36","HCO3":"20","Na":"135","K":"4.0","Cl":"105","Albumin":"3.5","Lactate":"1"},
 "steps_post":[("6. Anion gap","AG = 135 - (105 + 20) = 10 - normal."),
  ("9. SID / Stewart","SID = 135 - 105 = 30 (improving).")],
 "qs":["What is the likely cause of the metabolic acidosis in this child?",
  "How do the chloride and lactate values help you identify the mechanism?"],
 "ans":["Loss of bicarbonate-rich fluid in large-volume diarrhoea -> hyperchloraemic NAGMA.",
  "Chloride elevated (112) as it replaces lost bicarbonate; normal lactate (1) argues against significant hypoperfusion/shock."],
 "pitfalls":["Expecting a raised anion gap because the child is dehydrated.",
  "Not pairing with Case 4 as a contrast: correction reveals nothing hidden here."],
 "synthesis":"Pair explicitly with Case 4 - both have normal-looking raw AG and mild hypoalbuminaemia, but correction reveals nothing hidden here, whereas in Case 4 it unmasks a concealed HAGMA.",
 "take":"A normal-anion-gap acidosis with a normal lactate points to GI bicarbonate loss, not hypoperfusion. SID confirms the chloride-driven mechanism."})

CASES.append({"id":4,"title":"Suspected IEM",
 "vignette":"8-month-old girl with 1 day of fever and vomiting. Effortless tachypnoea, haemodynamically stable, lethargic. History of similar episodes in the past.",
 "gas_in":{"pH":"7.24","PaCO2":"38","HCO3":"16","PaO2":"38","Na":"135","K":"4","Cl":"107","Albumin":"2","Glucose":"85","Lactate":"3"},
 "steps_in":[("1. Clinical history","Short acute illness in an infant with history of similar prior episodes - recurrence is the key word."),
  ("2. Internal validity","[H+] = 24 x 38 / 16 = 57 -> pH 7.24 - matches."),
  ("3. pH","7.24 - acidaemia."),("4. Primary disorder","HCO3 16 (low) -> metabolic acidosis."),
  ("5. Expected compensation","Winter's: PaCO2 = 1.5 x 16 + 8 = 32 +/-2 (30-34). Actual 38 - higher than expected -> additional respiratory acidosis."),
  ("6. Anion gap","Raw AG = 135 - (107 + 16) = 12 (apparently normal). Albumin 2.0: corrected AG = 12 + 2.5 x (4 - 2) = 17 (clearly raised)."),
  ("7. Delta ratio","Using corrected AG: (17 - 12)/(24 - 16) = 5/8 = 0.625 -> mixed HAGMA + NAGMA."),
  ("8. Oxygenation & integration","Concealed HAGMA unmasked only after albumin correction, with inadequate respiratory compensation, in child with recurrent episodes -> suspect IEM.")],
 "sid_in":[("SID","135 - 107 = 28","Low - chloride-driven component."),
  ("Atot","Albumin 2.0","Markedly low - alkalinising, masking HAGMA."),
  ("Unmeasured anions","17 - 3 = 14","Raised."),
  ("Mechanism","-","Three forces: low SID, low Atot (masking), unmeasured anions.")],
 "intervention":"Critical sample, dextrose, stop protein.",
 "gas_post":{"pH":"7.35","PaCO2":"35","HCO3":"20","Na":"138","K":"4.2","Cl":"105","Albumin":"2.5","Glucose":"100","Lactate":"2"},
 "steps_post":[("9. SID / Stewart","SID = 138 - 105 = 33 (normalising). Atot still low (albumin 2.5) - still masking. Unmeasured anions = corrected AG (20 + 2.5x1.5 = 23.75) - 2 = 21.75 (still raised).")],
 "qs":["Calculate the albumin-corrected anion gap.","Is there an additional respiratory disorder?",
  "What is the significance of recurrent similar episodes in this clinical setting?"],
 "ans":["12 + 2.5 x (4.0 - 2.0) = 17 mEq/L. Raw gap of 12 looked normal; low albumin was masking a real HAGMA.",
  "Yes - Winter's predicts PaCO2 30-34; actual 38 is higher -> inadequate compensation (superimposed respiratory acidosis).",
  "Recurrent metabolic decompensation triggered by intercurrent illness raises strong suspicion for underlying IEM (organic acidaemia or fatty acid oxidation defect). Prompt metabolic work-up: ammonia, lactate, urine organic acids, plasma amino acids, acylcarnitine - the critical sample."],
 "pitfalls":["Stopping at AG 12, normal, without applying the albumin correction - the single most consequential miss in the whole case set.",
  "Treating lactate 3 as fully explaining the anion-gap elevation."],
 "synthesis":"Correct the anion gap for albumin as a reflex, every time, especially when the raw number looks reassuring. Here it changes the entire diagnostic direction.",
 "take":"Correct the anion gap for albumin as a reflex, every time - it is most consequential exactly when the raw number looks reassuring. Also check SID."})

CASES.append({"id":5,"title":"Salicylate poisoning",
 "vignette":"15-year-old boy with tinnitus, fast breathing, vomiting, and confusion after intentional ingestion.",
 "gas_in":{"pH":"7.42","PaCO2":"18","HCO3":"11","PaO2":"108","Na":"140","K":"4.2","Cl":"102","Albumin":"4.1","Glucose":"90","Lactate":"3.2"},
 "steps_in":[("1. Clinical history","Tinnitus, hyperventilation, vomiting, confusion after intentional ingestion in a teenager - tinnitus is the most specific clue."),
  ("2. Internal validity","[H+] = 24 x 18 / 11 = 39 -> pH 7.41 - matches 7.42. Plausible arterial sample."),
  ("3. pH","7.42 - essentially normal (the trap)."),
  ("4. Primary disorder","Two markedly abnormal primary values (PaCO2 18, HCO3 11) with near-normal pH - mixed disorder."),
  ("5. Expected compensation","If HCO3 11 were the only problem, Winter's predicts PaCO2 24.5 +/-2. Actual PaCO2 18 is far below that - separate primary respiratory alkalosis."),
  ("6. Anion gap","AG = 140 - (102 + 11) = 27 (markedly raised). Lactate only partly explains."),
  ("7. Delta ratio","(27 - 12)/(24 - 11) = 1.15 -> HAGMA."),
  ("8. Oxygenation & integration","Primary respiratory alkalosis + primary HAGMA, opposing pH effects cancelling to near-normal pH - classic salicylate poisoning.")],
 "sid_in":[("SID","140 - 102 = 38","High-normal - no chloride-driven component."),
  ("Atot","Albumin 4.1","Normal."),
  ("Unmeasured anions","27 - 3.2 = 23.8","Markedly raised - salicylate metabolites + ketones."),
  ("Mechanism","-","Unmeasured anions + primary respiratory alkalosis.")],
 "intervention":"Activated charcoal, IV fluids, sodium bicarbonate, alkalinise urine, consider dialysis.",
 "gas_post":{"pH":"7.48","PaCO2":"30","HCO3":"22","Na":"142","K":"3.8","Cl":"105","Albumin":"4.1","Lactate":"1.5"},
 "steps_post":[("9. SID / Stewart","SID = 142 - 105 = 37 (normal). Unmeasured anions = AG (142-105-22 = 15) - 1.5 = 13.5 (improving).")],
 "qs":["A near-normal pH can conceal a mixed disorder. What disorders are present here?",
  "What poisoning is suggested by the clinical history and ABG pattern?"],
 "ans":["Primary respiratory alkalosis (PaCO2 far lower than metabolic compensation alone would predict - direct salicylate stimulation of central respiratory centre) + primary HAGMA (AG 27, from lactate, ketosis, salicylate organic acids).",
  "Salicylate (aspirin) poisoning - classic triad of tinnitus, hyperventilation, and mixed respiratory-alkalosis/HAGMA pattern after intentional ingestion in an adolescent."],
 "pitfalls":["Seeing pH 7.42 and concluding the gas is essentially normal.",
  "Attributing low PaCO2 purely to appropriate compensation without checking against Winter's."],
 "synthesis":"This case exists to break the habit of reading the pH first and stopping. Always check PaCO2 and HCO3 against each other.",
 "take":"A near-normal pH never means a normal gas - check PaCO2 and HCO3 against each other before you trust it. SID helps distinguish chloride-driven from unmeasured-anion-driven acidosis."})

CASES.append({"id":6,"title":"Post-arrest hanging",
 "vignette":"5-year-old boy, 20 kg, accidental hanging. Post-arrest, ROSC after 15 min CPR, ventilated. PEEP 6, PIP 16, RR 20, I:E 1:2, FiO2 100%, TV 80 mL, MAP 17.",
 "gas_in":{"pH":"6.88","PaCO2":"65","HCO3":"12","PaO2":"70","Na":"138","K":"6.2","Cl":"98","Albumin":"4.1","Glucose":"210","Lactate":"3.2"},
 "steps_in":[("1. Clinical history","Post-cardiac-arrest after prolonged CPR for hanging - expect hypoxic-ischaemic metabolic acidosis and possible inadequate ventilation."),
  ("2. Internal validity","[H+] = 24 x 65 / 12 = 130 -> pH 6.89 - matches 6.88."),
  ("3. pH","6.88 - profound, life-threatening acidaemia."),
  ("4. Primary disorder","Both HCO3 12 and PaCO2 65 abnormal in acidifying direction - combined metabolic + respiratory acidosis."),
  ("5. Expected compensation","If pure metabolic, Winter's predicts PaCO2 26 +/-2. Actual 65 far above - large separate primary respiratory acidosis."),
  ("6. Anion gap","AG = 138 - (98 + 12) = 28 (markedly raised). Lactate 3.2 does not fully explain."),
  ("7. Delta ratio","(28 - 12)/(24 - 12) = 1.33 -> HAGMA component."),
  ("8. Oxygenation & integration","P/F = 70/1.0 = 70. OI = (17 x 1.0 x 100)/70 = 24.3. Severe ARDS (PALICC OI >=16).")],
 "sid_in":[("SID","138 - 98 = 40","High-normal - no chloride-driven component."),
  ("Atot","Albumin 4.1","Normal."),
  ("Unmeasured anions","28 - 3.2 = 24.8","Markedly raised - hypoxic-ischaemic anions."),
  ("Mechanism","-","Unmeasured anions + primary respiratory acidosis.")],
 "intervention":"Increase ventilation, treat hyperkalaemia, fluids, consider bicarbonate.",
 "gas_post":{"pH":"7.25","PaCO2":"40","HCO3":"17","PaO2":"90","Na":"138","K":"4.5","Cl":"100","Albumin":"4.1","Glucose":"180","Lactate":"2.5"},
 "steps_post":[("9. SID / Stewart","SID = 138 - 100 = 38 (normal). Unmeasured anions = AG (138-100-17 = 21) - 2.5 = 18.5 (still raised).")],
 "qs":["Identify all components of the mixed acid-base disorder.",
  "Calculate the P/F ratio and oxygenation index using the available data.",
  "How would you grade the severity of oxygenation failure?"],
 "ans":["(1) Primary metabolic acidosis (HCO3 12, AG 28 - hypoxic-ischaemic/lactic) and (2) primary respiratory acidosis (PaCO2 65, far exceeding expected ~26) - combined metabolic + respiratory acidosis.",
  "P/F = 70/1.0 = 70. OI = (17 x 1.0 x 100)/70 = 24.3.",
  "OI 24.3 = severe oxygenation failure (PALICC OI >=16 = severe)."],
 "pitfalls":["Assuming high PaCO2 is simply the ventilator not yet caught up without naming it as a second primary disorder.",
  "Not flagging K 6.2 as immediate actionable safety issue.",
  "Not noticing lactate 3.2 under-explains AG 28."],
 "synthesis":"Most acidotic gas in the set exists to force explicit separation of the two acidoses and bring in oxygenation indices.",
 "take":"When PaCO2 and HCO3 are both markedly abnormal in the same direction, name both disorders explicitly - one is not compensating for the other. SID confirms no chloride-driven component."})

CASES.append({"id":7,"title":"Septic shock + severe anaemia",
 "vignette":"4-year-old boy with septic shock and severe anaemia. FiO2 40%, SpO2 99%, ScvO2 42%.",
 "gas_in":{"pH":"7.25","PaCO2":"26","HCO3":"11","PaO2":"110","Na":"138","K":"4.3","Cl":"106","Albumin":"4.1","Hb":"4.5","Lactate":"7"},
 "steps_in":[("1. Clinical history","Septic shock with severe anaemia (Hb 4.5) - two independent reasons for impaired oxygen delivery."),
  ("2. Internal validity","[H+] = 24 x 26 / 11 = 57 -> pH 7.25 - matches."),
  ("3. pH","7.25 - acidaemia."),("4. Primary disorder","HCO3 11 (low) -> metabolic acidosis."),
  ("5. Expected compensation","Winter's: PaCO2 = 1.5 x 11 + 8 = 24.5 +/-2. Actual 26 - appropriate."),
  ("6. Anion gap","AG = 138 - (106 + 11) = 21 (raised). Albumin normal, negligible correction."),
  ("7. Delta ratio","(21 - 12)/(24 - 11) = 0.69 -> mixed HAGMA + NAGMA."),
  ("8. Oxygenation & integration","P/F = 110/0.4 = 275. ScvO2 42% - tissues extracting far more O2 than usual. CaO2 = (1.34 x 4.5 x 0.99) + (0.003 x 110) = 6.3 mL/dL.")],
 "sid_in":[("SID","138 - 106 = 32","Low - chloride-driven component from resuscitation fluids."),
  ("Atot","Albumin 4.1","Normal."),("Unmeasured anions","21 - 7 = 14","Raised - lactic acidosis."),
  ("Mechanism","-","Two forces: low SID + unmeasured anions.")],
 "intervention":"Blood transfusion, antibiotics, fluids, vasopressors.",
 "gas_post":{"pH":"7.35","PaCO2":"36","HCO3":"20","PaO2":"100","Na":"138","K":"4.0","Cl":"105","Albumin":"3.8","Hb":"9.0","Lactate":"2.5","ScvO2":"65%"},
 "steps_post":[("9. SID / Stewart","SID = 138 - 105 = 33 (low-normal). Unmeasured anions = AG (138-105-20 = 13) - 2.5 = 10.5 (normalising).")],
 "qs":["Calculate the P/F ratio.","How do you interpret the low ScvO2 despite a normal SpO2?",
  "What do the severe anaemia and elevated lactate indicate about oxygen delivery and extraction?"],
 "ans":["110 / 0.4 = 275 - mild oxygenation impairment; not where the problem lies.",
  "Large veno-arterial oxygen extraction gap: lungs saturating haemoglobin normally, but tissues extracting abnormally high fraction because overall DO2 inadequate relative to demand. SpO2 alone misses this.",
  "Severe anaemia critically reduces CaO2 and therefore DO2, even though saturation normal. Body compensates initially by increasing extraction (low ScvO2), but once exceeded, anaerobic metabolism follows - lactate 7. Content/delivery problem, not lung problem. Priority: transfusion."],
 "pitfalls":["Reassurance from normal SpO2/PaO2 without looking at ScvO2.",
  "Forgetting that severe anaemia is, by itself, full explanation for impaired oxygen delivery."],
 "synthesis":"Anchor on oxygen-delivery equation (DO2 = cardiac output x CaO2, and CaO2 driven mainly by Hb x SO2).",
 "take":"A normal SpO2 says nothing about oxygen delivery when haemoglobin is this low - look at ScvO2 and lactate, not the saturation monitor. SID reveals the chloride-driven component."})

CASES.append({"id":8,"title":"Methaemoglobinaemia",
 "vignette":"10-year-old boy with cyanosis, headache, tachycardia, and lethargy after receiving topical benzocaine. Blood sample drawn looks chocolate-brown. FiO2 90%, SpO2 85%, SO2 65%.",
 "gas_in":{"pH":"7.36","PaCO2":"38","HCO3":"21","PaO2":"550","Na":"138","K":"4.3","Cl":"105","Albumin":"4.1","MetHb":"35%","Lactate":"2"},
 "steps_in":[("1. Clinical history","Cyanosis, headache, tachycardia, lethargy after topical benzocaine, with chocolate-brown blood - close to diagnostic before numbers read."),
  ("2. Internal validity","[H+] = 24 x 38 / 21 = 43 -> pH 7.36 - matches. Essentially normal acid-base gas."),
  ("3. pH","7.36 - essentially normal."),
  ("4. Primary disorder","No significant primary acid-base disorder. Acid-base is distraction."),
  ("5. Expected compensation","Not applicable."),("6. Anion gap","AG = 138 - (105 + 21) = 12 (normal)."),
  ("7. Delta ratio","Not applicable."),
  ("8. Oxygenation & integration","P/F = 550/0.9 = 611 (remarkably high). Yet SpO2 85%, SO2 65% - large discordant saturation gap. MetHb 35% (normal <1-2%).")],
 "sid_in":[("SID","138 - 105 = 33","Low-normal - mild chloride-driven component."),
  ("Atot","Albumin 4.1","Normal."),("Unmeasured anions","12 - 2 = 10","Normal. Acid-base status benign."),
  ("Mechanism","-","Acid-base is not the story; oxygenation is.")],
 "intervention":"Methylene blue 1-2 mg/kg IV (check G6PD status first), oxygen, stop benzocaine.",
 "gas_post":{"pH":"7.38","PaCO2":"38","HCO3":"23","PaO2":"200","Na":"138","K":"4.0","Cl":"105","Albumin":"4.1","MetHb":"5%","Lactate":"1.5","SpO2":"98%","SO2":"95%"},
 "steps_post":[("9. SID / Stewart","SID = 138 - 105 = 33 (low-normal). Unmeasured anions = AG (138-105-23 = 10) - 1.5 = 8.5 (normal).")],
 "qs":["Calculate the P/F ratio.","How do you explain the discrepancy between the very high PaO2, SpO2, and SO2?",
  "What is the significance of the chocolate-brown blood and MetHb 35%?","What is the most likely diagnosis?"],
 "ans":["550 / 0.9 ~611.",
  "PaO2 measures dissolved oxygen tension and is unaffected by methaemoglobin, so remains high. Methaemoglobin (Fe3+, unable to bind oxygen) distorts pulse oximeter algorithm, driving SpO2 toward falsely fixed value ~82-85%. Directly measured SO2 by co-oximetry (65%) reflects true, much lower functional saturation - 35% of haemoglobin cannot carry oxygen at all.",
  "Chocolate-brown blood is classic bedside sign. MetHb 35% confirms severe elevation - enough to cause significant functional anaemia (only 65% of haemoglobin can carry oxygen). Explains cyanosis, headache, tachycardia, lethargy despite high PaO2.",
  "Acquired methaemoglobinaemia (benzocaine-induced)."],
 "pitfalls":["Getting drawn into acid-base analysis when the gas is essentially normal.",
  "Assuming a high PaO2 guarantees adequate oxygen delivery."],
 "synthesis":"Close with the rule this case exists to teach: a normal or high PaO2 does not guarantee normal oxygen-carrying capacity.",
 "take":"A high PaO2 does not guarantee oxygen-carrying capacity - whenever SpO2 and PaO2 disagree, request co-oximetry before you do anything else."})

CASES.append({"id":9,"title":"Two encephalopathic neonates",
 "vignette":"Baby A: 4 days old, fed well until day 2, now lethargic and tachypnoeic. Afebrile, clear chest. On antibiotics for sepsis. Baby B: 7 days old, vomiting, lethargic, deep rapid breathing. Platelets 60,000/uL, urine ketones 3+.",
 "gas_in":{"A pH":"7.51","A PaCO2":"26","A HCO3":"20","A SBE":"-1","A Na/Cl":"138/104","A Glucose":"85","A Lactate":"1.8","B pH":"7.14","B PaCO2":"18","B HCO3":"6","B SBE":"-21","B Na/Cl":"136/100","B Glucose":"45","B Lactate":"3.0"},
 "steps_in":[("1. Clinical history","A: fed well until day 2, now lethargic and tachypnoeic; sepsis label but afebrile, clear chest. B: vomiting, lethargic, deep rapid breathing, thrombocytopenia, ketonuria."),
  ("2. Internal validity","A: [H+] = 24 x 26 / 20 = 31 -> pH 7.51 - matches. B: [H+] = 24 x 18 / 6 = 72 -> pH 7.14 - matches."),
  ("3. pH","A: 7.51 - alkalaemia. B: 7.14 - acidaemia."),
  ("4. Primary disorder","A: PaCO2 26 (low) -> respiratory alkalosis. B: HCO3 6 (low) -> metabolic acidosis."),
  ("5. Expected compensation","A: acute resp alkalosis expected HCO3 ~21.2; actual 20 - appropriate. B: Winter's predicted PaCO2 17 +/-2; actual 18 - appropriate."),
  ("6. Anion gap","A: AG = 138 - (104 + 20) = 14 (normal). B: AG = 136 - (100 + 6) = 30 (markedly raised)."),
  ("7. Delta ratio","A: not applicable. B: (30 - 12)/(24 - 6) = 1.0 -> HAGMA."),
  ("8. Oxygenation & integration","A: sepsis alone does not explain respiratory alkalosis - suspect hyperammonaemia. B: lactate only 3.0 - rest of gap filled by ketones and organic acids.")],
 "sid_in":[("A SID","138 - 104 = 34","Low-normal."),
  ("A Unmeasured","14 - 1.8 = 12.2","Normal. Mechanism: respiratory alkalosis."),
  ("B SID","136 - 100 = 36","Normal."),
  ("B Unmeasured","30 - 3 = 27","Markedly raised - organic acids/ketones.")],
 "intervention":"Both: ammonia level, stop protein, dextrose. A: ammonia scavengers if high. B: carnitine, treat acidosis.",
 "gas_post":{"A pH":"7.45","A PaCO2":"35","A HCO3":"22","A Na/Cl":"138/105","A Glucose":"90","A Lactate":"1.5","B pH":"7.30","B PaCO2":"25","B HCO3":"12","B Na/Cl":"138/102","B Glucose":"100","B Lactate":"2.0"},
 "steps_post":[("9. SID / Stewart","A: SID = 138 - 105 = 33; unmeasured anions normal. B: SID = 138 - 102 = 36; unmeasured anions = AG (138-102-12 = 24) - 2 = 22 (still raised).")],
 "qs":["Name the primary disorder in each baby. Is compensation appropriate in each?",
  "Which features does sepsis alone fail to explain?",
  "Baby B has an anion gap of 30 but lactate is only 3. What fills the rest?",
  "Intervene: what one test do you send in both, how must the sample be handled, and what do you do while waiting?"],
 "ans":["A: respiratory alkalosis, appropriate. B: metabolic acidosis, appropriate.",
  "A: respiratory alkalosis without fever or distress. B: severe HAGMA with ketones and hypoglycaemia.",
  "Ketones (urine 3+) and organic acids from inborn error of metabolism.",
  "Ammonia. Sample on ice, delivered to lab within 15 minutes. While waiting: stop protein, give dextrose, prepare ammonia scavengers."],
 "pitfalls":["Attributing Baby A alkalosis to sepsis without considering hyperammonaemia.",
  "Not checking ammonia on ice for both babies.",
  "Assuming lactate explains Baby B AG when it only accounts for part."],
 "synthesis":"Both babies have a metabolic disorder masquerading as sepsis. The gas is the clue - ammonia on ice is the test.",
 "take":"Neonatal encephalopathy + abnormal gas = metabolic screen; ammonia on ice is critical. SID helps distinguish chloride-driven from unmeasured-anion-driven acidosis."})

CASES.append({"id":10,"title":"HUS-like",
 "vignette":"3-year-old, 5 days after bloody diarrhoea, now oliguric and pale. Hb 6.2 g/dL, platelets 40,000/uL, creatinine 3.8 mg/dL.",
 "gas_in":{"pH":"7.22","PaCO2":"25","HCO3":"10","SBE":"-16","Na":"131","K":"6.8","Cl":"104","Albumin":"3.0","Phosphate":"9.5","iCa":"0.92"},
 "steps_in":[("1. Clinical history","Bloody diarrhoea followed by oliguria and pallor, with anaemia, thrombocytopenia, and renal failure - HUS-like picture."),
  ("2. Internal validity","[H+] = 24 x 25 / 10 = 60 -> pH 7.22 - matches."),
  ("3. pH","7.22 - acidaemia."),("4. Primary disorder","HCO3 10 (low) -> metabolic acidosis."),
  ("5. Expected compensation","Winter's: PaCO2 = 1.5 x 10 + 8 = 23 +/-2. Actual 25 - appropriate."),
  ("6. Anion gap","AG = 131 - (104 + 10) = 17. Albumin-corrected AG = 17 + 2.5 x (4 - 3.0) = 19.5 (raised)."),
  ("7. Delta ratio","(17 - 12)/(24 - 10) = 5/14 = 0.36 -> mixed NAGMA + HAGMA."),
  ("8. Oxygenation & integration","Mixed acidosis; hyperkalaemia and hypocalcaemia are immediate threats.")],
 "sid_in":[("SID","131 - 104 = 27","Markedly low - chloride-driven."),
  ("Atot","Albumin 3.0 (alkalinising), phosphate 9.5 (markedly acidifying)","Net high Atot."),
  ("Unmeasured anions","19.5 - 0 = 19.5","Raised - urate, oxalate, retained organic anions."),
  ("Mechanism","-","Three forces: low SID + high Atot (phosphate) + unmeasured anions.")],
 "intervention":"Dialysis, treat hyperkalaemia and hypocalcaemia.",
 "gas_post":{"pH":"7.35","PaCO2":"35","HCO3":"18","Na":"135","K":"4.5","Cl":"105","Albumin":"3.2","Phosphate":"6.0","iCa":"1.0"},
 "steps_post":[("9. SID / Stewart","SID = 135 - 105 = 30 (improving). Atot: phosphate improved from 9.5 to 6.0. Unmeasured anions = AG (135-105-18 = 12) - 0 = 12 (normalising).")],
 "qs":["Is compensation appropriate? What are the anion gap and the albumin-corrected anion gap?",
  "Calculate the delta ratio. What does it tell you?",
  "Using SID and Atot, name the three separate forces acidifying this child.",
  "Intervene: which two sidekick values change your next 10 minutes? The team asks for bicarbonate - what do you say?"],
 "ans":["Appropriate. AG 17, corrected AG 19.5.","0.36 -> mixed NAGMA + HAGMA.",
  "Low SID (chloride-driven), high Atot (phosphate), unmeasured anions.",
  "K 6.8 (hyperkalaemia) and iCa 0.92 (hypocalcaemia). Bicarbonate? No - pH 7.22 not severe; bicarbonate can worsen hypocalcaemia and hyperkalaemia."],
 "pitfalls":["Missing that all three Stewart forces are active here.",
  "Not recognising K 6.8 and iCa 0.92 as immediate actionable threats.",
  "Reaching for bicarbonate without considering the risks."],
 "synthesis":"This is the triple-hit acidosis case. SID, Atot, and unmeasured anions each contribute. Treat the electrolytes first.",
 "take":"HUS = mixed acidosis; hyperkalaemia and hypocalcaemia are immediate threats. SID, Atot, and unmeasured anions each tell a different part of the story."})

CASES.append({"id":11,"title":"Hepatitis A encephalopathy",
 "vignette":"6-year-old with hepatitis A, grade II encephalopathy. INR 4.2, ammonia 180 umol/L.",
 "gas_in":{"pH":"7.49","PaCO2":"28","HCO3":"21","SBE":"-1","Na":"132","K":"3.0","Cl":"98","Albumin":"2.2","Lactate":"5.5","Glucose":"45"},
 "steps_in":[("1. Clinical history","Hepatitis A with grade II encephalopathy, coagulopathy, hyperammonaemia."),
  ("2. Internal validity","[H+] = 24 x 28 / 21 = 32 -> pH 7.49 - matches."),
  ("3. pH","7.49 - alkalaemia."),("4. Primary disorder","PaCO2 28 (low) -> respiratory alkalosis."),
  ("5. Expected compensation","Acute resp alkalosis: HCO3 falls ~2 per 10 mmHg fall in PaCO2. PaCO2 28 is 12 below 40 -> expected HCO3 ~21.6. Actual 21 - appropriate."),
  ("6. Anion gap","AG = 132 - (98 + 21) = 13. Corrected AG = 13 + 2.5 x (4 - 2.2) = 17.5 (HAGMA masked by hypoalbuminaemia)."),
  ("7. Delta ratio","Using corrected AG: (17.5 - 12)/(24 - 21) = 5.5/3 = 1.83 -> mixed."),
  ("8. Oxygenation & integration","Respiratory alkalosis + masked HAGMA + hypoglycaemia.")],
 "sid_in":[("SID","132 - 98 = 34","Low-normal."),
  ("Atot","Albumin 2.2","Markedly low - alkalinising, masking HAGMA."),
  ("Unmeasured anions","17.5 - 5.5 = 12","Raised."),
  ("Mechanism","-","Masked HAGMA + respiratory alkalosis.")],
 "intervention":"Dextrose, lactulose, ammonia scavengers.",
 "gas_post":{"pH":"7.42","PaCO2":"32","HCO3":"20","Na":"135","K":"3.5","Cl":"100","Albumin":"2.5","Lactate":"3.0","Glucose":"100"},
 "steps_post":[("9. SID / Stewart","SID = 135 - 100 = 35 (normal). Atot still low (albumin 2.5) - still masking. Unmeasured anions = corrected AG (15 + 3.75 = 18.75) - 3 = 15.75 (still raised).")],
 "qs":["What is the primary disorder, and why is this child alkaline?",
  "Calculate the anion gap, then correct it for albumin. What changes?",
  "The base excess is -1, which looks normal. Why is that misleading? How many processes are running at once?",
  "Intervene: which two sidekicks need treating in the next few minutes, and why does one of them worsen the encephalopathy?"],
 "ans":["Respiratory alkalosis due to hyperventilation from ammonia stimulating respiratory centre.",
  "AG 13, corrected AG 17.5. Low albumin was masking a HAGMA.",
  "Yes - because HAGMA is masked by hypoalbuminaemia. Multiple processes: respiratory alkalosis, HAGMA (lactic acidosis), hypoglycaemia.",
  "Glucose 45 (hypoglycaemia) and lactate 5.5 (lactic acidosis). Hypoglycaemia worsens encephalopathy."],
 "pitfalls":["Taking SBE -1 at face value without correcting AG for albumin.",
  "Missing that the low albumin is masking a HAGMA.","Not treating hypoglycaemia urgently."],
 "synthesis":"The SBE looks normal, but the low albumin is lying to you. Correct the AG, check SID, and treat the glucose.",
 "take":"Hepatitis A encephalopathy = respiratory alkalosis + HAGMA; check glucose. Always correct the AG for albumin, and check SID - the SBE may look normal while a HAGMA is masked."})

CASES.append({"id":12,"title":"Fasting hypoglycaemia",
 "vignette":"18-month-old, previously well, fasted overnight after gastroenteritis and presented with a seizure. Liver palpable 3 cm. ALT 180 U/L, ammonia 110 umol/L, free fatty acids raised.",
 "gas_in":{"Glucose":"30","pH":"7.36","PaCO2":"36","HCO3":"20","SBE":"-4","Na/Cl":"138/105","Lactate":"2.0","b-OHB":"0.3"},
 "steps_in":[("1. Clinical history","Fasting hypoglycaemia with seizure, hepatomegaly, raised ALT and ammonia, raised free fatty acids - key is the inappropriately low ketones."),
  ("2. Internal validity","[H+] = 24 x 36 / 20 = 43 -> pH 7.36 - matches."),
  ("3. pH","7.36 - normal."),
  ("4. Primary disorder","HCO3 20 (slightly low), SBE -4 -> mild metabolic acidosis."),
  ("5. Expected compensation","Not applicable (primary metabolic)."),
  ("6. Anion gap","AG = 138 - (105 + 20) = 13 (normal)."),
  ("7. Delta ratio","Not applicable (NAGMA)."),
  ("8. Oxygenation & integration","Near-normal gas but hypoglycaemia with low ketones -> failure of ketogenesis.")],
 "sid_in":[("SID","138 - 105 = 33","Low-normal - mild chloride-driven component."),
  ("Atot","Albumin not given","-"),("Unmeasured anions","13 - 2 = 11","Normal."),
  ("Mechanism","-","Acidosis mild and chloride-driven; the story is ketogenesis failure.")],
 "intervention":"Critical sample, then dextrose.",
 "gas_post":{"Glucose":"100","pH":"7.38","PaCO2":"38","HCO3":"22","SBE":"-1","Na/Cl":"138/105","Lactate":"1.5","b-OHB":"0.2"},
 "steps_post":[("9. SID / Stewart","SID = 138 - 105 = 33 (low-normal). Unmeasured anions = AG (138-105-22 = 11) - 1.5 = 9.5 (normal).")],
 "qs":["The gas looks almost normal. Why is that the most worrying finding?",
  "What should a fasting child gas and ketones look like?",
  "Free fatty acids are high but ketones are low. What does that mean? How would hyperinsulinism differ?",
  "Intervene: list the critical sample. When exactly must it be drawn, and what do you give immediately afterwards?"],
 "ans":["In a fasting child, expected ketosis and metabolic acidosis. Normal gas with low b-OHB (0.3) indicates failure of ketogenesis.",
  "Metabolic acidosis with high anion gap due to ketones.",
  "Block in fatty acid oxidation or ketogenesis (e.g., MCAD deficiency). Hyperinsulinism would have low FFA and low ketones.",
  "Must be drawn during hypoglycaemia before treatment. Includes glucose, insulin, C-peptide, cortisol, growth hormone, ketones, free fatty acids, acylcarnitine profile, ammonia, lactate, LFTs. Give dextrose (2-3 mL/kg of 10% dextrose) immediately after."],
 "pitfalls":["Being reassured by the near-normal gas and missing the hypoglycaemia with inappropriately low ketones.",
  "Drawing the critical sample after giving dextrose."],
 "synthesis":"The gas is a distraction. The diagnosis is in the glucose and ketones. Critical sample before dextrose.",
 "take":"Fasting hypoglycaemia with low ketones = think fatty acid oxidation defect; critical sample before treatment. SID confirms the acidosis was mild and chloride-driven, not the primary problem."})

CASES.append({"id":13,"title":"Shocked 2-week-old boy",
 "vignette":"2-week-old boy with 3 days of vomiting and poor feeding, now mottled and lethargic. Genitalia look normal. Weight below birth weight.",
 "gas_in":{"pH":"7.27","PaCO2":"28","HCO3":"12.5","SBE":"-13","Na":"122","K":"7.8","Cl":"98","Glucose":"40"},
 "steps_in":[("1. Clinical history","Neonatal shock with vomiting, poor feeding, mottling, lethargy, weight loss."),
  ("2. Internal validity","[H+] = 24 x 28 / 12.5 = 54 -> pH 7.27 - matches."),
  ("3. pH","7.27 - acidaemia."),("4. Primary disorder","HCO3 12.5 (low) -> metabolic acidosis."),
  ("5. Expected compensation","Winter's: PaCO2 = 1.5 x 12.5 + 8 = 26.75 +/-2. Actual 28 - appropriate."),
  ("6. Anion gap","AG = 122 - (98 + 12.5) = 11.5 (normal). NAGMA."),
  ("7. Delta ratio","Not applicable."),
  ("8. Oxygenation & integration","NAGMA with hyponatraemia, hyperkalaemia, hypoglycaemia -> CAH salt-wasting crisis.")],
 "sid_in":[("SID","122 - 98 = 24","Markedly low - chloride-driven acidosis."),
  ("Atot","Albumin not given","-"),("Unmeasured anions","11.5 - 0 = 11.5","Normal."),
  ("Mechanism","-","Chloride-driven NAGMA.")],
 "intervention":"Hydrocortisone, fluids with dextrose, treat hyperkalaemia.",
 "gas_post":{"pH":"7.35","PaCO2":"35","HCO3":"18","SBE":"-5","Na":"135","K":"5.0","Cl":"100","Glucose":"90"},
 "steps_post":[("9. SID / Stewart","SID = 135 - 100 = 35 (normalising). Unmeasured anions = AG (135-100-18 = 17) - 0 = 17 (raised - resolving).")],
 "qs":["Classify the acid-base disorder and check compensation. Is this a HAGMA or a NAGMA?",
  "Three sidekick values make the diagnosis before any specialised test. Which, and what is it?",
  "A vomiting 2-week-old with pyloric stenosis would show which gas instead?",
  "Intervene: what are your first three actions, and which sample must precede them?"],
 "ans":["NAGMA with appropriate compensation.",
  "Na 122 (hyponatraemia), K 7.8 (hyperkalaemia), glucose 40 (hypoglycaemia) -> CAH.",
  "Metabolic alkalosis (hypochloraemic, hypokalaemic).",
  "(1) IV access, draw critical sample (electrolytes, glucose, cortisol, ACTH, 17-OHP, renin, aldosterone). (2) Give stress-dose hydrocortisone. (3) IV fluids with dextrose and sodium (normal saline bolus, then D5NS; no potassium initially due to hyperkalaemia). Sample must precede hydrocortisone."],
 "pitfalls":["Not recognising the triad of hyponatraemia, hyperkalaemia, and hypoglycaemia as CAH.",
  "Giving hydrocortisone before drawing the critical sample.",
  "Giving potassium-containing fluids to a hyperkalaemic neonate."],
 "synthesis":"Neonatal shock + NAGMA + hyperkalaemia + hyponatraemia = CAH until proven otherwise. Draw the sample before steroids.",
 "take":"Neonatal shock + NAGMA + hyperkalaemia + hyponatraemia = CAH until proven otherwise. SID confirms the chloride-driven mechanism and tracks response to therapy."})


# Group -> Faculty facilitator allocation
GROUP_FACULTY = [
    ("1", "Manju",           3, "AGE (Gastroenteritis)"),
    ("2", "Shilpa",          6, "Hanging (Post-arrest)"),
    ("3", "Namitha",         9, "Encephalopathy (Two neonates)"),
    ("4", "Sivamurukan",     8, "Methaemoglobinaemia"),
    ("5", "Nikhil",          5, "Salicylate poisoning"),
    ("6", "Rohit",           7, "Septic shock + severe anaemia"),
    ("7", "Balachandar",     4, "Suspected IEM"),
    ("8", "Dipu / Sreedeep", 2, "Pyloric stenosis"),
]

def qblk(qs,ans=None,tq="Case-specific questions",ta="Answers"):
    r=[Paragraph(tq,ST["h3"])]
    for i,q in enumerate(qs,1): r.append(Paragraph("<b>"+str(i)+".</b> "+q,ST["b"]))
    if ans:
        r.append(Paragraph(ta,ST["h3"]))
        for i,a in enumerate(ans,1): r.append(Paragraph("<b>"+str(i)+".</b> "+a,ST["b"]))
    return r

TEN=[("1. Clinical history","What does the story alone suggest?"),
 ("2. Internal validity","[H+] = 24 x PaCO2 / HCO3- - does it match pH? Arterial?"),
 ("3. pH","Acidaemia, alkalaemia, or normal? A normal pH does not mean a normal gas."),
 ("4. Primary disorder","Does PaCO2 or HCO3- explain the pH direction?"),
 ("5. Expected compensation","Metabolic acidosis: PaCO2 = 1.5 x HCO3- + 8 +/-2. Metabolic alkalosis: PaCO2 = 0.7 x HCO3- + 21 +/-2."),
 ("6. Anion gap","Na+ - (Cl- + HCO3-); add 2.5 per 1 g/dL albumin below 4.0."),
 ("7. Delta ratio","(AG - 12)/(24 - HCO3-) - only if AG raised."),
 ("8. Oxygenation & integration","P/F, OI, CaO2, ScvO2, MetHb. Does the story fit the child?"),
 ("9. SID / Stewart analysis","SID = Na+ - Cl- (normal ~36). Low = chloride-driven acidosis. High = chloride-loss alkalosis. Atot = albumin + phosphate. Unmeasured anions = AG - (lactate + ketones)."),
 ("10. Post-intervention re-evaluation","Has the mechanism changed? Recalculate AG, SID, Atot.")]

def tensteps(): return stbl(TEN,hdr_=("Step","Tool / key question"))

def flow():
    d=[[Paragraph("Small Group - 8 min - Group faculty",ST["cb"]),
        Paragraph("Plenary - 7 min - Moderator",ST["cb"])],
       [Paragraph("0-3 min: Team interprets independently<br/>3-6 min: Faculty-mediated discussion<br/>6-8 min: Group synthesises answer",ST["c"]),
        Paragraph("0-3 min: Random draw - one group presents<br/>3-6 min: Case-specific Q and A plus post-intervention gas<br/>6-7 min: Take-home pearl",ST["c"])]]
    t=Table(d,colWidths=[85*mm,85*mm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),TEAL),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("BACKGROUND",(0,1),(-1,1),GREY_L),
        ("BOX",(0,0),(-1,-1),0.6,GREY_M),("INNERGRID",(0,0),(-1,-1),0.4,GREY_M),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return t

def build_q():
    p=OUT+"/1_Participant_Question_Booklet.pdf"
    d=doc(p,"Participant Question Booklet")
    s=hdr("PAEDIATRIC ACUTE CARE TEACHING","ABG Interpretation Workshop","Participant Question Booklet - 13 cases, 8 drawn live")
    s.append(Paragraph("How this session runs",ST["h1"]))
    s.append(Paragraph("You have all 13 cases in this booklet. Read them during the 8-minute settling period. Each case then runs as one 15-minute unit in two phases:",ST["b"]))
    s.append(flow())
    s.append(PageBreak())
    s.append(Paragraph("The Unified 10-Step Approach",ST["h1"]))
    s.append(tensteps())
    for c in CASES:
        s.append(PageBreak())
        s.append(Paragraph("Case "+str(c["id"]),ST["h1"]))
        s.append(Paragraph("<b>Vignette.</b> "+c["vignette"],ST["b"]))
        s.append(Paragraph("Initial gas",ST["h2"]))
        s.append(gas(c["gas_in"]))
        s.append(Spacer(1,8))
        s.append(Paragraph("Systematic interpretation",ST["h2"]))
        s.append(stbl([(a,"") for a,_ in c["steps_in"]],hdr_=("Step","Your answer")))
        s.append(Spacer(1,6))
        s.append(Paragraph("SID / Stewart analysis",ST["h2"]))
        s.append(sidt([(r[0],r[1],"") for r in c["sid_in"]]))
        s.append(Spacer(1,8))
        s+= qblk(c["qs"])
    d.build(s)
    print("OK",p)

def build_a():
    p=OUT+"/2_Participant_Answer_Booklet.pdf"
    d=doc(p,"Participant Answer Booklet")
    s=hdr("PAEDIATRIC ACUTE CARE TEACHING","ABG Interpretation Workshop","Participant Discussion and Answer Booklet - 13 cases, 8 drawn live")
    s.append(Paragraph("The Unified 10-Step Approach",ST["h1"]))
    s.append(tensteps())
    for c in CASES:
        s.append(PageBreak())
        s.append(Paragraph("Case "+str(c["id"])+" - "+c["title"],ST["h1"]))
        s.append(Paragraph("<b>Vignette.</b> "+c["vignette"],ST["b"]))
        s.append(Paragraph("Initial gas",ST["h2"]))
        s.append(gas(c["gas_in"]))
        s.append(Spacer(1,6))
        s.append(Paragraph("Systematic interpretation - answers",ST["h2"]))
        s.append(stbl(c["steps_in"]))
        s.append(Spacer(1,6))
        s.append(Paragraph("SID / Stewart - answers",ST["h2"]))
        s.append(sidt(c["sid_in"]))
        s.append(Spacer(1,8))
        s+= qblk(c["qs"],c["ans"])
        if c.get("gas_post"):
            s.append(Spacer(1,6))
            s.append(Paragraph("Post-intervention gas",ST["h2"]))
            s.append(Paragraph("<b>Intervention.</b> "+c["intervention"],ST["b"]))
            s.append(gas(c["gas_post"]))
            s.append(Spacer(1,6))
            s.append(Paragraph("Post-intervention interpretation",ST["h2"]))
            s.append(stbl(c["steps_post"]))
            if c.get("qs_post"): s+= qblk(c["qs_post"],c["ans_post"])
        s.append(Spacer(1,6))
        s.append(call("Take-home",c["take"]))
    d.build(s)
    print("OK",p)

def build_f():
    p=OUT+"/3_Faculty_Detailed_Guide.pdf"
    d=doc(p,"Faculty Detailed Guide")
    s=hdr("PAEDIATRIC ACUTE CARE TEACHING","ABG Interpretation Workshop","Faculty Detailed Guide")
    s.append(Paragraph("How this session runs",ST["h1"]))
    s.append(Paragraph("All 13 cases handed out. 8-minute settling period. Each case = 15-minute unit.",ST["b"]))
    s.append(flow())
    s.append(Spacer(1,6))
    s.append(Paragraph("<b>Timing discipline:</b> hold the 3-3-2 boundary. Resist answering in the first 3 minutes. If the group finishes early, ask a what-if variant.",ST["b"]))
    s.append(Paragraph("<b>Case 1 twist:</b> small-group phase works presenting gas only; moderator reveals the 14-hour repeat gas in plenary.",ST["b"]))

    s.append(Paragraph("Faculty allocation by group",ST["h1"]))
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
    s.append(fac_t)

    s.append(PageBreak())
    s.append(Paragraph("Quick Answer Index - all 13 cases",ST["h1"]))
    rows=[[Paragraph("#",ST["cl"]),Paragraph("Diagnosis",ST["cl"]),Paragraph("Moderator take-home",ST["cl"])]]
    for c in CASES:
        rows.append([Paragraph(str(c["id"]),ST["cb"]),Paragraph(c["title"],ST["c"]),Paragraph(c["take"],ST["c"])])
    t=Table(rows,colWidths=[10*mm,45*mm,115*mm],repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),TEAL),("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("BOX",(0,0),(-1,-1),0.6,GREY_M),("INNERGRID",(0,0),(-1,-1),0.4,GREY_M),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),3.5),
        ("BOTTOMPADDING",(0,0),(-1,-1),3.5)]))
    s.append(t)
    s.append(PageBreak())
    s.append(Paragraph("The Unified 10-Step Approach",ST["h1"]))
    s.append(tensteps())
    for c in CASES:
        s.append(PageBreak())
        s.append(Paragraph("Case "+str(c["id"])+" - "+c["title"],ST["h1"]))
        s.append(Paragraph("Small-group phase (8 min) - you run this",ST["h2"]))
        s.append(Paragraph("<b>Vignette.</b> "+c["vignette"],ST["b"]))
        s.append(Paragraph("Presenting gas",ST["h3"]))
        s.append(gas(c["gas_in"]))
        s.append(Paragraph("Worked interpretation",ST["h3"]))
        s.append(stbl(c["steps_in"]))
        s.append(Paragraph("SID / Stewart analysis",ST["h3"]))
        s.append(sidt(c["sid_in"]))
        s.append(Paragraph("Where groups go wrong",ST["h3"]))
        for pt in c["pitfalls"]: s.append(Paragraph("- "+pt,ST["bul"]))
        s.append(Spacer(1,4))
        s.append(call("Your synthesis (final 2 min)",c["synthesis"]))
        s.append(Paragraph("Plenary phase (7 min) - moderator runs this",ST["h2"]))
        s.append(Paragraph("Case-specific questions",ST["h3"]))
        for i,q in enumerate(c["qs"],1): s.append(Paragraph("<b>Q"+str(i)+".</b> "+q,ST["b"]))
        s.append(Paragraph("Answers",ST["h3"]))
        for i,a in enumerate(c["ans"],1): s.append(Paragraph("<b>A"+str(i)+".</b> "+a,ST["b"]))
        if c.get("gas_post"):
            s.append(Paragraph("Post-intervention reveal",ST["h3"]))
            s.append(Paragraph("<b>Intervention.</b> "+c["intervention"],ST["b"]))
            s.append(gas(c["gas_post"]))
            s.append(Spacer(1,4))
            s.append(stbl(c["steps_post"]))
            if c.get("qs_post"):
                s.append(Paragraph("Post-intervention case-specific answers",ST["h3"]))
                for i,q in enumerate(c["qs_post"],1): s.append(Paragraph("<b>Q"+str(i)+".</b> "+q,ST["b"]))
                for i,a in enumerate(c["ans_post"],1): s.append(Paragraph("<b>A"+str(i)+".</b> "+a,ST["b"]))
        s.append(Spacer(1,6))
        s.append(call("Moderator take-home (final 1 min)",c["take"]))
    d.build(s)
    print("OK",p)

def build_m():
    p=OUT+"/4_Moderator_Slide_Deck.pdf"
    from reportlab.lib.pagesizes import landscape as LS
    W=LS(A4)[0]-30*mm
    def foot_m(c,d):
        c.saveState()
        c.setFillColor(TEAL)
        c.rect(0,0,LS(A4)[0],3*mm,stroke=0,fill=1)
        c.setFont("Helvetica",7.5)
        c.setFillColor(GREY_T)
        c.drawString(15*mm,6*mm,"2nd JIPMER Paediatric Critical Care Meet - ABG Workshop")
        c.drawRightString(LS(A4)[0]-15*mm,6*mm,"Moderator Deck . Slide "+str(c.getPageNumber()))
        c.restoreState()
    d=BaseDocTemplate(p,pagesize=LS(A4),leftMargin=15*mm,rightMargin=15*mm,topMargin=15*mm,bottomMargin=20*mm)
    f=Frame(d.leftMargin,d.bottomMargin,d.width,d.height,id="m")
    d.addPageTemplates([PageTemplate(id="m",frames=[f],onPage=foot_m)])
    sl_h1=ParagraphStyle("slh1",fontName="Helvetica-Bold",fontSize=26,textColor=NAVY,leading=32,spaceAfter=4)
    sl_s=ParagraphStyle("sls",fontName="Helvetica",fontSize=12,textColor=GREY_T,leading=16,spaceAfter=14)
    sl_b=ParagraphStyle("slb",fontName="Helvetica",fontSize=11,textColor=NAVY,leading=15,spaceAfter=4)
    sl_h2=ParagraphStyle("slh2",fontName="Helvetica-Bold",fontSize=16,textColor=TEAL_D,leading=20,spaceBefore=4,spaceAfter=6)
    def slide(k,t,s_):
        return [Paragraph(k.upper(),ST["kick"]),Paragraph(t,sl_h1),Paragraph(s_,sl_s)]
    def block(t,bl,ac=TEAL):
        inner=[[Paragraph(t,sl_h2)]]+[[Paragraph(b,sl_b)] for b in bl]
        tb=Table(inner,colWidths=[250*mm])
        tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREY_L),
            ("LINEBEFORE",(0,0),(0,-1),4,ac),
            ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("VALIGN",(0,0),(-1,-1),"TOP")]))
        return tb
    s=[]
    s+=slide("Paediatric acute care teaching","ABG Interpretation Workshop","Moderator Slide Deck - 13 Cases")
    s.append(Paragraph("13 cases x 15 min = approx 3.25 hours  .  Or select 8 cases for 2 hours.",sl_b))
    s.append(PageBreak())
    s+=slide("How today runs","One case, 15 minutes, two phases","")
    s.append(block("Step 1 - All 13 cases handed out at once",["Every participant receives the full case booklet at once."]))
    s.append(Spacer(1,5))
    s.append(block("Step 2 - 8-minute settling period",["Participants may read ahead. Faculty do not teach yet."]))
    s.append(Spacer(1,5))
    s.append(block("Step 3 - Each case is one 15-minute unit",
        ["<b>Small group - 8 min:</b> 3 interpret, 3 discuss, 2 synthesise",
         "<b>Plenary - 7 min:</b> 3 random draw, 3 expert comment, 1 take-home"],ac=GOLD))
    s.append(PageBreak())
    s+=slide("The approach","The Unified 10-Step Method","")
    rows=[[Paragraph("Step",ST["cl"]),Paragraph("Tool / key question",ST["cl"])]]
    for a,b in TEN: rows.append([Paragraph(a,ST["cb"]),Paragraph(b,ST["c"])])
    t=Table(rows,colWidths=[55*mm,W-55*mm],repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),TEAL),("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("BOX",(0,0),(-1,-1),0.6,GREY_M),("INNERGRID",(0,0),(-1,-1),0.4,GREY_M),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    s.append(t)
    for c in CASES:
        s.append(PageBreak())
        s+=slide("Case "+str(c["id"])+" - "+c["title"],c["title"],"Small group - 8 min - Presenting gas")
        s.append(Paragraph(c["vignette"],sl_b))
        s.append(Spacer(1,6))
        s.append(gas(c["gas_in"],cw=30*mm,cpr=5))
        if c.get("gas_post"):
            s.append(Spacer(1,12))
            s.append(block("Plenary reveal - 7 min - Post-intervention gas",["<b>Intervention:</b> "+c["intervention"]]))
            s.append(Spacer(1,4))
            s.append(gas(c["gas_post"],cw=30*mm,cpr=5))
        s.append(PageBreak())
        s+=slide("Interpretation",c["title"],"Initial . SID . Post-intervention . Q and A")
        s.append(block("Initial interpretation",["<b>"+a+":</b> "+b for a,b in c["steps_in"][3:]]))
        s.append(Spacer(1,5))
        s.append(block("SID / Stewart",["<b>"+r[0]+":</b> "+r[1]+" - "+r[2] for r in c["sid_in"]],ac=TEAL_D))
        if c.get("steps_post"):
            s.append(Spacer(1,5))
            s.append(block("Post-intervention",["<b>"+a+":</b> "+b for a,b in c["steps_post"]],ac=GOLD))
        s.append(PageBreak())
        s+=slide("Case-specific Q and A",c["title"],"Expert comment . answers")
        for i,q in enumerate(c["qs"],1): s.append(Paragraph("<b>Q"+str(i)+".</b> "+q,sl_b))
        s.append(Spacer(1,6))
        for i,a in enumerate(c["ans"],1): s.append(Paragraph("<b>A"+str(i)+".</b> "+a,sl_b))
        if c.get("qs_post"):
            s.append(Spacer(1,6))
            s.append(block("Post-intervention case-specific answers",
                ["<b>Q"+str(i)+".</b> "+q for i,q in enumerate(c["qs_post"],1)]
                +["<b>A"+str(i)+".</b> "+a for i,a in enumerate(c["ans_post"],1)],ac=GOLD))
        s.append(Spacer(1,10))
        s.append(block("Take-home",[c["take"]],ac=GOLD))
    s.append(PageBreak())
    s+=slide("Close with the room","Two questions before the post-test","")
    s.append(block("For the whole room",
        ["1. Which case changed your mind about a value you thought you understood?",
         "2. Which correction step will you now do as a reflex, every single time - the albumin correction, the SID, or both?"],ac=GOLD))
    d.build(s)
    print("OK",p)


import json as _json
with open("cases.json","w",encoding="utf-8") as _f:
    _json.dump(CASES, _f, ensure_ascii=False, indent=2)
print("Wrote cases.json")

if __name__=="__main__":
    build_q()
    build_a()
    build_f()
    build_m()
    print()
    print("All 4 documents generated in:",os.path.abspath(OUT))
