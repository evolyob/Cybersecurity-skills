# Cyber Hardening Skills

A collection of production-ready cybersecurity, system hardening, threat intelligence, strategic governance, and lifecycle automation configurations for Google Antigravity (AGY).

---

## 1. Skills Catalog & Capabilities Matrix

| Skill | Category | Primary Mission & Scope | Core Tools & Technologies |
| :--- | :--- | :--- | :--- |
| **[`audit-skill`](audit-skill/)** | Governance & Quality | 12-Gate automated AST static code and skill auditor (<20ms). Enforces coding standards, dynamic line budgets, and security guardrails. | Python AST, Regex, Static Analysis |
| **[`env-audit`](env-audit/)** | Host Hardening & OS Audit | Multi-platform (Linux/macOS) binary, package EOL, and CVE audit engine with automated upstream target synchronization. | Python Stdlib, EndOfLife API, Regex |
| **[`sec-intel`](sec-intel/)** | Security & Threat Intel | Authoritative, evidence-based intelligence lookup for IPs, ASNs, Domains, and CVEs via ICANN RDAP, real DNS resolution, and dual-engine EUVD/OSV. | ICANN RDAP, `dnspython`, EUVD, OSV |
| **[`asset-risk`](asset-risk/)** | Security & Risk Assessment | Intelligently categorize information assets and select diverse, causally linked threats and vulnerabilities without repetitive monotony. | Python Stdlib, Anti-Monotony Round-Robin |
| **[`deep-grill`](deep-grill/)** | Strategic Decision-Making | Socratic interview protocol designed to challenge proposed plans, designs, and architectures to surface hidden risks and assumptions one question at a time. | Socratic Interview Heuristics |

---

## 2. Infrastructure Security & Reference Notes (`tooools/`)

| Directory | Scope & Description |
| :--- | :--- |
| **[`tooools/`](tooools/)** | Infra secure configuration benchmarks, security headers, SSL/TLS analyzers, and offensive/defensive cybersecurity reference notes. |

---

## 3. Reference Architectures & Examples (`examples/`)

The [`examples/`](examples/) directory provides reference implementations and foundational infrastructure templates:

| Component | Path | Description |
| :--- | :--- | :--- |
| **Prompt Template** | [`examples/gemini_template.md`](examples/gemini_template.md) | Standard system prompt template with structured workflow, writing style, persistent memory, and security guardrails. |
| **Automation & Quality Hooks** | [`examples/hooks/`](examples/hooks/) | Automated lifecycle event handlers and guardrails:<ul><li>`hooks.json`: Lifecycle hook configurations (`pre_tool_call`, `post_tool_call`, `on_user_message`).</li><li>`noai_gate.py` / `rules_gate.json`: Pre-tool Anti-AI cliché filter and mainland term detector.</li><li>`anti_blind_mutation.py`: Prevents destructive, unvalidated code edits.</li><li>`post_tool_quality_guard.py`: Post-tool execution verification and quality filter.</li><li>`secret_leak_guard.py`: Guardrail preventing accidental exposure of sensitive keys.</li></ul> |
| **Persistent Memory Framework** | [`examples/memory/`](examples/memory/) | Structured 3-tier long-term memory system (Load -> Save -> Recall):<ul><li>`core.md`: Master index and routing table for persistent memory (< 35 lines).</li><li>`topics/`: Governance rules and user preferences (`system_governance.md`, `user_preferences.md`).</li><li>`templates/`: Specification contracts, coding laws, and lifecycle guidelines.</li></ul> |
