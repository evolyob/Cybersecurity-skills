# Visual Layout Decision Rules

> Extends AGENTS.md "Structural Grounding". Governs layout structure following Line 1 verdicts.
> CLI Chat: ONLY use numbered lists (1.), tables (|), Unicode trees (├─), or vertical rails (│); NEVER emit Mermaid.

---

## 1. Decision Flow

When structural grounding is required beyond Line 1:

1. **Match Domain Pattern**: Classify topic as Strategy, Operations, or Architecture, then select a skeleton from Section 2.
2. **Verify Data Slots**: Ensure all mandatory fields (Requires: ...) are present before rendering.

---

## 2. Visual Layout Skeletons

### Strategy
> Use when the output communicates direction, prioritization, or executive judgment.

- **KPI Cards**: 3–4 metric badges with delta `▲/▼`.
  _(Requires: metric label, numerical value, delta `▲/▼`, optional baseline note)_
- **Strategic Matrix**: 2×2 quadrant grid.
  _(Requires: 2 evaluation axes, 4 quadrants each with 2 bullet items)_
- **Executive Bento**: Top-level overview layout.
  _(Requires: 3 strategic pillar cards + 2 quantified big-number metrics)_
- **Progress Gauges**: 2–3 comparative horizontal bars or donut rings.
  _(Requires: category labels, numeric percentages, target benchmark)_

---

### Operations
> Use when the output tracks status, compares states, or maps a process.

- **Comparison Split**: Side-by-side dual panel (Before/After, Current/Target, Problem/Solution).
  _(Requires: 2 panel labels, 3–5 bullet points per panel)_
- **Process Pipeline**: Sequential step flow with status indicators.
  _(Requires: step labels ordered chronologically, status per step `✓/▶/○`, owner or date optional)_
- **Status Table**: RAG traffic-light summary per workstream.
  _(Requires: workstream names, status `●Red/●Amber/●Green`, one-line rationale per row)_
- **Action Checklist**: Dual-column auditable verification or milestone readiness checklist.
  _(Requires: verification items, binary status cues `✓/○` or `[x]/[ ]`, owner or gate note; 4–6 items)_

---

### Architecture
> Use when the output maps system components, data flows, or structural hierarchies.

- **Topology Diagram**: Service or component topology with directional connections.
  _(Requires: named components, labeled edges, max 2 focal accent nodes)_
- **Sequence Flow**: Time-ordered interactions between actors (Mermaid `sequenceDiagram`).
  _(Requires: actor names, ordered message labels, at least 3 exchanges)_
- **Layer Stack**: Tiered infrastructure or responsibility layers (top-to-bottom).
  _(Requires: layer names ordered top→bottom, 1–3 components per layer)_
- **Data Flow**: Source → Processing → Output pipeline.
  _(Requires: named source, ≥1 transformation step, named output/sink)_
