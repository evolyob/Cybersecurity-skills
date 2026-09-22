# Antigravity Production Templates & Memory Architecture

This directory provides production-grade templates, governance scaffolds, and architectural memory models for building deterministic, context-efficient agentic workflows in Google Antigravity.

---

## 1. 3-Tier Memory Hierarchy & Execution Flow

The memory system decouples lean index routing from deep governance and concrete execution contracts:

```text
┌────────────────────────────────────────────────────────┐
│  Tier 0: Rule & Constitution (Highest Authority)       │
│  • System Prompt (GEMINI.md) / Plugin AGENTS.md        │
└──────────────────────────┬─────────────────────────────┘
                           │ Constrains
                           ▼
┌────────────────────────────────────────────────────────┐
│  Tier 1: Global Master Index (Lean & Resident)         │
│  • ~/.gemini/memory/core.md (< 35 lines routing index) │
└──────────────┬──────────────────────────┬──────────────┘
               │ On-demand loading        │ Task-specific contracts
               ▼                          ▼
┌──────────────────────────────┐ ┌───────────────────────────────┐
│ Tier 2: Governance & Topics  │ │ Tier 3: Templates & Workspace │
│ • topics/                    │ │ • templates/spec_template.md  │
│   ├── system_governance.md   │ │ • templates/senior_coding_laws│
│   └── agent_skill_archi...md │ │ • templates/SKILL_DATA_SPEC.md│
│                              │ │ • <workspace>/.memory/        │
│                              │ │   └── project.md              │
└──────────────────────────────┘ └───────────────────────────────┘
```

---

## 2. Component Directory & Responsibilities

### Governance & Architecture Topics (`topics/`)

| Topic | File | Core Responsibility & Boundary |
|---|---|---|
| **System Governance** | [`topics/system_governance.md`](topics/system_governance.md) | **Execution Verification SOP**: Pre-delivery machine verification (automated compiler/linting checks, Zero-Leakage regex scans, and 100% test pass enforcement). |
| **Agent Architecture** | [`topics/agent_skill_architecture.md`](topics/agent_skill_architecture.md) | **Task Architecture & Division of Labor**: Python deterministic computation vs LLM cognitive orchestration, 4-step skill build flow, 5 evolution traps rejection, and delivery cheatsheet. |

### Reference Templates (`templates/`)

| Template / Contract | File | Core Responsibility & Boundary |
|---|---|---|
| **Specification Contract** | [`spec_template.md`](templates/spec_template.md) | **No-Spec-No-Code Gate**: Freezes Goal, Non-Goals (what MUST NOT be done), Allowed Paths whitelist, dependencies, and deterministic verification command. |
| **Clean Code Radar** | [`senior_coding_laws.md`](templates/senior_coding_laws.md) | **5-Step Implementation Hygiene**: Boundary isolation, pure functional core, flattened flow (max `if` depth $\le 2$), useful error context, and subtractive delivery. |
| **Skill Data Standards** | [`SKILL_DATA_SPEC.md`](templates/SKILL_DATA_SPEC.md) | **Data & Indexing Rules**: Pattern A (flat list) universal default, thresholded in-memory inverted index ($N > 20$, $O(1)$ lookup), zero envelope tax. |

---

## 3. Directory Layout

```text
examples/memory/
├── README.md                    # Architecture overview and hierarchy guide
├── core.md                      # Lean index & routing table (< 35 lines)
├── topics/                      # Authoritative execution SOPs & task architecture
│   ├── system_governance.md     # Pre-delivery machine verification SOP
│   └── agent_skill_architecture.md # Python/LLM division of labor & skill build guide
└── templates/                   # Concrete implementation scaffolds & contracts
    ├── spec_template.md         # 4+1 item specification contract boilerplate
    ├── senior_coding_laws.md    # Clean code 5-step engineering radar
    └── SKILL_DATA_SPEC.md       # Pattern A flat list vs Pattern B grouped taxonomy
```

---

## 4. Deployment to Local Environment

### Step 1: Create Memory Directories
```bash
mkdir -p ~/.gemini/memory/topics ~/.gemini/memory/templates
```

### Step 2: Deploy Scaffolds
```bash
# Copy core index sample
cp examples/memory/core.md ~/.gemini/memory/core.md

# Copy topics
cp examples/memory/topics/*.md ~/.gemini/memory/topics/

# Copy production templates
cp examples/memory/templates/*.md ~/.gemini/memory/templates/
```
