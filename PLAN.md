# GTM Strategy Plan — Delfa AI Clinical Trial Site Sales Blitz

## Context

**What is Delfa AI?** A patient recruitment management system for clinical trial sites. Their product helps sites find and enroll patients into clinical trials faster — a critical bottleneck in the $80B+ clinical trials industry.

**The challenge:** Plan a 2-week in-person road trip to close maximum deals with clinical trial sites. We have two datasets:
- **Dataset A** (CSV, 4,551 sites): All US clinical trial sites with 2024 revenue/payments data
- **Dataset B** (Excel, 483 hot leads): Curated prospect list with enriched contact data, existing customers, and competitor intelligence

**Key business model insight:** Delfa sells to **For-Profit Organizations (FPOs)** — independent research sites that need patient recruitment help. Large academic NPOs (MD Anderson, Memorial Sloan Kettering) have their own patient pipelines and are NOT the target. FPOs are the ones paying for recruitment tools.

---

## Data Analysis Summary (Findings from Exploration)

### Hot Lead Landscape
- **483 hot leads** in CRIO Main Set
- **17 existing Delfa customers** (exclude from targeting — already closed)
- **13 competitor customers** (high priority — already understand the product category)
- **203 companies** with enriched contact info (Clay Outreach — LinkedIn, email, job titles)
- **259 FPO hot lead site entries** matched in the revenue dataset

### Top Hot Lead Clusters by State (FPO, non-customer)

| State | Hot Lead Sites | Total Revenue | Why It Matters |
|-------|---------------|---------------|----------------|
| **TX** | 55 | $119M | Dominant cluster. DM Clinical alone has 8+ TX locations. Huge Infectious Disease corridor. |
| **FL** | 42 | $50M | Second largest cluster. Mix of Infectious Disease, Endocrinology, Neurology. |
| **CA** | 22 | $50M | High revenue per site. Hope Clinical ($17M), Benchmark Research ($6.7M). |
| **MA** | 13 | $32M | Dense Boston corridor. Clinical Research Network ($10M), Excel Clinical ($7.8M). |
| **IL** | 13 | $15M | DM Clinical Chicago presence. |
| **NC** | 11 | $24M | Lucas Research ($7M), Trial Management ($6M). |

### Competitor Intelligence (from Excel)
- **Alleviate** customers: Centricity, Eximia, Conquest, Profound Research, Alcanza, CenExel, M3 Wake Research, Lucas Research
- **Grove** customers: K2 Medical, Celerion, CRCNJ, IMA Research
- These are *warm* — they already use a similar product, understand the value prop, and may be open to switching

---

## Execution Plan

### Step 1: Repository Structure Setup
**Assumption:** We need a clean, chronological folder structure so you can follow the storyline.

```
Interview-Analysis/
├── README.md                          (updated throughout)
├── PLAN.md                            (this plan, synced with changes)
├── data/                              (raw data files)
│   ├── Delfa_Pull_202512221346.csv
│   └── Example Prospect List (1).xlsx
├── 01_data_processing/                (data cleaning & prep scripts)
│   └── process_data.py
├── 02_landscape_map/                  (Task 1 deliverable)
│   ├── generate_map.py
│   └── us_clinical_sites_map.html
├── 03_road_trip_plan/                 (Task 2 deliverable)
│   ├── cluster_analysis.py
│   ├── road_trip_map.html
│   └── STRATEGY.md                   (written reasoning)
├── 04_sponsor_network/               (Bonus deliverable)
│   ├── network_graph.py
│   └── sponsor_site_network.html
└── output/                           (final presentation assets)
```

### Step 2: Data Processing (`01_data_processing/`)
**What:** Clean and merge both datasets into a unified analysis-ready format.

**Assumptions:**
- Use Python with pandas for data manipulation
- Geocode sites using zip codes (zip-to-lat/lng lookup) for mapping — no API needed, use a static zip code database
- Normalize site names between datasets for matching (fuzzy matching where needed)
- Mark each site with flags: `is_hot_lead`, `is_existing_customer`, `is_competitor_customer`, `has_contact_info`
- Revenue = "2024 Payments" column from CSV

**Key decisions:**
- **Exclude NPOs from road trip targeting** — Large academic medical centers (NPOs) have internal recruitment. Delfa's product is most valuable to independent FPO sites that need help finding patients.
- **Prioritize sites with enriched contact data** (Clay Outreach) — we can actually reach these people
- **Flag competitor customers as highest priority** — they already understand the product category

### Step 3: US Landscape Map (`02_landscape_map/` — Task 1)
**What:** Interactive HTML map of all 4,551 clinical trial sites, sized by revenue, colored by therapeutic area.

**Assumptions:**
- Use `folium` (Python Leaflet.js wrapper) for interactive HTML map
- Bubble size = revenue (log-scaled so huge NPOs don't dominate visually)
- Color = therapeutic area (top 8 areas get distinct colors, rest grouped as "Other")
- Popup on click = site name, revenue, therapeutic area, city/state, PI name
- Hot leads get a distinct marker style (star or highlighted border)
- Layer controls to toggle: All sites / Hot leads only / By therapeutic area

**Limitation:** Geocoding from zip codes gives city-center coordinates, not exact addresses. Good enough for a landscape view.

### Step 4: Hot Lead Cluster Analysis & Road Trip Plan (`03_road_trip_plan/` — Task 2)
**What:** Identify the optimal cluster(s) for a 2-week sales blitz. This is the strategic core.

**Assumptions & Approach:**

#### Prioritization Framework (Hierarchical — this is the key)
Each site gets a **composite score** based on:

1. **Is it a hot lead?** (binary gate — hot leads get 10x weight)
   - *Why:* The CRIO Main Set was curated for product-fit. These sites have operational profiles that match Delfa's value prop. Cold-calling random sites is a waste of the 2 weeks.

2. **Is it a competitor customer?** (+50% bonus)
   - *Why:* Alleviate/Grove customers already budget for patient recruitment tools. They understand the pain point. The conversation is "why Delfa is better" not "why you need this category."

3. **Revenue tier** (weighted score)
   - Tier 1: $5M+ revenue → highest value (large trial volume = more recruitment needs)
   - Tier 2: $1M-$5M → strong mid-market (bread and butter for a startup)
   - Tier 3: <$1M → lower priority (may not have budget for new tools)
   - *Why:* Revenue correlates with trial volume. More trials = more patients needed = more value from Delfa.

4. **Has enriched contact info?** (+30% bonus)
   - *Why:* Having a name, email, and LinkedIn for the decision-maker means we can pre-qualify and book meetings before arriving. Cold walk-ins have <10% meeting rate.

5. **Profit status: FPO strongly preferred**
   - *Why:* FPOs are Delfa's ICP (Ideal Customer Profile). They're independent, they make fast purchasing decisions, and they need recruitment help. NPOs have procurement bureaucracy and internal resources.

6. **Therapeutic area alignment** (slight bonus for high-volume areas)
   - Infectious Disease, Oncology, Cardiology, Endocrinology = highest trial volumes = most recruitment pain

#### Cluster Selection Logic
- **NOT optimizing for geographic efficiency** — we're optimizing for deal quality
- Score every hot lead site, then look at where the top-scored sites naturally cluster
- A "cluster" = metro area where 5+ high-scoring hot leads exist within reasonable driving distance
- The winning region is where the **density of high-quality opportunities** is highest

#### Expected Outcome (based on data exploration)
The **Texas Triangle (Houston-Dallas-San Antonio)** is likely the primary cluster because:
- 55 hot lead FPO sites (most of any state by far)
- $119M total revenue across those sites
- DM Clinical has 8+ locations in TX alone (network effect — close one, reference for others)
- Pillar Clinical Research in Richardson/Dallas ($15.5M, Psychiatry)
- Multiple Pinnacle Clinical Research sites in San Antonio
- Juno Research, SMS Clinical, ACRC Trials all in DFW/Houston

**Secondary cluster:** Florida (42 hot lead sites, $50M) — could be Week 2 if TX is Week 1.

**Trade-off acknowledged:** We're NOT visiting California ($50M, 22 sites) even though revenue-per-site is high, because the sites are spread across the entire state (LA, Sacramento, San Diego, SF) making density lower. Texas and Florida have tighter geographic clusters of hot leads.

### Step 5: Strategy Document (`03_road_trip_plan/STRATEGY.md`)
**What:** Written reasoning document explaining the road trip decision.

**Will cover:**
- Why hot leads > random high-revenue sites
- Why FPOs > NPOs for Delfa's business model
- The scoring framework and how clusters were ranked
- Specific site-by-site reasoning for the top 20 targets
- What to do before the trip (pre-outreach via Clay contact data)
- Trade-offs made and what we're leaving on the table

### Step 6: Sponsor-Site Network Map (`04_sponsor_network/` — Bonus)
**What:** Network graph showing sponsor-site-therapeutic area relationships.

**Assumptions:**
- Extract sponsor info from `Top Protocol` column (protocol IDs encode sponsor prefixes — e.g., "mRNA-" = Moderna, "CABL" = Novartis, etc.)
- Use `pyvis` or `networkx` + HTML export for interactive network visualization
- Nodes = Sites (sized by revenue) + Sponsors (colored differently)
- Edges = "Site runs trials for Sponsor"
- Cluster by therapeutic area
- **Limitation:** Protocol IDs are not always easily mappable to sponsors. We'll decode what we can and note limitations.

### Step 7: Sync All Outputs
**What:** Update README.md, PLAN.md, and all output files to be consistent.

Every commit will update:
- `README.md` — project overview, how to view deliverables, key findings
- `PLAN.md` — mark completed steps, add findings
- Chronological folders — each numbered folder tells part of the story

---

## Technical Stack
- **Python 3** with: pandas, folium, openpyxl, networkx/pyvis
- **HTML** outputs for interactive maps (viewable in any browser)
- **Markdown** for strategy documents

## Verification Plan
1. Open each HTML map in browser — verify sites render correctly
2. Spot-check 10 hot lead sites on the map — confirm they appear with correct data
3. Verify scoring ranks match intuition (competitor customers with high revenue should be at top)
4. Confirm existing Delfa customers are excluded from road trip targets
5. README.md accurately reflects all deliverables and how to access them

---

---

## Critical Insight: Network-Level Selling Changes Everything

The parent/network analysis reveals that many hot leads are **multi-site networks**. This fundamentally shifts the strategy from "visit the most sites" to "close the biggest network HQs":

| Network | Sites | Total Revenue | HQ/Key States | Strategic Value |
|---------|-------|---------------|---------------|-----------------|
| **DM Clinical Research** | 20 | $79M | TX (HQ Houston) | Close HQ → 20 sites. Massive TX presence. |
| **Alcanza Clinical Research** | 23 | $45M | FL (HQ Lake Mary) | Largest site count. Competitor customer (Alleviate). |
| **AMR (Alliance for Multispecialty Research)** | 16 | $43M | TN (Knoxville $34M top site) | Highest single-site revenue among hot leads. |
| **Alliance Clinical Network** | 15 | $35M | CA (Hope Clinical $17M) | Strong CA/TX/MA presence. |
| **Atlas Clinical Research** | 3 | $16M | NY (Rochester $13M) | Existing Delfa customer — reference account. |
| **Pinnacle Clinical Research** | 8 | $9M | TX (San Antonio) | Multi-state, TX-heavy. |
| **Phasewell/Renstar** | 2 | $9M | FL (Marion/Ocala) | Two high-revenue FL sites. |
| **Headlands Research** | 2 | $8M | NC/MO | Trial Management ($6M Wilmington). |

**Implication:** Instead of visiting 55 individual TX sites, visit DM Clinical HQ in Houston and Pinnacle in San Antonio → potential to close 28 sites in 2 meetings. The road trip becomes a **network HQ tour**, not a site-by-site crawl.

---

## Edge Cases, Flaws & Interviewer Challenges

### What an interviewer would challenge:

**1. "DM Clinical is 1 deal, not 20 — your TX cluster is inflated."**
- **Valid.** If DM Clinical is centrally managed, visiting 8 TX locations is redundant. The right move is: visit DM Clinical HQ once, then use remaining TX time for independent sites.
- **Our response:** We account for this. TX still has ~35 independent (non-DM) hot lead sites. Combined with the DM HQ visit, TX remains the top cluster.

**2. "Revenue ≠ recruitment need. High-revenue sites might NOT need Delfa."**
- **Valid.** A site earning $50M might have excellent recruitment already. A struggling $500K site might desperately need Delfa but can't afford it.
- **Our response:** We use revenue as a proxy for trial volume (more trials = more recruitment events), NOT as a measure of need. The sweet spot is $1M-$15M FPO sites — big enough to have budget, small enough to lack internal recruitment teams.
- **Flaw we acknowledge:** We don't have data on recruitment success rates or patient enrollment timelines. Revenue is an imperfect proxy.

**3. "You're ignoring the sales cycle. You can't close in 2 weeks."**
- **Valid.** Enterprise clinical trial software likely has a 3-6 month sales cycle. The 2-week trip is about OPENING relationships, not closing deals.
- **Our response:** Reframe the trip as "close as many first meetings and demos as possible." The goal is to fill the pipeline, not sign contracts on Day 1. Pre-trip outreach via Clay contact data (emails, LinkedIn) is critical to book confirmed meetings.

**4. "Competitor customers might be locked into contracts."**
- **Partially valid.** Alleviate/Grove customers (Alcanza, Lucas Research, etc.) may have annual contracts.
- **Our response:** Even if locked in, building relationships NOW means we're positioned when contracts expire. These are still the warmest leads because they already understand the product category. Meeting them in person gives us intel on competitor weaknesses.

**5. "Why not just call everyone? Why a road trip?"**
- **This is the right question.** The premise says "in-person is the best way to close." For clinical trial sites, the PI (Principal Investigator) and site director are busy clinicians. They don't take cold calls. Showing up with a demo — especially with a referral from an existing Delfa customer — is the highest-conversion channel.
- **Pre-trip play:** Use Clay contact data to email/LinkedIn 2 weeks before. "I'll be in Houston next week visiting DM Clinical — would love 30 minutes." Name-dropping other local sites creates urgency and social proof.

**6. "Your matching between datasets is imperfect."**
- **Valid.** Fuzzy name matching between CRIO list and CSV will miss some sites and create false matches. Site names vary (e.g., "Hope Clinical Research" vs "Hope Clinical Ressearch" — actual typo in data).
- **Our response:** We use normalized matching and flag low-confidence matches for manual review. The 327 unmatched hot leads likely operate under different names in the CSV or aren't in Dataset A at all (newer sites, different data vintage).

### Edge cases we're handling:

- **Existing Delfa customers (17 sites):** Excluded from targeting but USED as reference accounts. "Accurate Clinical Research is already using Delfa — want to hear their experience?"
- **Sites with no website/contact info:** Deprioritized. If we can't research them or reach out beforehand, cold walk-ins waste time.
- **Puerto Rico sites:** Excluded from road trip (separate travel logistics) but noted on landscape map.
- **Aggregator (AGG) profit status:** These are site management organizations, not individual sites. They could be high-leverage targets (close 1 AGG = access to many sites) but need different sales approach.

---

## Updated Approach: The "Network-First" Road Trip

Based on the network analysis, the optimal strategy is:

### Week 1: Texas (Houston → Dallas/Richardson → San Antonio)
**Why:** Highest concentration of hot lead networks + independents
- **Day 1-2: Houston** — DM Clinical HQ (20-site network, $79M), Juno Research ($3.7M)
- **Day 3-4: Dallas/Richardson** — Pillar Clinical Research ($15.5M, Psychiatry), ACRC Trials ($2.6M Plano), Pinnacle/Kerwin ($1.9M Dallas)
- **Day 5-6: San Antonio** — Pinnacle Clinical Research ($2.8M), other independents
- **Day 7: Austin** — Hope Clinical ($2.5M), Alliance Clinical Network sites, Zenos ($1.8M), Acclaim ($1M)

### Week 2: Florida (Lake Mary/Orlando → Miami → Tampa)
**Why:** Second-highest cluster + Alcanza HQ (23-site competitor customer)
- **Day 8-9: Lake Mary/Orlando** — Alcanza HQ (23 sites, $45M, Alleviate competitor customer!), Complete Health ($7M)
- **Day 10-11: Miami** — Innovation Medical ($3M), New Age Medical ($2M), Well Pharma ($2.3M)
- **Day 12-13: Tampa/Ocala** — Renstar/Phasewell ($8.7M, 2 sites), Accel Clinical ($3.2M DeLand)
- **Day 14: Wrap/overflow**

### Why NOT other regions:
- **California ($50M, 22 sites):** Sites spread LA to Sacramento. No network HQ advantage. Revisit in month 2.
- **Massachusetts ($32M, 13 sites):** Strong cluster but smaller than TX/FL. Clinical Research Network ($10M) is the main prize — can be a follow-up trip.
- **North Carolina ($24M, 11 sites):** Lucas Research ($7M, Alleviate competitor) is worth a dedicated trip later.

---

---

## Deep Rationale: What's Lucrative vs. What's Sensible

### The Lucrative vs. Sensible Matrix

Every target falls into one of four quadrants. Here's how we think about each:

#### Quadrant 1: Lucrative AND Sensible (PRIMARY TARGETS)
These are high-value sites that Delfa can realistically close. They combine revenue ($1M-$15M), FPO status, hot lead qualification, and accessible decision-makers.

**Scenario — DM Clinical Research ($79M across 20 sites):**
- **Lucrative because:** Single deal = 20 sites onboarded. At even $50K ARR per site, that's $1M ARR from one relationship. Their Infectious Disease focus means high patient volume trials with constant recruitment pressure.
- **Sensible because:** They're an FPO network, meaning a centralized business development team makes purchasing decisions. They're on the hot lead list, so Delfa has already identified product-market fit. Houston HQ visit is a single meeting.
- **Risk:** If DM Clinical has built internal recruitment tools, they don't need Delfa. Mitigation: research their current stack before the trip.

**Scenario — Alcanza Clinical Research ($45M, 23 sites, Alleviate competitor customer):**
- **Lucrative because:** Already paying for a competitor product (Alleviate) — budget is allocated, value is understood. If Delfa can demonstrate superiority in even one dimension (cost, efficacy, UX), switching is attractive.
- **Sensible because:** Competitor customers convert 3-5x faster than cold prospects. The conversation skips "why do I need this?" and goes straight to "why is Delfa better?" Plus, 23 sites makes this the largest network in our hot lead list.
- **Risk:** Multi-year contract lock-in with Alleviate. Mitigation: Even if locked in, this visit plants the seed for renewal season. Ask: "When does your Alleviate contract renew?"

#### Quadrant 2: Lucrative but NOT Sensible (DEPRIORITIZE)
High revenue but hard to close in 2 weeks.

**Scenario — MD Anderson ($267M, NPO):**
- **Lucrative because:** Largest clinical trial site in America by revenue. Landing MD Anderson as a customer would be transformative for Delfa's brand.
- **NOT sensible because:** It's a massive academic NPO with internal recruitment infrastructure, procurement committees, 6-12 month vendor approval cycles, and likely existing institutional tools. A 2-week road trip cannot close this. It requires a dedicated enterprise sales motion over many months.
- **Decision:** Exclude from road trip. Pursue separately with a dedicated account executive after Series A.

**Scenario — California hot leads (22 sites, $50M, spread across LA/Sacramento/SD/SF):**
- **Lucrative because:** Highest revenue-per-site ratio. Hope Clinical ($17M in Canoga Park) alone is worth more than most state clusters.
- **NOT sensible because:** 4 days driving between LA, Sacramento, San Diego, and SF. You'd spend more time on the 5/101 freeway than in meetings. The geographic spread kills meeting density.
- **Decision:** Skip for now. Target the 2-3 highest-value CA sites (Hope Clinical, Benchmark Research) in a separate, focused West Coast trip.

#### Quadrant 3: Sensible but NOT Lucrative (NICE-TO-HAVE)
Easy to close but small deal value.

**Scenario — Small FPO hot leads (<$500K revenue):**
- **Sensible because:** Small sites are often desperate for patient recruitment help. They'll take a meeting immediately and may close in one visit.
- **NOT lucrative because:** At $500K annual revenue, they likely can't afford a significant software contract. Even if they sign, the ARR is minimal.
- **Decision:** Don't plan travel specifically for these. But if they're on the route between two Tier 1 targets, take the meeting.

#### Quadrant 4: Neither Lucrative NOR Sensible (IGNORE)
**Example:** Rural NPO sites with <$100K revenue, no website, no contact info. Not worth any time.

---

### Why Texas is the #1 Region — The Full Reasoning

**The case FOR Texas:**
1. **Volume:** 55 FPO hot lead sites — 31% more than Florida (#2 with 42). Even deflating for DM Clinical (1 deal, not 20), TX still has ~35 independent targets.
2. **Network HQ leverage:** DM Clinical HQ is in Houston. One meeting potentially opens 20 sites. Pinnacle has San Antonio presence. ACRC Trials has 4 TX locations.
3. **Revenue density:** $119M total across hot leads. Even excluding DM Clinical's $79M, independent TX hot leads represent $40M — still competitive.
4. **Therapeutic concentration:** TX hot leads concentrate in Infectious Disease ($47M) and Endocrinology ($8M) — high patient volume specialties where recruitment is an acute pain point. Infectious Disease trials (vaccines, antivirals) require massive patient enrollment, making Delfa's value prop strongest here.
5. **Startup ecosystem:** Houston and Dallas have growing clinical research ecosystems. FPO sites in TX tend to be newer, more tech-forward, and more open to innovative tools vs. established Northeast sites.

**The case AGAINST Texas (devil's advocate):**
1. **DM Clinical dependency:** Remove DM Clinical and TX drops from $119M to $40M — still #1 by site count but #3 by revenue (behind CA and FL).
2. **Travel distances:** Houston to Dallas is 3.5 hours. Dallas to San Antonio is 4.5 hours. Austin adds another 1.5 hours. You're spending 2+ days just driving.
3. **No competitor customers in TX:** None of the Alleviate/Grove customers are TX-based. Florida has Alcanza (23-site Alleviate customer). NC has Lucas Research (Alleviate customer). TX has zero — these are all cold(er) leads.
4. **Seasonal consideration:** If this is summer, Houston is brutally hot and many researchers take time off. Conversion rates may be lower.

**Our verdict:** TX remains #1 because the DM Clinical HQ meeting is too valuable to skip, and the independent site count provides enough backup meetings to fill a full week. But we acknowledge: **if DM Clinical declines a meeting, the TX week becomes significantly less efficient.**

**Contingency:** If DM Clinical HQ declines, consider swapping Week 1 to Massachusetts (Clinical Research Network $10M, Excel Clinical $7.8M, ActivMed $4.1M — all within 30min of each other in the Boston corridor). TX becomes a 3-day trip within Week 2, sharing time with another cluster.

---

### Why Florida Week 2 — Alcanza is the "Must-Win"

**Scenario analysis for the Alcanza meeting:**

**Best case:** Alcanza is unhappy with Alleviate, their contract is up for renewal in Q2, and they're actively evaluating alternatives. Delfa shows up in person with a demo tailored to their 23-site network. They agree to a pilot at 3 sites. Pipeline value: $500K+ ARR.

**Base case:** Alcanza is satisfied with Alleviate but curious. They take the meeting, give honest feedback about what Alleviate does well and where it falls short. Delfa gains critical competitive intelligence and a warm relationship for future follow-up. Pipeline value: $0 immediate, $500K+ in 12 months.

**Worst case:** Alcanza declines the meeting or is locked into a 3-year Alleviate contract. Delfa still has 41 other FL hot leads to visit, including Complete Health ($7M), Renstar ($8.7M across 2 sites), Innovation Medical ($3M). The FL trip is still worth it.

---

### Site-Level Prioritization: Top 15 Targets with Rationale

| Rank | Site/Network | Revenue | State | Why This Target | Risk |
|------|-------------|---------|-------|-----------------|------|
| 1 | DM Clinical Research (HQ) | $79M (20 sites) | TX | Largest FPO network in hot leads. 1 deal = 20 sites. ID focus = high recruitment volume. | May have internal tools. HQ meeting hard to get. |
| 2 | Alcanza Clinical Research (HQ) | $45M (23 sites) | FL | Alleviate competitor customer. Already pays for recruitment tools. Most sites of any network. | Locked into Alleviate contract? |
| 3 | AMR Knoxville | $34M (single site) | TN | Highest single-site revenue among hot leads. Part of 16-site AMR network. | Off the TX/FL route. Would require detour. |
| 4 | Hope Clinical Research | $17M | CA | Alliance Clinical Network ($35M across 15 sites). Very high single-site revenue. | In CA — not on primary route. |
| 5 | Pillar Clinical Research | $15.5M | TX | Richardson/Dallas. Psychiatry focus — niche but deep trials. High per-site value. | Psychiatry may have different recruitment needs. |
| 6 | Clinical Research Network | $10M | MA | North Dartmouth, MA. Pulmonology focus. Part of 3-site network. | Not on TX/FL route. |
| 7 | Renstar/Phasewell | $8.7M (2 sites) | FL | Two sites in Marion/Ocala, FL. Close to FL route. Neurology focus. | Mid-FL location adds drive time. |
| 8 | DM Clinical Bellaire + Tomball | $23M (2 TX sites) | TX | Even if we don't close the HQ deal, these individual TX sites are massive. | Part of DM network — may not decide independently. |
| 9 | Excel Clinical Research | $7.9M | MA | Quincy, MA. Part of Alliance Clinical Network. Infectious Disease. | Not on primary route. |
| 10 | Complete Health (Alcanza) | $7M | FL | Lake Mary, FL. Near Alcanza HQ. Infectious Disease. | May be part of Alcanza deal. |
| 11 | Lucas Research | $7M | NC | Morehead City, NC. Alleviate competitor customer. Endocrinology. | Off primary route. |
| 12 | North Georgia Clinical Research | $6.6M | GA | Woodstock, GA. Part of Alcanza network. Endocrinology. | Part of Alcanza deal. |
| 13 | Benchmark Research | $6.8M | CA | Sacramento. Avacare network (3 sites). Infectious Disease. | CA — off route. |
| 14 | CTI Clinical Research Center | $6.2M | KY | Covington, KY. Endocrinology. Independent site. | Off TX/FL route. |
| 15 | Trial Management Associates | $6M | NC | Wilmington, NC. Headlands Research network. Infectious Disease. | Off primary route. |

**Key observation:** The top 15 includes sites in TX, FL, TN, CA, MA, NC, GA, KY. We can only realistically cover TX + FL in 2 weeks. Sites ranked 3, 4, 6, 9, 11, 13, 14, 15 are **left on the table** — these become Month 2 targets.

---

### What We're Leaving on the Table (and why that's OK)

| Region | What we miss | Total value | Why we skip it |
|--------|-------------|-------------|----------------|
| California | Hope Clinical ($17M), Benchmark ($6.8M), Science 37 ($3.9M), Topography ($4M) | ~$50M | Geographic spread. 4 cities across 400 miles. Low meeting density per day. |
| Massachusetts | Clinical Research Network ($10M), Excel Clinical ($7.9M), ActivMed ($4.1M) | ~$32M | Strong cluster but TX+FL have higher total value. MA becomes Trip #2. |
| North Carolina | Lucas Research ($7M, competitor customer), Trial Management ($6M) | ~$24M | Only 2 high-value targets don't justify a full trip. Bundle with MA in Trip #2. |
| Tennessee | AMR Knoxville ($34M — single highest-revenue hot lead site) | ~$37M | One site. Amazing revenue but one meeting doesn't fill a week. Add to Trip #2 MA/NC/TN corridor. |

**Trip #2 suggestion (Month 2):** Boston → New Haven → NYC → Philly → Wilmington NC → Knoxville TN. This northeastern corridor captures the #2 cluster with less total value but still significant deals.

---

## Key Assumptions to Challenge (for your review)

1. **Network-first strategy** — Should we prioritize closing network HQs (DM Clinical, Alcanza) over visiting more individual sites?
2. **TX Week 1 + FL Week 2** — Is this the right ordering, or should we lead with FL (Alcanza = competitor customer = warmest lead)?
3. **Excluding CA entirely** — California has high revenue-per-site but low density. Worth including even 2-3 days?
4. **Pre-trip outreach assumption** — We assume Clay contact data enables email/LinkedIn outreach before the trip. Should we build this into the deliverable?
5. **Revenue sweet spot $1M-$15M** — This is our assumed ICP range. Too low = no budget, too high = doesn't need help. Correct?
6. **"Lucrative AND Sensible" framework** — Is this the right 2x2 for evaluating targets, or should we add another dimension (e.g., urgency, competitive threat)?
7. **AMR Knoxville ($34M) left on the table** — This is the highest-revenue single hot lead site. Should we find a way to include TN despite being off-route?
