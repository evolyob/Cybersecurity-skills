# Visual Layout Decision Rules

> Extends AGENTS.md "Structural Grounding". Enforces structural decisions immediately after Line 1 verdicts.
> Emit rendered Markdown/Mermaid only; never expose internal pattern names.

---

## 1. 3-Step Decision Gate

Follow this sequence before emitting layout blocks:
1. **Identify Domain**: Classify the topic as Strategy, Operations, or Architecture.
2. **Select Pattern**: Match the domain to the mandatory visual layout pattern in Section 2.
3. **Dispatch to Output**: Render directly in Markdown/Mermaid or hand off to specialized skills.

---

## 2. Visual Layout Skeletons

### Strategy :
- **Metric Cards**: 3 to 4 metric badges with delta `▲/▼`. (Requires: metric label, numerical value, delta `▲/▼`, optional baseline note).
- **Strategic Matrix**: 2x2 quadrant grid. (Requires: 2 evaluation axes, 4 quadrants with 2 bullet items each).
- **Executive Bento**: Top-level overview layout. (Requires: 3 strategic pillar cards + 2 quantified big-number metrics).
- **Progress Gauges**: 2 to 3 comparative horizontal bars or donut rings. (Requires: category labels, numeric percentages, target benchmark).

### Operations :
- **Comparison Split**: 50/50 balanced dual columns. (Requires: left vs right symmetric entities, paired points).
- **Checklist Grid**: Dual-column verification readiness gates. (Requires: gate categories, check items with `✓` / `✖` status).
- **Pipeline Flow**: 4 horizontal sequential phases. (Requires: 4 sequential phase names, action verbs, transition flow).
- **Data Table**: 3 to 4 structured columns. (Requires: clear column headers, homogeneous structured row records).
- **Timeline**: Chronological horizontal baseline with milestones. (Requires: date/phase sequence, milestone deliverables).

### Architecture :
- **Pillar Grid**: 3 to 4 vertical capability or structural pillar cards. (Requires: 3 to 4 pillar titles, category tags, bulleted core tenets).
- **Anchor Card**: Upper central anchor + 2 to 3 lower sub-cards. (Requires: 1 foundational core mandate + 2 to 3 modular sub-domains).
- **Editorial Tree**: Hierarchical root + 90° T-split branches. (Requires: 1 root node + 2-tier parent-child structural nodes).
- **Topology Flow**: Full-width container with 5 to 8 nodes. (Requires: 5 to 8 entity nodes, directional source-to-target flows).
