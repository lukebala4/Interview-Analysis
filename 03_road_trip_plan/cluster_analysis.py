"""
Task 2: Road Trip Cluster Analysis & Map (Lightweight)
======================================================
Identifies optimal clusters, generates a lightweight interactive map.
"""

import pandas as pd
import json
import math

print("Loading processed data...")
df = pd.read_csv("01_data_processing/processed_sites.csv")
targets = pd.read_csv("01_data_processing/top_targets.csv")
df = df[df["lat"].notna() & df["lng"].notna()].copy()
targets = targets[targets["lat"].notna() & targets["lng"].notna()].copy()
print(f"  → {len(df)} total sites, {len(targets)} FPO hot lead targets")

# ── Build JSON for all sites (background) — minimal fields ────────────────
bg_json = []
for _, r in df.iterrows():
    bg_json.append([round(r["lat"], 4), round(r["lng"], 4)])

# ── Build JSON for targets — full fields ──────────────────────────────────
targets_json = []
for _, r in targets.iterrows():
    targets_json.append({
        "n": r["Site"],
        "la": round(r["lat"], 4),
        "ln": round(r["lng"], 4),
        "r": round(r["2024 Payments"]),
        "t": r.get("Top Therapeutic Area", "") or "",
        "c": r["City"],
        "s": r["State"],
        "sc": int(r.get("priority_score", 0)),
        "cc": int(r.get("is_competitor_customer", 0)),
        "ci": int(r.get("has_contact_info", 0)),
        "pa": r.get("Parent", "") if pd.notna(r.get("Parent")) else "",
        "rt": r.get("revenue_tier", ""),
    })

bg_str = json.dumps(bg_json, separators=(",", ":"))
tgt_str = json.dumps(targets_json, separators=(",", ":"))
print(f"  → Background: {len(bg_str)/1024:.0f} KB | Targets: {len(tgt_str)/1024:.0f} KB")

# ── Route stops ───────────────────────────────────────────────────────────
route_stops = [
    {"name": "Houston, TX", "lat": 29.7604, "lng": -95.3698,
     "desc": "Day 1-2: DM Clinical HQ (20 sites, $79M) + Juno Research ($3.7M)", "week": 1},
    {"name": "Dallas/Richardson, TX", "lat": 32.7767, "lng": -96.7970,
     "desc": "Day 3-4: Pillar Clinical ($15.5M) + ACRC Trials ($2.6M)", "week": 1},
    {"name": "San Antonio, TX", "lat": 29.4241, "lng": -98.4936,
     "desc": "Day 5-6: Pinnacle Clinical ($2.8M) + SMS Clinical ($3.7M)", "week": 1},
    {"name": "Austin, TX", "lat": 30.2672, "lng": -97.7431,
     "desc": "Day 7: Hope Clinical ($2.5M) + Zenos ($1.8M) + Acclaim ($1M)", "week": 1},
    {"name": "Lake Mary/Orlando, FL", "lat": 28.7461, "lng": -81.3184,
     "desc": "Day 8-9: Alcanza HQ (23 sites, $45M, Alleviate competitor!) + Complete Health ($7M)", "week": 2},
    {"name": "Miami, FL", "lat": 25.7617, "lng": -80.1918,
     "desc": "Day 10-11: Innovation Medical ($3M) + Well Pharma ($2.3M)", "week": 2},
    {"name": "Tampa/Ocala, FL", "lat": 28.0394, "lng": -82.4572,
     "desc": "Day 12-13: Renstar/Phasewell ($8.7M, 2 sites) + Accel ($3.2M)", "week": 2},
]
route_str = json.dumps(route_stops, separators=(",", ":"))

html = f"""<!DOCTYPE html>
<html>
<head>
<title>2-Week Sales Blitz — Road Trip Plan</title>
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
  border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.3);font-size:11px;max-width:220px}}
.dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px}}
#route-info{{position:fixed;top:80px;right:20px;z-index:1000;background:#fff;padding:12px;
  border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.3);font-size:11px;max-width:280px;max-height:70vh;overflow-y:auto}}
#controls{{position:fixed;bottom:20px;right:20px;z-index:1000;background:#fff;padding:10px;
  border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,.3);font-size:11px}}
</style>
</head>
<body>
<div id="title">
  <h3>2-Week Sales Blitz — Network-First Road Trip</h3>
  <p>Week 1: Texas (53 targets, $118M) → Week 2: Florida (41 targets, $47M)</p>
</div>
<div id="route-info">
  <b style="font-size:13px">Route Stops</b>
  <div id="stops"></div>
</div>
<div id="legend">
  <b>Priority Score</b><br>
  <span class="dot" style="background:#e74c3c"></span>200+ Top priority<br>
  <span class="dot" style="background:#f39c12"></span>150-199 High<br>
  <span class="dot" style="background:#3498db"></span>&lt;150 Standard<br>
  <hr style="margin:5px 0">
  <b>Fill = Therapeutic Area</b><br>
  <span class="dot" style="background:#e74c3c"></span>Oncology
  <span class="dot" style="background:#3498db"></span>Infect. Disease<br>
  <span class="dot" style="background:#e67e22"></span>Cardiology
  <span class="dot" style="background:#9b59b6"></span>Neurology<br>
  <span class="dot" style="background:#2ecc71"></span>Endocrinology
  <span class="dot" style="background:#f1c40f"></span>Dermatology<br>
  <hr style="margin:5px 0">
  <span style="color:#e74c3c">━━</span> Week 1: Texas<br>
  <span style="color:#3498db">━━</span> Week 2: Florida
</div>
<div id="controls">
  <label><input type="checkbox" id="showBg" checked onchange="toggleBg()"> Show all US sites</label>
</div>
<div id="map"></div>
<script>
var BG={bg_str};
var TGT={tgt_str};
var ROUTE={route_str};
var TC={{"Oncology":"#e74c3c","Infectious Disease":"#3498db","Cardiology":"#e67e22",
  "Neurology":"#9b59b6","Endocrinology":"#2ecc71","Dermatology":"#f1c40f",
  "Ophthalmology":"#1abc9c","Pulmonology":"#34495e"}};

var map=L.map("map").setView([31,-90],5);
L.tileLayer("https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}@2x.png",{{
  attribution:'&copy; OpenStreetMap &copy; CARTO',maxZoom:18
}}).addTo(map);

// Background sites
var bgLayer=L.layerGroup();
BG.forEach(function(b){{
  L.circleMarker([b[0],b[1]],{{radius:1.5,color:"#ddd",fillColor:"#ddd",fillOpacity:0.3,weight:0.5}}).addTo(bgLayer);
}});
bgLayer.addTo(map);

function toggleBg(){{
  if(document.getElementById("showBg").checked)bgLayer.addTo(map);
  else map.removeLayer(bgLayer);
}}

function fmt(n){{return"$"+n.toLocaleString()}}

// Target sites
TGT.forEach(function(d){{
  var col=TC[d.t]||"#bdc3c7";
  var rad=d.r>0?Math.max(4,Math.min(16,Math.log10(d.r+1)-2)):4;
  var border=d.sc>=200?"#e74c3c":d.sc>=150?"#f39c12":"#3498db";
  var bw=d.sc>=200?4:d.sc>=150?3:2;
  if(d.cc){{border="#ff6600";bw=4;rad+=2}}
  var m=L.circleMarker([d.la,d.ln],{{
    radius:rad,color:border,fillColor:col,fillOpacity:0.8,weight:bw
  }});
  var pop="<div style='font-family:Arial;min-width:200px'>"
    +"<b>"+d.n+"</b><br>"
    +"<b>Score:</b> <span style='color:"+border+";font-weight:bold'>"+d.sc+"</span><br>"
    +"<b>Payments:</b> "+fmt(d.r)+" ("+d.rt+")<br>"
    +"<b>Area:</b> "+d.t+"<br>"
    +"<b>Location:</b> "+d.c+", "+d.s+"<br>"
    +(d.pa?"<b>Network:</b> "+d.pa+"<br>":"")
    +(d.cc?"<span style='color:#ff6600;font-weight:bold'>⚡ COMPETITOR CUSTOMER</span><br>":"")
    +(d.ci?"<span style='color:#27ae60'>✓ Has contact info</span><br>":"")
    +"</div>";
  m.bindPopup(pop);
  m.addTo(map);
}});

// Route stops
var stopsHtml="";
var w1=[],w2=[];
ROUTE.forEach(function(s,i){{
  var icon=L.divIcon({{
    html:'<div style="font-size:15px;font-weight:bold;color:#fff;background:'+(s.week===1?'#e74c3c':'#3498db')
      +';border-radius:50%;width:26px;height:26px;text-align:center;line-height:26px;border:2px solid #fff;'
      +'box-shadow:0 2px 4px rgba(0,0,0,.3)">'+(i+1)+'</div>',
    iconSize:[26,26],iconAnchor:[13,13]
  }});
  L.marker([s.lat,s.lng],{{icon:icon}}).bindPopup("<b>Stop #"+(i+1)+": "+s.name+"</b><br>"+s.desc).addTo(map);
  if(s.week===1)w1.push([s.lat,s.lng]);
  else w2.push([s.lat,s.lng]);
  var col=s.week===1?"#e74c3c":"#3498db";
  stopsHtml+='<div style="margin:6px 0;padding:6px;background:#f9f9f9;border-left:3px solid '+col+';border-radius:4px">'
    +'<b style="color:'+col+'">#'+(i+1)+' '+s.name+'</b><br>'
    +'<span style="font-size:10px">'+s.desc+'</span></div>';
}});
document.getElementById("stops").innerHTML=stopsHtml;

// Route lines
if(w1.length>1)L.polyline(w1,{{color:"#e74c3c",weight:3,opacity:0.7,dashArray:"10 5"}}).addTo(map);
if(w2.length>1)L.polyline(w2,{{color:"#3498db",weight:3,opacity:0.7,dashArray:"10 5"}}).addTo(map);
// TX→FL transition
if(w1.length&&w2.length)L.polyline([w1[w1.length-1],w2[0]],{{color:"#999",weight:2,opacity:0.4,dashArray:"5 10"}}).addTo(map);
</script>
</body>
</html>"""

with open("03_road_trip_plan/road_trip_map.html", "w") as f:
    f.write(html)

size = len(html) / 1024
print(f"\n✓ Road trip map saved: {size:.0f} KB")
