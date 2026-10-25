# Service model and rollout for Hyderabad

---

## 1. The service model

### From call to dispatched vehicle
The end-to-end workflow connects citizens, the Telangana 108 / 112 Emergency Operations Center, AI prediction engines, and ambulance crews:

```text
[Citizen Dials 108 / 112] ──> [Telangana ERSS Dispatcher Logs Incident & Location]
                                           │
                                           ▼
                    [Project RUSH HOUR AI Cloud Microservice]
         - Ingests Hyderabad Traffic Police (HTP) & sensor telemetry
         - Computes cell cost surface & safety blocking mask
         - Solves kinematic Dijkstra route J(P) in <200ms
                                           │
                                           ▼
                 [Dispatcher Terminal: 108 CAD Route Overlay]
         - Displays recommended route, estimated travel cost, & warnings
         - Dispatcher verifies and assigns to nearest available 108 unit
                                           │
                                           ▼
                 [In-Cab Tablet: Turn-by-Turn Navigation]
         - Pilot 108 ambulance navigates; driver retains override authority
         - Arrival timestamp and telemetry logged to GHMC Smart City audit ledger
```

### Where humans stay in the loop
- **108 Dispatcher Review:** Dispatchers inspect the recommended route on CAD terminals alongside active traffic advisories from Hyderabad Traffic Police.
- **Pilot Driver / Paramedic Override:** Ambulance pilots retain visual authority to bypass recommended turns based on real-time waterlogging, local VIP movement, or construction diversions.
- **Failover / Manual Fallback:** If cellular network drops, in-cab tablets automatically fail over to preloaded offline GIS shortest-distance routing.

### Channels
- **Phase 1 (Current):** Dial 108 (Medical) / 112 (National ERSS) emergency calls.
- **Phase 2 (Future):** Integration with the *T-Safe* emergency app and GHMC Citizen Services portal.

### Who runs what in Hyderabad

| Function | Run by | Notes |
| :--- | :--- | :--- |
| **Call Handling & CAD** | Telangana ERSS (112 / 108 Center) | Operating under Department of Health & Family Welfare |
| **AI Routing Engine** | Cloud AI Vendor (SaaS Platform) | Managed cloud infrastructure, 99.99% uptime SLA |
| **Emergency Fleet** | Contracted Ambulance Operator (e.g. GVK EMRI) | Frontline 108 Advanced & Basic Life Support ambulances |
| **Telemetry & Traffic Feeds** | Hyderabad Traffic Police (HTP) & GHMC Smart City Command Center | Junction cameras, automated number plate recognition (ANPR), GPS probes |

---

## 2. Rollout

### Pilot
- **Location:** High-Traffic Zone 1: **Hitec City – Madhapur – Gachibowli IT Corridor**.
- **Duration:** 6 Months.
- **Rationale:** Highest peak-hour vehicular density in Telangana, multi-tier flyovers, metro rail feeder congestion, and heavy demand for emergency trauma transit to major hospitals (Continental, AIG, Care Gachibowli).

### Phases and go/no-go criteria

| Phase | Scope | Duration | Go/No-Go Criteria to Move On |
| :--- | :--- | :--- | :--- |
| **1. Pilot** | Zone 1 (Hitec City / Gachibowli, 40 Ambulances) | Months 1–6 | Median response time reduced by $\ge 15\%$; override rate $<15\%$; zero vehicle entrapment incidents |
| **2. Expansion** | Zones 2–4 (Secunderabad, Begumpet, Charminar / Old City, 120 Ambulances) | Months 7–12 | Response time target met on $\ge 88\%$ of calls; CAD integration latency $<300$ ms |
| **3. City-Wide** | Entire Hyderabad Metropolitan Area (HMDA, 350+ Ambulances) | Month 13+ | Full municipal adoption; continuous monsoon and festival retrainings; annual review |

### Key Performance Indicators (KPIs)

| KPI | Measurement Methodology | Baseline (Assumed) | Target |
| :--- | :--- | :--- | :--- |
| **Median Response Time** | Call receipt timestamp to ambulance arrival on-scene | 14.5 minutes | **< 11.5 minutes (-21%)** |
| **Target Attainment Rate** | % of high-acuity calls answered within 10 minutes | 68.0% | **> 85.0%** |
| **Driver Override Rate** | % of AI route suggestions modified by drivers/dispatchers | 25.0% (initial) | **< 12.0%** |
| **Cost Per Call Handled** | Total amortized system cost divided by total responses | ₹1,950 | **₹1,480** |

*All baselines and targets are itemized in `docs/07_assumptions_log.md`.*
