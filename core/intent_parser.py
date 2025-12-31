"""
Intent Parser & Command Router
Maps user requests to appropriate agent pipelines
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class TaskType(Enum):
    """Types of tasks the system can handle"""
    SCAN_PROJECT = "scan_project"
    LEARN_PATTERNS = "learn_patterns"
    BUILD_FEATURE = "build_feature"
    FIX_BUG = "fix_bug"
    DESIGN_UI = "design_ui"
    RUN_TESTS = "run_tests"
    SHIP_RELEASE = "ship_release"
    REFACTOR_CODE = "refactor_code"
    OPTIMIZE_PERFORMANCE = "optimize_performance"
    ADD_TESTS = "add_tests"
    SECURITY_AUDIT = "security_audit"
    UPDATE_DEPENDENCIES = "update_dependencies"
    QUESTION = "question"
    CONFIG = "config"
    STATUS = "status"


class IntentParser:
    """
    Parses user input and determines which agents to activate
    This is Phase 0 (INTAKE) from system_fast.md
    """
    
    def __init__(self):
        # Command patterns for explicit commands
        self.command_patterns = {
            # Discovery commands
            r'^/scan': TaskType.SCAN_PROJECT,
            r'^/learn': TaskType.LEARN_PATTERNS,
            r'^/audit': TaskType.SECURITY_AUDIT,
            
            # Development commands
            r'^/build': TaskType.BUILD_FEATURE,
            r'^/feature': TaskType.BUILD_FEATURE,
            r'^/fix': TaskType.FIX_BUG,
            r'^/bug': TaskType.FIX_BUG,
            r'^/refactor': TaskType.REFACTOR_CODE,
            r'^/optimize': TaskType.OPTIMIZE_PERFORMANCE,
            
            # Design commands
            r'^/design': TaskType.DESIGN_UI,
            r'^/vibe': TaskType.DESIGN_UI,
            r'^/ui': TaskType.DESIGN_UI,
            
            # Testing commands
            r'^/test': TaskType.RUN_TESTS,
            r'^/test-legacy': TaskType.ADD_TESTS,
            r'^/coverage': TaskType.RUN_TESTS,
            
            # Release commands
            r'^/ship': TaskType.SHIP_RELEASE,
            r'^/release': TaskType.SHIP_RELEASE,
            
            # System commands
            r'^/status': TaskType.STATUS,
            r'^/config': TaskType.CONFIG,
        }
        
        # Natural language keywords
        self.keyword_patterns = {
            # Scanning/analysis keywords
            ('scan', 'analyze', 'examine', 'inspect'): TaskType.SCAN_PROJECT,
            ('learn', 'understand', 'document patterns'): TaskType.LEARN_PATTERNS,
            
            # Building keywords
            ('build', 'create', 'add', 'implement', 'develop'): TaskType.BUILD_FEATURE,
            
            # Bug fixing keywords
            ('fix', 'bug', 'error', 'broken', 'issue', 'problem'): TaskType.FIX_BUG,
            
            # Design keywords
            ('design', 'style', 'ui', 'ux', 'layout', 'look'): TaskType.DESIGN_UI,
            
            # Testing keywords
            ('test', 'coverage', 'unit test', 'integration test'): TaskType.RUN_TESTS,
            
            # Refactoring keywords
            ('refactor', 'clean up', 'improve', 'restructure'): TaskType.REFACTOR_CODE,
            
            # Performance keywords
            ('optimize', 'performance', 'slow', 'speed up', 'faster'): TaskType.OPTIMIZE_PERFORMANCE,
            
            # Security keywords
            ('security', 'vulnerability', 'secure', 'audit'): TaskType.SECURITY_AUDIT,
            
            # Questions
            ('what', 'how', 'why', 'explain', 'show me', '?'): TaskType.QUESTION,
        }
    
    def parse(self, user_input: str) -> Tuple[TaskType, Dict]:
        """
        Parse user input and return task type + parameters
        
        Args:
            user_input: User's request (command or natural language)
        
        Returns:
            (TaskType, parameters dict)
        """
        user_input = user_input.strip()
        
        # Check for explicit commands first
        task_type, params = self._parse_command(user_input)
        if task_type:
            return task_type, params
        
        # Fall back to natural language parsing
        return self._parse_natural_language(user_input)
    
    def _parse_command(self, text: str) -> Tuple[Optional[TaskType], Dict]:
        """Parse explicit commands like /scan, /build, etc."""
        import re
        
        for pattern, task_type in self.command_patterns.items():
            if re.match(pattern, text, re.IGNORECASE):
                # Extract parameters
                params = self._extract_params(text, task_type)
                return task_type, params
        
        return None, {}
    
    def _parse_natural_language(self, text: str) -> Tuple[TaskType, Dict]:
        """Parse natural language requests"""
        text_lower = text.lower()
        
        # Score each task type
        scores = {}
        for keywords, task_type in self.keyword_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[task_type] = score
        
        # Return highest scoring task type
        if scores:
            best_task = max(scores, key=scores.get)
            params = {
                'description': text,
                'confidence': scores[best_task] / len(text_lower.split())
            }
            return best_task, params
        
        # Default to question if unsure
        return TaskType.QUESTION, {'description': text}
    
    def _extract_params(self, text: str, task_type: TaskType) -> Dict:
        """Extract parameters from command"""
        params = {'raw_input': text}
        
        # Extract flags
        if '--deep' in text:
            params['deep'] = True
        if '--fast' in text:
            params['fast'] = True
        if '--security' in text:
            params['security_focus'] = True
        
        # Extract arguments (everything after the command)
        parts = text.split(maxsplit=1)
        if len(parts) > 1:
            params['description'] = parts[1]
        
        return params
    
    def get_agent_pipeline(self, task_type: TaskType, is_existing_project: bool = False) -> List[str]:
        """
        Determine which agents to activate for a task
        
        Args:
            task_type: Type of task
            is_existing_project: Whether working on existing codebase
        
        Returns:
            List of agent IDs to execute in order
        """
        
        # Task-to-agent mapping
        pipelines = {
            TaskType.SCAN_PROJECT: ["00"],  # Agent 00 only
            TaskType.LEARN_PATTERNS: ["00"],  # Agent 00 only
            TaskType.SECURITY_AUDIT: ["00"],  # Agent 00 only
            
            TaskType.BUILD_FEATURE: [
                "00",  # Forensic - analyze existing code
                "01",  # Architect - design feature
                "02",  # Builder - implement
                "03",  # Designer - UI/UX
                "04",  # Reviewer - code review
                "05",  # Integrator - write files
                "09"   # Tester - run tests
            ],
            
            TaskType.FIX_BUG: [
                "07",  # Medic - diagnose & fix
                "09"   # Tester - verify fix
            ],
            
            TaskType.DESIGN_UI: [
                "03",  # Designer - create UI
                "04",  # Reviewer - review
                "05"   # Integrator - write files
            ],
            
            TaskType.RUN_TESTS: [
                "09"   # Tester only
            ],
            
            TaskType.ADD_TESTS: [
                "09"   # Tester - generate tests for existing code
            ],
            
            TaskType.SHIP_RELEASE: [
                "08",  # Shipper - prepare release
                "09"   # Tester - final validation
            ],
            
            TaskType.REFACTOR_CODE: [
                "00",  # Forensic - analyze current code
                "02",  # Builder - refactor
                "04",  # Reviewer - ensure behavior preserved
                "09",  # Tester - verify tests still pass
                "05"   # Integrator - write changes
            ],
            
            TaskType.OPTIMIZE_PERFORMANCE: [
                "00",  # Forensic - profile & analyze
                "01",  # Architect - optimization strategy
                "02",  # Builder - implement optimizations
                "09"   # Tester - performance tests
            ],
            
            TaskType.UPDATE_DEPENDENCIES: [
                "00",  # Forensic - impact analysis
                "01",  # Architect - migration plan
                "09"   # Tester - verify compatibility
            ],
        }
        
        pipeline = pipelines.get(task_type, [])
        
        # For existing projects, ALWAYS start with Agent 00 (unless it's a simple command)
        if is_existing_project and task_type not in [
            TaskType.SCAN_PROJECT, 
            TaskType.LEARN_PATTERNS,
            TaskType.RUN_TESTS,
            TaskType.STATUS,
            TaskType.CONFIG
        ]:
            if "00" not in pipeline:
                pipeline.insert(0, "00")
        
        return pipeline
    
    def should_ask_for_approval(self, task_type: TaskType) -> bool:
        """Determine if user approval required before execution"""
        requires_approval = [
            TaskType.BUILD_FEATURE,
            TaskType.REFACTOR_CODE,
            TaskType.UPDATE_DEPENDENCIES,
            TaskType.SHIP_RELEASE
        ]
        return task_type in requires_approval


# Example usage
if __name__ == "__main__":
    parser = IntentParser()
    
    # Test cases
    test_inputs = [
        "/scan --deep",
        "scan and learn this project",
        "fix the null reference error in UserProfile",
        "build user authentication feature",
        "optimize the DataTable component",
        "add tests to CheckoutFlow.ts",
        "what is the current test coverage?",
        "design a modern login page",
        "ship version 2.0",
    ]
    
    print("Intent Parser Test Results:\n")
    for user_input in test_inputs:
        task_type, params = parser.parse(user_input)
        pipeline = parser.get_agent_pipeline(task_type, is_existing_project=True)
        approval = parser.should_ask_for_approval(task_type)
        
        print(f"Input: {user_input}")
        print(f"  Task Type: {task_type.value}")
        print(f"  Parameters: {params}")
        print(f"  Pipeline: {' → '.join([f'Agent {id}' for id in pipeline])}")
        print(f"  Requires Approval: {approval}")
        print()
