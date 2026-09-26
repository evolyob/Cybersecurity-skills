#!/usr/bin/env python3
"""PostToolUse Quality Guard: Path leakage, invisibles/bidi, Markdown syntax, Mermaid 11.x."""
import sys
import json, re
from pathlib import Path

PATH_REGEX = re.compile(r"(?:/(?:Users|home)/[a-zA-Z0-9_-]+/|/root/|[a-zA-Z]:[\\/]|\\\\[a-zA-Z0-9_.-]+\\[a-zA-Z0-9_.-]+)")
INVISIBLES_REGEX = re.compile(r"[\u200b-\u200d\u2060\u202a-\u202e\u2066-\u2069]")

def check_path_leakage(content: str, filename: str) -> None:
    if "topics_architecture_optimization_guide" in filename or "template" in filename: return
    leaks = [f"Line {i}: {L.strip()[:75]}" for i, L in enumerate(content.splitlines(), 1)
             if not any(k in L for k in ('re.search', 'Zero-Leakage', 'Path Leakage', 'PATH_REGEX')) and PATH_REGEX.search(L)]
    if leaks:
        print(f"\n[PATH LEAK WARNING] {filename}: Detected hardcoded local user path:", file=sys.stderr)
        for leak in leaks[:3]: print(f"   {leak}", file=sys.stderr)

def check_invisible_characters(content: str, filename: str) -> None:
    if any(k in filename for k in ("quality_guard", "ingest", "rules_gate", "template")): return
    matches = INVISIBLES_REGEX.findall(content)
    if matches:
        hex_codes = sorted({f"U+{ord(c):04X}" for c in matches})[:3]
        print(f"\n[SECURITY ADVISORY] {filename}: Detected invisible/bidi characters {hex_codes}. May cause visual spoofing or syntax errors.", file=sys.stderr)

def check_mermaid_blocks(md_content: str, filename: str) -> None:
    pattern_square = re.compile(r'(\b[a-zA-Z0-9_.-]+)\[(?!\s*")([^\]\n]*?[\(\)<>][^\]\n]*?)\]')
    mermaid_block_re = re.compile(r'(^`{3,4})mermaid[^\n]*\n(.*?)\n\1', re.DOTALL | re.MULTILINE)
    unquoted = [bad.group(0) for m in mermaid_block_re.finditer(md_content) for bad in pattern_square.finditer(m.group(2))]
    if unquoted:
        print(f"\n[MERMAID SYNTAX ADVISORY] {filename}: Quote labels with special chars, e.g. id[\"Label (info)\"]. Found: {unquoted[:2]}", file=sys.stderr)

def check_code_fences(md_content: str, filename: str) -> None:
    fences = [i + 1 for i, L in enumerate(md_content.splitlines()) if L.strip().startswith("```")]
    if len(fences) % 2 != 0:
        print(f"\n[MARKDOWN FENCE ERROR] {filename}: Unbalanced code fences ({len(fences)} markers). Near lines: {fences[-3:]}", file=sys.stderr)

def check_setext_headings(md_content: str, filename: str) -> None:
    for m in re.finditer(r'^([^\w\s\r\n]{2,})\r?\n([=-]{3,})\s*$', md_content, re.MULTILINE):
        print(f"\n[SETEXT SYNTAX ADVISORY] {filename}: Phantom Setext heading '{m.group(1)}' followed by '{m.group(2)}'. Separate with blank line.", file=sys.stderr)
        return

def process_file(file_path: str) -> None:
    p = Path(file_path).resolve()
    if not p.is_file(): return
    try:
        content = p.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return

    check_path_leakage(content, p.name)
    check_invisible_characters(content, p.name)
    if p.suffix.lower() == '.md':
        check_code_fences(content, p.name)
        check_setext_headings(content, p.name)
        check_mermaid_blocks(content, p.name)

def main() -> None:
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input: return print("{}")
        args = json.loads(raw_input).get('toolCall', {}).get('args', {})
        target = args.get('TargetFile') or args.get('file_path')
        if target: process_file(target)
    except (json.JSONDecodeError, KeyError):
        pass
    print("{}")

if __name__ == '__main__':
    main()
