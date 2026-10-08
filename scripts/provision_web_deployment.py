#!/usr/bin/env python3
"""Provisions a CXAS AppVersion and WEB_UI (CHAT_AND_VOICE) Deployment for Cymbal Converged Commerce Demo."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

import google.auth
import google.auth.transport.requests

PROJECT_ID = "ces-demo-emea"
PROJECT_NUMBER = "1097682577517"
LOCATION = "eu"
APP_ID = "22e1dd89-dd92-4f83-b25f-0fc3d3ad0ae0"
APP_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/apps/{APP_ID}"
BASE_URL = f"https://ces.googleapis.com/v1beta/{APP_NAME}"
DEPLOYMENT_DISPLAY_NAME = "Cymbal Converged Commerce Web Widget"

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_OUT_PATH = REPO_ROOT / "web" / "deployment_config.json"


def get_access_token() -> str:
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token


def api_request(
    method: str,
    url: str,
    token: str,
    body: dict | None = None,
) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url=url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("x-goog-user-project", PROJECT_ID)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {e.code} on {method} {url}: {err_body}"
        ) from e


def wait_for_lro(op_data: dict, token: str) -> dict:
    if op_data.get("done") is True or "operations/" not in op_data.get("name", ""):
        return op_data.get("response", op_data)

    op_name = op_data["name"]
    op_url = f"https://ces.googleapis.com/v1beta/{op_name}"
    for _ in range(60):
        time.sleep(2)
        status = api_request("GET", op_url, token)
        if status.get("done"):
            if "error" in status:
                raise RuntimeError(f"Operation failed: {status['error']}")
            return status.get("response", status)
    raise TimeoutError(f"Timed out waiting for operation {op_name}")


def main() -> None:
    token = get_access_token()
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    version_display_name = f"v-converged-{ts}"

    print(f"1. Creating AppVersion '{version_display_name}' on {APP_NAME}...")
    version_resp = api_request(
        "POST",
        f"{BASE_URL}/versions",
        token,
        body={
            "displayName": version_display_name,
            "description": (
                "Cymbal Telecom Converged Commerce & Care Demo — 3-Pillar"
                " Tailored Home Bundle with widgetTool and update_storefront_ui"
            ),
        },
    )
    version = wait_for_lro(version_resp, token)
    version_name = version["name"]
    print(f"   -> Created AppVersion: {version_name}")

    print("2. Checking existing deployments...")
    deployments_resp = api_request("GET", f"{BASE_URL}/deployments", token)
    deployments = deployments_resp.get("deployments", [])
    existing = next(
        (
            d
            for d in deployments
            if d.get("displayName") == DEPLOYMENT_DISPLAY_NAME
        ),
        None,
    )

    channel_profile = {
        "channelType": "WEB_UI",
        "webWidgetConfig": {
            "modality": "CHAT_AND_VOICE",
            "theme": "LIGHT",
            "webWidgetTitle": "Cymbal Concierge",
            "securitySettings": {
                "enablePublicAccess": True,
                "enableOriginCheck": False,
                "enableRecaptcha": False,
            },
        },
    }

    if existing:
        dep_name = existing["name"]
        print(f"   -> Updating existing deployment: {dep_name}")
        patch_url = (
            f"https://ces.googleapis.com/v1beta/{dep_name}"
            "?updateMask=displayName,appVersion,channelProfile"
        )
        dep_resp = api_request(
            "PATCH",
            patch_url,
            token,
            body={
                "name": dep_name,
                "displayName": DEPLOYMENT_DISPLAY_NAME,
                "appVersion": version_name,
                "channelProfile": channel_profile,
            },
        )
        deployment = wait_for_lro(dep_resp, token)
    else:
        print(f"   -> Creating new WEB_UI deployment '{DEPLOYMENT_DISPLAY_NAME}'...")
        dep_resp = api_request(
            "POST",
            f"{BASE_URL}/deployments",
            token,
            body={
                "displayName": DEPLOYMENT_DISPLAY_NAME,
                "appVersion": version_name,
                "channelProfile": channel_profile,
            },
        )
        deployment = wait_for_lro(dep_resp, token)

    deployment_name = deployment["name"]
    deployment_id = deployment_name.split("/")[-1]
    deployment_name_by_id = (
        f"projects/{PROJECT_ID}/locations/{LOCATION}/apps/{APP_ID}/deployments/{deployment_id}"
    )
    deployment_name_by_number = (
        f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/apps/{APP_ID}/deployments/{deployment_id}"
    )

    print("3. Fetching tool resource IDs for Client Function registration...")
    tools_resp = api_request("GET", f"{BASE_URL}/tools?pageSize=50", token)
    client_tools = {}
    for t in tools_resp.get("tools", []):
        cf = t.get("clientFunction")
        if cf or t.get("displayName") in ("update_storefront_ui",):
            t_name = t.get("name", "")
            t_id = t_name.split("/")[-1] if t_name else ""
            fn_name = (
                (cf or {}).get("name")
                or t.get("displayName")
                or t_id
            )
            client_tools[fn_name] = {
                "functionName": fn_name,
                "toolId": t_id,
                "toolNameByProjectId": (
                    f"projects/{PROJECT_ID}/locations/{LOCATION}/apps/{APP_ID}/tools/{t_id}"
                ),
                "toolNameByProjectNumber": (
                    f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/apps/{APP_ID}/tools/{t_id}"
                ),
            }

    CONFIG_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    config_payload = {
        "projectId": PROJECT_ID,
        "projectNumber": PROJECT_NUMBER,
        "location": LOCATION,
        "appId": APP_ID,
        "appName": APP_NAME,
        "appVersion": version_name,
        "versionDisplayName": version_display_name,
        "deploymentId": deployment_id,
        "deploymentName": deployment_name_by_number,
        "deploymentNameByProjectId": deployment_name_by_id,
        "webWidgetTitle": "Cymbal Concierge",
        "clientTools": client_tools,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }
    CONFIG_OUT_PATH.write_text(
        json.dumps(config_payload, indent=2) + "\n", encoding="utf-8"
    )
    print(f"4. Saved deployment configuration to {CONFIG_OUT_PATH}:")
    print(json.dumps(config_payload, indent=2))


if __name__ == "__main__":
    main()
