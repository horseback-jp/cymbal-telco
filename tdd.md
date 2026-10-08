# Technical Design Document (TDD) — Cymbal Telecom Converged Commerce & Care (`cymbal_converged_commerce_demo`)

> This is a **living document** — update it whenever requirements, agent behavior, or evals change.
> Update the TDD first, then update evals to match.

## Overview & Target Deployment

- **Application Display Name:** `[jph]cymbal-converged-commerce-demo`
- **Local App Directory Name:** `cymbal_converged_commerce_demo`
- **GCP Project / Location:** `ces-demo-emea` / `eu`
- **Primary Source Artifact:** `sources/converged-bundle-prd.md` (*Cymbal Telecom — Consultative Commerce & Care (Multi-Product Home Convergence Bundle) PRD*)
- **Demo Objective (PRD §1):**
  > "Instead of treating a customer's entry as a rigid, reactive support form or pitching a single standalone hardware add-on, this demo showcases how **Google's Customer Engagement Suite (CXAS / GECX)** uses **Cymbal Elysium** (Cymbal Telecom's BigQuery-backed Customer Data Platform) to:
  > 1. Instantly recognize customer context, active tariff, and live home network telemetry.
  > 2. Defuse frustration immediately by proactively resolving a **£12.00 duplicate billing error** in the first response while diagnosing router hardware drops and Wi-Fi dead zones.
  > 3. Turn a service failure into **high-value multi-product basket expansion (+25% bundle discovery / ARPU expansion)** by constructing a bespoke **3-Pillar Tailored Home Bundle ("Cymbal One Converged Home Bundle")** that upgrades the customer from an out-of-contract **£44.00/mo** single-play broadband plan to an all-in-one **£68.00/mo** converged household bundle (saving **£22.00/mo** vs. £90.00/mo standalone).
  > 4. Drive both **native CXAS Rich Response Widgets (`widgetTool`)** inside the conversation and **CXAS Client Functions (`clientFunction`)** that dynamically update the clean, consumer-grade **Cymbal Telecom Main Web UI** (3-Pillar Bundle Showcase, Illustrative Home Wi-Fi Mesh Coverage Map, and 1-Click Multi-Item Basket + Pre-Provisioned ServiceNow Engineer Handover)."

---

## Agent Design

### 1. Architecture

#### Modality, Model & Voice Configuration (PRD §2)
- **Modality:** Bidirectional Voice + Multimodal Web Storefront Synchronization (`audio` + `text` + `widgetTool` + `clientFunction`).
- **Model:** `gemini-composite-v1` (`temperature: 1.0`).
- **Language & Locale:** `en-GB` (`enableMultilingualSupport: false`), timezone `Europe/London`.
- **Voice Configuration:** `en-GB-Chirp3-HD-Zephyr` with full Composite V1 `# Audio Profile` and `# Director's note` header (`* Accent: British English`, natural British conversational phrasing, GBP `£` readouts as "pounds", concise 2–3 sentence spoken turns, and trailing `## Transcript:\n` hook).
- **Brand Guardrail:** Strictly **Cymbal Telecom** UK branding (never reference BT, EE, or Openreach).
- **Storefront Aesthetic:** Clean, airy, consumer-grade UK telco design (white background `#F5F7F8`, dark navy top utility bar `#0D1B24`, teal `#00838F` and coral-orange `#FF5722` accents).

#### Agent Hierarchy (PRD §2)
- **Single-Agent Architecture:**
  - **Root Agent (`cymbal_converged_concierge`):** `childAgents: []` (26 characters; complies with CES resource ID regex `[a-zA-Z0-9][a-zA-Z0-9-_]{4,35}`).
  - **Scope & Justification:** As specified in PRD §2 (*"Single unified agent (`cymbal_converged_concierge` as `rootAgent`) owning the entire linear 4-step Care-to-Converged-Bundle journey with zero lossy sub-agent handoffs"*), a single agent eliminates transfer latency and context loss between billing care, live telemetry diagnostics, consultative multi-product bundle assembly, coverage map visualization, and 1-click checkout + ServiceNow engineer pre-provisioning.

```
app.json (rootAgent: "cymbal_converged_concierge")
└── cymbal_converged_concierge (childAgents: [])
    ├── resolve_billing_and_diagnostics (pythonFunction)
    ├── build_tailored_home_bundle (pythonFunction)
    ├── complete_converged_checkout (pythonFunction)
    ├── show_product_carousel (widgetTool: PRODUCT_CAROUSEL)
    ├── show_product_comparison (widgetTool: PRODUCT_COMPARISON)
    ├── update_storefront_ui (clientFunction)
    └── end_session (system tool)
```

---

### 2. Tools

All tool resource IDs strictly obey the CES platform length constraint (`[a-zA-Z0-9][a-zA-Z0-9-_]{4,35}`, max 36 characters). Note: The PRD's `complete_converged_checkout_and_servicenow` (42 chars) is named `complete_converged_checkout` (27 chars) to comply with the 36-character platform limit while preserving 100% of its functional behavior and state mutations.

| Tool Name | Chars | Type | Purpose & Source Justification |
|-----------|-------|------|--------------------------------|
| `resolve_billing_and_diagnostics` | 31 | `pythonFunction` | **PRD §4 Step 1:** Queries Elysium CDP for `customer_id`, confirms `Out-of-Contract Fibre 100 (£44.00/mo)` profile, retrieves `4 packet-drop events in 24h` across `14 devices` (`850 GB/mo`), executes instant **£12.00 auto-refund** (`INV-8841` duplicate Cyber Security charge) to `Visa-4412`, sets `billing_refund_status = "refunded_12_gbp"` and `journey_stage = "care_resolved"`, and returns the `account_diagnostics` UI payload. |
| `build_tailored_home_bundle` | 26 | `pythonFunction` | **PRD §4 Step 2:** Constructs the **3-Pillar Cymbal One Converged Home Bundle** (`BUNDLE-CYMBAL-ONE-HOME` at `£68.00/mo`, saving `£22.00/mo` vs. `£90.00/mo` standalone), populates `active_widget_data` with all 3 product cards (`Cymbal Full Fibre 900`, `Complete Wi-Fi Guarantee (3 Smart Discs + 4G Backup)`, `Cymbal TV Sport & Xbox Game Pass Ultimate`) formatted for `show_product_carousel` or `show_product_comparison`, sets `journey_stage = "bundle_pitched"`, and returns both the `widget_payload` and `storefront_payload`. |
| `complete_converged_checkout` | 27 | `pythonFunction` | **PRD §4 Step 4:** Injects all 3 bundled product pillars plus the `-£12.00` `INV-8841` instant refund credit and free priority engineer installation (`£0.00`) into `basket_state`; pre-provisions ServiceNow ticket `INC-904821` (`Thursday, 10:00 AM – 12:00 PM`) with router telemetry (`4 drops in 24h`), 3-disc placement plan, and omnichannel continuity summary in `servicenow_handover_payload`; sets `journey_stage = "checkout_complete"`. |
| `show_product_carousel` | 21 | `widgetTool` | **PRD §1 & §4 Step 2:** Native CXAS Rich Response Widget (`widgetType: "PRODUCT_CAROUSEL"`, `textResponseConfig: {"type": "LLM_GENERATED"}`) rendering the 3-pillar bundle cards inside the chat transcript. |
| `show_product_comparison` | 23 | `widgetTool` | **PRD §3 & §4 Step 2:** Native CXAS Rich Response Widget (`widgetType: "PRODUCT_COMPARISON"`, `textResponseConfig: {"type": "LLM_GENERATED"}`) rendering a side-by-side comparison between Geoff's Out-of-Contract Fibre 100 (`£44.00/mo`), Standalone Upgrades (`£90.00/mo`), and the Cymbal One Converged Home Bundle (`£68.00/mo`). |
| `update_storefront_ui` | 20 | `clientFunction` | **PRD §1 & §4 Steps 1–4:** Synchronizes the main Cymbal Telecom web storefront across four views: `account_diagnostics` (Step 1), `tailored_bundle_showcase` (Step 2), `mesh_coverage_map` with `view_mode="after_mesh_coverage"` or `"before_dead_zones"` (Step 3), and `checkout_and_servicenow` (Step 4). |
| `end_session` | 11 | `system` | Built-in CES system tool to cleanly terminate the session after checkout confirmation and final user sign-off. |

#### Detailed Tool Schemas & State Contracts

##### 2.1 `resolve_billing_and_diagnostics` (`pythonFunction`)
- **Input Schema:**
  - `customer_id` (`string`, optional, default `"CUST-GEOFF-001"`): Customer identifier in Cymbal Elysium CDP.
- **Session Variable Mutations (`context.variables`):**
  - `billing_refund_status` -> `"refunded_12_gbp"`
  - `journey_stage` -> `"care_resolved"`
- **Return Schema (`dict`):**
  - `status`: `"success"`
  - `customer_id`: `"CUST-GEOFF-001"`
  - `customer_name`: `"Geoffrey Horsfield (Geoff)"`
  - `refund_executed`: `{"invoice_id": "INV-8841", "amount_gbp": 12.00, "reason": "Duplicate Cymbal Cyber Security Add-On charge", "payment_method": "Visa ending 4412", "status": "refunded_12_gbp"}`
  - `telemetry_diagnosis`: `{"router_model": "Smart Hub 2", "mesh_discs": 0, "connected_devices": 14, "monthly_usage_gb": 850, "packet_drops_24h": 4, "weak_zones": ["Rear Kitchen-Diner (-79 dBm)", "Upstairs Back Bedrooms (-82 dBm)"], "exchange_status": "MANCHESTER-SOUTH-EX04: GREEN"}`
  - `current_plan`: `{"name": "Fibre 100", "contract_status": "Out of Contract", "monthly_price_gbp": 44.00}`
  - `storefront_payload_json`: JSON string ready to pass to `update_storefront_ui(view="account_diagnostics", payload_json=...)`.

##### 2.2 `build_tailored_home_bundle` (`pythonFunction`)
- **Input Schema:**
  - `customer_id` (`string`, optional, default `"CUST-GEOFF-001"`): Customer identifier.
  - `view_type` (`string`, optional, default `"carousel"`): `"carousel"` for `show_product_carousel` or `"comparison"` for `show_product_comparison`.
- **Session Variable Mutations (`context.variables`):**
  - `active_widget_data` -> JSON string containing the formatted `products` array (and comparison columns when `view_type == "comparison"`) for the 3-Pillar Cymbal One Converged Home Bundle.
  - `journey_stage` -> `"bundle_pitched"`
- **Return Schema (`dict`):**
  - `status`: `"success"`
  - `bundle_id`: `"BUNDLE-CYMBAL-ONE-HOME"`
  - `bundle_name`: `"Cymbal One Converged Home Bundle"`
  - `pricing_summary`: `{"old_price_gbp": 44.00, "standalone_total_gbp": 90.00, "bundle_price_gbp": 68.00, "monthly_savings_gbp": 22.00}`
  - `widget_payload`: `dict` containing the `products` list for immediate invocation of `show_product_carousel` or `show_product_comparison`:
    1. **Card 1 (`ITEM-FIBRE-900`):** Title `"Cymbal Full Fibre 900"`, Subtitle `"Included (£68/mo Bundle) • Standalone £55/mo"`, Description `"900 Mbps Symmetrical • Smart Hub 3 • Zero-Lag Gaming"`.
    2. **Card 2 (`ITEM-COMPLETE-WIFI`):** Title `"Complete Wi-Fi Guarantee (3 Smart Discs + 4G Backup)"`, Subtitle `"Included (£68/mo Bundle) • Standalone £20/mo"`, Description `"3 Wi-Fi 6E Mesh Discs + Hybrid 4G Failover • Zero Dead Zones"`.
    3. **Card 3 (`ITEM-TV-XBOX-SECURITY`):** Title `"Cymbal TV Sport & Xbox Game Pass Ultimate"`, Subtitle `"Included (£68/mo Bundle) • Standalone £15/mo"`, Description `"Xbox Game Pass Ultimate for Kids + 4K Family Sports + Cyber Security"`.
  - `storefront_payload_json`: JSON string ready to pass to `update_storefront_ui(view="tailored_bundle_showcase", payload_json=...)`.

##### 2.3 `complete_converged_checkout` (`pythonFunction`)
- **Input Schema:**
  - `customer_id` (`string`, optional, default `"CUST-GEOFF-001"`): Customer identifier.
  - `confirm_upgrade` (`string`, optional, default `"true"`): Confirmation flag (`"true"`).
- **Session Variable Mutations (`context.variables`):**
  - `basket_state` -> JSON string containing all 3 bundled pillars (`ITEM-FIBRE-900`, `ITEM-COMPLETE-WIFI`, `ITEM-TV-XBOX-SECURITY`), `-£12.00` `INV-8841` instant refund credit, `£0.00` priority engineer installation, `£68.00/mo` recurring total, and `£22.00/mo` bundle savings.
  - `servicenow_handover_payload` -> JSON string containing `ticket_id: "INC-904821"`, `appointment_slot: "Thursday, 10:00 AM – 12:00 PM"`, `engineer_tier: "Priority Cymbal Fibre & Mesh Specialist"`, attached telemetry (`4 packet drops in 24h`, `14 devices`, `850 GB/mo`), 3-disc house placement plan (`Hallway`, `Kitchen-Diner`, `Upstairs Landing`), and omnichannel continuity summary.
  - `journey_stage` -> `"checkout_complete"`
- **Return Schema (`dict`):**
  - `status`: `"success"`
  - `order_id`: `"ORD-CYM-904821"`
  - `basket`: parsed `basket_state` dictionary
  - `servicenow_ticket`: parsed `servicenow_handover_payload` dictionary (`INC-904821`)
  - `storefront_payload_json`: JSON string ready to pass to `update_storefront_ui(view="checkout_and_servicenow", payload_json=...)`.

##### 2.4 `update_storefront_ui` (`clientFunction`)
- **Input Schema:**
  - `view` (`string`, required): Target storefront view state. Enum values:
    - `"account_diagnostics"` (Step 1: Live Diagnostics & £12.00 Instant Refund Confirmed banner)
    - `"tailored_bundle_showcase"` (Step 2: "GEOFF'S TAILORED HOME BUNDLE" 3-pillar showcase)
    - `"mesh_coverage_map"` (Step 3: Illustrative 4-bedroom Home Wi-Fi Mesh Coverage diagram)
    - `"checkout_and_servicenow"` (Step 4: 1-Click Multi-Product Order Confirmation + ServiceNow `INC-904821` card)
  - `view_mode` (`string`, optional): Sub-view toggle used by `mesh_coverage_map` (`"after_mesh_coverage"` default or `"before_dead_zones"`).
  - `payload_json` (`string`, optional): Structured JSON string with view-specific telemetry, bundle pillars, coverage nodes, or basket/ServiceNow confirmation details.

---

### 3. Routing Logic & Linear 4-Step Taskflow

Because the application uses a **single unified agent** (`cymbal_converged_concierge` with `childAgents: []`), there are no inter-agent transfers. Instead, the agent progresses deterministically through a **Linear 4-Step Care-to-Converged-Bundle Taskflow** tracked by `journey_stage` (`"discovery"` -> `"care_resolved"` -> `"bundle_pitched"` -> `"coverage_visualized"` -> `"checkout_complete"`):

1. **Step 1 — Empathetic Care, Instant £12.00 Refund & Live Telemetry Diagnosis ("The Trust Builder") (PRD §4 Step 1):**
   - **Trigger:** Geoff reports broadband dropouts in the kitchen, teenage kids lagging on Xbox consoles upstairs, and/or an overcharge on his recent bill.
   - **Action Sequence:**
     1. Call `resolve_billing_and_diagnostics(customer_id="CUST-GEOFF-001")`.
     2. Call `update_storefront_ui(view="account_diagnostics", payload_json=...)`.
     3. Deliver a concise 2–3 sentence empathetic response confirming the **£12.00 duplicate charge (`INV-8841`) has already been refunded to his Visa ending 4412**, explaining the live telemetry finding (`Smart Hub 2` had `4 packet drops in 24h` across `14 devices` and `850 GB/mo`, with weak signal in the kitchen-diner and upstairs back bedrooms while the local Manchester South exchange is green), and pivoting consultatively:
        > *"Let's not just patch it — I can put together a tailored all-in-one home bundle that upgrades your speeds, blankets every room in guaranteed Wi-Fi, and includes gaming for the kids. Would you like to see what I've put together for your home?"*

2. **Step 2 — Personalised Multi-Product Basket Expansion ("Geoff's Tailored Home Bundle") (PRD §4 Step 2):**
   - **Trigger:** Geoff agrees to see the recommendation or asks how to fix his home setup.
   - **Action Sequence:**
     1. Call `build_tailored_home_bundle(customer_id="CUST-GEOFF-001", view_type="carousel")` (or `"comparison"` if Geoff specifically asks for a side-by-side price comparison table).
     2. Call native widget tool `show_product_carousel` (or `show_product_comparison`) using the `widget_payload` from `build_tailored_home_bundle`.
     3. Call `update_storefront_ui(view="tailored_bundle_showcase", payload_json=...)`.
     4. Deliver the 2–3 sentence consultative upsell pitch (PRD §4 Step 2):
        > *"Because your family games and streams heavily, I've built a tailored Cymbal One bundle combining three upgrades: Full Fibre 900 for ultra-stable speeds, our Complete Wi-Fi Guarantee with three Smart Mesh Discs and 4G backup, plus Cymbal TV Sport and Xbox Game Pass Ultimate for the kids. Instead of £90 a month separately, you get all three together for our converged rate of £68 a month — saving you £22 every month. Would you like to see on your screen how the three discs cover your kitchen and upstairs bedrooms, or shall we add the bundle straight to your basket?"*

3. **Step 3 — Illustrative Home Wi-Fi Mesh Coverage Visualisation & Consultative Q&A (PRD §4 Step 3):**
   - **Trigger:** Geoff asks how the 3 Smart Wi-Fi Discs will work in his house (kitchen-diner extension and upstairs back bedrooms) or asks to see the coverage map.
   - **Action Sequence:**
     1. Call `update_storefront_ui(view="mesh_coverage_map", view_mode="after_mesh_coverage", payload_json=...)`.
     2. Explain in 2–3 sentences how placing **Disc 1 in the hallway**, **Disc 2 in the rear kitchen-diner**, and **Disc 3 on the upstairs landing** eliminates the dead zones and gives the kids' Xbox consoles a rock-solid connection backed by automatic Hybrid 4G failover, then ask if he is ready to upgrade his home with this bundle.

4. **Step 4 — 1-Click Multi-Product Cart Injection & Zero-Friction ServiceNow Pre-Provisioning (PRD §4 Step 4):**
   - **Trigger:** Geoff confirms he wants to proceed (*"Yes, upgrade my home"* / *"Let's go ahead and add the bundle to my basket"*).
   - **Action Sequence:**
     1. Call `complete_converged_checkout(customer_id="CUST-GEOFF-001", confirm_upgrade="true")`.
     2. Call `update_storefront_ui(view="checkout_and_servicenow", payload_json=...)`.
     3. Confirm warmly in 2–3 sentences that the entire **Cymbal One Converged Home Bundle** (`Full Fibre 900`, `3 Smart Wi-Fi Discs with 4G Backup`, and `TV Sport & Xbox Game Pass Ultimate`) is in his checkout basket at **£68/month** with his **£12 refund credit** applied and free installation, and that **ServiceNow ticket `INC-904821`** has pre-scheduled a priority engineer for **Thursday between 10:00 AM and 12:00 PM** with his telemetry and 3-disc house map attached.
     4. When Geoff says goodbye or confirms he needs nothing else, deliver a warm farewell and call `end_session`.

---

### 4. Variables

All 12 session variables required by PRD §3 are declared in `app.json` under `variableDeclarations` with rich default values so the agent's consultative pitch is 100% grounded in session state from Turn 1.

> **Platform Constraint:** Never declare `current_date` in `app.json` `variableDeclarations` (reserved CES system variable).

| # | Variable Name | Schema Type | Source / Mutation Lifecycle | Default Value (Summary) | Eval Override Guidance |
|---|---------------|-------------|-----------------------------|-------------------------|------------------------|
| 1 | `customer_id` | `STRING` | Session parameter (`app.json` default) | `"CUST-GEOFF-001"` | May override in evals to test alternate profiles |
| 2 | `customer_name` | `STRING` | Session parameter (`app.json` default) | `"Geoffrey Horsfield (Geoff)"` | Keep default in standard Geoff evals |
| 3 | `household_profile` | `STRING` | Session parameter (`app.json` default) | `"4-bedroom home (14 Oakwood Avenue, Manchester, M20 2WQ) with rear kitchen-diner extension; Smart Hub 2 by front door in hallway; teenage kids gaming on Xbox consoles in upstairs back bedrooms"` | Keep default in standard Geoff evals |
| 4 | `current_broadband_plan` | `STRING` | Session parameter (`app.json` default) | `"Fibre 100 (100 Mbps download / 20 Mbps upload) — Out of Contract at £44.00/month"` | Keep default in standard Geoff evals |
| 5 | `network_telemetry_summary` | `STRING` | Session parameter (`app.json` default) | `"Smart Hub 2 (0 Mesh Discs) \| 850 GB/month usage across 14 connected devices \| 4 router packet-drop events in last 24h \| Weak RSSI (-79 to -82 dBm) in kitchen-diner and upstairs back bedrooms \| Local Exchange MANCHESTER-SOUTH-EX04: GREEN"` | Keep default in standard Geoff evals |
| 6 | `billing_discrepancy_details` | `STRING` | Session parameter (`app.json` default) | `"Invoice INV-8841 contains a £12.00 duplicate charge for Cymbal Cyber Security Add-On; eligible for instant auto-refund to Visa ending 4412"` | Keep default in standard Geoff evals |
| 7 | `billing_refund_status` | `STRING` | Default `"pending"`; updated to `"refunded_12_gbp"` by `resolve_billing_and_diagnostics` | `"pending"` | Override to `"refunded_12_gbp"` only in mid-journey evals starting at Step 2+ |
| 8 | `tailored_bundle_config` | `STRING` (JSON) | Session parameter (`app.json` default) | JSON string for `BUNDLE-CYMBAL-ONE-HOME` (`£68.00/mo`, save `£22.00/mo` vs. `£90.00/mo` standalone) across `ITEM-FIBRE-900` (`£55`), `ITEM-COMPLETE-WIFI` (`£20`), and `ITEM-TV-XBOX-SECURITY` (`£15`) | Keep default in standard Geoff evals |
| 9 | `active_widget_data` | `STRING` (JSON) | Default pre-populated 3-card JSON; refreshed by `build_tailored_home_bundle` | JSON string holding the 3-pillar widget payload for `show_product_carousel` / `show_product_comparison` | Updated by tool; do not manually override unless testing Step 3/4 in isolation |
| 10 | `journey_stage` | `STRING` | Default `"discovery"`; mutated by Python tools (`"care_resolved"` -> `"bundle_pitched"` -> `"checkout_complete"`) | `"discovery"` | Set to match starting step in single-turn/mid-journey evals |
| 11 | `basket_state` | `STRING` (JSON) | Default empty/initial cart JSON; populated by `complete_converged_checkout` | JSON string holding `items: []` initially, then populated with all 3 pillars + `-£12.00` credit + `£0.00` install (`£68.00/mo`) | Updated by `complete_converged_checkout` |
| 12 | `servicenow_handover_payload` | `STRING` (JSON) | Default pre-staged template JSON; finalized by `complete_converged_checkout` | JSON string for `INC-904821` (`Thursday, 10:00 AM – 12:00 PM`, telemetry + 3-disc placement + omnichannel handover) | Updated by `complete_converged_checkout` |

---

### 5. Callbacks

No agent callbacks (`before_agent_callback`, `before_model_callback`, `after_model_callback`, `after_agent_callback`) are proposed for `cymbal_converged_concierge`.

- **Rationale:**
  1. All 12 customer context, telemetry, billing, and bundle catalog variables are pre-populated via `app.json` `variableDeclarations` defaults (simulating Cymbal Elysium CDP session injection at call/chat start).
  2. All state transitions (`billing_refund_status`, `active_widget_data`, `journey_stage`, `basket_state`, `servicenow_handover_payload`) are executed deterministically inside the three `pythonFunction` tools (`resolve_billing_and_diagnostics`, `build_tailored_home_bundle`, `complete_converged_checkout`).
  3. Avoiding unnecessary callbacks prevents interference with native `widgetTool` (`show_product_carousel`, `show_product_comparison`) and `clientFunction` (`update_storefront_ui`) tool-call chains.

---

## Eval Design

### 6. Coverage Map

Every requirement in `sources/converged-bundle-prd.md` maps to deterministic Golden conversations, multi-turn Scenario Simulations, and isolated Python Tool Tests:

| Requirement | Source Reference | Eval Type | Rationale | Priority | Severity | Tags |
|-------------|------------------|-----------|-----------|----------|----------|------|
| **Full 4-Step Care-to-Converged-Bundle Happy Path** (Refund £12 + Telemetry Diagnosis -> 3-Pillar Carousel + Storefront Showcase -> Mesh Coverage Map -> 1-Click Checkout + ServiceNow `INC-904821`) | PRD §4 Steps 1–4 | **Golden** (`golden_full_converged_journey.yaml`) | Tool call sequence (`resolve_billing_and_diagnostics` + `update_storefront_ui` -> `build_tailored_home_bundle` + `show_product_carousel` + `update_storefront_ui` -> `update_storefront_ui(mesh_coverage_map)` -> `complete_converged_checkout` + `update_storefront_ui(checkout_and_servicenow)`) is strictly deterministic. | P0 | NO-GO | `happy-path, four-step-journey, PRD-4.1, PRD-4.2, PRD-4.3, PRD-4.4, P0` |
| **Step 1 Trust Builder: Instant £12.00 Refund & Telemetry Diagnosis** (Single-turn / focused verification of `INV-8841` auto-refund + 4 packet drops + consultative pivot) | PRD §4 Step 1 | **Golden** (`golden_step1_care_and_refund.yaml`) | Deterministic tool invocation (`resolve_billing_and_diagnostics` + `update_storefront_ui(view="account_diagnostics")`) and mandatory spoken data points (£12.00 refund to Visa 4412, 4 drops in 24h, 14 devices). | P0 | NO-GO | `step-1, billing-refund, telemetry, PRD-4.1, P0` |
| **Step 2 Price Comparison Variant (`show_product_comparison`)** (Customer asks how the £68/mo bundle compares against his £44/mo out-of-contract plan and £90/mo standalone pricing) | PRD §3 & §4 Step 2 | **Golden** (`golden_step2_bundle_comparison.yaml`) | Deterministic branching when customer requests a price comparison table (`build_tailored_home_bundle(view_type="comparison")` + `show_product_comparison` + `update_storefront_ui(view="tailored_bundle_showcase")`). | P1 | HIGH | `step-2, comparison-widget, bundle-pricing, PRD-4.2, P1` |
| **Direct Express Upgrade & Session Termination** (Customer accepts the bundle immediately after seeing the pitch and signs off cleanly with `end_session`) | PRD §4 Steps 2 & 4 | **Golden** (`golden_express_checkout_and_close.yaml`) | Verifies deterministic 1-click checkout (`complete_converged_checkout` + `update_storefront_ui(view="checkout_and_servicenow")`) followed by polite farewell and `end_session`. | P1 | HIGH | `step-4, checkout, servicenow, end-session, PRD-4.4, P1` |
| **Consultative Skeptical Customer Simulation** (Geoff is initially frustrated about the £12 overcharge and skeptical about paying £24/mo more than £44/mo until he hears the £22/mo savings vs £90/mo standalone and mesh coverage explanation) | PRD §1, §2, §4 Steps 1–4 | **Sim** (`sim_frustrated_to_converged_upgrade`) | Tests multi-turn conversational resilience, British English consultative tone, value justification (£68/mo vs £90/mo standalone), and complete 4-step progression under realistic user pushback (`max_turns: 8`). | P0 | HIGH | `sim, consultative-selling, objection-handling, PRD-1, PRD-4, P0` |
| **Mesh Placement & Hybrid 4G Failover Deep-Dive Simulation** (Geoff asks detailed questions about his rear kitchen-diner extension and kids' Xbox lag upstairs before agreeing to checkout) | PRD §4 Steps 3–4 | **Sim** (`sim_mesh_coverage_and_gaming_qa`) | Phrasing of technical Q&A varies naturally while requiring `update_storefront_ui(view="mesh_coverage_map")` and accurate 3-disc placement explanation (Hallway, Kitchen-Diner, Upstairs Landing) before checkout (`max_turns: 8`). | P1 | MEDIUM | `sim, mesh-coverage, gaming-qa, PRD-4.3, P1` |
| **Isolated Python Tool Unit Tests** (`resolve_billing_and_diagnostics`, `build_tailored_home_bundle`, `complete_converged_checkout`) | PRD §3 & §4 | **Tool Tests** (`evals/tool_tests/*.yaml`) | Verifies deterministic state mutations (`billing_refund_status`, `active_widget_data`, `journey_stage`, `basket_state`, `servicenow_handover_payload`) and JSON payload structures in isolation. | P0 | NO-GO | `tool-test, state-mutation, PRD-3, P0` |

---

### 7. Test Data (Customer Profiles)

Derived directly from **PRD §2 & §3** (Cymbal Elysium CDP pre-populated profile for Geoff):

| Profile Name | `customer_id` | `customer_name` | Current Plan & Billing Issue | Telemetry & Household Context | Target Bundle & ServiceNow Handover |
|--------------|---------------|-----------------|------------------------------|-------------------------------|-------------------------------------|
| **Geoff — Tech-Heavy Family Home (Primary Persona)** | `CUST-GEOFF-001` | `Geoffrey Horsfield (Geoff)` | `Fibre 100` (Out of Contract at `£44.00/mo`); `INV-8841` has `£12.00` duplicate Cymbal Cyber Security charge (`Visa-4412`) | `14 Oakwood Avenue, Manchester, M20 2WQ` (4-bed + rear kitchen-diner extension); `Smart Hub 2` (0 discs), `14 devices`, `850 GB/mo`, `4 packet drops in 24h`, `-79 to -82 dBm` in kitchen & upstairs bedrooms; Exchange `MANCHESTER-SOUTH-EX04: GREEN` | `BUNDLE-CYMBAL-ONE-HOME` (`£68.00/mo`, save `£22.00/mo` vs `£90.00/mo` standalone): Full Fibre 900 + 3 Smart Wi-Fi 6E Discs & 4G Backup + TV Sport & Xbox Game Pass Ultimate; ServiceNow `INC-904821` (`Thursday, 10:00 AM – 12:00 PM`) |

---

## Build Steps

1. **Create `gecx-config.json` and App Scaffold (`cxas_app/cymbal_converged_commerce_demo/`):**
   - Configure `app.json` with `rootAgent: "cymbal_converged_concierge"`, `gemini-composite-v1`, `en-GB` (`en-GB-Chirp3-HD-Zephyr`), `Europe/London`, and all 12 `variableDeclarations` with rich default values.
2. **Implement Python Function Tools (`tools/`):**
   - `resolve_billing_and_diagnostics` (31 chars)
   - `build_tailored_home_bundle` (26 chars)
   - `complete_converged_checkout` (27 chars)
3. **Configure Rich Widget Tools & Client Function (`tools/`):**
   - `show_product_carousel` (`widgetTool`, `PRODUCT_CAROUSEL`, `LLM_GENERATED`)
   - `show_product_comparison` (`widgetTool`, `PRODUCT_COMPARISON`, `LLM_GENERATED`)
   - `update_storefront_ui` (`clientFunction`)
4. **Author Root Agent Configuration & Instruction (`agents/cymbal_converged_concierge/`):**
   - `cymbal_converged_concierge.json` binding the 6 custom tools + `end_session` and `childAgents: []`.
   - `instruction.txt` with Composite V1 `# Audio Profile` (`en-GB` British English), `# Director's note`, XML `<role>`, `<persona>`, `<constraints>`, `<taskflow>` (Steps 1–4), `<examples>`, and trailing `## Transcript:\n`.
5. **Create Evaluation Suite (`evals/`):**
   - Golden conversations in `evals/goldens/*.yaml`
   - Scenario simulations in `evals/simulations/simulations.yaml`
   - Isolated tool tests in `evals/tool_tests/*.yaml`
6. **Lint, Push & Verify on Platform:**
   - Run `cxas lint` and `cxas push` to `ces-demo-emea` (`eu`), then execute tool tests, goldens, and simulations.

---

## Pass Rate History

| Date | Goldens | Sims | Tool Tests | Callback Tests | Notes |
|------|---------|------|------------|----------------|-------|
| — | — | — | — | N/A | Not yet executed |

---

## Known Issues & Design Notes

- **CES Tool Resource ID Length Limit (`≤36` chars):** PRD §4 Step 4 refers to `complete_converged_checkout_and_servicenow` (42 characters), which exceeds the CES platform resource ID regex `[a-zA-Z0-9][a-zA-Z0-9-_]{4,35}` (max 36 characters). The tool is implemented as `complete_converged_checkout` (27 characters) with identical parameters (`customer_id`, `confirm_upgrade`), session variable updates (`basket_state`, `servicenow_handover_payload`, `journey_stage`), and ServiceNow `INC-904821` pre-provisioning behavior.
- **Reserved System Variable (`current_date`):** Per GECX platform rules, `current_date` is never declared in `app.json` `variableDeclarations`.

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-10-07 | Initial requirements-derived TDD draft (sources: `sources/converged-bundle-prd.md`). | TDD-Writer Agent |

Review and approve before scaffolding the agent.
