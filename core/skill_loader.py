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
        self.description = ""
        self.keywords = []
        self.content = ""
        
        if self.skill_file.exists():
            self._parse_skill_file()
    
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
    
    def load_skill_content(self, skill: Skill) -> str:
        """Load full content of a skill"""
        return skill.content
    
    def build_skills_context(self, selected_skills: List[Skill]) -> str:
        """
        Build context string from selected skills
        
        Args:
            selected_skills: List of skills to include
        
        Returns:
            Formatted context string for AI
        """
        if not selected_skills:
            return ""
        
        context = "\n# === AVAILABLE SKILLS ===\n\n"
        context += "The following specialized skills are loaded for this task:\n\n"
        
        for i, skill in enumerate(selected_skills, 1):
            context += f"## Skill {i}: {skill.name}\n\n"
            context += skill.content
            context += "\n\n---\n\n"
        
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
