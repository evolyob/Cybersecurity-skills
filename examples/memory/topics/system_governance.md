# Engineering & System Governance Protocol (`system_governance.md`)

> **Role**: Authoritative execution SOP for pre-delivery machine verification, anti-whack-a-mole structural gates, deterministic large-input probing, and data quarantine.

---

## 1. Pre-Delivery Machine Verification (Zero Self-Assertion)

Never claim task completion without active terminal tool execution output:
1. **Compilation & Linting**: Run native compiler/linter (`python3 -m py_compile`, `tsc`, `go vet`).
2. **Empirical Delta Verification**: Any claimed token savings, latency reduction, or routing improvement MUST provide reproducible before/after benchmark data (`Measure-Not-Assert`).
3. **Automated Test Run**: Unit test suite must pass with 100% OK.
4. **Zero-Leakage Scan**: Static scan for hardcoded credentials, local paths, and plaintext API keys.

---

## 2. Anti-Whack-a-Mole Structural Governance

Eliminate fragmented keyword blacklists and iterative patch-work by enforcing structural constraints at the perimeter:
1. **Single Canonical Ingestion**: All inputs pass a single-pass normalization (`unicodedata.normalize("NFKC")` + single consolidated regex) to eliminate invisible chars, CIDs, and formatting artifacts.
2. **Density Budgets over Word Banning**: Enforce quantitative structural limits (e.g. nominalization rate, punctuation caps) rather than endless single-word blacklists.
3. **Full-Block Rejection**: When an anti-pattern or AI tell is flagged, reject and rewrite the entire surrounding paragraph in active standup voice; never patch individual words.

---

## 3. Deterministic REPL Probing Protocol (Large-Input Handling)

For documents exceeding 50k tokens, full-context reading via `view_file` is strictly prohibited:
1. **TOC & Heading Discovery**: Run `grep -n` or `ripgrep` to locate heading line numbers with minimal token expenditure (< 200 tokens).
2. **Windowed Sampling**: Use `sed -n 'X,Yp'` or sliced tool ranges to inspect specific section content.
3. **Chunked Pipeline Output**: Slice and output directly to disk (`chapters/ch*.md`) without ever buffering the entire document in model reasoning context.

---

## 4. Data Quarantine & Supply Chain Safety Boundaries

1. **Copyright Quarantine**: Evaluation and test fixtures must use 100% synthetic or public-domain corpora; never commit raw copyrighted text.
2. **Local-First Boundary**: Enforce 100% offline execution; zero telemetry, zero analytics, and interactive opt-in for package installations.
