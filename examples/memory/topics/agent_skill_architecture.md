# Agent Skill & Security Architecture Guide

> **Role**: Unified engineering reference for knowledge representation, 4-step skill build lifecycle, cryptography baselines, and runtime/web compliance standards.

---

## 1. Agent Knowledge Representation
- All memory topics, specs, and templates MUST be concrete, non-abstract, high-signal (plain English, operational tables/lists).
- **Prohibit**: Essays, full-file dumps for localized fixes, dramatic metaphors, or vague philosophy that bloats token context.

---

## 2. Skill Build & Validation Standard (4-Step Flow)
1. **Spec First** (`spec_template.md`): Freeze Goal, Non-Goals, Whitelist Paths, Zero-EOL Dependencies, and Acceptance Criteria.
2. **Data Structure** (`SKILL_DATA_SPEC.md`): Flat list default (Pattern A), zero envelope tax. Build in-memory inverted index when items > 20 (O(1) lookup). Data schema and documented counts MUST match physical assets exactly.
3. **Core Script & Tool Integrity** (`senior_coding_laws.md`): Python stdlib prioritized (`scripts/<module>.py`), max block nesting depth <= 2. All scripts referenced in `SKILL.md` MUST physically exist in `scripts/` (zero ghost tools; zero script paradox).
4. **Semantic Test Anchors** (`tests/`): Lock edge cases and naming collisions with unit tests. When input matches multiple categories equally, return candidate choices (`["A", "B"]`) for clarification rather than guessing.

---

## 3. Security, Cryptography & Compliance Standards
- **Approved Primitives**: Use ONLY proven cryptographic primitives: `AES-GCM`, `Ed25519`, `TLS 1.3`, `SHA-256+` via platform KMS/libraries. NEVER roll custom crypto.
- **Compliance Baselines**: Mandatory compliance with CIS Benchmarks, OWASP (Web 2025, API 2023, LLM 2025+), and ASVS v5.0.0. Never bypass input validation or security controls.
- **Zero-EOL & Dependency Hygiene**:
  - Enforce modern runtimes: Python >= 3.13, Node.js >= 24 (LTS), Go >= 1.26.
  - Prohibit PEP 594 removed modules (`cgi`, `pipes`, `crypt`, `distutils`, `chunk`, `telnetlib`, `sndhdr`, `imghdr`, `nntplib`, `xdrlib`).
  - Declare dependencies via PEP 723 (inline script metadata) or PEP 621 (`pyproject.toml`).
- **Frontend & Web Standards**:
  - Follow WHATWG HTML Living Standard & W3C CSS standards.
  - Deliverables must be self-contained single-file HTML5 with embedded CSS reset (`box-sizing: border-box`, `margin: 0`), zero unvetted external scripts.
  - Wrap embedded code blocks strictly with balanced 4-backtick (````) syntax to eliminate DOM leaking and markdown injection.
