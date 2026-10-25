# Funding and cost model (Hyderabad / INR Context)

---

## 1. Who pays for what

The Greater Hyderabad Municipal Corporation (GHMC) and the Government of Telangana fund the central AI platform and telemetry feeds under the Smart City Mission. Fleet operators (such as GVK EMRI 108 services) run and maintain emergency vehicles, receiving compensation under performance-linked state contracts.

| Item | Paid by | Payment Mechanism |
| :--- | :--- | :--- |
| **AI Routing Microservice & Cloud Compute** | GHMC / Telangana Smart City Mission | Annual SaaS license with high-availability cloud tier |
| **Ambulance Response Services (108 Fleet)** | Government of Telangana (Health Dept.) | Hybrid: Base Monthly Availability Fee (85%) + Performance Bonus (15%) |
| **Real-time Traffic & Telemetry Feeds** | Hyderabad Traffic Police & GHMC | Inter-departmental public data sharing agreement |
| **108 Dispatch Operations Staff & Training** | State Emergency Management Budget | Regular departmental operating budget |

---

## 2. How the government pays the operators

We evaluated three commercial reimbursement structures:

| Approach | How it works | Pros | Cons | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **A. Pure Per-Trip Fee** | Operator is paid fixed rupee amount per call attended (e.g. ₹1,800/call) | Simple billing; volume alignment | Incentivizes speeding; penalizes crews serving gridlocked zones | Rejected |
| **B. Fixed Annual Budget** | Lump-sum annual grant regardless of speed or volume | Budget certainty for state | No incentive to optimize routing or achieve response-time SLAs | Rejected |
| **C. Hybrid Availability + SLA Bonus** | 85% base availability fee + 15% incentive bonus for on-time arrival | Guarantees fleet readiness while driving performance and route compliance | Requires transparent CAD audit logging | **RECOMMENDED** |

**Recommendation:** Model C. An 85% monthly availability fee guarantees vehicle maintenance, fuel, and paramedic salaries, while the 15% performance bonus rewards operating clusters that maintain $>85\%$ on-time SLA compliance and $<12\%$ unnecessary route overrides.

---

## 3. Contract terms to require

1. **Service Levels (SLA):** Median response time $<11.5$ minutes for Priority 1 medical emergencies in Zone 1.
2. **Data Sharing & Telemetry Rights:** Operators must stream real-time GPS coordinates (1 Hz), vehicle status, and in-cab navigation logs into the GHMC Command and Control Centre.
3. **Audit Rights:** GHMC and Hyderabad Traffic Police retain audit rights over dispatch timestamps and telematics logs.
4. **Penalties:** Failure to achieve $75\%$ baseline response SLA results in a $5\%$ deduction from monthly availability disbursements.

---

## 4. Pilot cost estimate (6 Months, Zone 1: Hitec City Corridor)

*Currency: Indian Rupees (INR ₹). Target Fleet: 40 Frontline 108 Ambulances across 6 months.*

| Cost Item | Quantity | Unit Cost | Total Cost (INR) | Assumption / Justification |
| :--- | :--- | :--- | :--- | :--- |
| **Cloud Software & AI Compute** | 6 Months | ₹10,00,000 / mo | ₹60,00,000 | High-availability inference cluster, 99.99% uptime |
| **108 CAD Integration & APIs** | 1 Deployment | ₹95,00,000 lump | ₹95,00,000 | Custom API connectors with Telangana 108 dispatch system |
| **In-Cab Ruggedized Tablets & Mounts** | 40 Vehicles | ₹1,60,000 / unit | ₹64,00,000 | 4G/5G ruggedized tablets, GPS units, heavy-duty vehicle mounts |
| **Telemetry Feeds & SIM Bandwidth** | 6 Months | ₹8,00,000 / mo | ₹48,00,000 | Hyderabad Traffic Police camera telemetry & secure cellular data |
| **Dispatcher & Paramedic Training** | 150 Staff | ₹40,000 / trainee | ₹60,00,000 | Comprehensive simulation drills and route adherence training |
| **Contingency & Audit Reserve** | Fixed ~18% | — | ₹68,00,000 | Onboarding buffers, hardware replacements, and legal review |
| **TOTAL PILOT COST** | — | — | **₹3,95,00,000** | **₹3.95 Crore (All-inclusive 6-Month Pilot)** |

---

## 5. Expected value to Hyderabad

- **Zone 1 Call Volume:** Hitec City / Madhapur zone records approximately 28,000 emergency calls annually (14,000 during the 6-month pilot).
- **Time Saved:** Observed 27.8% reduction in travel cost translates to an estimated **3.0 to 4.5 minutes saved per high-acuity call**.
- **Clinical & Economic Return:** Emergency medicine benchmarks show that every 1-minute reduction in cardiac arrest and polytrauma response increases survival by up to 10%. Over 14,000 calls, this yields an estimated **40 to 50 additional lives saved annually**, preventing catastrophic socio-economic loss for families across Hyderabad.
