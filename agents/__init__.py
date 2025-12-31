"""
Vibecode Agents Module
Agent loader for markdown-based agent specifications
"""

from .agent_base import Agent, load_agent, load_all_agents

__all__ = [
    'Agent',
    'load_agent',
    'load_all_agents'
]
