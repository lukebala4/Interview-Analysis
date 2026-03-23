# Delfa AI — Founding GTM Technical Challenge

## Mission
Plan a 2-week road trip across the US to close maximum deals with clinical trial sites for Delfa AI's patient recruitment management system.

## Key Findings

- **4,551** clinical trial sites across the US (Dataset A)
- **482** hot leads curated for product-fit (Dataset B)
- **254** FPO hot lead targets scored and ranked for road trip
- **Top recommendation:** Week 1 Texas (DM Clinical HQ, 53 targets, $118M) → Week 2 Florida (Alcanza HQ, 41 targets, $47M)
- **Critical insight:** Network-first selling — closing 2-3 network HQs unlocks 40+ sites vs visiting individually

## Repository Structure

```
├── PLAN.md                           Full strategic plan with assumptions & rationale
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
│   └── us_clinical_sites_map.html    Interactive map (open in browser)
│
├── 03_road_trip_plan/                Task 2: Road Trip Strategy
│   ├── cluster_analysis.py           Cluster scoring script
│   ├── road_trip_map.html            Interactive route map (open in browser)
│   └── STRATEGY.md                   Written reasoning & day-by-day plan
│
└── 04_sponsor_network/              Bonus: Sponsor-Site Network
    ├── network_graph.py              Network analysis script
    └── sponsor_site_network.html     Interactive network graph (open in browser)
```

## How to View Deliverables

1. **Task 1 — Landscape Map:** Open `02_landscape_map/us_clinical_sites_map.html` in a browser. Toggle layers to view hot leads, tier 1 sites, and competitor customers.

2. **Task 2 — Road Trip Plan:** Open `03_road_trip_plan/road_trip_map.html` for the visual route, and read `03_road_trip_plan/STRATEGY.md` for the full written reasoning.

3. **Bonus — Sponsor Network:** Open `04_sponsor_network/sponsor_site_network.html` in a browser. Click nodes to explore sponsor-site relationships.

4. **Full Plan & Assumptions:** Read `PLAN.md` for the complete strategic analysis including edge cases, interviewer challenges, and the Lucrative vs. Sensible framework.

## Top 5 Priority Targets

| Rank | Target | Revenue | Why |
|------|--------|---------|-----|
| 1 | DM Clinical Research (TX HQ) | $79M (20 sites) | Largest FPO network. 1 deal = 20 sites. |
| 2 | Alcanza Clinical Research (FL HQ) | $45M (23 sites) | Alleviate competitor customer. Already pays for recruitment tools. |
| 3 | AMR Knoxville (TN) | $34M | Highest single-site revenue among hot leads. |
| 4 | Hope Clinical Research (CA) | $17M | Alliance Clinical Network (15 sites). |
| 5 | Pillar Clinical Research (TX) | $15.5M | Dallas/Richardson. Psychiatry niche. |

## Technical Stack
- Python 3 (pandas, folium, openpyxl, networkx)
- Interactive HTML maps (Leaflet.js via folium, vis.js for network graph)
