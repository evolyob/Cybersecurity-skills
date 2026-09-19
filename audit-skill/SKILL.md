---
name: audit-skill
description: Audits skills, Python code, and frontend web assets against quantitative context-efficiency, security boundaries, and Lazy Senior engineering standards.
dependencies: []
---

# Universal Skill & Code Auditor

## Objective
Provide automated quality, defensive bounds, and security guardrail auditing for skills, Markdown specifications, Python scripts, and frontend web assets.

---

## Routing & Architecture

| Component | Type | Responsibility |
|---|---|---|
| `scripts/audit.py` | Executable Engine | One-shot automated 12-Gate inspection (<20ms) for Skills, Markdown, Python, and Security |
| `scripts/audit_frontend.py` | Executable Engine | Specialized security, syntax, and dependency discovery auditor for JS/TS/Vue scripts |
| `references/remediation_guide.md` | Reference Guide | Standard refactoring templates and patterns for non-compliant skills |

---

## Execution Workflow

### Step 1: Execute Automated Auditor
- **Action**: Run the target engine based on file type in a single tool call:
  - **Skills, Python & Markdown**: `python3 <skill_dir>/scripts/audit.py <target_path>`
  - **Frontend Assets (JS/TS/Vue/HTML)**: `python3 <skill_dir>/scripts/audit_frontend.py <target_path>`
- **Core Automated Gates**:
  - **Quality & Bounds**: Zero-EOL (Python >= 3.13, Node >= 24 LTS), explicit dependency declarations, stdlib priority, clean imports, encoding safety, line budget.
  - **Markdown & Layout**: 4-backtick nesting, code fence balance, path purity, embedded snippet validation.
  - **Security Guardrails**: Zero plaintext secrets, zero privilege escalation, zero dynamic execution, zero prompt injections, DOMPurify XSS defenses.

### Step 2: Fact-Based Findings Report
- **Action**: Summarize audit output using the **1-2-3 Fact-Based format**:
  1. `Finding`: The factual condition observed (`PASS`, `WARN`, or `FAIL`).
  2. `Objective Evidence`: Exact line numbers, files, and metrics from the audit output.
  3. `Requirement`: The explicit rule or threshold.

### Step 3: User Gate & Remediation
- **Action**: If blockers or advisories exist and the user requests fixes, consult `references/remediation_guide.md` to propose concrete diffs.
- **Criteria**: Obtain explicit approval before modifying any files.
