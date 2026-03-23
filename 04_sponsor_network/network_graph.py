"""
Bonus: Sponsor-Site Network Map
================================
Extracts sponsor information from protocol IDs, builds a network graph
showing sponsor-site-therapeutic area relationships.
"""

import pandas as pd
import re
import json
from collections import defaultdict

print("Loading processed data...")
df = pd.read_csv("01_data_processing/processed_sites.csv")

# ── Protocol ID → Sponsor Mapping ─────────────────────────────────────────
# Protocol IDs encode sponsor information in their prefixes
SPONSOR_PATTERNS = {
    r"^mRNA": "Moderna",
    r"^BNT": "BioNTech/Pfizer",
    r"^C4591": "Pfizer",
    r"^PF-": "Pfizer",
    r"^B7451": "Pfizer",
    r"^CABL|^CAIN|^CLCZ|^CSOM|^CFTY|^CRDX|^CINC": "Novartis",
    r"^MK-|^V114|^V503": "Merck",
    r"^CNTO|^56021|^JNJ|^VAC": "Johnson & Johnson",
    r"^M[0-9]{2}-": "AbbVie",
    r"^WA[0-9]|^GA[0-9]|^BO[0-9]|^GR[0-9]|^YO[0-9]|^CO[0-9]{4}": "Roche/Genentech",
    r"^D[0-9]{4}C": "AstraZeneca",
    r"^ALTO|^AMG": "Amgen",
    r"^GSK|^2044": "GSK",
    r"^BAY": "Bayer",
    r"^EMR": "Merck KGaA/EMD Serono",
    r"^LY[0-9]|^I[0-9]{1}[A-Z]": "Eli Lilly",
    r"^HZNP|^HZN": "Horizon Therapeutics",
    r"^GS-": "Gilead",
    r"^ABT|^M14": "AbbVie",
    r"^AP[0-9]": "Astellas",
    r"^CC-|^BMS": "Bristol-Myers Squibb",
    r"^SDY": "Syndax",
    r"^AV-|^AVA": "Avacopan/ChemoCentryx",
    r"^INCB": "Incyte",
    r"^BWI": "Boston Scientific",
    r"^GN[0-9]": "Genentech",
    r"^IRB": "Institutional (IRB)",
    r"^RAF|^RVT": "Various Cardiovascular",
    r"^EFC|^LPS": "Sanofi",
    r"^CLIN": "Various",
}

def identify_sponsor(protocol):
    """Attempt to identify sponsor from protocol ID."""
    if not protocol or pd.isna(protocol):
        return "Unknown"
    protocol = str(protocol).strip()
    for pattern, sponsor in SPONSOR_PATTERNS.items():
        if re.match(pattern, protocol, re.IGNORECASE):
            return sponsor
    return "Unknown"

df["Sponsor"] = df["Top Protocol"].apply(identify_sponsor)

# ── Analyze sponsor distribution ──────────────────────────────────────────
sponsor_counts = df[df["Sponsor"] != "Unknown"].groupby("Sponsor").agg(
    site_count=("Site", "count"),
    total_revenue=("2024 Payments", "sum"),
    top_ta=("Top Therapeutic Area", lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "Mixed"),
    states=("State", lambda x: len(set(x))),
).sort_values("site_count", ascending=False)

print("\n" + "="*60)
print("SPONSOR DISTRIBUTION (Identified)")
print("="*60)
for sponsor, row in sponsor_counts.head(20).iterrows():
    print(f"  {sponsor:30s} | {int(row['site_count']):4d} sites | "
          f"${row['total_revenue']:>12,.0f} | Top: {row['top_ta']} | {int(row['states'])} states")

identified = (df["Sponsor"] != "Unknown").sum()
print(f"\nIdentified: {identified}/{len(df)} ({identified/len(df)*100:.0f}%)")
print(f"Unknown: {len(df) - identified}")

# ── Build Network Graph HTML ──────────────────────────────────────────────
print("\nBuilding network graph...")

# Focus on top sponsors and their connections to hot lead sites
top_sponsors = sponsor_counts.head(12).index.tolist()

# Build edges: Sponsor → Therapeutic Area → Sites (for hot leads only)
hot_df = df[df["is_hot_lead"] & (df["Sponsor"].isin(top_sponsors))].copy()

# Also include top non-hot-lead sites for context
top_sites_df = df[
    (df["Sponsor"].isin(top_sponsors)) &
    (df["2024 Payments"] >= 5_000_000)
].head(100)

network_df = pd.concat([hot_df, top_sites_df]).drop_duplicates(subset=["Site", "City"])

# Build the HTML visualization using D3.js-style force graph
nodes = []
edges = []
node_set = set()

# Add sponsor nodes
for sponsor in top_sponsors:
    sponsor_data = sponsor_counts.loc[sponsor]
    nodes.append({
        "id": f"sponsor_{sponsor}",
        "label": sponsor,
        "type": "sponsor",
        "size": min(40, max(15, int(sponsor_data["site_count"] / 10) + 15)),
        "color": "#e74c3c",
    })
    node_set.add(f"sponsor_{sponsor}")

# Add therapeutic area nodes
ta_set = set()
for _, row in network_df.iterrows():
    ta = row.get("Top Therapeutic Area", "Unknown")
    if ta and ta not in ta_set and pd.notna(ta):
        ta_set.add(ta)

TA_COLORS_NET = {
    "Oncology": "#e74c3c",
    "Infectious Disease": "#3498db",
    "Cardiology": "#e67e22",
    "Neurology": "#9b59b6",
    "Endocrinology": "#2ecc71",
    "Dermatology": "#f1c40f",
    "Ophthalmology": "#1abc9c",
    "Pulmonology": "#34495e",
    "Rheumatology": "#c0392b",
    "Psychiatry": "#8e44ad",
    "Gastroenterology": "#d35400",
    "Hepatology": "#16a085",
}

for ta in ta_set:
    nodes.append({
        "id": f"ta_{ta}",
        "label": ta,
        "type": "therapeutic_area",
        "size": 20,
        "color": TA_COLORS_NET.get(ta, "#95a5a6"),
    })
    node_set.add(f"ta_{ta}")

# Add site nodes (limit to top 60 for readability)
sites_to_show = network_df.nlargest(60, "2024 Payments")
for _, row in sites_to_show.iterrows():
    site_id = f"site_{row['Site']}_{row['City']}"
    if site_id not in node_set:
        import math
        rev = row["2024 Payments"]
        size = max(5, min(25, int(math.log10(rev + 1)) - 2))
        nodes.append({
            "id": site_id,
            "label": f"{row['Site']} ({row['State']})",
            "type": "site",
            "size": size,
            "color": "#3498db" if not row.get("is_hot_lead") else "#27ae60",
            "revenue": f"${rev:,.0f}",
            "hot_lead": bool(row.get("is_hot_lead", False)),
        })
        node_set.add(site_id)

        # Edge: Sponsor → Site
        sponsor = row["Sponsor"]
        sponsor_id = f"sponsor_{sponsor}"
        if sponsor_id in node_set:
            edges.append({
                "source": sponsor_id,
                "target": site_id,
                "type": "funds",
            })

        # Edge: Site → Therapeutic Area
        ta = row.get("Top Therapeutic Area")
        ta_id = f"ta_{ta}"
        if ta_id in node_set:
            edges.append({
                "source": site_id,
                "target": ta_id,
                "type": "specializes",
            })

# Also add sponsor → TA edges for the overall relationship
for sponsor in top_sponsors:
    sponsor_sites = df[df["Sponsor"] == sponsor]
    top_ta = sponsor_sites["Top Therapeutic Area"].value_counts().head(2)
    for ta, count in top_ta.items():
        ta_id = f"ta_{ta}"
        if ta_id in node_set:
            edges.append({
                "source": f"sponsor_{sponsor}",
                "target": ta_id,
                "type": "therapeutic_focus",
                "weight": int(count),
            })

# ── Generate HTML with embedded vis.js ────────────────────────────────────
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Sponsor-Site Network — Delfa AI GTM Analysis</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; }}
        #network {{ width: 100vw; height: 100vh; }}
        #title {{
            position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
            z-index: 1000; background: white; padding: 10px 25px;
            border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }}
        #legend {{
            position: fixed; bottom: 30px; left: 30px; z-index: 1000;
            background: white; padding: 15px; border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3); font-size: 12px; max-width: 220px;
        }}
        #info {{
            position: fixed; top: 80px; right: 20px; z-index: 1000;
            background: white; padding: 15px; border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3); font-size: 12px;
            max-width: 300px; display: none;
        }}
    </style>
</head>
<body>
    <div id="title">
        <h3 style="margin: 0;">Sponsor–Site Network Map</h3>
        <p style="margin: 2px 0 0 0; font-size: 12px; color: #666;">
            {len(top_sponsors)} sponsors | {len(sites_to_show)} sites | {len(ta_set)} therapeutic areas
        </p>
    </div>
    <div id="legend">
        <b>Node Types</b><br>
        <span style="color:#e74c3c;">⬤</span> Sponsor (pharma company)<br>
        <span style="color:#27ae60;">⬤</span> Hot Lead Site<br>
        <span style="color:#3498db;">⬤</span> Other High-Revenue Site<br>
        <span style="color:#95a5a6;">⬤</span> Therapeutic Area<br>
        <hr style="margin: 5px 0;">
        <b>Size</b> = Revenue (sites) / Site count (sponsors)<br>
        <b>Edges</b> = Sponsor funds site / Site specializes in area<br>
        <hr style="margin: 5px 0;">
        <em>Click any node for details. Drag to rearrange.</em>
    </div>
    <div id="info"></div>
    <div id="network"></div>

    <script>
        var nodesData = {json.dumps(nodes)};
        var edgesData = {json.dumps(edges)};

        var visNodes = nodesData.map(function(n) {{
            var shape = n.type === 'sponsor' ? 'diamond' :
                        n.type === 'therapeutic_area' ? 'triangle' : 'dot';
            return {{
                id: n.id,
                label: n.label,
                size: n.size,
                color: {{
                    background: n.color,
                    border: n.type === 'sponsor' ? '#c0392b' :
                            n.hot_lead ? '#27ae60' : '#2980b9',
                    highlight: {{ background: '#f39c12', border: '#e67e22' }}
                }},
                shape: shape,
                font: {{
                    size: n.type === 'sponsor' ? 14 : n.type === 'therapeutic_area' ? 12 : 9,
                    color: '#333',
                    strokeWidth: 2,
                    strokeColor: '#fff'
                }},
                title: n.label + (n.revenue ? ' | ' + n.revenue : ''),
                borderWidth: n.hot_lead ? 3 : 1,
            }};
        }});

        var visEdges = edgesData.map(function(e, i) {{
            return {{
                from: e.source,
                to: e.target,
                color: {{
                    color: e.type === 'funds' ? '#e74c3c' :
                           e.type === 'therapeutic_focus' ? '#f39c12' : '#bdc3c7',
                    opacity: 0.4
                }},
                width: e.weight ? Math.min(e.weight / 20, 3) : 1,
                smooth: {{ type: 'continuous' }},
            }};
        }});

        var container = document.getElementById('network');
        var data = {{
            nodes: new vis.DataSet(visNodes),
            edges: new vis.DataSet(visEdges)
        }};
        var options = {{
            physics: {{
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {{
                    gravitationalConstant: -100,
                    centralGravity: 0.01,
                    springLength: 150,
                    springConstant: 0.02,
                    damping: 0.5,
                }},
                stabilization: {{ iterations: 200 }},
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 100,
            }},
        }};
        var network = new vis.Network(container, data, options);

        network.on('click', function(params) {{
            var infoDiv = document.getElementById('info');
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = nodesData.find(function(n) {{ return n.id === nodeId; }});
                if (node) {{
                    var html = '<b>' + node.label + '</b><br>Type: ' + node.type;
                    if (node.revenue) html += '<br>Revenue: ' + node.revenue;
                    if (node.hot_lead) html += '<br><span style="color:#27ae60;font-weight:bold;">★ Hot Lead</span>';
                    infoDiv.innerHTML = html;
                    infoDiv.style.display = 'block';
                }}
            }} else {{
                infoDiv.style.display = 'none';
            }}
        }});
    </script>
</body>
</html>"""

output_path = "04_sponsor_network/sponsor_site_network.html"
with open(output_path, "w") as f:
    f.write(html_content)

print(f"\n✓ Network graph saved to {output_path}")
print(f"  Nodes: {len(nodes)} | Edges: {len(edges)}")
print(f"  Sponsors identified: {len(top_sponsors)}")
print(f"  Therapeutic areas: {len(ta_set)}")

# ── Key Findings ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("KEY NETWORK FINDINGS")
print("="*60)

print("\nTop Sponsor-TA Connections:")
sponsor_ta = df[df["Sponsor"] != "Unknown"].groupby(["Sponsor", "Top Therapeutic Area"]).size()
sponsor_ta = sponsor_ta.reset_index(name="count").sort_values("count", ascending=False)
for _, row in sponsor_ta.head(15).iterrows():
    print(f"  {row['Sponsor']:25s} → {row['Top Therapeutic Area']:25s} ({int(row['count'])} sites)")

print("\nSponsors active with hot lead sites:")
hot_sponsors = df[df["is_hot_lead"] & (df["Sponsor"] != "Unknown")].groupby("Sponsor").agg(
    sites=("Site", "count"),
    revenue=("2024 Payments", "sum"),
).sort_values("revenue", ascending=False)
for sponsor, row in hot_sponsors.head(10).iterrows():
    print(f"  {sponsor:25s} | {int(row['sites']):3d} hot lead sites | ${row['revenue']:>12,.0f}")
