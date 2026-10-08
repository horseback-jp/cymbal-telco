# Cymbal Telecom — Converged Commerce & Care Demo Guide & Presenter Script

## 1. Executive Overview & Quick Links

This demo showcases **Cymbal Telecom’s Consultative Commerce & Care Concierge** built on **Google Cloud CX Agent Studio (CXAS)** using the **Gemini Composite Architecture (`en-GB`)**. It demonstrates how an AI concierge turns a frustrated broadband support and billing call into a high-value, consultative **3-pillar home convergence upgrade**—combining empathetic voice delivery, in-chat **Rich Response Widgets** (`PRODUCT_CAROUSEL` and `PRODUCT_COMPARISON`), and real-time **Client Function** synchronization (`update_storefront_ui`) that drives the main Cymbal Telecom web storefront.

| Resource | Link / Identifier |
| :--- | :--- |
| **Live Cloud Run Storefront Web UI** | [https://jph-cymbal-converged-web-hkzaa2nmka-ew.a.run.app](https://jph-cymbal-converged-web-hkzaa2nmka-ew.a.run.app) |
| **CXAS Console Application (`eu`)** | [https://ces.cloud.google.com/projects/ces-demo-emea/locations/eu/apps/22e1dd89-dd92-4f83-b25f-0fc3d3ad0ae0](https://ces.cloud.google.com/projects/ces-demo-emea/locations/eu/apps/22e1dd89-dd92-4f83-b25f-0fc3d3ad0ae0) |
| **Logged-in Customer Persona** | **Geoffrey "Geoff" Horsfield** (`customer_id: CUST-GEOFF-001`) |
| **Voice Configuration** | British English (`en-GB-Chirp3-HD-Zephyr`) with dynamic affective prosody |
| **Demo Owner** | `jphorsfield` |

---

## 2. Understanding the Demo Data: What the Agent Knows vs. What You Must Share

To make the consultation feel genuinely human rather than pre-scripted, the agent's knowledge is purposefully split between **account/router telemetry** (which the agent knows immediately) and **physical house layout & family usage** (which the agent asks you about in Stage 1).

### A. What the Agent Already Knows (Account & Router Telemetry in Session State)

| Data Domain | Pre-Loaded Account & Telemetry Details (`CUST-GEOFF-001`) |
| :--- | :--- |
| **Customer Profile** | **Geoffrey "Geoff" Horsfield**, 14 Oakwood Avenue, Manchester, M20 2WQ |
| **Current Broadband Plan** | **Cymbal Fibre 100** (100 Mbps download / 20 Mbps upload) — **Out of Contract at £44.00/month** |
| **Billing Discrepancy** | **Invoice `INV-8841`** contains a **£12.00 duplicate Cymbal Cyber Security Add-On charge**, eligible for instant auto-refund to **Visa ending `4412`** |
| **Street Fibre Line** | Local Exchange `MANCHESTER-SOUTH-EX04` is **GREEN** (no street fault) |
| **Home Router Telemetry** | Single **Smart Hub 2** in the hallway (`0 Mesh Discs`) handling **14 active devices** and **850 GB/month** of traffic, with **4 Wi-Fi signal drops in the last 24 hours** on distant devices (`-79 dBm` to `-82 dBm`) |

### B. Crucial Presenter Tip: What You Must State in Stage 2

Because a broadband router cannot see internal walls or room names on its own, the agent **does not assume the size of Geoff's house or which rooms have weak signal** on Turn 1. Instead, after refunding your £12.00 and sharing the router telemetry, the agent asks you where in the house the dropouts happen and what the family is doing online.

> **IMPORTANT FOR PRESENTERS:** When replying in **Stage 2**, explicitly mention these three details so the subsequent **Xbox Game Pass** recommendation (Stage 3) and **4-Bedroom 3D Home Wi-Fi Map** (Stage 4B) feel completely natural:
> 1. You live in a **4-bedroom house** (the router is by the front door in the hallway).
> 2. The Wi-Fi drops in your **rear kitchen-diner extension** (e.g., during work video calls).
> 3. Your **teenage kids get lag on their Xbox consoles in the upstairs back bedrooms**.

### C. The Tailored Converged Bundle & ServiceNow Handover Data

| Pillar / Item | Standalone Price | Converged Bundle Status | Key Highlights |
| :--- | :--- | :--- | :--- |
| **1. Cymbal Full Fibre 900** (`ITEM-FIBRE-900`) | £55.00/mo | **Included in £68/mo Bundle** | 900 Mbps symmetrical speeds (9x faster than Fibre 100) + Wi-Fi 6E Smart Hub 3 |
| **2. Complete Wi-Fi Guarantee** (`ITEM-COMPLETE-WIFI`) | £20.00/mo | **Included in £68/mo Bundle** | 3 Smart Wi-Fi 6E Mesh Discs (Hallway, Kitchen-Diner, Upstairs Landing) + Automatic Hybrid 4G Backup |
| **3. Cymbal TV Sport & Xbox Game Pass Ultimate** (`ITEM-TV-XBOX-SECURITY`) | £15.00/mo | **Included in £68/mo Bundle** | Xbox Game Pass Ultimate for the kids' consoles + Live 4K Family Sport + Multi-Device Cyber Security |
| **Total Monthly Price** | **£90.00/mo** separately | **£68.00/mo** (**Save £22.00/mo**) | £24/mo more than out-of-contract Fibre 100 (£44/mo) for £90/mo of standalone value |
| **Instant Bill Refund Credit** (`INV-8841`) | — | **-£12.00** | Already refunded to Visa ending `4412` |
| **Priority Engineer Installation** (`INC-904821`) | — | **£0.00 (Complimentary)** | Pre-reserved for **Thursday, 10:00 AM – 12:00 PM** with router telemetry and 3-disc room map attached |

---

## 3. How to Launch & Reset the Demo

1. Open the live storefront in Chrome: **[https://jph-cymbal-converged-web-hkzaa2nmka-ew.a.run.app](https://jph-cymbal-converged-web-hkzaa2nmka-ew.a.run.app)**.
2. Notice the **Side-by-Side Split-Stage Layout**:
   - **Left Stage:** The Cymbal Telecom Personal Storefront, signed in as **Geoff Horsfield**.
   - **Right Rail:** The **Cymbal Concierge** (`<chat-messenger>`) panel, which starts completely empty on every page load.
3. Click the **Microphone icon** in the Cymbal Concierge input bar to start a live bidirectional voice session (or type any prompt below in text mode).
4. **Resetting Between Runs:** Simply refresh the browser page (`Cmd+R` / `Ctrl+R`) or click the **Start new chat** reset icon in the Cymbal Concierge titlebar. You can also use the subtle presenter dock at the bottom of the screen (`Home`, `1. Care & £12 Refund`, `2. Tailored Bundle`, `3. Home Wi-Fi Map`, `4. Order Confirmed`) to inspect any stage manually.

---

## 4. Turn-by-Turn Consultative Narrative Script (5 Stages)

### Stage 1 — Empathetic Care, Instant £12 Refund & Open Diagnostic Question

- **Goal:** Show how the agent resolves a billing complaint and runs live router diagnostics in a single turn—building trust before ever mentioning an upgrade—and asks an open question to understand the customer's home.

| Step | Details |
| :--- | :--- |
| **What You Say (Presenter)** | *"Hi, my broadband keeps cutting out at home, and I also noticed my latest bill is twelve pounds higher than usual."* |
| **Behind-the-Scenes Tools** | Silently calls `resolve_billing_and_diagnostics(customer_id="CUST-GEOFF-001")` and `update_storefront_ui(view="account_diagnostics")` in parallel (<100ms) so audio never clips. |
| **Main Storefront UI Transition** | Automatically switches from the Hero Banner to **`1. Care & £12 Refund`**, displaying two visual cards:<br>• **Left Card:** *£12.00 Refunded — Credited straight back to Visa •••• 4412 (Invoice #INV-8841)*<br>• **Right Card:** *Street fibre is healthy — your single Smart Hub 2 is overloaded (14 Active Devices • 850 GB Monthly Usage • 4 Drops in Last 24 Hours)* |
| **What the Agent Says** | Confirms empathetically that it has already spotted and refunded the £12.00 duplicate Cymbal Cyber Security charge on Invoice `INV-8841` back to Geoff's Visa ending `4412`. Shares that the street fibre exchange is green, while his single `Smart Hub 2` on out-of-contract Fibre 100 is handling 14 devices and 850 GB/mo with 4 Wi-Fi drops in the last 24 hours. **Ends by asking where in the house he notices the weak signal most and what the family is doing online when it lags.** |

---

### Stage 2 — Consultative Discovery & Introducing the Bundle Concept

- **Goal:** Supply the house layout and family usage details (4-bedroom house, kitchen extension, kids on Xbox upstairs) so the agent validates the bottleneck in human terms and introduces the *concept* of a converged bundle before pushing product cards.

| Step | Details |
| :--- | :--- |
| **What You Say (Presenter)** | *"We're in a four-bedroom house with the router by the front door. It keeps dropping out in our rear kitchen extension when I'm on work calls, and my teenage kids are constantly complaining about lag on their Xbox consoles in the upstairs bedrooms."* |
| **Behind-the-Scenes Tools** | Pure consultative dialogue turn (no premature tool call yet). |
| **Main Storefront UI Transition** | Remains on **`1. Care & £12 Refund`** while the agent consults with Geoff. |
| **What the Agent Says** | Validates Geoff's experience and explains in plain human terms why a single hallway router on 100 Mbps struggles to push through internal walls to a kitchen extension while the kids are gaming upstairs across 14 devices. Explains that because his £44/mo Fibre 100 plan is out of contract, Cymbal can combine **900 Mbps Full Fibre**, **Whole-Home Mesh Wi-Fi discs**, and **Xbox Game Pass Ultimate with TV Sport** into a single package that saves money over separate add-ons—and **asks permission to bring it up on his screen**. |

---

### Stage 3 — Showing the Tailored Bundle & Exploring Benefits

- **Goal:** Trigger the synchronized multimodal transition (both the main storefront showcase and the in-chat Product Carousel) and let the agent highlight family benefits while giving Geoff space to ask questions.

| Step | Details |
| :--- | :--- |
| **What You Say (Presenter)** | *"Yes, please bring that up on screen so I can see what's in it."* |
| **Behind-the-Scenes Tools** | Calls `build_tailored_home_bundle(view_type="carousel")` and `update_storefront_ui(view="tailored_bundle_showcase")` silently in parallel, followed immediately by `show_product_carousel`. |
| **Main Storefront UI & Chat Widget** | • **Main Storefront:** Transitions to **`2. Tailored Bundle`**, showcasing the **Cymbal One Converged Home Bundle** (`£68/month` vs `£90/mo separately`, `Save £22/mo`) and the 3 visual pillar cards.<br>• **In-Chat Widget:** Renders the interactive 3-card **Product Carousel** inside the Cymbal Concierge rail. |
| **What the Agent Says** | Walks through the real-life benefits for Geoff's family: **Cymbal Full Fibre 900** (9x faster symmetrical speeds), **Complete Wi-Fi Guarantee** (3 Smart Wi-Fi 6E Mesh Discs + Hybrid 4G Backup to eliminate dead zones), and **Cymbal TV Sport & Xbox Game Pass Ultimate** for the kids—all for **£68/mo** instead of **£90/mo** separately (saving **£22/mo**). **Invites Geoff to ask questions** (e.g., comparing the pricing against his current £44/mo bill or seeing how the 3 mesh discs work around his rooms). |

---

### Stage 4A — Handling Price Concerns (Side-by-Side Comparison Table)

- **Goal:** Demonstrate consultative objection handling when the customer points out that £68/mo is £24 more than their current £44/mo bill.

| Step | Details |
| :--- | :--- |
| **What You Say (Presenter)** | *"Hold on—sixty-eight pounds a month is twenty-four pounds more than the forty-four pounds I'm paying right now. Can you break down why it's worth the extra?"* |
| **Behind-the-Scenes Tools** | Calls `build_tailored_home_bundle(view_type="comparison")` and `update_storefront_ui(view="tailored_bundle_showcase")` in parallel, followed by `show_product_comparison`. |
| **Main Storefront UI & Chat Widget** | • **In-Chat Widget:** Renders the native **Side-by-Side Product Comparison Table** comparing **Current Fibre 100 (£44/mo OOC)** vs. **Standalone Upgrades (£90/mo)** vs. **Cymbal One Converged Bundle (£68/mo)**. |
| **What the Agent Says** | Acknowledges fairly that £68/mo is £24 more than his out-of-contract £44/mo plan, then walks through the value breakdown: buying Full Fibre 900 (£55), 3 Smart Mesh Discs with 4G Backup (£20), and TV Sport with Xbox Game Pass Ultimate (£15) separately costs £90/mo—so the bundle saves £22 every month, includes free priority engineer installation, and pairs with the £12 refund already back on his Visa card. |

---

### Stage 4B — Exploring Home Wi-Fi Coverage & Confirming Room Layout

- **Goal:** Show how the agent drives the interactive 3D floorplan on the main webpage to explain mesh disc placement and confirms that the layout matches Geoff's rooms.

| Step | Details |
| :--- | :--- |
| **What You Say (Presenter)** | *"That pricing breakdown makes sense. How do those three mesh discs actually work around our house to fix the kitchen extension and the upstairs bedrooms?"* |
| **Behind-the-Scenes Tools** | Calls `update_storefront_ui(view="mesh_coverage_map", view_mode="after_mesh_coverage")`. |
| **Main Storefront UI Transition** | Transitions to **`3. Home Wi-Fi Map`**, displaying the **3D Home Cutaway Visualizer** with pulsing green coverage pins in the **Front Hallway (`Smart Hub 3 + Disc 1`)**, **Rear Kitchen-Diner (`Disc 2 • Full Signal`)**, and **Upstairs Bedrooms (`Disc 3 • 8ms Gaming`)**, plus interactive mode toggles (*With 3 Smart Discs*, *Before (Dead Zones)*, and *Hybrid 4G Backup*). |
| **What the Agent Says** | Explains how placing Smart Hub 3 with Disc 1 in the front hallway, Disc 2 in the rear kitchen-diner extension, and Disc 3 on the upstairs landing creates one seamless Wi-Fi 6E mesh network—backed by automatic Hybrid 4G failover if the street line ever drops. **Confirms with Geoff whether that 3-disc layout matches his rooms and asks if he has any questions about installation.** |

---

### Stage 5 — Complimentary Priority Engineer Install & 1-Click Checkout

- **Goal:** Close the loop with 1-click multi-product basket population and pre-provisioned ServiceNow field-engineer handover (`INC-904821`).

| Step | Details |
| :--- | :--- |
| **What You Say (Presenter)** | *"Yes, that layout matches our house perfectly. Can an engineer help us set it all up? Let's go ahead and order it."* |
| **Behind-the-Scenes Tools** | Calls `complete_converged_checkout(customer_id="CUST-GEOFF-001", confirm_upgrade="true")` and `update_storefront_ui(view="checkout_and_servicenow")` silently in parallel. |
| **Main Storefront UI Transition** | Transitions to **`4. Order Confirmed`** (and bumps the top-right header basket badge to `3`), displaying:<br>• **Left Card:** *Cymbal One Converged Home Bundle* itemized basket (`Full Fibre 900`, `Complete Wi-Fi 3 Smart Discs + 4G Backup`, `TV Sport & Xbox Game Pass Ultimate`, `-£12.00 Instant Bill Refund Credit #INV-8841`, `Upfront Installation: £0.00 Free`, and `£68.00/mo` total).<br>• **Right Card:** *White-Glove Home Setup Included (`Ref: INC-904821`)* reserved for **Thursday, 10:00 AM – 12:00 PM** with router diagnostics and the 3-disc floorplan attached. |
| **What the Agent Says** | Reassures Geoff that **Priority Engineer Installation is completely complimentary (£0.00)**, confirms all three pillars are in his checkout basket at £68.00/month with his £12.00 refund credit applied, and confirms that ServiceNow reference **`INC-904821`** has pre-reserved a specialist engineer for **Thursday between 10:00 AM and 12:00 PM** with his telemetry and 3-disc map attached—checking if Thursday morning works well for him. |
| **Optional Sign-Off** | Say *"Thursday morning works great, thank you and goodbye."* — the agent delivers a warm British sign-off and calls `end_session`. |
