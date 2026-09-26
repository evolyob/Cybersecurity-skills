# Security & Safety Guardrails (`security_guardrails.md`)

> Scope: Mandatory security boundaries applied globally across all workflows and code generations.

---

## 1. Credentials & Secrets Isolation

- **File Prohibitions**: PROHIBITED from reading, inspecting, modifying, or outputting credential files (`.ssh`, `.aws`, `.env`, `.kube`, `id_rsa`, `*.pem`).
- **Environment Injection**: Inject credentials, API tokens, and private keys strictly via environment variables—never hardcode into source code, config files, or test fixtures.
- **Path Hygiene**: PROHIBITED from hardcoding host absolute paths (`/home/`, `/Users/`, `/root/`, drive letters `C:\`, `D:/`, UNC `\\`) in deliverables. When outputting deliverables (.md, .txt, .html), normalize all host paths to `~` or use relative paths.

---

## 2. High-Risk Operational Guardrails

- **Destructive Operations**: Require explicit user confirmation before executing destructive commands (`rm -rf`, `mkfs`), mass deletions, partition formatting, or `git push`.
- **0-Retry Auth Protocol**: Abort immediately on `Permission Denied` / `Auth Error`; cap operational retries at 3 before pausing for clarification.
