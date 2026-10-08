# Cymbal Telecom — Consultative Commerce & Care (Multi-Product Home Convergence Bundle) PRD

## 1. Executive Summary & Demo Objective

Instead of treating a customer's entry as a rigid, reactive support form or pitching a single standalone hardware add-on, this demo showcases how **Google's Customer Engagement Suite (CXAS / GECX)** uses **Cymbal Elysium** (Cymbal Telecom's BigQuery-backed Customer Data Platform) to:
1. Instantly recognize customer context, active tariff, and live home network telemetry.
2. Defuse frustration immediately by proactively resolving a **£12.00 duplicate billing error** in the first response while diagnosing router hardware drops and Wi-Fi dead zones.
3. Turn a service failure into **high-value multi-product basket expansion (+25% bundle discovery / ARPU expansion)** by constructing a bespoke **3-Pillar Tailored Home Bundle ("Cymbal One Converged Home Bundle")** that upgrades the customer from an out-of-contract **£44.00/mo** single-play broadband plan to an all-in-one **£68.00/mo** converged household bundle (saving **£22.00/mo** vs. £90.00/mo standalone).
4. Drive both **native CXAS Rich Response Widgets (`widgetTool`)** inside the conversation and **CXAS Client Functions (`clientFunction`)** that dynamically update the clean, consumer-grade **Cymbal Telecom Main Web UI** (3-Pillar Bundle Showcase, Illustrative Home Wi-Fi Mesh Coverage Map, and 1-Click Multi-Item Basket + Pre-Provisioned ServiceNow Engineer Handover).

---

## 2. Branding, Modality & Persona

- **Brand:** **Cymbal Telecom** (strictly Cymbal Telecom UK branding — never reference BT, EE, or Openreach).
- **Visual Storefront Aesthetic:** Clean, airy, consumer-grade UK telco design (white background `#F5F7F8`, dark navy top utility bar `#0D1B24`, teal `#00838F` and coral-orange `#FF5722` accents, large rounded cards with minimal text density).
- **Customer Persona:** **Geoff** (`Geoffrey Horsfield`, `customer_id = "CUST-GEOFF-001"`), father of a tech-heavy household in a 4-bedroom house (`14 Oakwood Avenue, Manchester, M20 2WQ`) with a rear kitchen-diner extension and teenage kids gaming on Xbox consoles in the upstairs back bedrooms.
- **Modality & Voice Architecture:**
  - **Model:** `gemini-composite-v1` (`temperature: 1.0`)
  - **Language:** `en-GB` (`enableMultilingualSupport: false`), timezone `Europe/London`
  - **Voice:** `en-GB-Chirp3-HD-Zephyr` with full Composite V1 `# Audio Profile` and `# Director's note` (`* Accent: British English`, natural British conversational phrasing, GBP readouts, and trailing `## Transcript:\n` hook).
  - **Agent Architecture:** Single unified agent (`cymbal_converged_concierge` as `rootAgent`) owning the entire linear 4-step Care-to-Converged-Bundle journey with zero lossy sub-agent handoffs.

---

## 3. Pre-Populated App Session Variables (Elysium CDP, Telemetry, Billing & Bundle Catalog)

All customer profile, usage, telemetry, billing, and multi-product bundle data must be declared as session variables in `app.json` (`variableDeclarations`) with rich default values and synchronized by deterministic Python tools so the agent's consultative pitch is 100% grounded in session state:

1. `customer_id`: `"CUST-GEOFF-001"`
2. `customer_name`: `"Geoffrey Horsfield (Geoff)"`
3. `household_profile`: `"4-bedroom home (14 Oakwood Avenue, Manchester, M20 2WQ) with rear kitchen-diner extension; Smart Hub 2 by front door in hallway; teenage kids gaming on Xbox consoles in upstairs back bedrooms"`
4. `current_broadband_plan`: `"Fibre 100 (100 Mbps download / 20 Mbps upload) — Out of Contract at £44.00/month"`
5. `network_telemetry_summary`: `"Smart Hub 2 (0 Mesh Discs) | 850 GB/month usage across 14 connected devices | 4 router packet-drop events in last 24h | Weak RSSI (-79 to -82 dBm) in kitchen-diner and upstairs back bedrooms | Local Exchange MANCHESTER-SOUTH-EX04: GREEN"`
6. `billing_discrepancy_details`: `"Invoice INV-8841 contains a £12.00 duplicate charge for Cymbal Cyber Security Add-On; eligible for instant auto-refund to Visa ending 4412"`
7. `billing_refund_status`: `"pending"` (transitions to `"refunded_12_gbp"` when `resolve_billing_and_diagnostics` runs)
8. `tailored_bundle_config`: JSON string defining the **3-Pillar Cymbal One Converged Home Bundle (`BUNDLE-CYMBAL-ONE-HOME` at `£68.00/mo`, saving `£22.00/mo` vs. `£90.00/mo` standalone, upgrading from `£44.00/mo` out-of-contract)**:
   - **Pillar 1 — Core Service (`ITEM-FIBRE-900`):** `Cymbal Full Fibre 900` (`900 Mbps ultra-stable speeds for heavy console gaming & 4K streaming`, standalone value `£55.00/mo`, included in bundle)
   - **Pillar 2 — Smart Hardware (`ITEM-COMPLETE-WIFI`):** `Cymbal Complete Wi-Fi Guarantee` (`Smart Hub 3 + 3 Smart Wi-Fi 6E Mesh Discs for whole-home coverage + Hybrid 4G Backup so connection never drops`, standalone value `£20.00/mo`, included in bundle)
   - **Pillar 3 — Entertainment & Gaming Add-ons (`ITEM-TV-XBOX-SECURITY`):** `Cymbal TV Sport + Xbox Game Pass Ultimate + Multi-Device Cyber Security` (`Ultimate console gaming for the kids, live family 4K sports, and whole-home cyber protection`, standalone value `£15.00/mo`, included in bundle)
9. `active_widget_data`: JSON string holding the active `widgetTool` payload (`show_product_carousel` or `show_product_comparison`)
10. `journey_stage`: `"discovery"` -> `"care_resolved"` -> `"bundle_pitched"` -> `"coverage_visualized"` -> `"checkout_complete"`
11. `basket_state`: JSON string holding the multi-product cart items (`ITEM-FIBRE-900`, `ITEM-COMPLETE-WIFI`, `ITEM-TV-XBOX-SECURITY`, and `-£12.00` `INV-8841` instant credit)
12. `servicenow_handover_payload`: JSON string holding the pre-provisioned ServiceNow ticket (`INC-904821`), priority Cymbal Fibre & Mesh engineer appointment (`Thursday, 10:00 AM – 12:00 PM`), attached router telemetry (`4 drops in 24h`), 3-disc house placement plan, and omnichannel retail/call-center continuity summary.

---

## 4. Linear 4-Step Customer Journey & Operating Procedure

### Step 1: Empathetic Care, Instant £12.00 Refund & Live Telemetry Diagnosis ("The Trust Builder")
- **Customer Input:** Geoff reports that his broadband has been cutting out in the kitchen, his teenage kids are lagging on their gaming consoles upstairs, and/or he thinks he was overcharged on his last bill.
- **System / Tool Action:**
  1. Call `resolve_billing_and_diagnostics(customer_id="CUST-GEOFF-001")`.
     - Queries Elysium CDP, confirms the `Out-of-Contract Fibre 100 (£44.00/mo)` profile, logs the `4 packet-drop events in 24h` across `14 devices` (`850 GB/mo`), and immediately executes the **£12.00 auto-refund** (`INV-8841` duplicate Cyber Security charge) to `Visa-4412`, setting `billing_refund_status = "refunded_12_gbp"` and `journey_stage = "care_resolved"`.
  2. Call Client Function `update_storefront_ui(view="account_diagnostics", payload_json=...)` so the main Cymbal Telecom webpage displays a clean **Live Diagnostics & £12.00 Instant Refund Confirmed** status banner.
- **Spoken Response (2–3 concise sentences, empathetic problem-solver register):**
  - Acknowledge Geoff's frustration warmly, confirm that you have **already refunded the £12.00 duplicate billing charge directly back to his Visa card**, and share the live telemetry finding (his Smart Hub 2 logged 4 packet drops in the last 24 hours while handling 14 devices and 850 GB/mo, causing weak signal in the kitchen and upstairs bedrooms).
  - Pivot consultatively: *"Let's not just patch it — I can put together a tailored all-in-one home bundle that upgrades your speeds, blankets every room in guaranteed Wi-Fi, and includes gaming for the kids. Would you like to see what I've put together for your home?"*

### Step 2: Personalised Multi-Product Basket Expansion ("Geoff's Tailored Home Bundle")
- **Customer Input:** Geoff agrees to see the recommendation / asks what we can do to fix the house and upgrade his setup.
- **System / Tool Action:**
  1. Call `build_tailored_home_bundle(customer_id="CUST-GEOFF-001", view_type="carousel")` (or `"comparison"` if Geoff asks for a price comparison table).
     - Populates `active_widget_data` with the **3-Pillar Multi-Product Bundle Cards** so the chat widget displays **all 3 distinct product categories included in the bundle**:
       - **Card 1 — Core Service:** `Cymbal Full Fibre 900` (`Included (£68/mo Bundle)` — `900 Mbps Symmetrical • Smart Hub 3 • Zero-Lag Gaming`)
       - **Card 2 — Smart Hardware:** `Complete Wi-Fi Guarantee (3 Smart Discs + 4G Backup)` (`Included (£68/mo Bundle)` — `3 Wi-Fi 6E Mesh Discs + Hybrid 4G Failover • Zero Dead Zones`)
       - **Card 3 — Entertainment & Gaming:** `Cymbal TV Sport & Xbox Game Pass Ultimate` (`Included (£68/mo Bundle)` — `Xbox Game Pass Ultimate for Kids + 4K Family Sports + Cyber Security`)
  2. Immediately call native `widgetTool` `show_product_carousel` (or `show_product_comparison` if requested) with `payload` from `active_widget_data` and a concise 2–3 sentence `textResponse`.
  3. Call Client Function `update_storefront_ui(view="tailored_bundle_showcase", payload_json=...)` so the main Cymbal Telecom webpage renders the visual **"GEOFF'S TAILORED HOME BUNDLE"** 3-column showcase (`Core Service: Full Fibre 900` | `Smart Hardware: 3 Smart Wi-Fi Discs + Hybrid 4G Backup` | `Premium Add-ons: TV Sport & Xbox Game Pass Ultimate`), showing `Old Price: £44.00/mo (Out of contract) -> NEW ALL-IN-ONE BUNDLE: £68.00/mo (Save £22/mo)`.
- **Spoken Consultative Upsell Pitch (2–3 sentences):**
  - *"Because your family games and streams heavily, I've built a tailored Cymbal One bundle combining three upgrades: Full Fibre 900 for ultra-stable speeds, our Complete Wi-Fi Guarantee with three Smart Mesh Discs and 4G backup, plus Cymbal TV Sport and Xbox Game Pass Ultimate for the kids. Instead of £90 a month separately, you get all three together for our converged rate of £68 a month — saving you £22 every month. Would you like to see on your screen how the three discs cover your kitchen and upstairs bedrooms, or shall we add the bundle straight to your basket?"*

### Step 3: Illustrative Home Wi-Fi Mesh Coverage Visualisation & Consultative Q&A
- **Customer Input:** Geoff asks how the 3 Smart Wi-Fi Discs will work in his house (kitchen and upstairs back bedrooms) or asks to see the coverage map.
- **System / Tool Action:**
  1. Call Client Function `update_storefront_ui(view="mesh_coverage_map", view_mode="after_mesh_coverage", payload_json=...)`.
     - Switches the main Cymbal Telecom webpage to a clean, **pre-built illustrative Home Wi-Fi Mesh Coverage diagram** (no live image generation latency) of Geoff's 4-bedroom home showing the **Before (Smart Hub 2 only — red dead zones in kitchen & upstairs bedrooms)** vs. **After (Smart Hub 3 in Hallway + Disc 1 in Hallway + Disc 2 in Kitchen-Diner + Disc 3 on Upstairs Landing — 100% green coverage + Hybrid 4G Backup)**.
- **Spoken Explanation (2–3 sentences):**
  - Explain clearly how placing Disc 1 in the hallway, Disc 2 in the kitchen-diner, and Disc 3 on the upstairs landing eliminates the dead zones and gives the kids' consoles a rock-solid connection, backed by automatic 4G failover. Ask if he is ready to upgrade his home with this bundle.

### Step 4: 1-Click Multi-Product Cart Injection & Zero-Friction ServiceNow Pre-Provisioning
- **Customer Input:** Geoff says *"Yes, upgrade my home"* / *"Let's go ahead and add the bundle to my basket"*.
- **System / Tool Action:**
  1. Call `complete_converged_checkout_and_servicenow(customer_id="CUST-GEOFF-001", confirm_upgrade="true")`.
     - Injects **all 3 bundled product pillars** (`Cymbal Full Fibre 900`, `Complete Wi-Fi 3 Smart Mesh Discs + Hybrid 4G Backup`, `Cymbal TV Sport & Xbox Game Pass Ultimate + Cyber Security`) plus the `-£12.00` billing refund credit and free priority installation (`£0.00`) into `basket_state`.
     - Pre-provisions the **ServiceNow Handover & Engineer Installation Record (`INC-904821`)** for `Thursday, 10:00 AM – 12:00 PM` in `servicenow_handover_payload`, attaching Geoff's router telemetry history (`4 packet drops in 24h`), the 3-disc placement map, and the omnichannel continuity summary for retail/contact-centre advisors.
     - Sets `journey_stage = "checkout_complete"`.
  2. Call Client Function `update_storefront_ui(view="checkout_and_servicenow", payload_json=...)` so the main Cymbal Telecom webpage displays the **Multi-Product Order Confirmation & Live Basket** alongside the **ServiceNow Pre-Provisioned Priority Engineer Ticket (`INC-904821`) & Omnichannel Continuity Card**.
- **Spoken Confirmation (2–3 sentences):**
  - Confirm warmly that the entire Cymbal One bundle (Full Fibre 900, 3 Smart Wi-Fi Discs with 4G Backup, and TV Sport & Xbox Game Pass) is in his checkout basket at £68 a month with his £12 refund applied, and that ServiceNow ticket `INC-904821` has pre-scheduled a priority engineer for Thursday between 10 AM and 12 PM with his full telemetry and house map attached. Ask if there is anything else you can help him with today.
