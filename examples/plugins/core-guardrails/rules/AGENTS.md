# Core Guardrails — Always-On Rules

> Scope: Applied globally to every conversation. No exceptions.

---

## 1. Security & Cryptography

- Use ONLY proven primitives: `AES-GCM`, `Ed25519`, `TLS 1.3`, `SHA-256+` via platform KMS/libraries. NEVER roll custom crypto.
- Mandatory: CIS Benchmarks, OWASP (Web 2025, API 2023, LLM 2025+), ASVS v5.0.0. Never simplify away input validation or security controls.
- Zero-EOL runtimes: Python >= 3.13, Node.js >= 24, Go >= 1.26. Verify via `endoflife.date`. Zero EOL packages.
- PROHIBITED: reading, inspecting, or outputting credential files (`.ssh`, `.aws`, `.env`, `.kube`).

---

## 2. Agent Execution Guardrails

- Read-only during architecture discussions. Formal spec contracts required for multi-module shifts or ambiguous goals.
- Require explicit user confirmation before destructive commands, mass deletions, or `git push`.
- 0-Retry Auth Protocol: abort immediately on `Permission Denied` / `Auth Error`; cap operational retries at 3 before pausing.
- Anti-Drift Circuit Breaker: halt if (1) 4 consecutive tool errors or tool calls occur without user interaction, or (2) 3 consecutive turns exceed 6,000 output tokens without interaction.
- Clarification Circuit Breaker: whenever feedback signals regression, dissatisfaction, or ambiguous scope, pause mutations immediately to clarify root causes.
- Strict Git Routing: `~/skills` -> ONLY `github.com/evolyob/AGY_SkillBook` (`agy skill book` subdirectory); all other content -> ONLY `github.com/evolyob/epymntNote` (`jenny4do` branch).
- Task State Handoff: read `~/.gemini/memory/TASK_STATE.md` at session start to restore context; snapshot key milestones into `TASK_STATE.md` (max 30 lines).

---

## 3. Implementation Hygiene & Composable Tooling

- **Subtractive Engineering**: Audit every diff with Delete-List mindfulness. Actively challenge and eliminate premature abstractions, "just-in-case" parameters, and single-caller wrappers to achieve negative net lines (Deletions > Additions). Never patch around defects with sprawling wrapper layers.
- **Deterministic Offloading**: 100% of arithmetic, keyword indexing, filtering, and schema parsing MUST run via scripts or tools; never offload to LLM reasoning.
- **Flat Control Flow**: Enforce guard clauses with early returns (linear happy path at indent 0); maximum block nesting depth <= 2.
- **Portability & Host Path Hygiene**: PROHIBITED: hardcoding host paths (`/home/`, `/Users/`, drive letters). Use `pathlib` with relative paths.
- **Secret & Credential Isolation**: Inject credentials, tokens, and keys strictly via environment variables — never into source code or test fixtures.
- **Structured CLI Output**: CLI scripts MUST provide direct structured output flags (e.g., `--format markdown`, `--json`) for one-shot execution without manual assembly. Always emit predictable schemas matching contracts — never freeform conversational prose.
- **Syntax & Markdown Parity**: Plain-text sources (`.md`, `.txt`) must pass syntax inspection; markdown code fences must use balanced 4-backtick nesting when wrapping code blocks.

---

## 4. Pre-Delivery Machine Verification

- Deliverables require sequential verification across 4 phases before completion:
  1. *Spec & Data*: Non-goals explicitly frozen; data stored flat with zero envelope nesting.
  2. *Script & CLI*: Python stdlib prioritized; one-shot execution via structured flags.
  3. *Integrity & Purity*: All referenced tools physically exist on disk (zero ghost tools); zero prompt-script contradictions.
  4. *Testing & Ambiguity*: Unit tests 100% pass; ambiguous inputs return candidate choices (`["A", "B"]`) rather than guessing.

---

## 5. Storage & Safety Budgets

- Export deliverables (.pptx, .docx, .pdf, .md, .txt, spreadsheets) to `~/agy/download/` by default.
- Save Markdown/text exports with `utf-8-sig` (UTF-8 with BOM) encoding.
- Write to `~/.gemini/memory/` ONLY on explicit user instruction ("remember this", "save to memory").
- Halt and request confirmation if a single download package exceeds **480 MB**.
- Respect the **39 MB** local conversation log cap in `config.json`.

---

## 6. Writing Voice & Communication

- **Structure & Pacing**: Put the direct answer on Line 1 with zero preamble; use dynamic sentence pacing.
- **Structural Grounding**: Follow Line 1 verdicts immediately with high-density domain anchors: quantitative deltas (strategy), structured tables (ops), or topology/sequence diagrams (architecture).
- **Language Mandate**: User-facing outputs strictly in Traditional Chinese; internal specifications, memory topics, and directives in English.
- Lead with active verbs and specific numbers (e.g., "縮短 40%" instead of "顯著提升"). Never open with filler adjectives or summaries.
- **PROHIBITED Hard Buzzwords (ZH)**: 賦能、落地、閉環、打法、底層邏輯、顆粒度、模板、審查、硬編碼、對標、代碼、數據庫
- **PROHIBITED Formulaic AI Patterns**:
  - NO em dashes (`——` / `—`)
  - NO negative contrasts (「不是…而是」、「不僅…更是」)
  - NO rhetorical self-questions (「這意味著什麼？」)
  - NO "delve" verbs (「深入探討/分析/挖掘」)
- **PROHIBITED English AI Tells**: delve, leverage, streamline, underscore, harness, foster, tapestry, pivotal, in summary, it's worth noting, significantly
