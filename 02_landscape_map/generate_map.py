"""
Task 1: US Clinical Trial Sites Landscape Map (Lightweight)
============================================================
Generates a self-contained HTML map under 1MB using Leaflet CDN
and client-side rendering from embedded JSON data.
"""

import pandas as pd
import json
import math

print("Loading processed data...")
df = pd.read_csv("01_data_processing/processed_sites.csv")
df = df[df["lat"].notna() & df["lng"].notna()].copy()
print(f"  → {len(df)} geocoded sites")

# Build compact JSON data for client-side rendering
sites_json = []
for _, r in df.iterrows():
    sites_json.append({
        "n": r["Site"],
        "la": round(r["lat"], 4),
        "ln": round(r["lng"], 4),
        "r": round(r["2024 Payments"]),
        "t": r.get("Top Therapeutic Area", "") or "",
        "c": r["City"],
        "s": r["State"],
        "p": r["Profit Status"],
        "h": int(r.get("is_hot_lead", 0)),
        "cc": int(r.get("is_competitor_customer", 0)),
        "ec": int(r.get("is_existing_customer", 0)),
        "sc": int(r.get("priority_score", 0)),
        "pa": r.get("Parent", "") if pd.notna(r.get("Parent")) else "",
    })

data_str = json.dumps(sites_json, separators=(",", ":"))
print(f"  → JSON data: {len(data_str)/1024:.0f} KB")

html = f"""<!DOCTYPE html>
<html>
<head>
<title>US Clinical Trial Sites — Delfa AI GTM Landscape</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
body{{margin:0;font-family:Arial,sans-serif}}
#map{{width:100vw;height:100vh}}
#title{{position:fixed;top:10px;left:50%;transform:translateX(-50%);z-index:1000;
  background:#fff;padding:10px 20px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.3);text-align:center}}
#title h3{{margin:0;font-size:16px}}
#title p{{margin:2px 0 0;font-size:11px;color:#666}}
#legend{{position:fixed;bottom:20px;left:20px;z-index:1000;background:#fff;padding:12px;
  border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.3);font-size:11px;max-width:200px}}
#legend b{{font-size:12px}}
.dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px}}
#controls{{position:fixed;top:80px;right:20px;z-index:1000;background:#fff;padding:12px;
  border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.3);font-size:12px}}
#controls label{{display:block;margin:3px 0;cursor:pointer}}
#stats{{position:fixed;bottom:20px;right:20px;z-index:1000;background:#fff;padding:10px;
  border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.3);font-size:11px}}
</style>
</head>
<body>
<div id="title">
  <h3>US Clinical Trial Sites — Delfa AI GTM Landscape</h3>
  <p>4,505 sites | 268 hot leads | Colored by therapeutic area | Sized by 2024 sponsor payments</p>
</div>
<div id="controls">
  <b>Show:</b>
  <label><input type="checkbox" id="showAll" checked onchange="render()"> All sites (faint)</label>
  <label><input type="checkbox" id="showHot" checked onchange="render()"> Hot leads (bold)</label>
  <label><input type="checkbox" id="showComp" checked onchange="render()"> Competitor customers</label>
  <label><input type="checkbox" id="showT1" onchange="render()"> Tier 1 only ($5M+)</label>
</div>
<div id="legend">
  <b>Therapeutic Areas</b><br>
  <span class="dot" style="background:#e74c3c"></span>Oncology<br>
  <span class="dot" style="background:#3498db"></span>Infectious Disease<br>
  <span class="dot" style="background:#e67e22"></span>Cardiology<br>
  <span class="dot" style="background:#9b59b6"></span>Neurology<br>
  <span class="dot" style="background:#2ecc71"></span>Endocrinology<br>
  <span class="dot" style="background:#f1c40f"></span>Dermatology<br>
  <span class="dot" style="background:#1abc9c"></span>Ophthalmology<br>
  <span class="dot" style="background:#34495e"></span>Pulmonology<br>
  <span class="dot" style="background:#bdc3c7"></span>Other<br>
  <hr style="margin:5px 0">
  <b>Size</b> = Payment volume (log)<br>
  <b>Bold border</b> = Hot lead<br>
  <span class="dot" style="background:#ff6600"></span>Competitor customer
</div>
<div id="stats"></div>
<div id="map"></div>
<script>
var DATA={data_str};
var TC={{
  "Oncology":"#e74c3c","Infectious Disease":"#3498db","Cardiology":"#e67e22",
  "Neurology":"#9b59b6","Endocrinology":"#2ecc71","Dermatology":"#f1c40f",
  "Ophthalmology":"#1abc9c","Pulmonology":"#34495e"
}};
var map=L.map("map").setView([39.8,-98.6],4);
L.tileLayer("https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}@2x.png",{{
  attribution:'&copy; OpenStreetMap &copy; CARTO',maxZoom:18
}}).addTo(map);
var layers=[];
function fmt(n){{return"$"+n.toLocaleString()}}
function render(){{
  layers.forEach(function(l){{map.removeLayer(l)}});
  layers=[];
  var sa=document.getElementById("showAll").checked;
  var sh=document.getElementById("showHot").checked;
  var sc=document.getElementById("showComp").checked;
  var st=document.getElementById("showT1").checked;
  var shown=0,hotShown=0,rev=0;
  DATA.forEach(function(d){{
    var isHot=d.h===1,isComp=d.cc===1;
    var show=false;
    if(st&&d.r<5000000)return;
    if(sa&&!isHot&&!isComp)show=true;
    if(sh&&isHot)show=true;
    if(sc&&isComp)show=true;
    if(!sa&&!sh&&!sc)show=true;
    if(!show)return;
    shown++;rev+=d.r;
    if(isHot)hotShown++;
    var col=TC[d.t]||"#bdc3c7";
    var rad=d.r>0?Math.max(2,Math.min(12,Math.log10(d.r+1)-3)):2;
    var opacity=isHot?0.8:0.25;
    var weight=isHot?2.5:0.5;
    var border=isComp?"#ff6600":isHot?"#c0392b":col;
    if(isComp){{rad+=3;opacity=0.9;weight=3}}
    var m=L.circleMarker([d.la,d.ln],{{
      radius:rad,color:border,fillColor:col,fillOpacity:opacity,weight:weight
    }});
    var pop="<div style='font-family:Arial;min-width:180px'>"
      +"<b>"+d.n+"</b><br>"
      +"<span style='color:"+col+"'>●</span> "+d.t+"<br>"
      +"<b>Payments:</b> "+fmt(d.r)+"<br>"
      +"<b>Location:</b> "+d.c+", "+d.s+"<br>"
      +"<b>Status:</b> "+d.p+"<br>"
      +(d.pa?"<b>Parent:</b> "+d.pa+"<br>":"")
      +(isHot?"<span style='color:#e74c3c;font-weight:bold'>★ HOT LEAD (Score: "+d.sc+")</span><br>":"")
      +(isComp?"<span style='color:#ff6600;font-weight:bold'>⚡ COMPETITOR CUSTOMER</span><br>":"")
      +(d.ec?"<span style='color:#27ae60;font-weight:bold'>✓ EXISTING CUSTOMER</span><br>":"")
      +"</div>";
    m.bindPopup(pop);
    m.addTo(map);
    layers.push(m);
  }});
  document.getElementById("stats").innerHTML="<b>Showing:</b> "+shown+" sites | "+hotShown+" hot leads<br><b>Total payments:</b> "+fmt(rev);
}}
render();
</script>
</body>
</html>"""

with open("02_landscape_map/us_clinical_sites_map.html", "w") as f:
    f.write(html)

size = len(html) / 1024
print(f"\n✓ Map saved: {size:.0f} KB")
