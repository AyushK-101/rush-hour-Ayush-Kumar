# Stakeholder map: Hyderabad Metropolitan Region

| Stakeholder | What they need | What they fear or lose | Role in the service | Accountable for |
| :--- | :--- | :--- | :--- | :--- |
| **Citizens of Hyderabad** | Rapid ambulance arrival; reliable emergency medical care | Delay causing patient deterioration or loss of life | End beneficiaries / service users | Calling 108/112; providing accurate landmark information |
| **GHMC & Telangana Govt (Payer)** | Lower response times; fiscal accountability; high public trust | Budget overruns; public backlash if routes encounter bottlenecks | Funder, regulator, and procurement authority | Service funding, contract governance, public oversight |
| **108 / 112 CAD Dispatchers** | Intuitive route prompts without software lag | Blame for delays; confusing interface | Reviewers and dispatch coordinators | Validating CAD recommendations, alerting nearest units |
| **Contracted Fleet Operators (GVK EMRI)** | Fair reimbursement; predictable availability payments | Unrealistic SLAs; financial penalties for citywide gridlock | Fleet operators and employers of pilots/EMTs | Fleet maintenance, pilot readiness, vehicle uptime |
| **Ambulance Pilots & Paramedics** | Safe, collision-free transit around road closures | Getting trapped in narrow alleys; corner-cutting accidents | Frontline navigators and care providers | Safe driving, patient triage, feedback on road obstructions |
| **Hyderabad Traffic Police (HTP)** | Smooth corridor movement; zero spillover gridlock | Uncoordinated diversions causing secondary traffic jams | Traffic management and enforcement partners | Green corridor coordination, junction clearance, incident reporting |

---

## Who makes the final routing decision, and who is accountable if it goes wrong?
- **Final Decision Authority:** The frontline ambulance pilot and 108 dispatcher retain absolute authority to accept, modify, or override the AI recommendation.
- **Accountability:** 
  - If a pilot follows the AI route and encounters an unnotified blockage, the incident is classified as a *Systemic Telemetry Anomaly* (owned jointly by GHMC IT and Vendor; no operator penalty).
  - If a pilot overrides the route without justification and incurs delay, the operator is accountable under SLA metrics.

---

## Conflicts between stakeholders & resolution
- **Speed vs. Safety:** Urgent transit vs. avoiding risky corner cutting in narrow streets. *Resolution:* Enforce Slide 85 diagonal invariants and set safety threshold $\tau = 0.18$.
- **Cost vs. Readiness:** City seeks lower per-call expenditure; operators need guaranteed availability income. *Resolution:* 85/15 hybrid availability payment model.
