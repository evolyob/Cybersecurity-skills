# Visual Layout Decision Rules

> Extends AGENTS.md "Structural Grounding". Enforces structural decisions immediately after Line 1 verdicts.
> Emit rendered Markdown/Mermaid only; never expose internal pattern names.

---

## 1. 3-Step Decision Gate

Follow this sequence before emitting layout blocks:
1. **Identify Domain**: Classify the topic as Strategy, Operations, or Architecture.
2. **Select Component**: Match the domain to the mandatory anchor primitive in Section 2.
3. **Apply Proportions**: Enforce width limits, symmetry rules, and item caps.

---

## 2. Decision Matrix

| Domain | Anchor Type | Universal Component | Balance Guardrails | When to Use (Use Case) |
| :--- | :--- | :--- | :--- | :--- |
| **Strategy** | Quantitative deltas | **Metric Cards (Row)**<br>(100% full width) | 3 to 4 cards max. Center numbers with delta `▲/▼`. Subtitle <= 8 words. | Standalone metrics, SLA %, latency drop, cost savings. |
| **Strategy** | Quantitative deltas | **2x2 Quadrant Grid**<br>(100% full width) | 2x2 grid. Equal text density. Exactly 2 bullet points per quadrant. | P0 to P3 priorities, Quick Wins (High Impact / Low Effort). |
| **Ops** | Structured tables | **Comparison Split**<br>(50/50 split) | 2 equal columns. Left-to-right character length ratio <= 1.5x. | As-Is vs To-Be comparisons, Pain Points vs Solutions. |
| **Ops** | Structured tables | **Structured Data Table**<br>(100% full width) | 3 to 4 columns. Uniform column widths. Concise table headers. | Compliance audits, security control lists, asset inventory. |
| **Ops** | Structured tables | **Linear Progression**<br>(100% full width) | 4 horizontal phases. Equal text length per step. Left-to-right flow. | SOP steps, 4-phase incident response (Triage -> Review). |
| **Architecture** | Topology / Sequence | **Topology Diagram**<br>(100% full width) | Full-width container. 5 to 8 nodes total. Single flow direction (LR/TD). | Service topology, API auth sequence (JWT), entity relations. |
