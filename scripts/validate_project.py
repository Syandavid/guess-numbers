#!/usr/bin/env python3
"""Run offline integrity checks for the guess-numbers PWA."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FILES = (
    "index.html",
    "manifest.webmanifest",
    "sw.js",
    ".firebaserc",
    "firebase.json",
    "firestore.rules",
    "firestore.indexes.json",
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(relative: str):
    try:
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        fail(f"{relative} is not valid JSON: {exc}")


def check_manifest() -> None:
    manifest = load_json("manifest.webmanifest")
    for key in ("name", "short_name", "start_url", "scope", "display", "icons"):
        if not manifest.get(key):
            fail(f"manifest.webmanifest missing {key}")
    if manifest["display"] not in {"standalone", "fullscreen", "minimal-ui"}:
        fail("manifest.webmanifest has an unexpected display mode")
    if not isinstance(manifest["icons"], list) or len(manifest["icons"]) < 2:
        fail("manifest.webmanifest should define at least two icons")
    for icon in manifest["icons"]:
        if not (ROOT / str(icon.get("src", ""))).is_file():
            fail(f"manifest icon is missing: {icon.get('src')}")


def check_firebase_config() -> None:
    firebase = load_json("firebase.json")
    fire = firebase.get("firestore") or {}
    if fire.get("rules") != "firestore.rules" or fire.get("indexes") != "firestore.indexes.json":
        fail("firebase.json must point to the checked-in Firestore rules and indexes")
    firebase_rc = load_json(".firebaserc")
    project = (firebase_rc.get("projects") or {}).get("default")
    if not project:
        fail(".firebaserc has no default Firebase project")


def check_html_and_service_worker() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    if 'rel="manifest"' not in html:
        fail("index.html must reference manifest.webmanifest")
    if "serviceWorker.register" not in html:
        fail("index.html must register the service worker")
    if "firestore.googleapis.com" not in html:
        fail("index.html must contain the Firestore API integration")

    sw = (ROOT / "sw.js").read_text(encoding="utf-8")
    if not re.search(r'const\s+CACHE\s*=\s*["\'][^"\']+["\']', sw):
        fail("sw.js has no cache version")
    for asset in re.findall(r'["\'](\./[^"\']+)["\']', sw):
        relative = asset[2:]
        if relative and not (ROOT / relative).is_file():
            fail(f"service worker asset is missing: {relative}")


def check_rules() -> None:
    rules = (ROOT / "firestore.rules").read_text(encoding="utf-8")
    for marker in ("rules_version = '2';", "service cloud.firestore", "match /rooms/{code}"):
        if marker not in rules:
            fail(f"firestore.rules is missing: {marker}")
    if "allow write: if true" in rules or "allow read: if true" in rules:
        fail("firestore.rules contains an unrestricted allow rule")


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))
    check_manifest()
    check_firebase_config()
    check_html_and_service_worker()
    check_rules()
    print("OK: guess-numbers PWA integrity checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
