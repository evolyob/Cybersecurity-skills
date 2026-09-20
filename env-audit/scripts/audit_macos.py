#!/usr/bin/env python3
"""
macOS Environment & Security Audit Script (Ultra-Lightweight Engine)
Reads tool registry from targets.json and executes native macOS / Homebrew queries.
"""
import os
import shutil
import platform
import subprocess
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TARGETS_FILE = os.path.join(SCRIPT_DIR, "targets.json")

def get_os_info():
    arch = platform.machine()
    try:
        ver = subprocess.check_output(["sw_vers", "-productVersion"], text=True).strip()
        product_name = subprocess.check_output(["sw_vers", "-productName"], text=True).strip()
        return f"{product_name} {ver}", f"Darwin ({arch})", "macos"
    except Exception:
        return "macOS", f"Darwin ({arch})", "macos"

def get_tool_version(tool_item):
    names = [tool_item["name"]] + tool_item.get("aliases", [])
    path = next((shutil.which(n) for n in names if shutil.which(n)), None)
    if not path or path.startswith("/Volumes/") or path.startswith("/mnt/"):
        return None
    
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", SUDO_ASKPASS="/bin/false", SUDO_NONINTERACTIVE="true")
    ver = "Installed"
    flags = tool_item.get("flags", ["--version", "-v", "version"])
    for flag in flags:
        try:
            cmd = [path] + flag.split()
            proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=1.0, env=env, start_new_session=True)
            out = proc.stdout.strip() if proc.stdout else ""
            if proc.returncode == 0 and out and not any(err in out.lower() for err in ["usage:", "password for", "invalid option", "unknown option", "xcode-select: error"]):
                ver = out.split("\n")[0]
                break
        except Exception:
            continue
            
    lts = tool_item.get("lts", "Latest")
    is_eol = False
    eol_below = tool_item.get("eol_below")
    if eol_below and ver != "Installed":
        m = re.search(r"(\d+)\.(\d+)", ver)
        try:
            is_eol = bool(m and (int(m.group(1)), int(m.group(2))) < tuple(eol_below))
        except Exception:
            pass
                
    res = {
        "path": path,
        "version": ver,
        "category": tool_item.get("category", "General"),
        "recommended_lts": lts,
        "is_eol": is_eol
    }
    if tool_item["name"] == "ssh":
        out = subprocess.run([path, "-G", "localhost"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout
        if out:
            res["cipher_suite"] = dict(re.findall(r"^(ciphers|macs)\s+(.*)", out, re.M))
    return res

def attach_brew_info(results):
    brew_path = shutil.which("brew")
    if not brew_path:
        return
    try:
        proc = subprocess.run([brew_path, "outdated", "--json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3)
        outdated_set = set()
        if proc.returncode == 0 and proc.stdout.strip():
            data = json.loads(proc.stdout)
            formulae = data.get("formulae", [])
            outdated_set = {item.get("name") for item in formulae}
        
        for k, data in results.items():
            is_eol = data.get("is_eol", False)
            is_outdated = k in outdated_set or is_eol
            data["is_upgradable"] = is_outdated
            data["pkg_manager"] = {
                "brew_package": k,
                "is_outdated": is_outdated
            }
    except Exception:
        pass

def audit_guards(guards, family):
    results = {}
    for g in guards:
        if family not in g.get("platform", [family]):
            continue
        try:
            out = subprocess.run(g["cmd"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=1).stdout.strip()
            passed = bool(re.search(g["expect"], out, re.I)) if out else (g.get("expect") == "0")
        except Exception as e:
            out, passed = str(e), False
        results[g["id"]] = {"name": g["name"], "category": g["category"], "status": "PASS" if passed else "FAIL", "evidence": out}
    return results

def main():
    os_name, kernel, family = get_os_info()
    targets, guards = [], []
    if os.path.exists(TARGETS_FILE):
        with open(TARGETS_FILE, encoding="utf-8") as f:
            raw = json.load(f)
            targets = raw if isinstance(raw, list) else raw.get("binaries", [])
            guards = raw.get("system_guards", []) if isinstance(raw, dict) else []

    results = {}
    for item in targets:
        info = get_tool_version(item)
        if info:
            results[item["name"]] = info

    attach_brew_info(results)
    guard_results = audit_guards(guards, family)

    report = {
        "os_name": os_name,
        "kernel": kernel,
        "family": family,
        "shell": os.environ.get("SHELL", "/bin/zsh"),
        "detected_count": len(results),
        "installed_binaries": results,
        "system_guards": guard_results,
        "cve_vulnerabilities": []
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
