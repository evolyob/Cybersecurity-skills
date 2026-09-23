# Agent Architecture & Skill Lifecycle Guide

> **Role**: Unified reference for knowledge representation and the 4-step skill build contract.

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
