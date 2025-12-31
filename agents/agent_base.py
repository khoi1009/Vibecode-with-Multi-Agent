"""
Agent Loader
Simple loader for agent markdown specifications
"""

from pathlib import Path
from typing import Dict, Any, Optional


class Agent:
    """
    Generic Agent class that loads instructions from .md files
    Each agent is defined by its markdown specification file
    """
    
    def __init__(self, agent_file: Path):
        """
        Initialize agent from markdown file
        
        Args:
            agent_file: Path to agent .md file (e.g., 00_auditor.md)
        """
        self.file_path = agent_file
        self.id = agent_file.stem.split('_')[0]  # Extract "00" from "00_auditor"
        self.name = '_'.join(agent_file.stem.split('_')[1:])  # Extract "auditor" from "00_auditor"
        self.instructions = self._load_instructions()
        self.description = self._extract_description()
    
    def _load_instructions(self) -> str:
        """Load full agent instructions from markdown file"""
        if self.file_path.exists():
            return self.file_path.read_text(encoding='utf-8')
        return f"# Agent {self.id} - {self.name}\n\nNo instructions found."
    
    def _extract_description(self) -> str:
        """Extract first line/description from markdown"""
        lines = self.instructions.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                return line.strip()
        return f"Agent {self.id}"
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "file": str(self.file_path),
            "instructions_length": len(self.instructions)
        }
    
    def __repr__(self) -> str:
        return f"Agent {self.id} ({self.name})"


def load_agent(agent_file: Path) -> Agent:
    """
    Load a single agent from markdown file
    
    Args:
        agent_file: Path to .md file
    
    Returns:
        Agent instance
    """
    return Agent(agent_file)


def load_all_agents(agents_dir: Path) -> Dict[str, Agent]:
    """
    Load all agents from directory
    
    Args:
        agents_dir: Directory containing agent .md files
    
    Returns:
        Dictionary mapping agent ID to Agent instance
    """
    agents = {}
    
    if not agents_dir.exists():
        return agents
    
    # Load all .md files except shortcuts.md
    for agent_file in sorted(agents_dir.glob('*.md')):
        if agent_file.name == 'shortcuts.md':
            continue
        
        agent = load_agent(agent_file)
        agents[agent.id] = agent
    
    return agents
