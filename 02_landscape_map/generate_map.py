"""
Task 1: US Clinical Trial Sites Landscape Map
=============================================
Creates an interactive HTML map of all 4,551 clinical trial sites,
sized by revenue, colored by therapeutic area, with hot lead highlighting.
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import math
import json

print("Loading processed data...")
df = pd.read_csv("01_data_processing/processed_sites.csv")
print(f"  → {len(df)} sites loaded")

# ── Color mapping for therapeutic areas ────────────────────────────────────
TA_COLORS = {
    "Oncology": "#e74c3c",          # Red
    "Infectious Disease": "#3498db", # Blue
    "Cardiology": "#e67e22",         # Orange
    "Neurology": "#9b59b6",          # Purple
    "Endocrinology": "#2ecc71",      # Green
    "Dermatology": "#f1c40f",        # Yellow
    "Ophthalmology": "#1abc9c",      # Teal
    "Pulmonology": "#34495e",        # Dark gray
}
DEFAULT_COLOR = "#95a5a6"  # Light gray for other areas

def get_color(ta):
    return TA_COLORS.get(ta, DEFAULT_COLOR)

# ── Create base map ───────────────────────────────────────────────────────
print("Creating map...")
m = folium.Map(
    location=[39.8283, -98.5795],  # Center of US
    zoom_start=4,
    tiles="CartoDB positron",
    width="100%",
    height="100%",
)

# ── Add all sites as circle markers ───────────────────────────────────────
# Use feature groups for layer control
all_sites_group = folium.FeatureGroup(name="All Sites (4,551)", show=True)
hot_leads_group = folium.FeatureGroup(name="Hot Leads (268)", show=True)
tier1_group = folium.FeatureGroup(name="Tier 1: $5M+ Revenue", show=False)
competitor_group = folium.FeatureGroup(name="Competitor Customers", show=False)

print("Adding site markers...")
for _, row in df.iterrows():
    if pd.isna(row["lat"]) or pd.isna(row["lng"]):
        continue

    rev = row["2024 Payments"]
    ta = row.get("Top Therapeutic Area", "Unknown")
    color = get_color(ta)

    # Scale radius by revenue (log scale)
    if rev > 0:
        radius = max(2, min(15, math.log10(rev + 1) - 3))
    else:
        radius = 2

    # Popup content
    popup_html = f"""
    <div style="font-family: Arial; min-width: 200px;">
        <b style="font-size: 14px;">{row['Site']}</b><br>
        <span style="color: {color};">●</span> {ta}<br>
        <b>Revenue:</b> ${rev:,.0f}<br>
        <b>City:</b> {row['City']}, {row['State']}<br>
        <b>PI:</b> {row.get('PI Name', 'N/A')}<br>
        <b>Status:</b> {row['Profit Status']}<br>
        {'<span style="color: #e74c3c; font-weight: bold;">★ HOT LEAD</span><br>' if row.get('is_hot_lead') else ''}
        {'<span style="color: #f39c12; font-weight: bold;">⚡ COMPETITOR CUSTOMER</span><br>' if row.get('is_competitor_customer') else ''}
        {'<span style="color: #27ae60; font-weight: bold;">✓ EXISTING CUSTOMER</span><br>' if row.get('is_existing_customer') else ''}
        {f'<b>Parent:</b> {row["Parent"]}<br>' if pd.notna(row.get('Parent')) and row['Parent'] else ''}
        {f'<b>Score:</b> {row.get("priority_score", 0):.0f}' if row.get('is_hot_lead') else ''}
    </div>
    """

    # Determine which groups to add to
    opacity = 0.3 if not row.get("is_hot_lead") else 0.8
    weight = 1 if not row.get("is_hot_lead") else 2

    marker = folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=radius,
        popup=folium.Popup(popup_html, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=opacity,
        weight=weight,
    )
    all_sites_group.add_child(marker)

    # Hot leads get a second, highlighted marker
    if row.get("is_hot_lead"):
        hot_marker = folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=radius + 3,
            popup=folium.Popup(popup_html, max_width=300),
            color="#e74c3c",
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            weight=3,
        )
        hot_leads_group.add_child(hot_marker)

    # Tier 1 sites
    if rev >= 5_000_000:
        tier1_marker = folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=radius + 2,
            popup=folium.Popup(popup_html, max_width=300),
            color="#f39c12",
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            weight=2,
        )
        tier1_group.add_child(tier1_marker)

    # Competitor customers
    if row.get("is_competitor_customer"):
        comp_marker = folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=radius + 4,
            popup=folium.Popup(popup_html, max_width=300),
            color="#ff6600",
            fill=True,
            fill_color="#ff6600",
            fill_opacity=0.9,
            weight=3,
        )
        competitor_group.add_child(comp_marker)

m.add_child(all_sites_group)
m.add_child(hot_leads_group)
m.add_child(tier1_group)
m.add_child(competitor_group)

# ── Add legend ────────────────────────────────────────────────────────────
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
    max-width: 220px;
">
    <b style="font-size: 14px;">Therapeutic Areas</b><br>
"""
for ta, color in TA_COLORS.items():
    legend_html += f'<span style="color:{color};">●</span> {ta}<br>'
legend_html += f'<span style="color:{DEFAULT_COLOR};">●</span> Other<br>'
legend_html += """
    <hr style="margin: 5px 0;">
    <b>Markers</b><br>
    <span style="color:#e74c3c;">◉</span> Hot Lead (red border)<br>
    <span style="color:#f39c12;">◉</span> Tier 1 $5M+ (gold border)<br>
    <span style="color:#ff6600;">◉</span> Competitor Customer<br>
    <hr style="margin: 5px 0;">
    <b>Size</b> = Revenue (log scale)<br>
    <b>Opacity</b> = Hot lead status
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ── Add title ─────────────────────────────────────────────────────────────
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
    <h3 style="margin: 0;">US Clinical Trial Sites — Delfa AI GTM Landscape</h3>
    <p style="margin: 2px 0 0 0; font-size: 12px; color: #666;">
        4,551 sites | 268 hot leads | Colored by therapeutic area | Sized by 2024 revenue
    </p>
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

# Add layer control
folium.LayerControl(collapsed=False).add_to(m)

# ── Save ──────────────────────────────────────────────────────────────────
output_path = "02_landscape_map/us_clinical_sites_map.html"
m.save(output_path)
print(f"\n✓ Map saved to {output_path}")
print(f"  Open in browser to explore interactively.")
