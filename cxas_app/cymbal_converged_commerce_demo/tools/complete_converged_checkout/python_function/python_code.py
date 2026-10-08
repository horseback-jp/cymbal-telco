import json


def complete_converged_checkout(
    customer_id: str = "CUST-GEOFF-001",
    confirm_upgrade: str = "true",
) -> dict:
    """Injects all 3 pillars of the Cymbal One Converged Home Bundle plus the -£12.00 INV-8841 refund credit and free priority installation into basket_state, pre-provisions ServiceNow ticket INC-904821 (Thursday, 10:00 AM – 12:00 PM) with attached telemetry and 3-disc house placement plan in servicenow_handover_payload, and returns the checkout_and_servicenow storefront payload.

    IMPORTANT AUDIO CONTINUITY RULE: Do NOT output any spoken text before or during this tool call. Call this tool silently in parallel with update_storefront_ui(view="checkout_and_servicenow") and speak your complete confirmation only after the tool returns so TTS playback is never clipped.

    When to Call:
    - Call in Stage 5 when the customer confirms they want to upgrade their home, asks to proceed with installation, or asks to add the Cymbal One Converged Home Bundle to their basket.

    When NOT to Call:
    - Do NOT call before the customer explicitly agrees to proceed with the bundle upgrade or installation.

    Args:
        customer_id: (OPTIONAL) Customer identifier in Cymbal Elysium CDP. Defaults to "CUST-GEOFF-001".
        confirm_upgrade: (OPTIONAL) Confirmation flag ("true" default) verifying customer consent to add the bundle to their basket.

    Returns:
        dict: Contains 'status', 'order_id', 'basket', 'servicenow_ticket', and
              'storefront_payload_json' for update_storefront_ui(view="checkout_and_servicenow").
              On error, returns 'status': 'error', 'error', and 'agent_action'.
    """
    try:
        resolved_id = (customer_id or "CUST-GEOFF-001").strip()
        confirmed = (confirm_upgrade or "true").strip().lower()
        if confirmed in ("false", "no", "0"):
            return {
                "status": "error",
                "error": "Customer did not confirm the upgrade.",
                "agent_action": "Ask Geoff if he has any questions about the £68.00/mo Cymbal One Converged Home Bundle or the 3-disc coverage map before adding the bundle to his basket.",
            }

        basket = {
            "order_id": "ORD-CYM-904821",
            "customer_id": resolved_id,
            "bundle_id": "BUNDLE-CYMBAL-ONE-HOME",
            "bundle_name": "Cymbal One Converged Home Bundle",
            "items": [
                {
                    "sku": "ITEM-FIBRE-900",
                    "category": "Core Service",
                    "title": "Cymbal Full Fibre 900 (900 Mbps Symmetrical + Smart Hub 3)",
                    "standalone_price_gbp": 55.00,
                    "bundle_status": "Included in £68.00/mo Bundle",
                },
                {
                    "sku": "ITEM-COMPLETE-WIFI",
                    "category": "Smart Hardware",
                    "title": "Complete Wi-Fi Guarantee (3 Smart Wi-Fi 6E Mesh Discs + Hybrid 4G Backup)",
                    "standalone_price_gbp": 20.00,
                    "bundle_status": "Included in £68.00/mo Bundle",
                },
                {
                    "sku": "ITEM-TV-XBOX-SECURITY",
                    "category": "Entertainment & Gaming",
                    "title": "Cymbal TV Sport + Xbox Game Pass Ultimate + Multi-Device Cyber Security",
                    "standalone_price_gbp": 15.00,
                    "bundle_status": "Included in £68.00/mo Bundle",
                },
                {
                    "sku": "CREDIT-INV-8841",
                    "category": "Billing Credit",
                    "title": "Instant Auto-Refund Credit (Invoice INV-8841 Duplicate Cyber Security Charge to Visa 4412)",
                    "one_off_amount_gbp": -12.00,
                    "bundle_status": "-£12.00 Instant Refund Applied",
                },
                {
                    "sku": "INSTALL-PRIORITY-ENG",
                    "category": "Engineer Installation",
                    "title": "Priority Cymbal Fibre & Mesh Specialist Installation (Thu 10:00 AM – 12:00 PM)",
                    "one_off_amount_gbp": 0.00,
                    "bundle_status": "£0.00 (Complimentary Priority Install)",
                },
            ],
            "old_monthly_price_gbp": 44.00,
            "standalone_monthly_total_gbp": 90.00,
            "monthly_total_gbp": 68.00,
            "monthly_savings_gbp": 22.00,
            "one_off_credit_gbp": -12.00,
            "installation_fee_gbp": 0.00,
            "checkout_status": "ready_for_1_click_confirm",
        }

        servicenow_ticket = {
            "ticket_id": "INC-904821",
            "status": "PRE_PROVISIONED",
            "customer_id": resolved_id,
            "customer_name": "Geoffrey Horsfield (Geoff)",
            "address": "14 Oakwood Avenue, Manchester, M20 2WQ",
            "appointment_slot": "Thursday, 10:00 AM – 12:00 PM",
            "engineer_tier": "Priority Cymbal Fibre & Mesh Specialist",
            "telemetry_attached": "Smart Hub 2: 4 packet drops in last 24h across 14 connected devices (850 GB/mo); Weak RSSI in Rear Kitchen-Diner (-79 dBm) and Upstairs Back Bedrooms (-82 dBm); Local Exchange MANCHESTER-SOUTH-EX04: GREEN",
            "disc_placement_plan": [
                "Smart Hub 3 + Disc 1: Ground-Floor Front Hallway",
                "Disc 2: Rear Kitchen-Diner Extension (eliminates -79 dBm dead zone)",
                "Disc 3: Upstairs Landing outside Back Bedrooms (eliminates -82 dBm Xbox gaming lag)",
            ],
            "omnichannel_continuity_summary": "Care-to-Converged-Commerce upgrade completed: £12.00 INV-8841 duplicate Cyber Security charge refunded to Visa 4412; upgraded from Out-of-Contract Fibre 100 (£44/mo) to Cymbal One Converged Home Bundle (£68/mo, saving £22/mo vs £90/mo standalone). Full telemetry and 3-disc floorplan attached for field engineer and retail/contact-centre advisors.",
        }

        basket_json = json.dumps(basket)
        servicenow_json = json.dumps(servicenow_ticket)

        try:
            if hasattr(context, "variables") and isinstance(context.variables, dict):
                context.variables["basket_state"] = basket_json
                context.variables["servicenow_handover_payload"] = servicenow_json
                context.variables["journey_stage"] = "checkout_complete"
            if hasattr(context, "state") and isinstance(context.state, dict):
                context.state["basket_state"] = basket_json
                context.state["servicenow_handover_payload"] = servicenow_json
                context.state["journey_stage"] = "checkout_complete"
        except NameError:
            pass

        storefront_payload = {
            "view": "checkout_and_servicenow",
            "order_id": "ORD-CYM-904821",
            "basket": basket,
            "servicenow_ticket": servicenow_ticket,
        }
        storefront_payload_json = json.dumps(storefront_payload)

        return {
            "status": "success",
            "order_id": "ORD-CYM-904821",
            "journey_stage": "checkout_complete",
            "basket": basket,
            "servicenow_ticket": servicenow_ticket,
            "storefront_payload_json": storefront_payload_json,
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": f"Failed to complete converged checkout and ServiceNow pre-provisioning: {str(exc)}",
            "agent_action": "Confirm verbally that Geoff's Cymbal One Converged Home Bundle (£68.00/mo with £12.00 credit applied) and priority ServiceNow engineer appointment INC-904821 for Thursday 10:00 AM – 12:00 PM are being finalized.",
        }
