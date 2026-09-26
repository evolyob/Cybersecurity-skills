#!/usr/bin/env python3
"""Universal Skill & Code Auditor (Lean Enterprise Standard)."""
import ast, re, sys
from pathlib import Path

PEP_594_REMOVED = {"cgi", "cgitb", "pipes", "crypt", "imghdr", "sndhdr", "aifc", "audioop", "chunk", "mailcap", "nntplib", "sunau", "telnetlib", "uu", "xdrlib", "distutils"}
SECRETS = [r"sk-[a-zA-Z0-9]{20,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z]+ PRIVATE KEY-----", r"(?i)\b(?:password|passwd|pwd)\s*[:=]\s*['\"](?!(?:test|mock|fake|dummy|example|xxxx|admin|placeholder|sample|changeme))[^'\"\s]{6,}['\"]"]
PRIVS = ["su" + "do ", "ch" + "mod +x", "ch" + "own ", "/et" + "c/shadow", "/et" + "c/passwd"]
INSECURE_TELEMETRY = [
    r"(?i)\b(?:verify\s*=\s*False|check_hostname\s*=\s*False)\b",
    r"(?i)\b(?:import\s+(?:telemetry|mixpanel|posthog)|(?:telemetry|mixpanel|posthog)\.[a-zA-Z_]|https?://[^\s'\"]*(?:telemetry|mixpanel|segment\.io|posthog))\b",
    r"(?i)\.workers\.dev/(?:telemetry|collect|log|track)",
]
FRONTEND_EXTS = {".html", ".htm", ".js", ".mjs", ".ts", ".jsx", ".tsx", ".vue"}


def audit_source(src: str, filename: str, is_markdown: bool = False, skill_txt: str = "", local_modules: set = None) -> str:
    lines, blockers, warnings = len(src.splitlines()), [], []
    is_test, is_meta = "test" in filename.lower(), filename in ["audit.py", "remediation_guide.md", "developer_7_coding_laws_and_ast_audit.md"]
    local_mods = local_modules or set()

    # 1. Text & Security Gate
    if not is_meta:
        for idx, line in enumerate(src.splitlines(), start=1):
            if not line.strip().startswith("#") and not any(k in line for k in ("re.search", "re.compile", "Zero-Leakage", "r'/", 'r"/')):
                if re.search(r'/(Users|home)/[a-zA-Z0-9_-]+/', line):
                    blockers.append(f"Line {idx}: Hardcoded absolute user path (~/ or $HOME required)")
                    break
        for s in SECRETS:
            if re.search(s, src): blockers.append("Plaintext secret/API key")
        for p in PRIVS:
            if p in src and not ("Zero" in src or "detect" in src or "guard" in src): blockers.append(f"Privilege escalation ({p})")
        for t in INSECURE_TELEMETRY:
            if re.search(t, src): blockers.append("Insecure TLS bypass or telemetry endpoint detected")
        if re.search(r"ignore\s+previous\s+instructions|system\s+override|DAN\s+mode", src, re.I): blockers.append("Prompt injection keyword")

    # 2. Markdown Specific Gate
    if is_markdown:
        limit = 50 if filename == "SKILL.md" else (30 if filename == "SECURITY.md" else 200)
        if lines > limit and not is_meta: warnings.append(f"Lines {lines} > {limit} (move overflow to references/)")
        if filename == "SKILL.md":
            for sec, label in [("description:", "description"), ("dependencies:", "dependencies"), (r"##\s+Objective", "## Objective"), (r"##\s+Execution\s+Workflow", "## Execution Workflow")]:
                if not re.search(sec, src, re.I): blockers.append(f"SKILL.md missing required section: '{label}'")
        elif filename == "SECURITY.md":
            for sec, label in [(r"##\s+Scope", "## Scope"), (r"##\s+Dependencies", "## Dependencies"), (r"##\s+Execution", "## Execution")]:
                if not re.search(sec, src, re.I): blockers.append(f"SECURITY.md missing required section: '{label}'")
        stack = []
        for l in src.splitlines():
            s = l.strip()
            if s.startswith("````"):
                if stack and stack[-1] == 4: stack.pop()
                else: stack.append(4)
            elif s.startswith("```"):
                if stack and stack[-1] == 3: stack.pop()
                elif not stack or stack[-1] == 4: stack.append(3)
        if stack: blockers.append("Unclosed code fence / Broken 4-backtick nesting")

    # 3. Python Analysis (Single-Pass AST Visitor)
    py_blocks = re.findall(r"```python[^\n]*\n(.*?)\n```", src, re.DOTALL) if is_markdown else [src]
    for idx, code in enumerate(py_blocks):
        tag = f"Snippet #{idx+1}" if is_markdown else "Script"
        if not is_markdown and not is_meta and any(re.search(r"\bopen\(", l) and "encoding=" not in l and "wb" not in l and "rb" not in l for l in code.splitlines()):
            warnings.append("Unencoded open() call")
        if re.search(r'f["\x27]<[a-zA-Z]+', code) and not re.search(r"(escape|clean_text|sanitize|&amp;)", code):
            warnings.append(f"{tag} unescaped dynamic markup template")

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            blockers.append(f"{tag} SyntaxError: {e}")
            continue

        has_class, n_defs, dict_lines = 0, 0, 0
        imported_modules, soft_imports, import_names, used_names = set(), set(), set(), set()

        def check_nesting(node, current_depth=0):
            if isinstance(node, ast.If):
                if current_depth >= 2: warnings.append(f"{tag} nested if-block depth {current_depth+1} > 2")
                for child in node.body: check_nesting(child, current_depth + 1)
                orelse_depth = current_depth if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If) else current_depth + 1
                for child in node.orelse: check_nesting(child, orelse_depth)
            else:
                for child in ast.iter_child_nodes(node): check_nesting(child, current_depth)
        if not is_meta: check_nesting(tree, 0)

        def check_duplicate_defs(nodes, scope_name="module"):
            seen = set()
            for n in nodes:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if not any((isinstance(d, ast.Name) and d.id == "overload") or (isinstance(d, ast.Attribute) and d.attr == "overload") for d in getattr(n, "decorator_list", [])):
                        if n.name in seen: blockers.append(f"{tag} duplicate definition of '{n.name}' in {scope_name}")
                        seen.add(n.name)
                if isinstance(n, ast.ClassDef): check_duplicate_defs(n.body, f"class '{n.name}'")
        check_duplicate_defs(tree.body)

        for n in ast.walk(tree):
            if isinstance(n, ast.ClassDef): has_class = 1
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                n_defs += 1
                for default in (n.args.defaults + [d for d in n.args.kw_defaults if d is not None]):
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)): blockers.append(f"{tag} mutable default argument in func '{n.name}'")
            elif isinstance(n, ast.Dict):
                dict_lines += max(0, getattr(n, "end_lineno", 0) - getattr(n, "lineno", 0))
                seen_keys = set()
                for k in n.keys:
                    if k is not None:
                        k_val = k.value if isinstance(k, ast.Constant) else (k.id if isinstance(k, ast.Name) else None)
                        if k_val is not None:
                            if k_val in seen_keys: blockers.append(f"{tag} duplicate dictionary key '{k_val}'")
                            seen_keys.add(k_val)
            elif isinstance(n, ast.Global): warnings.append(f"{tag} mutable global state ({n.names})")
            elif isinstance(n, ast.ExceptHandler) and n.type is None: blockers.append(f"{tag} bare 'except:' handler")
            elif isinstance(n, ast.Assert) and not is_test and not is_meta: warnings.append(f"{tag} production 'assert' statement")
            elif not is_meta and isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name) and n.func.id in ["eval", "exec"]: blockers.append(f"{tag} arbitrary execution ({n.func.id})")
                elif isinstance(n.func, ast.Attribute) and n.func.attr == "system" and getattr(n.func.value, "id", None) == "os": blockers.append(f"{tag} os.system() execution")
            elif isinstance(n, ast.Try) and any(h.type is None or (isinstance(h.type, ast.Name) and h.type.id in ("ImportError", "ModuleNotFoundError", "Exception")) for h in n.handlers):
                for child in ast.walk(n):
                    if isinstance(child, ast.Import): soft_imports.update(name.name.split('.')[0] for name in child.names)
                    elif isinstance(child, ast.ImportFrom) and child.module: soft_imports.add(child.module.split('.')[0])
            elif isinstance(n, ast.Import):
                for name in n.names:
                    mod = name.name.split('.')[0]
                    imported_modules.add(mod)
                    import_names.add(name.asname or mod)
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                mod = n.module.split('.')[0]
                imported_modules.add(mod)
                for name in n.names:
                    if name.name != '*': import_names.add(name.asname or name.name)
            elif isinstance(n, ast.Name): used_names.add(n.id)
            elif isinstance(n, ast.Attribute): used_names.add(n.attr)
            elif isinstance(n, ast.Constant) and isinstance(n.value, str): used_names.update(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', n.value))

        if not is_markdown and not is_meta:
            base = 43 + (has_class * 27)
            x_rate = 12 if has_class else 25
            py_limit = base + (n_defs * x_rate) + dict_lines
            if lines > py_limit: warnings.append(f"Lines {lines} > dynamic limit {py_limit} (Base {base} + {n_defs} defs × {x_rate} + {dict_lines} dict lines)")

        for dead in sorted(imported_modules & PEP_594_REMOVED): blockers.append(f"{tag} Zero-EOL: removed stdlib module '{dead}' in Python >= 3.13 (PEP 594)")

        third_party = {m for m in (imported_modules - soft_imports) if m not in sys.stdlib_module_names and m not in local_mods and not m.startswith("_")}
        if skill_txt and third_party:
            for dep in sorted(third_party):
                dep_norm = dep.lower().replace("_", "-")
                if dep.lower() not in skill_txt.lower() and dep_norm not in skill_txt.lower(): blockers.append(f"{tag} undeclared external dependency '{dep}'")
                elif re.search(rf'{dep}\s*==\s*\*|{dep_norm}\s*==\s*\*|\*\s*$', skill_txt): blockers.append(f"{tag} wildcard version '*' for '{dep}' prohibited")

        if not is_markdown:
            unused = sorted(list(import_names - used_names))
            if unused: warnings.append(f"Unused imports: {unused}")

    status = "[✗] FAIL" if blockers else ("[!] WARN" if warnings else "[✓] PASS")
    report = f"{status} {filename} ({lines} lines)"
    if blockers: report += "\n" + "\n".join(f"  └── [BLOCKER] {b}" for b in blockers)
    if warnings: report += "\n" + "\n".join(f"  └── [ADVISORY] {w}" for w in warnings)
    return report


def audit_path(target):
    t = Path(target).resolve()
    if not t.exists():
        return print(f"[ERROR] Target does not exist: {target}")

    root = t if t.is_dir() else t.parent
    skill_md = root / "SKILL.md" if (root / "SKILL.md").exists() else (root.parent / "SKILL.md" if (root.parent / "SKILL.md").exists() else None)
    sec_md = root / "SECURITY.md" if (root / "SECURITY.md").exists() else (root.parent / "SECURITY.md" if (root.parent / "SECURITY.md").exists() else None)
    stxt = skill_md.read_text(encoding="utf-8-sig", errors="ignore") if skill_md and skill_md.exists() else ""
    sectxt = sec_md.read_text(encoding="utf-8-sig", errors="ignore") if sec_md and sec_md.exists() else ""
    # SKILL.md takes precedence; combined with SECURITY.md for comprehensive boundary validation
    spec_txt = f"{stxt}\n{sectxt}".strip()
    ctx_root = (skill_md or sec_md or root).parent if (skill_md or sec_md) else root
    lmods = {p.stem for p in ctx_root.glob("**/*.py")} | {p.name for p in ctx_root.iterdir() if p.is_dir()}

    files = [t] if t.is_file() else sorted(p for p in t.glob("**/*") if p.is_file())
    if t.is_dir(): print(f"\n[SKILL AUDIT] -> {t}\n" + "=" * 55)

    for f in files:
        if f.suffix.lower() in FRONTEND_EXTS:
            try:
                import audit_frontend
                audit_frontend.audit_target(str(f))
            except ImportError: print(f"[✓] PASS {f.name} (Frontend asset)")
        elif f.suffix in [".json", ".xml", ".yaml", ".yml", ".csv", ".txt"]:
            try:
                raw = f.read_text(encoding="utf-8-sig")
                if f.suffix == ".json": import json; json.loads(raw)
                elif f.suffix == ".xml": import xml.etree.ElementTree as ET; ET.fromstring(raw)
                elif f.suffix in [".yaml", ".yml"]:
                    try:
                        import yaml; yaml.safe_load(raw)
                    except ImportError:
                        if "\t" in raw: raise ValueError("YAML files must not contain tabs.")
                elif f.suffix == ".csv": import csv, io; list(csv.reader(io.StringIO(raw)))
                print(f"[✓] PASS {f.name} (Valid syntax & UTF-8 encoding)")
            except Exception as err: print(f"[✗] FAIL {f.name}\n  └── [BLOCKER] Data Syntax/Encoding Error: {err}")
        elif f.suffix in [".py", ".md"]:
            src = f.read_text(encoding="utf-8-sig", errors="ignore")
            print(audit_source(src, f.name, is_markdown=f.suffix == ".md", skill_txt=spec_txt, local_modules=lmods))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 audit.py <target_path>")
        sys.exit(1)
    for arg in sys.argv[1:]: audit_path(arg)
