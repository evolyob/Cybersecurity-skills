# Security & Safety Guardrails (`security_guardrails.md`)

> Scope: Mandatory security boundaries applied globally across all workflows and code generations.

---

## 1. Security & Cryptography Primitives

- **Approved Primitives**: Use ONLY proven cryptographic primitives: `AES-GCM`, `Ed25519`, `TLS 1.3`, `SHA-256+` via platform KMS/libraries. NEVER roll custom crypto.
- **Compliance Baselines**: Mandatory compliance with CIS Benchmarks, OWASP (Web 2025, API 2023, LLM 2025+), and ASVS v5.0.0. Never bypass input validation or security controls.
- **Zero-EOL & Dead Batteries**: Enforce runtimes (Python >= 3.13, Node.js >= 24, Go >= 1.26). Prohibit PEP 594 removed modules (`cgi`, `pipes`, `crypt`, `distutils`). Declare dependencies via PEP 723 or PEP 621.

---

## 2. Credentials & Secrets Isolation

- **File Prohibitions**: PROHIBITED from reading, inspecting, modifying, or outputting credential files (`.ssh`, `.aws`, `.env`, `.kube`, `id_rsa`, `*.pem`).
- **Environment Injection**: Inject credentials, API tokens, and private keys strictly via environment variables—never hardcode into source code, config files, or test fixtures.
- **Path Hygiene**: PROHIBITED from hardcoding host absolute paths (`/home/`, `/Users/`, drive letters) in deliverables. Use `pathlib` with relative paths.

---

## 3. High-Risk Operational Guardrails

- **Destructive Operations**: Require explicit user confirmation before executing destructive commands (`rm -rf`, `mkfs`), mass deletions, partition formatting, or `git push`.
- **0-Retry Auth Protocol**: Abort immediately on `Permission Denied` / `Auth Error`; cap operational retries at 3 before pausing for clarification.
