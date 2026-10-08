import json


def build_tailored_home_bundle(
    customer_id: str = "CUST-GEOFF-001",
    view_type: str = "carousel",
) -> dict:
    """Constructs the 3-Pillar Cymbal One Converged Home Bundle (BUNDLE-CYMBAL-ONE-HOME at £68.00/mo, saving £22.00/mo vs £90.00/mo standalone), populates active_widget_data for show_product_carousel or show_product_comparison, and returns the tailored_bundle_showcase storefront payload.

    IMPORTANT AUDIO CONTINUITY RULE: Do NOT output any spoken text before or during this tool call. Call this tool silently in parallel with update_storefront_ui(view="tailored_bundle_showcase"), then invoke show_product_carousel or show_product_comparison and speak your complete response once so TTS playback is never clipped.

    When to Call:
    - Call in Stage 3 when the customer agrees to see the tailored home bundle recommendation (view_type="carousel") or in Stage 4 when the customer asks for a side-by-side price comparison against their £44.00/mo plan and £90.00/mo standalone pricing (view_type="comparison").

    When NOT to Call:
    - Do NOT call in Stage 1 or Stage 2 before the customer agrees to see the bundle recommendation.

    Args:
        customer_id: (OPTIONAL) Customer identifier in Cymbal Elysium CDP. Defaults to "CUST-GEOFF-001".
        view_type: (OPTIONAL) Widget presentation mode: "carousel" for show_product_carousel (default) or "comparison" for show_product_comparison.

    Returns:
        dict: Contains 'status', 'bundle_id', 'bundle_name', 'pricing_summary',
              'widget_tool_to_call', 'widget_payload', and 'storefront_payload_json'
              for update_storefront_ui(view="tailored_bundle_showcase"). On error, returns
              'status': 'error', 'error', and 'agent_action'.
    """
    try:
        resolved_id = (customer_id or "CUST-GEOFF-001").strip()
        normalized_view = (view_type or "carousel").strip().lower()
        if normalized_view not in ("carousel", "comparison"):
            normalized_view = "carousel"

        pillars = [
            {
                "product_id": "ITEM-FIBRE-900",
                "category": "Core Service",
                "title": "Cymbal Full Fibre 900",
                "standalone_price_gbp": 55.00,
                "standalone_price_formatted": "£55.00/mo",
                "bundle_status": "Included (£68/mo Bundle)",
                "subtitle": "Included (£68/mo Bundle) • Standalone £55/mo",
                "description": "900 Mbps Symmetrical • Smart Hub 3 • Zero-Lag Gaming",
                "image_uri": "/assets/pillar_fibre_900.jpg",
                "uri": "https://store.cymbaltelecom.co.uk/bundles/cymbal-one-home#fibre-900",
            },
            {
                "product_id": "ITEM-COMPLETE-WIFI",
                "category": "Smart Hardware",
                "title": "Complete Wi-Fi Guarantee (3 Smart Discs + 4G Backup)",
                "standalone_price_gbp": 20.00,
                "standalone_price_formatted": "£20.00/mo",
                "bundle_status": "Included (£68/mo Bundle)",
                "subtitle": "Included (£68/mo Bundle) • Standalone £20/mo",
                "description": "3 Wi-Fi 6E Mesh Discs + Hybrid 4G Failover • Zero Dead Zones",
                "image_uri": "/assets/pillar_complete_wifi.jpg",
                "uri": "https://store.cymbaltelecom.co.uk/bundles/cymbal-one-home#complete-wifi",
            },
            {
                "product_id": "ITEM-TV-XBOX-SECURITY",
                "category": "Entertainment & Gaming",
                "title": "Cymbal TV Sport & Xbox Game Pass Ultimate",
                "standalone_price_gbp": 15.00,
                "standalone_price_formatted": "£15.00/mo",
                "bundle_status": "Included (£68/mo Bundle)",
                "subtitle": "Included (£68/mo Bundle) • Standalone £15/mo",
                "description": "Xbox Game Pass Ultimate for Kids + 4K Family Sports + Cyber Security",
                "image_uri": "/assets/pillar_tv_xbox.jpg",
                "uri": "https://store.cymbaltelecom.co.uk/bundles/cymbal-one-home#tv-xbox",
            },
        ]

        carousel_products = [
            {
                "productId": p["product_id"],
                "title": p["title"],
                "price": p["subtitle"],
                "subtitle": p["description"],
                "imageUris": [p["image_uri"]],
                "uri": p["uri"],
            }
            for p in pillars
        ]

        if normalized_view == "comparison":
            comparison_products = [
                {
                    "productId": "PLAN-FIBRE-100-OOC",
                    "title": "Current Plan: Fibre 100 (Out of Contract)",
                    "price": "£44.00/mo",
                    "subtitle": "100 Mbps • Single Smart Hub 2 • No Mesh Discs",
                    "imageUris": [
                        "/assets/pillar_fibre_900.jpg"
                    ],
                    "uri": "https://store.cymbaltelecom.co.uk/broadband/fibre-100",
                },
                {
                    "productId": "STANDALONE-UPGRADES",
                    "title": "Standalone Upgrades (Purchased Separately)",
                    "price": "£90.00/mo",
                    "subtitle": "Full Fibre 900 (£55) + 3 Mesh Discs (£20) + TV & Xbox (£15)",
                    "imageUris": [
                        "/assets/pillar_complete_wifi.jpg"
                    ],
                    "uri": "https://store.cymbaltelecom.co.uk/broadband/standalone",
                },
                {
                    "productId": "BUNDLE-CYMBAL-ONE-HOME",
                    "title": "Cymbal One Converged Home Bundle",
                    "price": "£68.00/mo (Save £22/mo)",
                    "subtitle": "Full Fibre 900 + 3 Smart Discs & 4G Backup + TV Sport & Xbox Game Pass",
                    "imageUris": [
                        "/assets/pillar_tv_xbox.jpg"
                    ],
                    "uri": "https://store.cymbaltelecom.co.uk/bundles/cymbal-one-home",
                },
            ]
            comparison_features = [
                {
                    "label": "Monthly Price",
                    "productSpecs": [
                        {"text": "£44.00/mo (Out of Contract)"},
                        {"text": "£90.00/mo (£55 + £20 + £15)"},
                        {"text": "£68.00/mo (Save £22.00/mo)"},
                    ],
                },
                {
                    "label": "Core Broadband Speed",
                    "productSpecs": [
                        {"text": "100 Mbps Download / 20 Mbps Upload"},
                        {"text": "900 Mbps Symmetrical Full Fibre"},
                        {"text": "900 Mbps Symmetrical Full Fibre (Smart Hub 3)"},
                    ],
                },
                {
                    "label": "Whole-Home Wi-Fi Hardware",
                    "productSpecs": [
                        {"text": "Single Smart Hub 2 (0 Mesh Discs)"},
                        {"text": "3 Wi-Fi 6E Mesh Discs + 4G Backup (£20/mo)"},
                        {"text": "Included: 3 Wi-Fi 6E Mesh Discs + Hybrid 4G Backup"},
                    ],
                },
                {
                    "label": "Entertainment, Gaming & Security",
                    "productSpecs": [
                        {"text": "Not Included"},
                        {"text": "TV Sport + Xbox Game Pass + Cyber Security (£15/mo)"},
                        {"text": "Included: Cymbal TV Sport + Xbox Game Pass Ultimate + Cyber Security"},
                    ],
                },
            ]
            widget_payload = {
                "title": "Geoff's Tailored Home Bundle — Price & Value Comparison",
                "productDetails": comparison_products,
                "features": comparison_features,
            }
            widget_tool_to_call = "show_product_comparison"
        else:
            widget_payload = {
                "productDetails": carousel_products,
            }
            widget_tool_to_call = "show_product_carousel"

        widget_data_json = json.dumps(widget_payload)

        try:
            if hasattr(context, "variables") and isinstance(context.variables, dict):
                context.variables["active_widget_data"] = widget_data_json
                context.variables["journey_stage"] = "bundle_pitched"
            if hasattr(context, "state") and isinstance(context.state, dict):
                context.state["active_widget_data"] = widget_data_json
                context.state["journey_stage"] = "bundle_pitched"
        except NameError:
            pass

        pricing_summary = {
            "old_price_gbp": 44.00,
            "standalone_total_gbp": 90.00,
            "bundle_price_gbp": 68.00,
            "monthly_savings_gbp": 22.00,
            "headline": "Old Price: £44.00/mo (Out of contract) -> NEW ALL-IN-ONE BUNDLE: £68.00/mo (Save £22/mo vs £90/mo standalone)",
        }

        storefront_payload = {
            "view": "tailored_bundle_showcase",
            "customer_id": resolved_id,
            "headline": "GEOFF'S TAILORED HOME BUNDLE",
            "bundle_id": "BUNDLE-CYMBAL-ONE-HOME",
            "bundle_name": "Cymbal One Converged Home Bundle",
            "pricing_summary": pricing_summary,
            "pillars": pillars,
        }
        storefront_payload_json = json.dumps(storefront_payload)

        return {
            "status": "success",
            "customer_id": resolved_id,
            "bundle_id": "BUNDLE-CYMBAL-ONE-HOME",
            "bundle_name": "Cymbal One Converged Home Bundle",
            "journey_stage": "bundle_pitched",
            "pricing_summary": pricing_summary,
            "widget_tool_to_call": widget_tool_to_call,
            "widget_payload": widget_payload,
            "storefront_payload_json": storefront_payload_json,
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": f"Failed to build tailored home bundle: {str(exc)}",
            "agent_action": "Explain the 3-pillar Cymbal One Converged Home Bundle verbally (Full Fibre 900, 3 Smart Wi-Fi Discs with 4G Backup, and Cymbal TV Sport & Xbox Game Pass Ultimate for £68/mo, saving £22/mo vs £90/mo standalone) and ask if Geoff wants to see the coverage map or add the bundle to his basket.",
        }
