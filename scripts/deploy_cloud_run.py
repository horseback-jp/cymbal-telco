#!/usr/bin/env python3
"""Deploys the Cymbal Telecom Converged Storefront Web UI to Cloud Run using ADC."""

from __future__ import annotations

from datetime import datetime, timezone
import io
import json
from pathlib import Path
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request

import google.auth
import google.auth.transport.requests

PROJECT_ID = "ces-demo-emea"
PROJECT_NUMBER = "1097682577517"
REGION = "europe-west1"
SERVICE_NAME = "jph-cymbal-converged-web"
AR_REPO = "cloud-run-source-deploy"
STAGING_BUCKET = f"{PROJECT_ID}_cloudbuild"

REPO_ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = REPO_ROOT / "web"


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
    body: dict | bytes | None = None,
    content_type: str = "application/json",
) -> dict:
    if isinstance(body, dict):
        data = json.dumps(body).encode("utf-8")
    else:
        data = body
    req = urllib.request.Request(url=url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("x-goog-user-project", PROJECT_ID)
    if data is not None:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {e.code} on {method} {url}: {err_body}"
        ) from e


def build_tarball(source_dir: Path) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for item in sorted(source_dir.rglob("*")):
            if "__pycache__" in item.parts or item.name.startswith("."):
                if item.name != ".dockerignore":
                    continue
            rel = item.relative_to(source_dir)
            tar.add(item, arcname=str(rel), recursive=False)
    return buf.getvalue()


def ensure_bucket(token: str, bucket_name: str) -> None:
    try:
        api_request(
            "GET",
            f"https://storage.googleapis.com/storage/v1/b/{bucket_name}",
            token,
        )
    except RuntimeError as e:
        if "HTTP 404" in str(e):
            print(f"Creating staging bucket {bucket_name}...")
            api_request(
                "POST",
                f"https://storage.googleapis.com/storage/v1/b?project={PROJECT_ID}",
                token,
                body={"name": bucket_name, "location": "EU"},
            )
        else:
            raise


def wait_for_lro(op_url: str, token: str, label: str = "operation") -> dict:
    for _ in range(120):
        time.sleep(3)
        status = api_request("GET", op_url, token)
        if status.get("done"):
            if "error" in status:
                raise RuntimeError(f"{label} failed: {status['error']}")
            return status.get("response", status)
    raise TimeoutError(f"Timed out waiting for {label}: {op_url}")


def main() -> None:
    token = get_access_token()
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    object_name = f"source/{SERVICE_NAME}-{ts}.tgz"
    image_uri = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/{AR_REPO}/{SERVICE_NAME}:{ts}"

    print(f"1. Packaging {WEB_DIR} and uploading to gs://{STAGING_BUCKET}/{object_name}...")
    ensure_bucket(token, STAGING_BUCKET)
    tar_bytes = build_tarball(WEB_DIR)
    upload_url = (
        f"https://storage.googleapis.com/upload/storage/v1/b/{STAGING_BUCKET}/o"
        f"?uploadType=media&name={urllib.parse.quote(object_name, safe='')}"
    )
    api_request(
        "POST",
        upload_url,
        token,
        body=tar_bytes,
        content_type="application/gzip",
    )
    print(f"   -> Uploaded {len(tar_bytes):,} bytes")

    print(f"2. Submitting Cloud Build for {image_uri}...")
    build_body = {
        "source": {
            "storageSource": {
                "bucket": STAGING_BUCKET,
                "object": object_name,
            }
        },
        "steps": [
            {
                "name": "gcr.io/cloud-builders/docker",
                "args": ["build", "-t", image_uri, "."],
            }
        ],
        "images": [image_uri],
    }
    build_op = api_request(
        "POST",
        f"https://cloudbuild.googleapis.com/v1/projects/{PROJECT_ID}/builds",
        token,
        body=build_body,
    )
    op_name = build_op["name"]
    wait_for_lro(
        f"https://cloudbuild.googleapis.com/v1/{op_name}",
        token,
        label="Cloud Build",
    )
    print(f"   -> Built and pushed image: {image_uri}")

    print(f"3. Deploying Cloud Run service '{SERVICE_NAME}' in {REGION} (invokerIamDisabled=True)...")
    service_parent = f"projects/{PROJECT_ID}/locations/{REGION}"
    service_full_name = f"{service_parent}/services/{SERVICE_NAME}"
    service_url_base = f"https://run.googleapis.com/v2/{service_full_name}"

    service_spec = {
        "ingress": "INGRESS_TRAFFIC_ALL",
        "invokerIamDisabled": True,
        "template": {
            "serviceAccount": f"{PROJECT_NUMBER}-compute@developer.gserviceaccount.com",
            "containers": [
                {
                    "image": image_uri,
                    "ports": [{"containerPort": 8080}],
                    "resources": {
                        "limits": {
                            "cpu": "1",
                            "memory": "512Mi",
                        }
                    },
                }
            ],
        },
    }

    exists = False
    try:
        api_request("GET", service_url_base, token)
        exists = True
    except RuntimeError as e:
        if "HTTP 404" not in str(e):
            raise

    if exists:
        print("   -> Updating existing Cloud Run service...")
        run_op = api_request(
            "PATCH",
            service_url_base,
            token,
            body=service_spec,
        )
    else:
        print("   -> Creating new Cloud Run service...")
        create_url = (
            f"https://run.googleapis.com/v2/{service_parent}/services"
            f"?serviceId={SERVICE_NAME}"
        )
        run_op = api_request(
            "POST",
            create_url,
            token,
            body=service_spec,
        )

    wait_for_lro(
        f"https://run.googleapis.com/v2/{run_op['name']}",
        token,
        label="Cloud Run deployment",
    )

    svc = api_request("GET", service_url_base, token)
    uri = svc.get("uri", "")
    urls = svc.get("urls", [])
    print("\n✓ Cloud Run Deployment Complete!")
    print(f"  Primary URL: {uri}")
    if urls:
        print(f"  All URLs:    {', '.join(urls)}")


if __name__ == "__main__":
    main()
