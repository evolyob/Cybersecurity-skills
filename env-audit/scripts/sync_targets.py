#!/usr/bin/env python3
"""
Sync targets.json with live endoflife.date & Homebrew Formulae APIs
"""
import os
import json
import re
import datetime
import urllib.request
from concurrent.futures import ThreadPoolExecutor

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TARGETS_FILE = os.path.join(SCRIPT_DIR, "targets.json")

def parse_cycle_version(cycle_str):
    m = re.findall(r"\d+", str(cycle_str))
    return (int(m[0]), int(m[1])) if len(m) >= 2 else ((int(m[0]), 0) if m else None)

def fetch_slug_data(slug):
    url = f"https://endoflife.date/api/{slug}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "env-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return slug, json.loads(resp.read().decode())
    except Exception:
        return slug, None

def fetch_brew_data(formula):
    url = f"https://formulae.brew.sh/api/formula/{formula}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "env-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return formula, data.get("versions", {}).get("stable")
    except Exception:
        return formula, None

def sync():
    if not os.path.exists(TARGETS_FILE):
        print(f"Error: {TARGETS_FILE} not found.")
        return

    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    targets = raw if isinstance(raw, list) else raw.get("binaries", [])

    unique_slugs = list({t["eol_slug"] for t in targets if "eol_slug" in t})
    unique_brews = list({t["brew_formula"] for t in targets if "brew_formula" in t})
    print(f"Fetching live data for {len(unique_slugs)} EOL slugs and {len(unique_brews)} Homebrew formulae...")

    slug_data_map, brew_data_map = {}, {}
    with ThreadPoolExecutor(max_workers=10) as ex:
        for slug, data in ex.map(fetch_slug_data, unique_slugs):
            if data:
                slug_data_map[slug] = data
        for formula, ver in ex.map(fetch_brew_data, unique_brews):
            if ver:
                brew_data_map[formula] = ver

    today = datetime.date.today().isoformat()
    updated_count = 0
    print("\nSynchronizing target definitions:")
    for item in targets:
        slug = item.get("eol_slug")
        changed = False

        if slug and slug in slug_data_map:
            active_lts, active_supported = [], []
            for c in slug_data_map[slug]:
                eol_val, cycle_name = c.get("eol"), str(c.get("cycle"))
                if (isinstance(eol_val, str) and eol_val <= today) or eol_val is True:
                    continue
                if c.get("lts"):
                    active_lts.append(cycle_name)
                active_supported.append(cycle_name)

            old_lts, old_eol = item.get("lts", ""), item.get("eol_below")
            new_lts = (" / ".join(active_lts[:2]) + " LTS") if active_lts else (" / ".join(active_supported[:2]) if active_supported else old_lts)
            parsed = parse_cycle_version(active_supported[-1]) if active_supported else None
            new_eol = list(parsed) if parsed else old_eol

            if (new_eol != old_eol) or (new_lts != old_lts):
                item["eol_below"], item["lts"] = new_eol, new_lts
                changed = True

        bf = item.get("brew_formula")
        if bf and bf in brew_data_map:
            if item.get("brew_latest") != brew_data_map[bf]:
                item["brew_latest"] = brew_data_map[bf]
                changed = True

        status_str = f"LTS: {item.get('lts')} | Brew: {item.get('brew_latest')}"
        if changed:
            updated_count += 1
            print(f"  [UPDATED] {item['name']} -> {status_str}")
        else:
            print(f"  [UP-TO-DATE] {item['name']} -> {status_str}")

    with open(TARGETS_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)
    print(f"\nSuccessfully synchronized! ({updated_count} targets updated, saved to targets.json)")

if __name__ == "__main__":
    sync()
