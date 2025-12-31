"""
How Vibecode Studio Integrates the Orchestrator
================================================

## Architecture Overview

Vibecode Studio uses a **hybrid approach**:
- Python handles state management, file operations, and workflow coordination
- GitHub Copilot acts as the "AI brain" that executes agent instructions
- Markdown files contain all the intelligence and rules

## Components

### 1. system_fast.md (The Orchestrator)
Location: `core/system_fast.md`

This is the **master orchestration specification** (3,200+ lines):
- Defines the Golden Pipeline (Phases A-E)
- Specifies when to activate each agent
- Contains quality gates, error recovery, and safety protocols
- Acts as instructions for GitHub Copilot to coordinate agents

### 2. Agent Specifications (00-09)
Location: `agents/*.md`

Each agent has a markdown file:
- `00_auditor.md` - Security & analysis
- `01_planner.md` - Architecture & planning
- `02_coder.md` - Code implementation
- `03_ui_premium.md` - UI/UX design
- `04_reviewer.md` - Code review
- `05_apply.md` - File operations
- `06_runtime.md` - Server management
- `07_autofix.md` - Bug fixing
- `08_export.md` - Release management
- `09_testing.md` - Test generation

### 3. Python Orchestrator (orchestrator.py)
Location: `core/orchestrator.py`

The Python code does NOT implement agents - it:
- **Loads** system_fast.md and agent .md files
- **Builds context** for GitHub Copilot
- **Manages state** (.vibecode/state.json)
- **Logs actions** (.vibecode/session_context.md)
- **Coordinates workflow** (which agent, when, handoffs)

## How It Works (Example: Build Feature)

### Step 1: User Request
```
User: "Build a user authentication feature"
```

### Step 2: Orchestrator Loads Context
```python
orchestrator = Orchestrator(workspace)
# Loads:
# - system_fast.md (orchestration rules)
# - All agent .md files (agent capabilities)
# - Current state (what's already done)
```

### Step 3: Orchestrator Determines Workflow
Based on system_fast.md, it determines:
- Phase A1: Run Agent 00 (Auditor) first
- Phase A2: Then Agent 01 (Planner)
- Phase B1: Then Agent 02 (Coder)
- etc.

### Step 4: Execute Agent 00
```python
# Orchestrator builds context:
context = {
    "orchestrator_instructions": system_fast.md content,
    "agent_instructions": agents['00'].instructions,  # 00_auditor.md
    "task": "Analyze codebase for authentication feature",
    "workspace": workspace_files
}

# GitHub Copilot receives this context and acts as Agent 00
# It analyzes the codebase following 00_auditor.md instructions
```

### Step 5: State Management
```python
orchestrator.state = {
    "current_phase": "DISCOVERY",
    "current_agent": "00",
    "task": "user authentication",
    "results": {
        "00": "audit_report.md generated"
    }
}
orchestrator.save_state()  # Persists to .vibecode/state.json
```

### Step 6: Handoff to Agent 01
```python
# Orchestrator loads next agent:
context = {
    "orchestrator_instructions": system_fast.md content,
    "agent_instructions": agents['01'].instructions,  # 01_planner.md
    "previous_results": audit_report from Agent 00,
    "task": "Design authentication architecture"
}

# GitHub Copilot now acts as Agent 01 (Planner)
```

### Step 7: Continue Through Pipeline
Orchestrator coordinates:
- Agent 01 → Creates plan (vibecode_plan.md)
- Agent 02 → Implements code
- Agent 03 → Designs UI
- Agent 04 → Reviews code
- Agent 05 → Writes files to disk
- Agent 09 → Runs tests
- Agent 08 → Prepares release

## Key Integration Points

### 1. Context Builder
```python
def build_agent_context(self, agent_id: str, task: Dict) -> str:
    """
    Builds the full context for GitHub Copilot
    """
    context = f"""
# ORCHESTRATOR INSTRUCTIONS
{self.orchestrator_instructions}

# CURRENT AGENT: {agent_id}
{self.agents[agent_id].instructions}

# TASK
{task['description']}

# PREVIOUS RESULTS
{self._get_previous_results()}

# CURRENT STATE
{json.dumps(self.state, indent=2)}
"""
    return context
```

### 2. State Tracker
```python
def track_agent_execution(self, agent_id: str, result: Any):
    """
    Updates state after agent execution
    """
    self.state["current_agent"] = agent_id
    self.state["results"][agent_id] = result
    self.state["history"].append({
        "agent": agent_id,
        "timestamp": datetime.now().isoformat(),
        "result": result
    })
    self.save_state()
    self.log_action(agent_id, "completed", result)
```

### 3. Pipeline Executor
```python
def execute_pipeline(self, task_type: str, task_desc: str):
    """
    Executes multi-agent pipeline
    """
    if task_type == "build_feature":
        # Golden Pipeline from system_fast.md
        agents_sequence = ["00", "01", "02", "03", "04", "05", "09"]
        
        for agent_id in agents_sequence:
            context = self.build_agent_context(agent_id, task_desc)
            # GitHub Copilot uses this context to act as the agent
            result = self.execute_agent(agent_id, context)
            self.track_agent_execution(agent_id, result)
            
            # Check quality gates (from system_fast.md)
            if not self.validate_quality_gate(agent_id, result):
                # Trigger error recovery
                self.handle_failure(agent_id, result)
                break
```

## Benefits of This Architecture

### ✅ Separation of Concerns
- **Markdown** = Intelligence & rules (easy to update)
- **Python** = State management & coordination (stable)
- **GitHub Copilot** = Execution engine (powerful AI)

### ✅ Easy to Maintain
- Update agent behavior? → Edit .md file
- Update orchestration? → Edit system_fast.md
- Update workflow logic? → Edit orchestrator.py

### ✅ Portable
- Markdown specs work with any AI (Copilot, Claude, GPT-4)
- Python orchestrator is lightweight
- No complex AI integration code

### ✅ Transparent
- All agent instructions visible in .md files
- State tracked in JSON
- Session log shows exactly what happened

## User Perspective

User doesn't see the complexity:

```
1. User: "Build authentication feature"
   
2. System: [Scans codebase] → Agent 00
   
3. System: [Creates plan] → Agent 01
   "Here's the architecture plan. Approve? (y/n)"
   
4. User: "y"
   
5. System: [Writes code] → Agent 02
           [Designs UI] → Agent 03
           [Reviews] → Agent 04
           [Writes files] → Agent 05
           [Tests] → Agent 09
   
6. System: "✅ Feature complete! 
            - 8 files created
            - 23 tests passing
            - 94% coverage
            Ready to ship?"
```

Behind the scenes, orchestrator:
- Loaded system_fast.md (3,200 lines of coordination logic)
- Loaded 6 agent .md files (100,000+ chars of agent specs)
- Built context for each agent execution
- Managed state transitions
- Validated quality gates
- Logged all actions

## Summary

**The orchestrator integration is a "context engine":**
1. Loads all intelligence from .md files
2. Builds rich context for AI
3. Manages state and workflow
4. Lets GitHub Copilot be the "brain"
5. Tracks everything for safety and auditability

**It's like having a senior engineering manager** (orchestrator.py) **who:**
- Knows all the processes (system_fast.md)
- Knows each team member's skills (agent .md files)
- Assigns tasks to the right person
- Tracks progress
- Ensures quality

**And the team members** (GitHub Copilot) **who:**
- Receive clear instructions
- Execute tasks based on their role
- Deliver results back to the manager
