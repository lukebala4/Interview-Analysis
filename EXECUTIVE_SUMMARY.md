# Delfa AI — GTM Road Trip: What We Did & What We Found

**Prepared for:** Delfa AI CEO
**Context:** Founding GTM Technical Challenge — plan a 2-week in-person sales blitz to close maximum deals with US clinical trial sites.

---

## What We Started With

Two datasets:
- **Dataset A** — 4,551 US clinical trial sites with 2024 sponsor payment data
- **Dataset B** — 482 curated hot leads with contact info, competitor intelligence, and existing customer flags

## What We Did

### 1. Cleaned & Merged the Data
Combined both datasets, geocoded every site by zip code, and flagged each site as: hot lead, existing customer, competitor customer, has contact info, FPO/NPO.

**Key filter:** We focused on **For-Profit Organizations (FPOs)** — independent research sites that make their own purchasing decisions and need patient recruitment help. Large academic NPOs (MD Anderson, Memorial Sloan Kettering) have internal recruitment teams and aren't the target.

After filtering: **254 FPO hot lead targets** ready for the road trip.

### 2. Scored & Ranked Every Target

Each site got a composite priority score:

| Factor | Points | Why |
|--------|--------|-----|
| Hot lead (on curated list) | +100 | Already vetted for product-fit |
| Competitor customer (Alleviate/Grove) | +50 | Already pays for recruitment tools — warmest leads |
| Revenue $5M+ | +40 | High trial volume = acute recruitment need |
| Revenue $1M–$5M | +25 | Sweet spot: has budget, lacks internal tools |
| Has contact info (email/LinkedIn) | +30 | Can pre-book meetings before arriving |
| FPO status | +20 | Fast decision-makers vs. NPO procurement |
| High-volume therapeutic area | +10 | Infectious Disease, Oncology = most patients needed |

### 3. Discovered the Network-First Insight

This changed the entire strategy. Many hot leads belong to **multi-site networks**:

| Network | Sites | Payments | HQ |
|---------|-------|----------|----|
| DM Clinical Research | 20 | $79M | Houston, TX |
| Alcanza Clinical Research | 23 | $45M | Lake Mary, FL |
| AMR | 16 | $43M | Knoxville, TN |
| Alliance Clinical Network | 15 | $35M | National |

**The implication:** Instead of visiting 94 individual sites, close 2–3 network HQs and unlock 40+ sites from 2–3 meetings. The trip becomes a **network HQ tour**, not a site-by-site crawl.

### 4. Built 3 Visual Maps

All included in this repo:
- **US Landscape Map** — 4,505 sites colored by therapeutic area, sized by payments
- **Road Trip Route Map** — 254 targets with the 7-stop route overlaid
- **Sponsor Network Chart** — Top pharma sponsors decoded from trial protocol IDs

---

## The Recommendation

### Week 1: Texas — 53 targets, $118M in payments

| Days | City | Key Meeting | Why |
|------|------|------------|-----|
| 1–2 | Houston | **DM Clinical HQ** ($79M, 20 sites) | 1 deal = 20 sites. Infectious Disease focus. |
| 3–4 | Dallas | **Pillar Clinical** ($15.5M, Psychiatry) | Highest independent-site value in TX. |
| 5–6 | San Antonio | **Pinnacle Clinical** ($2.8M, 8-site network) | Multi-state network anchor. |
| 7 | Austin | **Hope Clinical** ($2.5M) + Alliance sites | Network hub + local independents. |

### Week 2: Florida — 41 targets, $47M in payments

| Days | City | Key Meeting | Why |
|------|------|------------|-----|
| 8–9 | Orlando/Lake Mary | **Alcanza HQ** ($45M, 23 sites) | Alleviate competitor customer. Already budgets for recruitment tools. |
| 10–11 | Miami | Innovation Medical, Well Pharma | Test cross-specialty appeal. |
| 12–13 | Tampa/Ocala | **Renstar/Phasewell** ($8.7M, 2 sites) | Second-highest FL revenue outside Alcanza. |
| 14 | Buffer | Follow-ups, rescheduled meetings | Overflow day. |

### Why Texas + Florida?

- **TX** has the most hot leads of any state (55) and the single most valuable network deal (DM Clinical, 20 sites)
- **FL** has the warmest lead in the entire dataset — Alcanza is already paying a competitor (Alleviate) for a similar product. They understand the value prop. The conversation is "why switch to Delfa" not "why do you need this."
- Together: **94 targets covering $165M in sponsor payments** — 64% of all hot lead payment volume in just 2 states.

---

## Top 5 Must-Win Targets

| # | Target | Payments | Why This One |
|---|--------|----------|-------------|
| 1 | **DM Clinical Research** (TX) | $79M across 20 sites | Largest FPO network. One enterprise deal opens 20 sites. |
| 2 | **Alcanza Clinical Research** (FL) | $45M across 23 sites | Competitor customer — already pays for recruitment tools. Warmest possible lead. |
| 3 | **AMR Knoxville** (TN) | $34M single site | Highest individual-site payments among all hot leads. Month 2 target. |
| 4 | **Hope Clinical Research** (CA) | $17M | Alliance Clinical Network hub (15 sites nationally). Month 2 target. |
| 5 | **Pillar Clinical Research** (TX) | $15.5M | Dallas. Psychiatry niche with deep trial portfolio. On Week 1 route. |

---

## What We're Intentionally Leaving for Month 2

| Region | What We Miss | Payment Volume | Why Skip Now |
|--------|-------------|----------------|-------------|
| California | Hope Clinical, Benchmark Research | $50M | Sites spread across 400 miles — low meeting density |
| Massachusetts | Clinical Research Network, Excel Clinical | $32M | Strong cluster but smaller than TX/FL |
| Tennessee | AMR Knoxville ($34M single site) | $37M | One meeting doesn't fill a week |
| North Carolina | Lucas Research (competitor customer) | $24M | Only 2 high-value targets |

**Suggested Month 2 route:** Boston → NYC → Philly → Wilmington NC → Knoxville TN

---

## Key Assumptions (Worth Discussing)

1. **Revenue ≠ recruitment need.** We use 2024 sponsor payments as a proxy for trial volume (more trials = more patients needed). It's imperfect — a high-revenue site might already recruit well.

2. **"Closing" means opening relationships.** Enterprise clinical trial software has a 3–6 month sales cycle. The 2-week trip fills the pipeline with first meetings and demos, not signed contracts.

3. **Pre-trip outreach is critical.** We have contact info (name, email, LinkedIn) for 203 companies. Emailing 2 weeks before — "I'll be in Houston visiting DM Clinical, would love 30 minutes" — creates urgency and books confirmed meetings.

4. **Network HQs are single points of decision.** We assume DM Clinical and Alcanza make centralized purchasing decisions. If individual sites buy independently, the "1 deal = 20 sites" math breaks down (but TX still has 35 independent targets).

---

## How to View the Output

**On GitHub:** Scroll up in the README — all 3 maps are embedded as images.

**Interactive versions:** Download and open locally in your browser:
- `02_landscape_map/us_clinical_sites_map.html` — click any site for details
- `03_road_trip_plan/road_trip_map.html` — click route stops + targets
- `04_sponsor_network/sponsor_site_network.html` — drag nodes to explore sponsor relationships

**Deep-dive documents:**
- `PLAN.md` — Full strategic plan with edge cases, interviewer challenges, and the "Lucrative vs. Sensible" framework
- `03_road_trip_plan/STRATEGY.md` — Day-by-day reasoning with per-site rationale

---

## Technical Approach

1. **Data processing** — Python (pandas, openpyxl) to clean, merge, and score 4,551 sites
2. **Geocoding** — pgeocode library for real zip-to-coordinate mapping (99% coverage)
3. **Maps** — Leaflet.js interactive HTML maps + matplotlib static PNGs for GitHub display
4. **Network analysis** — networkx for sponsor-site relationship mapping
5. **Protocol decoding** — Mapped trial protocol ID prefixes to pharma sponsors (Moderna, Novartis, Pfizer, etc.)
