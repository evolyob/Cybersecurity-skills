# Engineering Verification Protocol (`system_governance.md`)

> **Role**: Authoritative execution SOP for pre-delivery machine verification and zero self-assertion.

---

## Pre-Delivery Machine Verification (Zero Self-Assertion)

Never claim task completion without active terminal tool execution output:
1. **Compilation & Linting**: Run native compiler/linter (`python3 -m py_compile`, `tsc`, `go vet`).
2. **Zero-Leakage Scan**: Static regex scan for local paths and plaintext secrets; match count MUST be 0.
3. **Automated Test Run**: Unit test suite must pass with 100% OK.
