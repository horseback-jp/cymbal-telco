# Cymbal Telecom — Converged Commerce & Care Demo (CX Agent Studio)

An executive-ready **Consultative Commerce & Care** demo built on **Google Cloud CX Agent Studio (CXAS)** using the **Gemini Composite Architecture (`en-GB`)**.

It demonstrates how a multimodal telecom concierge turns an inbound broadband support and billing complaint into a consultative **3-Pillar Home Convergence Bundle** upgrade—combining empathetic British English voice synthesis, native CXAS **Rich Response Widgets** (`PRODUCT_CAROUSEL` and `PRODUCT_COMPARISON`), and real-time **Client Function** storefront synchronization (`update_storefront_ui`).

---

## Live Links

- **Live Storefront Web UI (Cloud Run):** [https://jph-cymbal-converged-web-hkzaa2nmka-ew.a.run.app](https://jph-cymbal-converged-web-hkzaa2nmka-ew.a.run.app)
- **Presenter Guide & Turn-by-Turn Demo Script:** See [`docs/demo-script.md`](docs/demo-script.md)
- **Technical Design Document (TDD):** See [`tdd.md`](tdd.md)

---

## Repository Structure

```text
.
├── cxas_app/
│   └── cymbal_converged_commerce_demo/     # Exported CXAS application
│       ├── app.json                        # App config, 12 session variables & en-GB Director's Note
│       ├── global_instruction.txt          # Affective Delivery & Voice Guidelines
│       ├── agents/
│       │   └── cymbal_converged_concierge/ # Unified root concierge agent & 5-stage taskflow
│       └── tools/
│           ├── resolve_billing_and_diagnostics/  # Python tool: £12 auto-refund + router telemetry
│           ├── build_tailored_home_bundle/       # Python tool: 3-pillar bundle & comparison builder
│           ├── complete_converged_checkout/      # Python tool: 1-click basket + ServiceNow INC-904821
│           ├── show_product_carousel/            # Native widgetTool (PRODUCT_CAROUSEL)
│           ├── show_product_comparison/          # Native widgetTool (PRODUCT_COMPARISON)
│           └── update_storefront_ui/             # Client Function driving main web UI views
├── web/                                    # Cymbal Telecom Storefront Web UI + <chat-messenger>
│   ├── index.html                          # Split-stage storefront & Bidi WebChannel tool bridge
│   ├── server.py                           # Lightweight Python HTTP server (local & Cloud Run)
│   ├── Dockerfile                          # Cloud Run container definition
│   ├── deployment_config.json              # Active CXAS Web Widget deployment metadata
│   └── assets/                             # Product & 3D home mesh cutaway visuals
├── scripts/
│   ├── provision_web_deployment.py         # Creates CXAS AppVersion & updates WEB_UI deployment
│   └── deploy_cloud_run.py                 # Builds & deploys web/ to Cloud Run
├── evals/                                  # CXAS Golden, Simulation & Isolated Tool Test suites
│   ├── goldens/goldens.yaml
│   ├── simulations/simulations.yaml
│   └── tool_tests/tool_tests.yaml
├── docs/
│   └── demo-script.md                      # Turn-by-turn presenter script & data reference
└── tdd.md                                  # Technical Design Document
```

---

## 5-Stage Consultative Customer Journey

1. **Stage 1 — Empathetic Care, Instant £12 Refund & Open Diagnostic Question:**
   - Calls `resolve_billing_and_diagnostics` + `update_storefront_ui(view="account_diagnostics")` in parallel.
   - Auto-refunds the **£12.00 duplicate Cymbal Cyber Security charge** (`INV-8841`) to **Visa ending `4412`**, shares live router telemetry (`Smart Hub 2`, `14 active devices`, `850 GB/mo`, `4 Wi-Fi drops in 24h`, green street exchange), and asks Geoff an open diagnostic question about his home layout and where dropouts occur.
2. **Stage 2 — Consultative Discovery & Introducing the Bundle Concept:**
   - Validates Geoff's 4-bedroom house setup (rear kitchen-diner extension and teenage kids gaming on Xbox consoles upstairs), explains why a single hallway router struggles, introduces the concept of combining Full Fibre 900, Whole-Home Mesh Wi-Fi, and Xbox Game Pass Ultimate with TV Sport into one package, and asks permission to show it on screen.
3. **Stage 3 — Showing the Tailored Bundle & Exploring Benefits:**
   - Calls `build_tailored_home_bundle(view_type="carousel")` + `update_storefront_ui(view="tailored_bundle_showcase")` in parallel, followed by `show_product_carousel`.
   - Presents the **Cymbal One Converged Home Bundle** at **£68.00/mo** vs **£90.00/mo** standalone (**saving £22.00/mo**) and invites Geoff to ask questions.
4. **Stage 4 — Handling Price Objections & Confirming Home Mesh Layout:**
   - **Price Objection (`show_product_comparison`):** Renders a side-by-side comparison table (`£44/mo Out-of-Contract Fibre 100` vs `£90/mo Standalone` vs `£68/mo Converged Bundle`).
   - **Coverage Map (`update_storefront_ui(view="mesh_coverage_map")`):** Switches the main storefront to the interactive **3D Home Wi-Fi Mesh Visualizer** (Hallway, Rear Kitchen-Diner Extension, Upstairs Kids' Bedrooms + Hybrid 4G Failover) and confirms that the 3-disc placement matches Geoff's rooms.
5. **Stage 5 — Complimentary Priority Engineer Install & 1-Click Checkout:**
   - Calls `complete_converged_checkout` + `update_storefront_ui(view="checkout_and_servicenow")`.
   - Confirms **£0.00 complimentary priority engineer installation**, populates the £68.00/mo basket with the -£12.00 refund credit applied, and pre-reserves ServiceNow ticket **`INC-904821`** for **Thursday, 10:00 AM – 12:00 PM**.

---

## Running Locally

```bash
python3 web/server.py --port 8081
```

Then open `http://localhost:8081` in Chrome.
