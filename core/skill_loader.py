"""
Intelligent Skill Loader
Dynamically selects and loads the most relevant skills for each task
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re


class Skill:
    """Represents a single skill"""
    
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.skill_file = path / "SKILL.md"
        self.references_dir = path / "references"
        self.scripts_dir = path / "scripts"
        self.description = ""
        self.keywords = []
        self.content = ""
        self.reference_files = []
        self.script_files = []
        
        if self.skill_file.exists():
            self._parse_skill_file()
        
        # Load all reference files and scripts
        self._load_references()
        self._load_scripts()
    
    def _parse_skill_file(self):
        """Parse SKILL.md and extract metadata"""
        content = self.skill_file.read_text(encoding='utf-8')
        self.content = content
        
        # Extract YAML frontmatter
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            
            # Extract description
            desc_match = re.search(r'description:\s*(.+)', frontmatter)
            if desc_match:
                self.description = desc_match.group(1).strip()
            
            # Extract keywords if present
            keywords_match = re.search(r'keywords:\s*\[(.+)\]', frontmatter)
            if keywords_match:
                self.keywords = [k.strip().strip('"\'') for k in keywords_match.group(1).split(',')]
        
        # If no keywords, extract from description and content
        if not self.keywords:
            self.keywords = self._extract_keywords(self.description + " " + content[:500])
    
    def _load_references(self):
        """Load all reference markdown files from the references folder"""
        if not self.references_dir.exists():
            return
        
        # Find all .md files in references directory
        for ref_file in self.references_dir.glob("*.md"):
            self.reference_files.append(ref_file)
        
        print(f"[DEBUG] Loaded {len(self.reference_files)} reference files for {self.name}")
    
    def _load_scripts(self):
        """Load all executable Python scripts from the scripts folder"""
        if not self.scripts_dir.exists():
            return
        
        # Find all .py files in scripts directory (excluding tests and __init__)
        for script_file in self.scripts_dir.rglob("*.py"):
            # Skip test files and __init__.py
            if script_file.name.startswith("test_") or script_file.name == "__init__.py":
                continue
            # Skip files in __pycache__ or .coverage
            if "__pycache__" in str(script_file) or ".coverage" in script_file.name:
                continue
            self.script_files.append(script_file)
        
        print(f"[DEBUG] Loaded {len(self.script_files)} executable scripts for {self.name}")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        # Common technical keywords
        keywords = []
        text_lower = text.lower()
        
        # Technology keywords
        tech_keywords = [
            'react', 'vue', 'angular', 'typescript', 'javascript', 'python',
            'node', 'express', 'django', 'flask', 'fastapi', 'next.js',
            'authentication', 'auth', 'jwt', 'oauth', 'security',
            'database', 'sql', 'mongodb', 'postgres', 'mysql',
            'api', 'rest', 'graphql', 'websocket',
            'ui', 'ux', 'design', 'css', 'tailwind', 'styling',
            'test', 'testing', 'jest', 'pytest', 'unit test',
            'debug', 'error', 'bug', 'fix',
            'deploy', 'devops', 'docker', 'kubernetes',
            'performance', 'optimize', 'cache',
            'mobile', 'ios', 'android', 'react-native',
            'payment', 'stripe', 'shopify',
            '3d', 'threejs', 'webgl', 'canvas',
            'pdf', 'excel', 'word', 'document',
            'planning', 'architecture', 'design pattern'
        ]
        
        for keyword in tech_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        return keywords[:10]  # Limit to top 10
    
    def relevance_score(self, query: str, agent_id: str = None) -> float:
        """
        Calculate relevance score for this skill given a query
        
        Args:
            query: User's request
            agent_id: Current agent ID (optional, for agent-skill affinity)
        
        Returns:
            Relevance score (0.0 to 1.0)
        """
        query_lower = query.lower()
        score = 0.0
        
        # 1. Direct skill name match (strongest signal)
        if self.name.replace('-', ' ') in query_lower:
            score += 0.5
        
        # 2. Description keyword match
        if self.description:
            desc_words = set(self.description.lower().split())
            query_words = set(query_lower.split())
            common = desc_words & query_words
            if common:
                score += 0.3 * (len(common) / max(len(query_words), 1))
        
        # 3. Keyword match
        for keyword in self.keywords:
            if keyword in query_lower:
                score += 0.15
        
        # 4. Agent-skill affinity boost
        if agent_id:
            affinity = self._get_agent_affinity(agent_id)
            score += affinity * 0.2
        
        return min(score, 1.0)
    
    def _get_agent_affinity(self, agent_id: str) -> float:
        """Get affinity score between this skill and an agent"""
        # Define which agents naturally use which skills
        affinities = {
            '00': ['code-review', 'sequential-thinking', 'problem-solving', 'debugging'],
            '01': ['planning', 'sequential-thinking', 'problem-solving'],
            '02': ['backend-development', 'frontend-development', 'web-frameworks', 
                   'databases', 'better-auth', 'payment-integration', 'debugging'],
            '03': ['ui-ux-pro-max', 'frontend-design', 'ui-styling', 'threejs', 'ai-artist'],
            '04': ['code-review', 'sequential-thinking', 'problem-solving'],
            '05': ['common'],
            '06': ['devops', 'chrome-devtools'],
            '07': ['debugging', 'problem-solving', 'sequential-thinking'],
            '08': ['devops', 'planning'],
            '09': ['debugging', 'code-review']
        }
        
        relevant_skills = affinities.get(agent_id, [])
        return 1.0 if self.name in relevant_skills else 0.0


class SkillLoader:
    """
    Intelligent skill loader that selects relevant skills for each task
    """
    
    def __init__(self, skills_dir: Path):
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, Skill] = {}
        self._load_all_skills()
    
    def _load_all_skills(self):
        """Load metadata for all skills (not full content yet)"""
        if not self.skills_dir.exists():
            return
        
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill = Skill(skill_dir)
                self.skills[skill.name] = skill
    
    def select_skills(self, 
                     query: str, 
                     agent_id: str = None, 
                     max_skills: int = 3,
                     min_score: float = 0.1) -> List[Tuple[Skill, float]]:
        """
        Select most relevant skills for a query
        
        Args:
            query: User's request
            agent_id: Current agent ID (for affinity scoring)
            max_skills: Maximum number of skills to return
            min_score: Minimum relevance score threshold
        
        Returns:
            List of (skill, score) tuples, ordered by relevance
        """
        # Score all skills
        scored_skills = []
        for skill in self.skills.values():
            score = skill.relevance_score(query, agent_id)
            if score >= min_score:
                scored_skills.append((skill, score))
        
        # Sort by score (highest first)
        scored_skills.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N with scores
        return scored_skills[:max_skills]
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Get a specific skill by name"""
        return self.skills.get(skill_name)
    
    def load_skill_content(self, skill: Skill, include_references: bool = True, include_scripts: bool = True) -> str:
        """
        Load full content of a skill including all reference files AND executable scripts
        
        Args:
            skill: The skill to load
            include_references: Whether to include all reference markdown files (default: True)
            include_scripts: Whether to include all executable Python scripts (default: True)
        
        Returns:
            Complete skill content with all references AND automation scripts
        """
        full_content = skill.content
        
        # Include reference documentation
        if include_references and skill.reference_files:
            full_content += "\n\n# === DETAILED REFERENCES ===\n\n"
            full_content += f"The following {len(skill.reference_files)} reference documents provide in-depth knowledge:\n\n"
            
            for ref_file in skill.reference_files:
                try:
                    ref_content = ref_file.read_text(encoding='utf-8')
                    full_content += f"\n## Reference: {ref_file.stem}\n\n"
                    full_content += ref_content
                    full_content += "\n\n---\n\n"
                except Exception as e:
                    print(f"[WARNING] Could not load {ref_file.name}: {e}")
        
        # Include executable automation scripts
        if include_scripts and skill.script_files:
            full_content += "\n\n# === AUTOMATION SCRIPTS ===\n\n"
            full_content += f"This skill includes {len(skill.script_files)} ready-to-use automation scripts:\n\n"
            
            for script_file in skill.script_files:
                try:
                    script_content = script_file.read_text(encoding='utf-8')
                    relative_path = script_file.relative_to(skill.path)
                    full_content += f"\n## Script: {relative_path}\n\n"
                    full_content += f"**Purpose:** Automated tool for this skill\n\n"
                    full_content += "```python\n"
                    full_content += script_content
                    full_content += "\n```\n\n"
                    full_content += "**Usage:** Can be executed directly or adapted for the current task\n\n"
                    full_content += "---\n\n"
                except Exception as e:
                    print(f"[WARNING] Could not load {script_file.name}: {e}")
        
        return full_content
    
    def build_skills_context(self, selected_skills: List[Skill], include_references: bool = True, include_scripts: bool = True) -> str:
        """
        Build context string from selected skills with ALL resources (references + scripts)
        
        Args:
            selected_skills: List of skills to include
            include_references: Whether to include all reference markdown files (default: True)
            include_scripts: Whether to include all executable Python scripts (default: True)
        
        Returns:
            Formatted context string for AI with COMPLETE skill content including automation tools
        """
        if not selected_skills:
            return ""
        
        context = "\n# === AVAILABLE SKILLS ===\n\n"
        context += "The following specialized skills are loaded for this task:\n\n"
        
        for i, skill in enumerate(selected_skills, 1):
            ref_count = len(skill.reference_files)
            script_count = len(skill.script_files)
            
            context += f"## Skill {i}: {skill.name}\n"
            context += f"**Resources:** {ref_count} reference docs"
            if script_count > 0:
                context += f" + {script_count} automation scripts"
            context += "\n\n"
            
            # Load COMPLETE content: SKILL.md + references + scripts
            full_content = self.load_skill_content(skill, 
                                                   include_references=include_references,
                                                   include_scripts=include_scripts)
            context += full_content
            context += "\n\n═══════════════════════════════════════\n\n"
        
        return context
    
    def list_all_skills(self) -> List[Tuple[str, str]]:
        """List all available skills with descriptions"""
        return [(name, skill.description) for name, skill in self.skills.items()]


# Example usage and testing
if __name__ == "__main__":
    # Initialize loader
    loader = SkillLoader(Path(__file__).parent.parent / "skills")
    
    print(f"✅ Loaded {len(loader.skills)} skills\n")
    
    # Test queries
    test_cases = [
        ("build user authentication with JWT", "02"),
        ("fix the null reference bug", "07"),
        ("design a modern dashboard UI", "03"),
        ("optimize database queries", "02"),
        ("create a payment integration with Stripe", "02"),
        ("review the code for security issues", "04"),
        ("deploy to production with Docker", "06"),
        ("generate tests for UserService", "09"),
        ("plan the architecture for a new feature", "01"),
    ]
    
    for query, agent_id in test_cases:
        print(f"Query: '{query}' (Agent {agent_id})")
        selected = loader.select_skills(query, agent_id, max_skills=3)
        
        if selected:
            print(f"  Selected Skills:")
            for skill in selected:
                score = skill.relevance_score(query, agent_id)
                print(f"    • {skill.name:30} (score: {score:.2f})")
        else:
            print(f"  No relevant skills found")
        print()
