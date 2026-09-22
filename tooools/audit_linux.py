#!/usr/bin/env python3
"""
Linux Environment & Security Audit Script (Ultra-Lightweight Engine)
Reads tool registry from targets.json and executes native OS queries.
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
    distro = "Linux"
    family = "debian"
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release", encoding="utf-8") as f:
            content = f.read().lower()
            for line in content.splitlines():
                if line.startswith("pretty_name="):
                    distro = line.split("=", 1)[1].strip('"\'\n')
            if any(x in content for x in ["rhel", "centos", "rocky", "fedora"]):
                family = "redhat"
    return distro, f"Linux ({platform.machine()})", family

def get_tool_version(tool_item):
    names = [tool_item["name"]] + tool_item.get("aliases", [])
    path = next((shutil.which(n) for n in names if shutil.which(n)), None)
    if not path or path.startswith("/mnt/"):
        return None
    
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", SUDO_ASKPASS="/bin/false", SUDO_NONINTERACTIVE="true")
    ver = "Installed"
    flags = tool_item.get("flags", ["--version", "-v", "version"])
    for flag in flags:
        try:
            cmd = [path] + flag.split()
            proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=1.0, env=env, start_new_session=True)
            out = proc.stdout.strip() if proc.stdout else ""
            if proc.returncode == 0 and out and not any(err in out.lower() for err in ["usage:", "password for", "invalid option", "unknown option"]):
                ver = out.split("\n")[0]
                break
        except Exception:
            continue
            
    # Evaluate EOL against endoflife.date rule
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
        out = subprocess.run([path, "-G", "localhost"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout.lower()
        ciphers = next((l for l in out.splitlines() if l.startswith("ciphers ")), "")
        macs = next((l for l in out.splitlines() if l.startswith("macs ")), "")
        res["weak_algo"] = {
            "cbc": "cbc" in ciphers or "3des" in ciphers,
            "sha1": "sha1" in macs or "md5" in macs
        }
    return res

def get_outdated_packages(family):
    outdated = {}
    if family == "debian" and shutil.which("apt"):
        try:
            proc = subprocess.run(["apt", "list", "--upgradable"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3)
            lines = proc.stdout.splitlines() if proc.returncode == 0 else []
            for line in lines:
                if "upgradable from:" not in line:
                    continue
                parts = line.split()
                pkg_name = parts[0].split("/")[0]
                candidate_ver = parts[1]
                installed_ver = line.split("upgradable from:")[1].strip(" ]\n")
                outdated[pkg_name] = {"installed": installed_ver, "candidate": candidate_ver}
        except Exception:
            pass
        return outdated

    if family == "redhat":
        pkg_mgr = shutil.which("dnf") or shutil.which("yum")
        if not pkg_mgr:
            return outdated
        try:
            proc = subprocess.run([pkg_mgr, "check-update", "--quiet"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            lines = proc.stdout.splitlines() if (proc.returncode in (0, 100) and proc.stdout) else []
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 2:
                    pkg_name = parts[0].split(".")[0]
                    outdated[pkg_name] = {"candidate": parts[1]}
        except Exception:
            pass
    return outdated

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

    outdated_pkgs = get_outdated_packages(family)
    pkg_map = {"pip3": "python3-pip", "node": "nodejs", "ssh": "openssh-client", "psql": "postgresql-client"}
    
    for name, data in results.items():
        pkg_name = pkg_map.get(name, name)
        is_upgradable = pkg_name in outdated_pkgs
        is_eol = data.get("is_eol", False)
        candidate = outdated_pkgs[pkg_name]["candidate"] if is_upgradable else data["version"]
        
        data["is_upgradable"] = is_upgradable or is_eol
        data["candidate"] = candidate
        data["pkg_manager"] = {
            "pkg_package": pkg_name,
            "is_upgradable": is_upgradable or is_eol,
            "candidate": candidate
        }

    guard_results = audit_guards(guards, family)

    report = {
        "os_name": os_name,
        "kernel": kernel,
        "family": family,
        "shell": os.environ.get("SHELL", "/bin/bash"),
        "detected_count": len(results),
        "installed_binaries": results,
        "system_guards": guard_results,
        "outdated_system_packages": outdated_pkgs,
        "cve_vulnerabilities": []
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
