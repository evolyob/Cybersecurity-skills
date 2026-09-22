# Agent Architecture & Skill Lifecycle Guide

> **Role**: Unified reference for knowledge representation principles, Python/LLM division of labor, and skill build execution.

---

## 1. Agent Knowledge Representation
- All memory topics, specs, and templates MUST be concrete, non-abstract, high-signal (plain English, operational tables/lists).
- **Prohibit**: Essays, full-file dumps for localized fixes, dramatic metaphors, or vague philosophy that bloats token context.

---

## 2. Division of Labor: Python vs LLM (分工明確)
- **Deterministic Computation**: Python handles 100% of arithmetic, data filtering, keyword indexing, and schema validation. Never offload math or lookup logic to LLM deduction.
- **Cognitive Orchestration**: LLM handles intent classification, candidate selection, user clarification, and compact formatting (surgical diffs, ASCII trees, terminal box-drawing diagrams).
- **Contract Enforcement**: Hard boundaries (Non-Goals, Allowed Paths, Verification Commands) MUST be defined before any code execution begins.

---

## 3. Skill Build Flow (4-Step Standard)
1. **Spec First** (`spec_template.md`): Freeze Goal, Non-Goals, Allowed Paths, Dependencies, Acceptance Criteria.
2. **Data Structure** (`SKILL_DATA_SPEC.md`): Flat list default (Pattern A), zero envelope wrapping. Build in-memory inverted index when items > 20 (O(1) lookup).
3. **Core Script** (`senior_coding_laws.md`): Python stdlib only (`scripts/<module>.py`). Max `if` nesting <= 2. Python computes; LLM formats.
4. **Semantic Test Anchors** (`tests/`): Lock edge cases, ambiguous matches, and naming collisions with deterministic unit tests.

---

## 4. Evolution Traps to Reject (MUST NOT)
1. **No Cognitive Dump**: Never delete Python analyzer scripts to make LLM deduce rules. Keep computation in Python.
2. **No Script Paradox**: Never instruct LLM to avoid rigid templates if the script outputs fixed templates. Script output IS the baseline.
3. **No Ghost Tools**: Every script named in `SKILL.md` MUST physically exist in `scripts/`. Never reference unbuilt scripts.
4. **No Silent Ambiguity**: When input matches multiple categories equally, return `candidates: ["A", "B"]` for user clarification. Never guess.
5. **No Data Drift**: Documented counts, flags, and schema fields MUST match underlying data assets exactly.

---

## 5. Composable CLI & Pre-Delivery Checklist
- CLI scripts MUST provide structured output flags (`--format markdown`, `--json`) for one-shot execution without manual assembly.

| Phase | Check |
|---|---|
| Spec | Non-Goals explicitly defined? |
| Data | Flat with zero envelope nesting? |
| Script | Python stdlib only? |
| CLI | One-shot execution via flags? |
| Integrity | All `SKILL.md` tools physically exist? |
| Purity | No prompt-script contradictions? |
| Test | Unit tests pass with zero failures? |
| Ambiguity | Ambiguous inputs return candidate choices? |
