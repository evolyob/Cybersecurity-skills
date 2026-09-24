# Visual Layout Decision Rules

> Extends AGENTS.md "Structural Grounding". Governs layout structure following Line 1 verdicts.
> Bypass for short Q&A (< 3 lines). Emit rendered Markdown/Mermaid directly; never expose internal pattern names.

---

## 1. Decision & Dispatch Flow

When structural grounding is required beyond Line 1:
1. **Route Destination**: If delegating output to a dedicated Skill, defer to that Skill's specification. Otherwise, proceed below.
2. **Match Domain Pattern**: Classify topic as Strategy, Operations, or Architecture, then select a skeleton from Section 2.
3. **Verify Data Slots**: Ensure all mandatory fields (Requires: ...) are present before rendering.

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
