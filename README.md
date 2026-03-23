# Delfa AI — Founding GTM Technical Challenge

## Mission
Plan a 2-week road trip across the US to close maximum deals with clinical trial sites for Delfa AI's patient recruitment management system.

## Key Findings

- **4,551** clinical trial sites across the US (Dataset A)
- **482** hot leads curated for product-fit (Dataset B)
- **254** FPO hot lead targets scored and ranked for road trip
- **Top recommendation:** Week 1 Texas (DM Clinical HQ, 53 targets, $118M) → Week 2 Florida (Alcanza HQ, 41 targets, $47M)
- **Critical insight:** Network-first selling — closing 2-3 network HQs unlocks 40+ sites vs visiting individually

---

## Deliverables

### Task 1 — US Landscape Map (4,505 sites)
All clinical trial sites colored by therapeutic area, sized by 2024 sponsor payments.

![US Clinical Trial Sites Landscape](02_landscape_map/us_clinical_sites_map.png)

### Task 2 — Road Trip Route Map (254 targets)
FPO hot lead targets with 7-stop route: Week 1 Texas, Week 2 Florida.

![Road Trip Route Map](03_road_trip_plan/road_trip_map.png)

### Bonus — Sponsor-Site Network Analysis
Top pharma sponsors decoded from protocol IDs, showing site relationships.

![Sponsor-Site Network](04_sponsor_network/sponsor_site_network.png)

> **Interactive versions** (download and open locally): [Landscape Map HTML](02_landscape_map/us_clinical_sites_map.html) | [Road Trip HTML](03_road_trip_plan/road_trip_map.html) | [Network HTML](04_sponsor_network/sponsor_site_network.html)

---

## Repository Structure

```
├── PLAN.md                           Full strategic plan with assumptions & rationale
├── index.html                        Landing page with links to all deliverables
├── data/                             Raw data files
│   ├── Delfa_Pull_202512221346.csv   Dataset A: All US clinical trial sites
│   ├── Example Prospect List (1).xlsx Dataset B: Hot leads + contacts
│   └── Founding GTM - Technical Challenge (Candidate).pdf
│
├── 01_data_processing/               Data cleaning, merging, scoring
│   ├── process_data.py               Processing pipeline
│   ├── processed_sites.csv           All sites with scores & flags
│   ├── top_targets.csv               FPO hot leads ranked by priority
│   └── network_summary.csv           Site network analysis
│
├── 02_landscape_map/                 Task 1: US Clinical Sites Map
│   ├── generate_map.py               Map generation script
│   └── us_clinical_sites_map.html    Interactive map
│
├── 03_road_trip_plan/                Task 2: Road Trip Strategy
│   ├── cluster_analysis.py           Cluster scoring script
│   ├── road_trip_map.html            Interactive route map
│   └── STRATEGY.md                   Written reasoning & day-by-day plan
│
└── 04_sponsor_network/              Bonus: Sponsor-Site Network
    ├── network_graph.py              Network analysis script
    └── sponsor_site_network.html     Interactive network graph
```

## Top 5 Priority Targets

| Rank | Target | Payments | Why |
|------|--------|---------|-----|
| 1 | DM Clinical Research (TX HQ) | $79M (20 sites) | Largest FPO network. 1 deal = 20 sites. |
| 2 | Alcanza Clinical Research (FL HQ) | $45M (23 sites) | Alleviate competitor customer. Already pays for recruitment tools. |
| 3 | AMR Knoxville (TN) | $34M | Highest single-site payment volume among hot leads. |
| 4 | Hope Clinical Research (CA) | $17M | Alliance Clinical Network (15 sites). |
| 5 | Pillar Clinical Research (TX) | $15.5M | Dallas/Richardson. Psychiatry niche. |

## Technical Stack
- Python 3 (pandas, pgeocode, openpyxl, networkx)
- Interactive HTML maps (Leaflet.js, vis.js for network graph)
- Real zip-code geocoding via pgeocode (99% coverage)
