"""
Data Processing Pipeline for Delfa AI GTM Strategy
===================================================
Merges Dataset A (all US clinical trial sites) with Dataset B (hot leads),
geocodes via zip codes, scores sites for road trip prioritization.
"""

import pandas as pd
import openpyxl
import re
import pgeocode

# ── Load Dataset A (CSV - All US Clinical Trial Sites) ─────────────────────
print("Loading Dataset A (CSV)...")
df = pd.read_csv("data/Delfa_Pull_202512221346.csv")
df.columns = df.columns.str.strip()
df["2024 Payments"] = pd.to_numeric(df["2024 Payments"], errors="coerce").fillna(0)
print(f"  → {len(df)} sites loaded")

# ── Load Dataset B (Excel - Hot Leads) ─────────────────────────────────────
print("Loading Dataset B (Excel)...")
wb = openpyxl.load_workbook("data/Example Prospect List (1).xlsx", data_only=True)

# CRIO Main Set = hot leads
hot_lead_names = set()
ws = wb["CRIO Main Set"]
for row in ws.iter_rows(values_only=True):
    if row[0] and row[0] != "Client":
        hot_lead_names.add(row[0].strip())
print(f"  → {len(hot_lead_names)} hot leads")

# Delfa existing customers
delfa_customers = set()
ws2 = wb["Delfa Customers"]
for row in ws2.iter_rows(values_only=True):
    if row[0] and row[0] != "Current Customers":
        delfa_customers.add(row[0].strip())
print(f"  → {len(delfa_customers)} existing Delfa customers")

# Competitor customers
competitor_customers = {}
ws3 = wb["Competition Cusomters"]
for row in ws3.iter_rows(values_only=True):
    if row[0] and row[0] != "Competition" and row[1]:
        competitor_customers[row[1].strip().lower()] = row[0].strip()
print(f"  → {len(competitor_customers)} competitor customers")

# Clay Outreach - companies with enriched contact data
clay_companies = set()
ws4 = wb["Clay Outreach"]
for row in ws4.iter_rows(values_only=True):
    if row[0] and row[0] != "Company Table Data":
        clay_companies.add(row[0].strip().lower())
print(f"  → {len(clay_companies)} companies with Clay contact data")

# ── Normalize names for matching ───────────────────────────────────────────
def normalize(s):
    if not s or (isinstance(s, float) and pd.isna(s)):
        return ""
    return re.sub(r"[^a-z0-9]", "", str(s).lower())

hot_lead_normalized = {normalize(n): n for n in hot_lead_names}
delfa_normalized = {normalize(n) for n in delfa_customers}
competitor_normalized = {normalize(k): v for k, v in competitor_customers.items()}

# ── Match sites to hot leads / customers / competitors ─────────────────────
print("\nMatching sites to hot leads...")

def check_match(site_name, parent_name, lookup_dict):
    site_key = normalize(site_name)
    parent_key = normalize(parent_name) if parent_name else ""
    return site_key in lookup_dict or (parent_key and parent_key in lookup_dict)

df["is_hot_lead"] = df.apply(
    lambda r: check_match(str(r["Site"]), str(r.get("Parent", "")), hot_lead_normalized), axis=1
)
df["is_existing_customer"] = df.apply(
    lambda r: check_match(str(r["Site"]), str(r.get("Parent", "")), {n: True for n in delfa_normalized}), axis=1
)
df["is_competitor_customer"] = df.apply(
    lambda r: check_match(str(r["Site"]), str(r.get("Parent", "")), competitor_normalized), axis=1
)
df["has_contact_info"] = df.apply(
    lambda r: normalize(str(r["Site"])) in clay_companies or
              (pd.notna(r.get("Parent")) and normalize(str(r["Parent"])) in clay_companies), axis=1
)

print(f"  → Hot leads matched: {df['is_hot_lead'].sum()}")
print(f"  → Existing customers matched: {df['is_existing_customer'].sum()}")
print(f"  → Competitor customers matched: {df['is_competitor_customer'].sum()}")
print(f"  → Has contact info: {df['has_contact_info'].sum()}")

# ── Geocode via real zip codes ─────────────────────────────────────────────
print("\nGeocoding via pgeocode (real coordinates)...")
nomi = pgeocode.Nominatim('us')

# Batch geocode all unique zip codes
unique_zips = df["Zip Code"].dropna().unique()
zip_coords = {}
for z in unique_zips:
    z_str = str(int(z)).zfill(5) if not pd.isna(z) else None
    if z_str:
        result = nomi.query_postal_code(z_str)
        if not pd.isna(result.latitude):
            zip_coords[z] = (result.latitude, result.longitude)

print(f"  → Geocoded {len(zip_coords)}/{len(unique_zips)} unique zip codes")

df["lat"] = df["Zip Code"].map(lambda z: zip_coords.get(z, (None, None))[0] if not pd.isna(z) else None)
df["lng"] = df["Zip Code"].map(lambda z: zip_coords.get(z, (None, None))[1] if not pd.isna(z) else None)
df["lat"] = pd.to_numeric(df["lat"])
df["lng"] = pd.to_numeric(df["lng"])

geocoded = df["lat"].notna().sum()
print(f"  → {geocoded}/{len(df)} sites geocoded ({geocoded/len(df)*100:.0f}%)")

# ── Scoring for road trip prioritization ───────────────────────────────────
print("\nScoring sites for prioritization...")

def compute_score(row):
    score = 0
    rev = row["2024 Payments"]

    if row["is_hot_lead"]:
        score += 100
    if row["is_competitor_customer"]:
        score += 50
    if rev >= 5_000_000:
        score += 40
    elif rev >= 1_000_000:
        score += 25
    elif rev >= 500_000:
        score += 10
    if row["has_contact_info"]:
        score += 30
    if row["Profit Status"] == "FPO":
        score += 20
    elif row["Profit Status"] == "AGG":
        score += 10
    high_volume_ta = {"Infectious Disease", "Oncology", "Cardiology", "Endocrinology"}
    if row.get("Top Therapeutic Area") in high_volume_ta:
        score += 10
    if row["is_existing_customer"]:
        score -= 200
    return score

df["priority_score"] = df.apply(compute_score, axis=1)

def rev_tier(rev):
    if rev >= 5_000_000: return "Tier 1 ($5M+)"
    elif rev >= 1_000_000: return "Tier 2 ($1M-$5M)"
    elif rev >= 500_000: return "Tier 3 ($500K-$1M)"
    else: return "Tier 4 (<$500K)"

df["revenue_tier"] = df["2024 Payments"].apply(rev_tier)

# ── Save processed data ───────────────────────────────────────────────────
print("\nSaving processed data...")
df.to_csv("01_data_processing/processed_sites.csv", index=False)

# Save top targets
targets = df[
    (df["is_hot_lead"]) &
    (df["Profit Status"] == "FPO") &
    (~df["is_existing_customer"])
].sort_values("priority_score", ascending=False)
targets.to_csv("01_data_processing/top_targets.csv", index=False)

# Network summary
network_sites = df[df["Parent"].notna() & (df["Parent"] != "")].copy()
network_summary = network_sites.groupby("Parent").agg(
    site_count=("Site", "count"),
    total_revenue=("2024 Payments", "sum"),
    states=("State", lambda x: list(set(x))),
    has_hot_lead=("is_hot_lead", "any"),
).reset_index()
network_summary = network_summary[network_summary["has_hot_lead"]].sort_values(
    "total_revenue", ascending=False
)
network_summary.to_csv("01_data_processing/network_summary.csv", index=False)

print(f"  → processed_sites.csv ({len(df)} rows)")
print(f"  → top_targets.csv ({len(targets)} rows)")
print(f"  → network_summary.csv ({len(network_summary)} rows)")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total sites: {len(df)} | Geocoded: {geocoded}")
print(f"Hot leads: {df['is_hot_lead'].sum()} | FPO targets: {len(targets)}")
print(f"\nTop 5 targets:")
for _, row in targets.head(5).iterrows():
    print(f"  Score {row['priority_score']:3.0f} | ${row['2024 Payments']:>12,.0f} | "
          f"{row['Site']:40s} | {row['City']}, {row['State']}")
