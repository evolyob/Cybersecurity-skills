---
name: env-audit
description: Audit OS binaries, CVEs, EOL risks, upstream versions, and generate upgrade commands.
dependencies: []
---

# Terminal Environment & Security Audit Skill (`env-audit`)

## Objective & Priority
Act as a Senior System Security Auditor to inspect host OS binaries, audit installed tool CVEs/EOL risks against endoflife.date lifecycle standards, compare versions against native package managers, and generate targeted upgrade commands.

Priority Rules: `Dynamic OS Routing > Package Manager Querying > Risk Filtering > Targeted Repair`

## Execution Workflow

### Step 1: Dynamic Environment Discovery & Target Inspection
- Action: Execute the OS-dispatching audit router script to extract host details, functional installed binaries, and package manager candidates in JSON format:
  ```bash
  python3 <skill_dir>/scripts/audit.py
  ```
- Completion Criterion: Exit code 0 with valid JSON containing host OS, functional binaries, and vulnerability status.

### Step 2: Real-Time Upstream & Vulnerability Assessment
- Action: Parse inspection JSON, query native package manager candidates (`apt policy`, `dnf info`, `brew info`), and evaluate security risk status against synchronized endoflife.date rules.
- Completion Criterion: Package manager versions and EOL statuses are fully evaluated.

### Step 3: Render Structured Audit Report
- Action: Synthesize inspection JSON into a 3-part structured audit report (render display labels in user's conversation language):
  1. **Host Header**: Render host metadata and evaluated OS defenses on a single line:
     - Format: `<Host Specs>: <os_name> (<arch>) | <Kernel>: <kernel> | Core Defense: <evaluated_guards_status>`.
     - Dynamic guard evaluation: display `SIP / Gatekeeper / ALF Enabled` if all pass; explicitly flag any disabled component (e.g., `⚠️ ALF Disabled`).
  2. **System & Binary Inventory**: Single consolidated markdown table (`Category`, `Component`, `Installed Version`, `Recommended LTS Version`, `Status`):
     - Enumerate all functional binaries. Set status to `PASS` or `FAIL` based on lifecycle standard.
     - Beneath `ssh`, insert sub-row `↳ SSH Cipher Suite`: display active symmetric ciphers in installed column (e.g., `AES-GCM / ChaCha20`), risk audit criteria in LTS column (e.g., `MAC 含 SHA-1 / CBC`), and status as `WARN` (if legacy MAC/cipher present) or `PASS`.
  3. **Risk Summary & Targeted Remediation**:
     - Detail ONLY components marked as `FAIL` or `WARN` with EOL thresholds and CVE/cryptographic risks.
     - Provide copy-paste remediation commands structured by: (1) repo index update, (2) package manager upgrade, (3) post-install verification.
- Completion Criterion: Structured report rendered cleanly without redundant clean-item noise.
