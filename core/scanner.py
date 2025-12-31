"""
Core Scanner Module
Handles project analysis and context generation
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple


class ProjectScanner:
    """
    Analyzes project structure, tech stack, and patterns
    Equivalent to /scan --deep from CLI tool
    """
    
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.vibecode_dir = self.project_path / ".vibecode"
        self.vibecode_dir.mkdir(exist_ok=True)
        
        self.ignore_dirs = {
            'node_modules', 'venv', '.venv', 'env', '.env',
            'dist', 'build', '.git', '.svn', '__pycache__',
            'coverage', '.next', '.nuxt', 'vendor', 'bower_components'
        }
    
    def scan_deep(self) -> Dict:
        """
        Perform deep project scan
        Returns comprehensive analysis results
        """
        print("  → Detecting tech stack...")
        tech_stack = self.detect_tech_stack()
        
        print("  → Analyzing files...")
        file_counts, line_counts = self.count_files_and_lines()
        
        print("  → Analyzing code patterns...")
        patterns = self.analyze_patterns()
        
        print("  → Detecting testing setup...")
        testing = self.detect_testing()
        
        print("  → Running security checks...")
        security = self.check_security()
        
        results = {
            'scan_date': datetime.now().isoformat(),
            'tech_stack': tech_stack,
            'file_analysis': {
                'total_files': sum(file_counts.values()),
                'total_lines': sum(line_counts.values()),
                'by_extension': file_counts,
                'lines_by_extension': line_counts
            },
            'patterns': patterns,
            'testing': testing,
            'security': security
        }
        
        # Save reports
        self._save_json_report(results)
        self._save_markdown_report(results)
        self._save_context_file(results)
        
        return results
    
    def detect_tech_stack(self) -> Dict:
        """Detect technologies used"""
        tech = {
            'languages': set(),
            'frameworks': set(),
            'tools': set()
        }
        
        # Check for Node.js
        if (self.project_path / 'package.json').exists():
            tech['tools'].add('Node.js/npm')
            try:
                with open(self.project_path / 'package.json') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                    
                    if 'react' in deps: tech['frameworks'].add('React')
                    if 'vue' in deps: tech['frameworks'].add('Vue')
                    if 'next' in deps: tech['frameworks'].add('Next.js')
                    if '@angular/core' in deps: tech['frameworks'].add('Angular')
                    if 'typescript' in deps: tech['languages'].add('TypeScript')
            except:
                pass
        
        # Check for Python
        if (self.project_path / 'requirements.txt').exists() or \
           (self.project_path / 'setup.py').exists() or \
           (self.project_path / 'pyproject.toml').exists():
            tech['languages'].add('Python')
            
            if (self.project_path / 'requirements.txt').exists():
                try:
                    with open(self.project_path / 'requirements.txt') as f:
                        content = f.read().lower()
                        if 'django' in content: tech['frameworks'].add('Django')
                        if 'flask' in content: tech['frameworks'].add('Flask')
                        if 'fastapi' in content: tech['frameworks'].add('FastAPI')
                except:
                    pass
        
        # Check for Ruby
        if (self.project_path / 'Gemfile').exists():
            tech['languages'].add('Ruby')
            try:
                with open(self.project_path / 'Gemfile') as f:
                    if 'rails' in f.read().lower():
                        tech['frameworks'].add('Ruby on Rails')
            except:
                pass
        
        # Check for Rust
        if (self.project_path / 'Cargo.toml').exists():
            tech['languages'].add('Rust')
        
        # Check for Go
        if (self.project_path / 'go.mod').exists():
            tech['languages'].add('Go')
        
        # Detect by file extensions
        for ext in ['.js', '.jsx', '.ts', '.tsx', '.py', '.rb', '.rs', '.go', '.java', '.php', '.cs']:
            if list(self.project_path.rglob(f'*{ext}')):
                lang_map = {
                    '.js': 'JavaScript', '.jsx': 'JavaScript',
                    '.ts': 'TypeScript', '.tsx': 'TypeScript',
                    '.py': 'Python', '.rb': 'Ruby',
                    '.rs': 'Rust', '.go': 'Go',
                    '.java': 'Java', '.php': 'PHP', '.cs': 'C#'
                }
                tech['languages'].add(lang_map.get(ext, ext[1:].upper()))
        
        return {k: sorted(list(v)) for k, v in tech.items()}
    
    def count_files_and_lines(self) -> Tuple[Dict, Dict]:
        """Count files and lines by extension"""
        file_counts = defaultdict(int)
        line_counts = defaultdict(int)
        
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                ext = Path(file).suffix.lower() or 'no-ext'
                file_counts[ext] += 1
                
                try:
                    filepath = Path(root) / file
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        line_counts[ext] += sum(1 for _ in f)
                except:
                    pass
        
        return dict(file_counts), dict(line_counts)
    
    def analyze_patterns(self) -> Dict:
        """Analyze code patterns"""
        patterns = {
            'naming_conventions': defaultdict(int),
            'import_styles': defaultdict(int)
        }
        
        # Sample files
        js_files = list(self.project_path.rglob('*.js'))[:20] + \
                   list(self.project_path.rglob('*.ts'))[:20]
        
        for filepath in js_files:
            if any(ignore in str(filepath) for ignore in self.ignore_dirs):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Naming conventions
                    if re.search(r'const\s+[a-z][a-zA-Z0-9]*\s*=', content):
                        patterns['naming_conventions']['camelCase'] += 1
                    if re.search(r'const\s+[A-Z][a-zA-Z0-9]*\s*=', content):
                        patterns['naming_conventions']['PascalCase'] += 1
                    
                    # Import styles
                    if 'import {' in content:
                        patterns['import_styles']['ES6 named imports'] += 1
                    if re.search(r'import\s+\w+\s+from', content):
                        patterns['import_styles']['ES6 default imports'] += 1
                    if 'require(' in content:
                        patterns['import_styles']['CommonJS require'] += 1
            except:
                continue
        
        return {
            'naming_conventions': dict(patterns['naming_conventions']),
            'import_styles': dict(patterns['import_styles'])
        }
    
    def detect_testing(self) -> Dict:
        """Detect testing setup"""
        testing = {
            'frameworks': [],
            'test_files': 0,
            'has_tests': False
        }
        
        # Count test files
        test_patterns = ['*.test.js', '*.test.ts', '*.spec.js', '*.spec.ts', 'test_*.py']
        for pattern in test_patterns:
            testing['test_files'] += len(list(self.project_path.rglob(pattern)))
        
        testing['has_tests'] = testing['test_files'] > 0
        
        # Detect frameworks
        if (self.project_path / 'package.json').exists():
            try:
                with open(self.project_path / 'package.json') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                    
                    if 'jest' in deps: testing['frameworks'].append('Jest')
                    if 'vitest' in deps: testing['frameworks'].append('Vitest')
                    if 'mocha' in deps: testing['frameworks'].append('Mocha')
            except:
                pass
        
        if (self.project_path / 'pytest.ini').exists():
            testing['frameworks'].append('pytest')
        
        return testing
    
    def check_security(self) -> Dict:
        """Basic security checks"""
        issues = []
        warnings = []
        
        # Check for .env exposure
        if (self.project_path / '.env').exists():
            if (self.project_path / '.gitignore').exists():
                try:
                    with open(self.project_path / '.gitignore') as f:
                        if '.env' not in f.read():
                            issues.append('.env file not in .gitignore')
                except:
                    pass
            else:
                issues.append('.env exists but no .gitignore found')
        
        # Check for hardcoded secrets (sample only)
        secret_patterns = [
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', 'API key in code'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Password in code')
        ]
        
        sample_files = list(self.project_path.rglob('*.js'))[:10] + \
                       list(self.project_path.rglob('*.py'))[:10]
        
        for filepath in sample_files:
            if any(ignore in str(filepath) for ignore in self.ignore_dirs):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern, desc in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            warnings.append(f'{desc} in {filepath.name}')
            except:
                continue
        
        return {
            'critical_issues': issues,
            'warnings': warnings[:5]  # Limit warnings
        }
    
    def _save_json_report(self, results: Dict):
        """Save JSON report"""
        report_path = self.vibecode_dir / 'scan_report.json'
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
    
    def _save_markdown_report(self, results: Dict):
        """Save Markdown audit report"""
        report_path = self.vibecode_dir / 'audit_report.md'
        
        with open(report_path, 'w') as f:
            f.write("# Vibecode Audit Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Tech Stack
            f.write("## Tech Stack\n\n")
            for category, items in results['tech_stack'].items():
                if items:
                    f.write(f"**{category.title()}:** {', '.join(items)}\n\n")
            
            # File Analysis
            f.write("## File Analysis\n\n")
            f.write(f"- **Total Files:** {results['file_analysis']['total_files']:,}\n")
            f.write(f"- **Total Lines:** {results['file_analysis']['total_lines']:,}\n\n")
            
            # Testing
            if results['testing']['has_tests']:
                f.write("## Testing\n\n")
                f.write(f"✓ {results['testing']['test_files']} test files found\n\n")
                if results['testing']['frameworks']:
                    f.write(f"**Frameworks:** {', '.join(results['testing']['frameworks'])}\n\n")
            
            # Security
            if results['security']['critical_issues'] or results['security']['warnings']:
                f.write("## Security\n\n")
                for issue in results['security']['critical_issues']:
                    f.write(f"- ❌ {issue}\n")
                for warning in results['security']['warnings']:
                    f.write(f"- ⚠️ {warning}\n")
    
    def _save_context_file(self, results: Dict):
        """Save project context for AI"""
        context_path = self.vibecode_dir / 'project_context.md'
        
        with open(context_path, 'w') as f:
            f.write("# Project Context\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            # Tech Stack
            f.write("## Tech Stack\n\n")
            for category, items in results['tech_stack'].items():
                if items:
                    f.write(f"- **{category.title()}:** {', '.join(items)}\n")
            f.write("\n")
            
            # Patterns
            if results['patterns']['naming_conventions']:
                f.write("## Coding Conventions\n\n")
                dominant = max(results['patterns']['naming_conventions'].items(), 
                             key=lambda x: x[1])[0]
                f.write(f"**Primary naming convention:** {dominant}\n\n")
            
            # Testing
            if results['testing']['has_tests']:
                f.write("## Testing\n\n")
                f.write(f"- **Test files:** {results['testing']['test_files']}\n")
                if results['testing']['frameworks']:
                    f.write(f"- **Frameworks:** {', '.join(results['testing']['frameworks'])}\n")
                f.write("\n")
            
            # AI Guidelines
            f.write("## Guidelines for AI Agents\n\n")
            f.write("1. Follow existing conventions documented above\n")
            f.write("2. Match the coding style of surrounding code\n")
            f.write("3. Add tests if the project has test coverage\n")
            f.write("4. Keep changes surgical and minimal\n")
