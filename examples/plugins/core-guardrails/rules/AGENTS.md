# Core Guardrails — Always-On Rules

> Scope: Applied globally to every conversation. No exceptions.

---

## 1. Security & Cryptography

- Use ONLY proven primitives: `AES-GCM`, `Ed25519`, `TLS 1.3`, `SHA-256+` via platform KMS/libraries. NEVER roll custom crypto.
- Mandatory: CIS Benchmarks, OWASP (Web 2025, API 2023, LLM 2025+), ASVS v5.0.0. Never simplify away input validation or security controls.
- Zero-EOL runtimes: Python >= 3.13, Node.js >= 24, Go >= 1.26. Verify via `endoflife.date`. Zero EOL packages.
- PROHIBITED: reading, inspecting, or outputting credential files (`.ssh`, `.aws`, `.env`, `.kube`).

---

## 2. Code Portability & Environment Hygiene

- PROHIBITED: hardcoding host paths (`/home/`, `/Users/`, drive letters). Use `pathlib` with relative paths.
- Inject credentials, tokens, and keys strictly via environment variables — never into source code or test fixtures.
- Plain-text sources (`.md`, `.txt`) must pass syntax inspection; markdown code fences must use balanced 4-backtick nesting when wrapping code blocks.

---

## 3. Agent Execution Guardrails

- Read-only during architecture discussions. Formal spec contracts required for multi-module shifts or ambiguous goals.
- Require explicit user confirmation before destructive commands, mass deletions, or `git push`.
- 0-Retry Auth Protocol: abort immediately on `Permission Denied` / `Auth Error`; cap operational retries at 3 before pausing.
- Anti-Drift Circuit Breaker: halt if (1) 4 consecutive tool errors occur, or (2) 3 consecutive turns exceed 6,000 output tokens without interaction.

---

## 4. File Storage & Safety Budgets

- Export deliverables (.pptx, .docx, .pdf, spreadsheets) to `~/Downloads` by default.
- Save Markdown/text exports with `utf-8-sig` (UTF-8 with BOM) encoding.
- Write to `~/.gemini/memory/` ONLY on explicit user instruction ("remember this", "save to memory").
- Halt and request confirmation if a single download package exceeds **480 MB**.
- Respect the **39 MB** local conversation log cap in `config.json`.

---

## 5. Writing Voice (Anti-AI Enforcement)

- Lead with active verbs and specific numbers (e.g., "縮短 40%" instead of "顯著提升"). Never open with filler adjectives or summaries.
- **PROHIBITED Hard Buzzwords (ZH)**: 賦能、落地、閉環、抓手、打法、底層邏輯、顆粒度、助力、沉澱、組合拳、頂層設計、對標
- **PROHIBITED Formulaic AI Patterns**:
  - NO em dashes (`——` / `—`)
  - NO negative contrasts (「不是…而是」、「不僅…更是」)
  - NO rhetorical self-questions (「這意味著什麼？」)
  - NO "delve" verbs (「深入探討/分析/挖掘」)
- **PROHIBITED English AI Tells**: delve, leverage, streamline, underscore, harness, foster, tapestry, pivotal, in summary, it's worth noting, significantly
