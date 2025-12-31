# How Vibecode Routes User Requests to Agents

## The Flow (From User Input to Agent Execution)

```
┌─────────────────────────────────────────────────────┐
│ USER INPUT                                          │
│ "scan and learn this project"                       │
│ OR "/fix the null reference error"                  │
│ OR "build user authentication"                      │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ PHASE 0: INTAKE (orchestrator.py)                  │
│ • Receives user input                               │
│ • Calls intent_parser.parse()                       │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ INTENT PARSER (intent_parser.py)                   │
│                                                      │
│ Step 1: Detect command vs natural language          │
│   • "/scan" → Command (direct match)                │
│   • "scan and learn" → Natural language (keywords)  │
│                                                      │
│ Step 2: Map to TaskType                             │
│   • "scan" → SCAN_PROJECT                           │
│   • "fix" → FIX_BUG                                 │
│   • "build" → BUILD_FEATURE                         │
│                                                      │
│ Step 3: Determine agent pipeline                    │
│   • SCAN_PROJECT → [Agent 00]                       │
│   • FIX_BUG → [Agent 07, Agent 09]                  │
│   • BUILD_FEATURE → [00,01,02,03,04,05,09]          │
│                                                      │
│ Step 4: Check if existing project                   │
│   • If YES → Prepend Agent 00 (analyze first)       │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ ORCHESTRATOR RECEIVES                               │
│ • TaskType: SCAN_PROJECT                            │
│ • Pipeline: [Agent 00]                              │
│ • Params: {deep: true, description: "..."}          │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ ORCHESTRATOR BUILDS CONTEXT                         │
│                                                      │
│ context = {                                          │
│   orchestrator_instructions: system_fast.md,        │
│   agent_instructions: agents['00'].instructions,    │
│   task: {                                            │
│     type: "SCAN_PROJECT",                           │
│     description: "scan and learn this project",     │
│     params: {deep: true}                            │
│   },                                                 │
│   workspace: workspace_path,                        │
│   is_existing_project: true,                        │
│   state: current_state                              │
│ }                                                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ GITHUB COPILOT RECEIVES CONTEXT                     │
│                                                      │
│ Copilot now has:                                     │
│ 1. Full orchestrator rules (system_fast.md)         │
│ 2. Agent 00 specifications (00_auditor.md)          │
│ 3. The specific task to perform                     │
│ 4. Current project state                            │
│                                                      │
│ Copilot acts as Agent 00 and executes:              │
│ • Scans workspace files                             │
│ • Detects tech stack                                │
│ • Analyzes patterns                                 │
│ • Generates audit_report.md                         │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ ORCHESTRATOR TRACKS RESULT                          │
│                                                      │
│ state.json updated:                                  │
│ {                                                    │
│   current_phase: "DISCOVERY",                       │
│   current_agent: "00",                              │
│   results: {                                         │
│     "00": "audit_report.md generated"               │
│   }                                                  │
│ }                                                    │
│                                                      │
│ session_context.md logged:                          │
│ "Agent 00 completed scan - Tech stack: React..."    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ RESULT RETURNED TO USER                             │
│ "✅ Project scanned successfully"                    │
│ "Tech stack: React 18, TypeScript, Vite"            │
│ "See audit_report.md for details"                   │
└─────────────────────────────────────────────────────┘
```

## Example Scenarios

### Scenario 1: Existing Project - Scan & Learn
```
User: "scan and learn this project"

Intent Parser:
  ├─ Detects keywords: "scan", "learn"
  ├─ Maps to: SCAN_PROJECT
  ├─ Checks: is_existing_project = True
  └─ Pipeline: [Agent 00]

Orchestrator:
  ├─ Loads: system_fast.md + 00_auditor.md
  ├─ Builds context with workspace files
  └─ Executes: Agent 00

Agent 00 (via Copilot):
  ├─ Scans all files in workspace
  ├─ Detects: React, TypeScript, Tailwind CSS
  ├─ Analyzes patterns (component structure, state management)
  ├─ Generates: audit_report.md, project_context.md
  └─ Returns: Tech stack summary

Result: ✅ Project analyzed and documented
```

### Scenario 2: Existing Project - Fix Bug
```
User: "fix the null reference error in UserProfile"

Intent Parser:
  ├─ Detects keywords: "fix", "error"
  ├─ Maps to: FIX_BUG
  ├─ Checks: is_existing_project = True
  ├─ Prepends Agent 00 (analyze first)
  └─ Pipeline: [Agent 00, Agent 07, Agent 09]

Orchestrator:
  ├─ Step 1: Execute Agent 00
  │   └─ Analyzes UserProfile.tsx and related files
  │
  ├─ Step 2: Execute Agent 07 (Medic)
  │   ├─ Receives Agent 00's analysis
  │   ├─ Diagnoses null reference error
  │   ├─ Implements surgical fix (adds null check)
  │   └─ Returns: Fixed code
  │
  └─ Step 3: Execute Agent 09 (Tester)
      ├─ Verifies fix works
      ├─ Runs existing tests
      └─ Returns: All tests passing

Result: ✅ Bug fixed in 2-3 minutes
```

### Scenario 3: Existing Project - Build Feature
```
User: "build user authentication feature"

Intent Parser:
  ├─ Detects keywords: "build", "feature"
  ├─ Maps to: BUILD_FEATURE
  ├─ Checks: is_existing_project = True
  ├─ Pipeline: [00, 01, 02, 03, 04, 05, 09]
  └─ Approval required: YES

Orchestrator:
  ├─ Asks user for approval
  │   "This will create authentication. Proceed? (y/n)"
  │
  ├─ Step 1: Agent 00 (Forensic)
  │   └─ Analyzes existing auth patterns, security setup
  │
  ├─ Step 2: Agent 01 (Planner)
  │   ├─ Receives audit from Agent 00
  │   ├─ Designs authentication architecture
  │   ├─ Follows existing patterns (Redux, API client, etc.)
  │   └─ Creates: vibecode_plan.md
  │
  ├─ Step 3: Agent 02 (Builder)
  │   ├─ Implements according to plan
  │   ├─ Matches existing code style
  │   └─ Writes tests first (TDD)
  │
  ├─ Step 4: Agent 03 (Designer)
  │   ├─ Designs login/signup UI
  │   └─ Uses existing design system
  │
  ├─ Step 5: Agent 04 (Reviewer)
  │   ├─ Reviews code quality
  │   ├─ Checks security
  │   └─ Validates against plan
  │
  ├─ Step 6: Agent 05 (Integrator)
  │   └─ Writes files to disk
  │
  └─ Step 7: Agent 09 (Tester)
      ├─ Runs all tests
      └─ Verifies 80%+ coverage

Result: ✅ Authentication feature complete in 10-15 minutes
```

### Scenario 4: New Project - Build Feature
```
User: "build a todo app"

Intent Parser:
  ├─ Detects keywords: "build"
  ├─ Maps to: BUILD_FEATURE
  ├─ Checks: is_existing_project = False (no src/ folder)
  └─ Pipeline: [01, 02, 03, 04, 05, 09]
      (Note: No Agent 00 - nothing to analyze)

Orchestrator:
  ├─ Step 1: Agent 01 (Planner)
  │   ├─ Asks: "What tech stack? React? Vue? Next.js?"
  │   ├─ Designs architecture from scratch
  │   └─ Creates: vibecode_plan.md
  │
  ├─ Step 2: Agent 02 (Builder)
  │   └─ Implements fresh code (modern best practices)
  │
  ├─ Step 3: Agent 03 (Designer)
  │   └─ Designs UI (no existing patterns to follow)
  │
  ├─ ... (rest of pipeline)

Result: ✅ New todo app created
```

## Key Differences: Existing vs New Projects

| Aspect | Existing Project | New Project |
|:-------|:-----------------|:------------|
| **Agent 00** | Always runs first | Skipped (nothing to analyze) |
| **Patterns** | Must follow existing | Use modern best practices |
| **Style** | Match existing code | Fresh, consistent style |
| **Safety** | High (surgical changes) | Standard (full control) |
| **Context** | Load project_context.md | None available |
| **Speed** | Faster (patterns known) | Slower (more decisions) |

## How Orchestrator Knows What to Do

The orchestrator combines:
1. **Intent Parser** (intent_parser.py) - Maps user input to task type
2. **Pipeline Mapper** - Maps task type to agent sequence
3. **Context Builder** - Loads appropriate .md files for each agent
4. **State Tracker** - Remembers what's done, what's next
5. **Quality Gates** - Validates each step (from system_fast.md)

All the intelligence is in:
- **system_fast.md** (3,200 lines) - How to orchestrate
- **Agent .md files** (10 files) - What each agent does
- **intent_parser.py** - How to understand user requests

The Python code just **loads, routes, and tracks** - it doesn't contain the AI logic!

## Summary

**The orchestrator is a smart router:**
1. Understands hundreds of different user requests
2. Knows which agents to call for each scenario
3. Adapts behavior for existing vs new projects
4. Loads the right context for each agent
5. Tracks progress and manages state
6. Enforces quality gates and safety rules

**It's like a senior project manager who:**
- Understands what you want
- Knows who on the team can do it
- Assigns the right people in the right order
- Gives them all the information they need
- Tracks progress and ensures quality
