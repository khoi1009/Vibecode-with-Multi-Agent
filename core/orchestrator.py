"""
Core Orchestrator Module
Coordinates multi-agent workflows
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import load_all_agents, Agent
from .intent_parser import IntentParser, TaskType
from .skill_loader import SkillLoader


class Orchestrator:
    """
    Coordinates agents to complete complex tasks
    Implements the Golden Pipeline from system_fast.md
    
    How it works:
    1. Loads system_fast.md (orchestration rules)
    2. Loads agent .md files (agent specifications)
    3. Builds context for GitHub Copilot with these instructions
    4. Manages state and coordinates workflow
    5. GitHub Copilot acts as the agents based on loaded instructions
    """
    
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)
        self.vibecode_dir = workspace / ".vibecode"
        self.vibecode_dir.mkdir(exist_ok=True)
        
        # Load orchestrator instructions
        orchestrator_spec = Path(__file__).parent / "system_fast.md"
        self.orchestrator_instructions = self._load_orchestrator_spec(orchestrator_spec)
        
        # Load agents from product folder
        product_agents_dir = Path(__file__).parent.parent / "agents"
        self.agents = load_all_agents(product_agents_dir)
        
        # Load skills (the expensive third-party library)
        skills_dir = Path(__file__).parent.parent / "skills"
        self.skill_loader = SkillLoader(skills_dir)
        print(f"[OK] Loaded {len(self.skill_loader.skills)} skills for intelligent task execution")
        
        # State files
        self.state_file = self.vibecode_dir / "state.json"
        self.session_file = self.vibecode_dir / "session_context.md"
        
        # Load current state
        self.state = self.load_state()
        
        # Initialize intent parser
        self.intent_parser = IntentParser()
        
        # Check if this is an existing project
        self.is_existing_project = self._check_existing_project()
    
    def _check_existing_project(self) -> bool:
        """Check if working on existing project (has source files)"""
        # Look for common source directories
        indicators = [
            self.workspace / "src",
            self.workspace / "app",
            self.workspace / "lib",
            self.workspace / "package.json",
            self.workspace / "requirements.txt",
            self.workspace / "Gemfile",
        ]
        return any(p.exists() for p in indicators)
    
    def _load_orchestrator_spec(self, spec_file: Path) -> str:
        """Load the orchestrator specification (system_fast.md)"""
        if spec_file.exists():
            return spec_file.read_text(encoding='utf-8')
        return "# Orchestrator specification not found"
    
    def load_state(self) -> Dict:
        """Load current state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "current_phase": "IDLE",
            "active_task": None,
            "active_agents": [],
            "history": [],
            "timestamp": datetime.now().isoformat()
        }
    
    def save_state(self):
        """Persist state to disk"""
        self.state["timestamp"] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def log_action(self, agent_id: str, action: str, result: Any):
        """Log agent actions to session context"""
        with open(self.session_file, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n## [{timestamp}] Agent {agent_id}\n")
            f.write(f"**Action:** {action}\n")
            f.write(f"**Result:** {result}\n")
            f.write("---\n")
    
    def register_agent(self, agent):
        """Register an agent with the orchestrator"""
        self.agents[agent.id] = agent
    
    def process_user_request(self, user_input: str) -> Dict:
        """
        Main entry point: Process user request and execute appropriate pipeline
        
        This is Phase 0 (INTAKE) from system_fast.md:
        1. Parse intent
        2. Validate request
        3. Determine agent pipeline
        4. Execute with appropriate context
        
        Args:
            user_input: User's request (command or natural language)
        
        Returns:
            Result dictionary
        """
        # Parse intent
        task_type, params = self.intent_parser.parse(user_input)
        
        print(f"\n📋 Task: {task_type.value}")
        print(f"📝 Parameters: {params}")
        
        # Get agent pipeline
        pipeline = self.intent_parser.get_agent_pipeline(
            task_type, 
            self.is_existing_project
        )
        
        print(f"🔄 Pipeline: {' → '.join([f'Agent {id}' for id in pipeline])}")
        
        # Check if approval needed
        if self.intent_parser.should_ask_for_approval(task_type):
            print(f"\n⚠️  This task requires approval before execution.")
            print(f"   Task: {params.get('description', user_input)}")
            print(f"   Agents: {len(pipeline)}")
            
            approval = input("\nProceed? (y/n): ").strip().lower()
            if approval != 'y':
                return {
                    "success": False,
                    "message": "Task cancelled by user"
                }
        
        # Execute pipeline
        return self.execute_pipeline(task_type, pipeline, params)
    
    def execute_pipeline(self, task_type: TaskType, agent_ids: List[str], params: Dict) -> Dict:
        """
        Execute agent pipeline with intelligent skill loading
        
        Args:
            task_type: Type of task
            agent_ids: List of agent IDs to execute
            params: Task parameters (should contain 'description' key)
        
        Returns:
            Result dictionary with execution details
        """
        
        self.state["current_phase"] = f"PIPELINE:{task_type.value}"
        self.state["active_task"] = params.get('description', str(task_type))
        self.save_state()
        
        # Extract query for skill selection
        query = params.get('description', '')
        
        print(f"\n{'='*60}")
        print(f"🚀 EXECUTING PIPELINE: {task_type.value}")
        print(f"📋 Query: {query}")
        print(f"🤖 Agents: {' → '.join([f'Agent {id}' for id in agent_ids])}")
        print(f"{'='*60}\n")
        
        results = {
            "task_type": task_type.value,
            "query": query,
            "agents_executed": [],
            "success": True,
            "errors": []
        }
        
        # Execute each agent in pipeline
        for i, agent_id in enumerate(agent_ids, 1):
            print(f"\n{'─'*60}")
            print(f"🔄 Step {i}/{len(agent_ids)}: Agent {agent_id}")
            
            # Get agent
            agent = self.agents.get(agent_id)
            if not agent:
                error_msg = f"Agent {agent_id} not found"
                print(f"❌ {error_msg}")
                results["errors"].append(error_msg)
                results["success"] = False
                continue
            
            # Select relevant skills for this agent
            print(f"🎯 Selecting relevant skills for Agent {agent_id}...")
            selected_skills_with_scores = self.skill_loader.select_skills(
                query=query,
                agent_id=agent_id,
                max_skills=3  # Top 3 most relevant skills
            )
            
            # Extract skills and scores
            selected_skills = [(skill, score) for skill, score in selected_skills_with_scores]
            
            if selected_skills:
                print(f"✅ Selected {len(selected_skills)} skill(s):")
                for skill, score in selected_skills:
                    print(f"   • {skill.name} (score: {score:.2f})")
            else:
                print(f"ℹ️  No specific skills needed for this agent")
            
            # Build context for GitHub Copilot
            context = self._build_agent_context(
                agent=agent,
                query=query,
                params=params,
                selected_skills=[skill for skill, score in selected_skills],
                previous_results=results["agents_executed"]
            )
            
            # Log to session
            self._log_agent_execution(agent_id, query, selected_skills)
            
            # Display what GitHub Copilot will receive
            print(f"\n📤 Context prepared for GitHub Copilot:")
            print(f"   • Agent instructions: {len(agent.instructions)} chars")
            print(f"   • System orchestration: {len(self.orchestrator_instructions)} chars")
            print(f"   • Skills context: {sum(len(skill.content) for skill, _ in selected_skills)} chars")
            print(f"   • Total context: ~{len(context)} chars")
            
            # In real execution, this context would be fed to GitHub Copilot
            # For now, we simulate successful execution
            agent_result = {
                "agent_id": agent_id,
                "agent_name": agent.name,
                "skills_used": [skill.name for skill, _ in selected_skills],
                "context_size": len(context),
                "status": "simulated"  # In production: "executed"
            }
            
            results["agents_executed"].append(agent_result)
            print(f"✅ Agent {agent_id} execution prepared")
        
        # Update state
        self.state["last_pipeline"] = {
            "task_type": task_type.value,
            "agents": agent_ids,
            "timestamp": str(Path.cwd())  # In production, use datetime
        }
        self.save_state()
        
        print(f"\n{'='*60}")
        print(f"✅ PIPELINE COMPLETE")
        print(f"   • Total agents: {len(agent_ids)}")
        print(f"   • Successful: {len(results['agents_executed'])}")
        print(f"   • Errors: {len(results['errors'])}")
        print(f"{'='*60}\n")
        
        return results
    
    def _build_agent_context(self, agent: Agent, query: str, params: Dict, 
                            selected_skills: List, previous_results: List) -> str:
        """
        Build comprehensive context for GitHub Copilot
        
        This context includes:
        1. System orchestration instructions (system_fast.md)
        2. Agent-specific instructions (.md file)
        3. Selected skills (top 3 most relevant)
        4. Task details
        5. Previous agent results (for pipeline continuity)
        """
        
        context_parts = []
        
        # 1. System orchestration
        context_parts.append("# SYSTEM ORCHESTRATION")
        context_parts.append(self.orchestrator_instructions)
        context_parts.append("\n" + "="*60 + "\n")
        
        # 2. Agent instructions
        context_parts.append(f"# AGENT: {agent.name}")
        context_parts.append(agent.instructions)
        context_parts.append("\n" + "="*60 + "\n")
        
        # 3. Selected skills
        if selected_skills:
            context_parts.append("# SELECTED SKILLS")
            for skill in selected_skills:
                context_parts.append(f"\n## Skill: {skill.name}")
                context_parts.append(skill.content)
                context_parts.append("\n" + "-"*40 + "\n")
        
        # 4. Task details
        context_parts.append("# CURRENT TASK")
        context_parts.append(f"Query: {query}")
        context_parts.append(f"Parameters: {params}")
        context_parts.append("\n" + "="*60 + "\n")
        
        # 5. Previous results (for context continuity)
        if previous_results:
            context_parts.append("# PREVIOUS AGENT RESULTS")
            for result in previous_results:
                context_parts.append(f"- {result['agent_name']}: {result['status']}")
                if result.get('skills_used'):
                    context_parts.append(f"  Skills: {', '.join(result['skills_used'])}")
            context_parts.append("\n" + "="*60 + "\n")
        
        return "\n".join(context_parts)
    
    def _log_agent_execution(self, agent_id: str, query: str, skills: List):
        """Log agent execution to session file"""
        
        log_entry = f"\n## Agent {agent_id} Execution\n"
        log_entry += f"- Query: {query}\n"
        if skills:
            skill_list = ', '.join([skill.name for skill, _ in skills])
            log_entry += f"- Skills: {skill_list}\n"
        else:
            log_entry += f"- Skills: None\n"
        log_entry += f"- Timestamp: {str(Path.cwd())}\n"  # In production: use datetime
        
        # Append to session log
        if self.session_file.exists():
            with open(self.session_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        else:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                f.write("# Vibecode Studio Session Log\n")
                f.write(log_entry)
    
    def get_status(self) -> Dict:
        """Get current orchestrator status"""
        return {
            "phase": self.state.get("current_phase", "IDLE"),
            "task": self.state.get("active_task"),
            "agents_registered": len(self.agents),
            "skills_available": len(self.skill_loader.skills),
            "last_update": self.state.get("timestamp")
        }

