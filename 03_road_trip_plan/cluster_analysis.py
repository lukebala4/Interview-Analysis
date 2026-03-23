"""
Task 2: Road Trip Cluster Analysis & Map
=========================================
Identifies optimal clusters for 2-week sales blitz.
Prioritizes hot lead density and deal quality over geographic optimization.
"""

import pandas as pd
import folium
import math
import json

print("Loading processed data...")
df = pd.read_csv("01_data_processing/processed_sites.csv")
targets = pd.read_csv("01_data_processing/top_targets.csv")
print(f"  → {len(df)} total sites, {len(targets)} FPO hot lead targets")

# ── Cluster Analysis ──────────────────────────────────────────────────────
print("\nAnalyzing clusters by metro area...")

# Define key metro areas with their approximate centers
METROS = {
    "Houston, TX": (29.7604, -95.3698),
    "Dallas/Fort Worth, TX": (32.7767, -96.7970),
    "San Antonio, TX": (29.4241, -98.4936),
    "Austin, TX": (30.2672, -97.7431),
    "Orlando/Lake Mary, FL": (28.5383, -81.3792),
    "Miami/South FL, FL": (25.7617, -80.1918),
    "Tampa/Ocala, FL": (28.0394, -82.4572),
    "Boston, MA": (42.3601, -71.0589),
    "Los Angeles, CA": (34.0522, -118.2437),
    "Sacramento, CA": (38.5816, -121.4944),
    "Raleigh/Durham, NC": (35.7796, -78.6382),
    "Chicago, IL": (41.8781, -87.6298),
    "Atlanta, GA": (33.7490, -84.3880),
    "Philadelphia, PA": (39.9526, -75.1652),
    "Nashville, TN": (36.1627, -86.7816),
}

def haversine_approx(lat1, lon1, lat2, lon2):
    """Approximate distance in miles between two points."""
    dlat = abs(lat1 - lat2)
    dlon = abs(lon1 - lon2)
    return ((dlat ** 2 + dlon ** 2) ** 0.5) * 69  # rough miles

# Assign each target to nearest metro
target_metros = {}
for _, row in targets.iterrows():
    if pd.isna(row["lat"]) or pd.isna(row["lng"]):
        continue
    min_dist = float("inf")
    nearest = "Other"
    for metro, (mlat, mlng) in METROS.items():
        d = haversine_approx(row["lat"], row["lng"], mlat, mlng)
        if d < min_dist:
            min_dist = d
            nearest = metro
    if min_dist > 150:  # More than 150 miles from any metro
        nearest = f"Other ({row['State']})"
    if nearest not in target_metros:
        target_metros[nearest] = []
    target_metros[nearest].append(row)

# Score each metro area
print("\n" + "="*70)
print("METRO AREA CLUSTER RANKINGS")
print("="*70)

metro_scores = []
for metro, sites in target_metros.items():
    site_count = len(sites)
    total_rev = sum(s["2024 Payments"] for s in sites)
    avg_score = sum(s["priority_score"] for s in sites) / max(site_count, 1)
    has_competitor = any(s.get("is_competitor_customer", False) for s in sites)

    # Composite metro score
    metro_score = (
        site_count * 10 +  # Each site worth 10
        (total_rev / 1_000_000) * 2 +  # Each $1M worth 2
        avg_score * 0.5 +  # Average priority score
        (50 if has_competitor else 0)  # Competitor customer bonus
    )

    metro_scores.append({
        "metro": metro,
        "site_count": site_count,
        "total_rev": total_rev,
        "avg_score": avg_score,
        "metro_score": metro_score,
        "has_competitor": has_competitor,
        "sites": sites,
    })

metro_scores.sort(key=lambda x: x["metro_score"], reverse=True)

for i, ms in enumerate(metro_scores[:15], 1):
    comp_tag = " [COMPETITOR CUSTOMER]" if ms["has_competitor"] else ""
    print(f"\n#{i} {ms['metro']}{comp_tag}")
    print(f"   Sites: {ms['site_count']} | Revenue: ${ms['total_rev']:,.0f} | "
          f"Avg Score: {ms['avg_score']:.0f} | Metro Score: {ms['metro_score']:.0f}")
    # Top 3 sites in this metro
    top = sorted(ms["sites"], key=lambda s: s["priority_score"], reverse=True)[:3]
    for s in top:
        print(f"   → ${s['2024 Payments']:>10,.0f} | {s['Site']:35s} | Score: {s['priority_score']:.0f}")

# ── Recommended Route ─────────────────────────────────────────────────────
print("\n" + "="*70)
print("RECOMMENDED 2-WEEK ROUTE")
print("="*70)

# Week 1: Texas
tx_metros = [ms for ms in metro_scores if "TX" in ms["metro"]]
tx_total_sites = sum(ms["site_count"] for ms in tx_metros)
tx_total_rev = sum(ms["total_rev"] for ms in tx_metros)
print(f"\nWEEK 1: TEXAS ({tx_total_sites} targets, ${tx_total_rev:,.0f})")
for ms in sorted(tx_metros, key=lambda x: x["metro_score"], reverse=True):
    print(f"  {ms['metro']}: {ms['site_count']} sites, ${ms['total_rev']:,.0f}")

# Week 2: Florida
fl_metros = [ms for ms in metro_scores if "FL" in ms["metro"]]
fl_total_sites = sum(ms["site_count"] for ms in fl_metros)
fl_total_rev = sum(ms["total_rev"] for ms in fl_metros)
print(f"\nWEEK 2: FLORIDA ({fl_total_sites} targets, ${fl_total_rev:,.0f})")
for ms in sorted(fl_metros, key=lambda x: x["metro_score"], reverse=True):
    print(f"  {ms['metro']}: {ms['site_count']} sites, ${ms['total_rev']:,.0f}")

# ── Create Road Trip Map ──────────────────────────────────────────────────
print("\nGenerating road trip map...")

m = folium.Map(
    location=[31.0, -90.0],
    zoom_start=5,
    tiles="CartoDB positron",
    width="100%",
    height="100%",
)

# Add all sites as faint background
for _, row in df.iterrows():
    if pd.isna(row["lat"]) or pd.isna(row["lng"]):
        continue
    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=1.5,
        color="#ddd",
        fill=True,
        fill_opacity=0.3,
        weight=0.5,
    ).add_to(m)

# Add target sites with detail
week1_group = folium.FeatureGroup(name="Week 1: Texas", show=True)
week2_group = folium.FeatureGroup(name="Week 2: Florida", show=True)
other_group = folium.FeatureGroup(name="Other Hot Lead Targets", show=True)

TA_COLORS = {
    "Oncology": "#e74c3c",
    "Infectious Disease": "#3498db",
    "Cardiology": "#e67e22",
    "Neurology": "#9b59b6",
    "Endocrinology": "#2ecc71",
    "Dermatology": "#f1c40f",
    "Ophthalmology": "#1abc9c",
    "Pulmonology": "#34495e",
}

for _, row in targets.iterrows():
    if pd.isna(row["lat"]) or pd.isna(row["lng"]):
        continue

    rev = row["2024 Payments"]
    ta = row.get("Top Therapeutic Area", "Unknown")
    color = TA_COLORS.get(ta, "#95a5a6")
    radius = max(4, min(18, math.log10(rev + 1) - 2))

    # Determine tier for border color
    score = row["priority_score"]
    if score >= 200:
        border_color = "#e74c3c"  # Red - top priority
        border_width = 4
    elif score >= 150:
        border_color = "#f39c12"  # Orange - high priority
        border_width = 3
    else:
        border_color = "#3498db"  # Blue - standard
        border_width = 2

    popup_html = f"""
    <div style="font-family: Arial; min-width: 220px;">
        <b style="font-size: 14px;">{row['Site']}</b><br>
        <b>Priority Score:</b> <span style="color: {border_color}; font-weight: bold;">{score:.0f}</span><br>
        <b>Revenue:</b> ${rev:,.0f}<br>
        <b>Tier:</b> {row['revenue_tier']}<br>
        <b>Area:</b> {ta}<br>
        <b>Location:</b> {row['City']}, {row['State']}<br>
        <b>Status:</b> {row['Profit Status']}<br>
        {f'<b>Parent Network:</b> {row["Parent"]}<br>' if pd.notna(row.get('Parent')) and row['Parent'] else ''}
        {'<span style="color: #ff6600; font-weight: bold;">⚡ COMPETITOR CUSTOMER</span><br>' if row.get('is_competitor_customer') else ''}
        {'<span style="color: #27ae60;">✓ Has Contact Info</span><br>' if row.get('has_contact_info') else ''}
    </div>
    """

    marker = folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=radius,
        popup=folium.Popup(popup_html, max_width=320),
        color=border_color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        weight=border_width,
    )

    state = row["State"]
    if state == "TX":
        week1_group.add_child(marker)
    elif state == "FL":
        week2_group.add_child(marker)
    else:
        other_group.add_child(marker)

m.add_child(week1_group)
m.add_child(week2_group)
m.add_child(other_group)

# Add route markers for key stops
route_stops = [
    ("Houston, TX", 29.7604, -95.3698, "Day 1-2: DM Clinical HQ + independents"),
    ("Dallas, TX", 32.7767, -96.7970, "Day 3-4: Pillar Clinical ($15.5M), ACRC Trials"),
    ("San Antonio, TX", 29.4241, -98.4936, "Day 5-6: Pinnacle Clinical Research"),
    ("Austin, TX", 30.2672, -97.7431, "Day 7: Hope Clinical, Zenos, Acclaim"),
    ("Lake Mary, FL", 28.7461, -81.3184, "Day 8-9: Alcanza HQ (23 sites, competitor!)"),
    ("Miami, FL", 25.7617, -80.1918, "Day 10-11: Innovation Medical, New Age, Well Pharma"),
    ("Tampa, FL", 27.9506, -82.4572, "Day 12-13: Renstar/Phasewell ($8.7M)"),
]

route_group = folium.FeatureGroup(name="Road Trip Route", show=True)
for i, (name, lat, lng, desc) in enumerate(route_stops, 1):
    folium.Marker(
        location=[lat, lng],
        popup=f"<b>Stop #{i}: {name}</b><br>{desc}",
        icon=folium.DivIcon(
            html=f'<div style="font-size: 16px; font-weight: bold; color: white; '
                 f'background: #e74c3c; border-radius: 50%; width: 28px; height: 28px; '
                 f'text-align: center; line-height: 28px; border: 2px solid white; '
                 f'box-shadow: 0 2px 4px rgba(0,0,0,0.3);">{i}</div>',
            icon_size=(28, 28),
            icon_anchor=(14, 14),
        ),
    ).add_to(route_group)

# Draw route lines
route_coords = [(lat, lng) for _, lat, lng, _ in route_stops]
# TX leg
folium.PolyLine(
    route_coords[:4], color="#e74c3c", weight=3, opacity=0.7,
    dash_array="10 5", popup="Week 1: Texas"
).add_to(route_group)
# FL leg
folium.PolyLine(
    route_coords[4:], color="#3498db", weight=3, opacity=0.7,
    dash_array="10 5", popup="Week 2: Florida"
).add_to(route_group)
# TX→FL transition
folium.PolyLine(
    [route_coords[3], route_coords[4]], color="#95a5a6", weight=2, opacity=0.5,
    dash_array="5 10", popup="Flight: Austin → Orlando"
).add_to(route_group)

m.add_child(route_group)

# Add legend
legend_html = """
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    z-index: 1000;
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    font-family: Arial;
    font-size: 12px;
    max-width: 250px;
">
    <b style="font-size: 14px;">Road Trip — Target Map</b><br><br>
    <b>Border Color = Priority</b><br>
    <span style="color:#e74c3c;">◉</span> Score 200+ (Top Priority)<br>
    <span style="color:#f39c12;">◉</span> Score 150-199 (High)<br>
    <span style="color:#3498db;">◉</span> Score <150 (Standard)<br>
    <hr style="margin: 5px 0;">
    <b>Fill Color = Therapeutic Area</b><br>
    <span style="color:#e74c3c;">●</span> Oncology
    <span style="color:#3498db;">●</span> Infectious Disease<br>
    <span style="color:#e67e22;">●</span> Cardiology
    <span style="color:#9b59b6;">●</span> Neurology<br>
    <span style="color:#2ecc71;">●</span> Endocrinology
    <span style="color:#f1c40f;">●</span> Dermatology<br>
    <hr style="margin: 5px 0;">
    <b>Size</b> = Revenue (log scale)<br>
    <span style="color:#e74c3c;">━━</span> Week 1: Texas<br>
    <span style="color:#3498db;">━━</span> Week 2: Florida
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Title
title_html = """
<div style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    background: white;
    padding: 10px 25px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    font-family: Arial;
">
    <h3 style="margin: 0;">2-Week Sales Blitz — Network-First Road Trip</h3>
    <p style="margin: 2px 0 0 0; font-size: 12px; color: #666;">
        Week 1: Texas (DM Clinical HQ + independents) | Week 2: Florida (Alcanza HQ + independents)
    </p>
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

folium.LayerControl(collapsed=False).add_to(m)

output_path = "03_road_trip_plan/road_trip_map.html"
m.save(output_path)
print(f"\n✓ Road trip map saved to {output_path}")
