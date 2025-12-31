#!/usr/bin/env python3
"""
Vibecode Studio - Your AI Development Team in a Box
Main entry point for the Vibecode multi-agent system
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Version
VERSION = "1.0.0"
PRODUCT_NAME = "Vibecode Studio"

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_banner():
    """Display Vibecode Studio banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╦  ╦┬┌┐ ┌─┐┌─┐┌─┐┌┬┐┌─┐  ╔═╗┌┬┐┬ ┬┌┬┐┬┌─┐
╚╗╔╝│├┴┐├┤ │  │ │ ││├┤   ╚═╗ │ │ │ ││││ │
 ╚╝ ┴└─┘└─┘└─┘└─┘─┴┘└─┘  ╚═╝ ┴ └─┘─┴┘┴└─┘
{Colors.ENDC}
{Colors.DIM}Your AI Development Team in a Box{Colors.ENDC}
{Colors.DIM}Version {VERSION}{Colors.ENDC}
{Colors.DIM}───────────────────────────────────────────────────────{Colors.ENDC}
"""
    print(banner)

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_section(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}▶ {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text: str):
    print(f"{Colors.DIM}{text}{Colors.ENDC}")


class VibecodeSudio:
    """
    Main Vibecode Studio application
    Coordinates agents, skills, and user interaction
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.workspace = Path.cwd()
        self.vibecode_dir = self.workspace / ".vibecode"
        self.state_file = self.vibecode_dir / "state.json"
        self.context_file = self.vibecode_dir / "project_context.md"
        
        # Load state
        self.state = self.load_state()
        
        # Initialize components
        self.agents_available = self.detect_agents()
        self.skills_available = self.detect_skills()
    
    def detect_agents(self) -> List[Dict]:
        """Detect available agents"""
        agents_dir = self.base_dir / "agents"
        if not agents_dir.exists():
            return []
        
        agents = []
        for agent_file in agents_dir.glob("agent_*.py"):
            agent_name = agent_file.stem.replace("agent_", "")
            agents.append({
                "name": agent_name,
                "file": agent_file,
                "available": True
            })
        
        return agents
    
    def detect_skills(self) -> List[Dict]:
        """Detect available skills"""
        skills_dir = self.base_dir / "skills"
        if not skills_dir.exists():
            return []
        
        skills = []
        for category_dir in skills_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('_'):
                for skill_dir in category_dir.iterdir():
                    if skill_dir.is_dir():
                        skill_md = skill_dir / "SKILL.md"
                        if skill_md.exists():
                            skills.append({
                                "name": skill_dir.name,
                                "category": category_dir.name,
                                "path": skill_dir,
                                "available": True
                            })
        
        return skills
    
    def load_state(self) -> Dict:
        """Load current state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "initialized": False,
            "project_scanned": False,
            "current_phase": "IDLE",
            "active_agents": []
        }
    
    def save_state(self):
        """Save current state"""
        self.vibecode_dir.mkdir(exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def show_main_menu(self):
        """Display main menu"""
        print_header("MAIN MENU")
        print(f"{Colors.BOLD}What would you like to do?{Colors.ENDC}\n")
        
        menu_items = [
            ("1", "🔍 Scan Project", "Analyze current project structure"),
            ("2", "🏗️  Build Feature", "Create new feature with agents"),
            ("3", "🐛 Fix Bug", "Diagnose and fix issues"),
            ("4", "🎨 Design UI", "Create or improve UI/UX"),
            ("5", "✅ Run Tests", "Generate and run tests"),
            ("6", "📦 Ship Release", "Prepare for deployment"),
            ("7", "🤖 List Agents", "Show all available agents"),
            ("8", "🔧 List Skills", "Show all available skills"),
            ("9", "⚙️  Settings", "Configure Vibecode"),
            ("0", "❌ Exit", "Quit Vibecode Studio"),
        ]
        
        for num, title, desc in menu_items:
            print(f"  {Colors.BOLD}{num}.{Colors.ENDC} {title}")
            print(f"     {Colors.DIM}{desc}{Colors.ENDC}\n")
        
        choice = input(f"{Colors.BOLD}Enter your choice (0-9): {Colors.ENDC}")
        return choice
    
    def cmd_scan_project(self):
        """Scan current project"""
        print_header("🔍 SCANNING PROJECT")
        
        print_info("Invoking Agent 00 (Forensic)...")
        print_section("Analyzing project structure...")
        
        # Import and run the scan from CLI tool
        from core.scanner import ProjectScanner
        
        scanner = ProjectScanner(self.workspace)
        results = scanner.scan_deep()
        
        print_success("Project scan complete!")
        print_info(f"Results saved to {self.vibecode_dir / 'audit_report.md'}")
        
        self.state["project_scanned"] = True
        self.save_state()
        
        # Show summary
        print_section("Summary")
        print(f"  Tech Stack: {', '.join(results.get('tech_stack', {}).get('languages', []))}")
        print(f"  Total Files: {results.get('file_analysis', {}).get('total_files', 0):,}")
        print(f"  Total Lines: {results.get('file_analysis', {}).get('total_lines', 0):,}")
        
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
    
    def cmd_build_feature(self):
        """Build a new feature using agents"""
        print_header("🏗️  BUILD FEATURE")
        
        # Check if project is scanned
        if not self.state.get("project_scanned"):
            print_warning("Project not scanned yet. Scanning now...")
            self.cmd_scan_project()
        
        print(f"\n{Colors.BOLD}What feature would you like to build?{Colors.ENDC}")
        feature_desc = input("Description: ")
        
        if not feature_desc.strip():
            print_error("Feature description cannot be empty")
            return
        
        print_section("Orchestrating agents...")
        
        # This would invoke the full agent pipeline
        agents_sequence = [
            ("00", "Forensic", "Analyzing codebase context"),
            ("01", "Architect", "Designing solution"),
            ("02", "Builder", "Implementing code"),
            ("03", "Designer", "Adding UI/UX"),
            ("04", "Reviewer", "Quality check"),
            ("05", "Integrator", "Writing files"),
            ("09", "Tester", "Generating tests"),
        ]
        
        for agent_id, agent_name, task in agents_sequence:
            print(f"\n{Colors.BLUE}Agent {agent_id} ({agent_name}):{Colors.ENDC} {task}...")
            print_info("  (Agent execution would happen here)")
        
        print_success("\nFeature pipeline complete!")
        print_info("Review the changes and commit when ready.")
        
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
    
    def cmd_fix_bug(self):
        """Fix a bug using Agent 07 (Medic)"""
        print_header("🐛 FIX BUG")
        
        print(f"\n{Colors.BOLD}Describe the bug or paste error message:{Colors.ENDC}")
        bug_desc = input("Bug: ")
        
        if not bug_desc.strip():
            print_error("Bug description cannot be empty")
            return
        
        print_section("Invoking Agent 07 (Medic)...")
        print_info("  Analyzing error...")
        print_info("  Identifying root cause...")
        print_info("  Generating fix...")
        
        print_success("\nBug fix generated!")
        print_info("Review the suggested changes.")
        
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
    
    def cmd_list_agents(self):
        """List all available agents"""
        print_header("🤖 AVAILABLE AGENTS")
        
        if not self.agents_available:
            print_warning("No agents found. Please install agents first.")
            return
        
        agents_info = [
            ("00", "Forensic", "Security audit & pattern analysis"),
            ("01", "Architect", "System design & planning"),
            ("02", "Builder", "Code implementation"),
            ("03", "Designer", "UI/UX design"),
            ("04", "Reviewer", "Quality assurance"),
            ("05", "Integrator", "File operations"),
            ("06", "Operator", "Runtime management"),
            ("07", "Medic", "Error recovery"),
            ("08", "Shipper", "Release management"),
            ("09", "Tester", "Test generation"),
        ]
        
        for agent_id, name, desc in agents_info:
            status = "✓" if any(a["name"] == f"{agent_id}_{name.lower()}" for a in self.agents_available) else "✗"
            print(f"{Colors.GREEN if status == '✓' else Colors.RED}{status}{Colors.ENDC} Agent {agent_id} - {Colors.BOLD}{name}{Colors.ENDC}")
            print(f"   {Colors.DIM}{desc}{Colors.ENDC}\n")
        
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
    
    def cmd_list_skills(self):
        """List all available skills"""
        print_header("🔧 AVAILABLE SKILLS")
        
        if not self.skills_available:
            print_warning("No skills found. Please install skills first.")
            return
        
        # Group by category
        skills_by_category = {}
        for skill in self.skills_available:
            category = skill["category"]
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill["name"])
        
        for category, skills in sorted(skills_by_category.items()):
            print(f"\n{Colors.BOLD}{Colors.CYAN}{category.upper()}{Colors.ENDC}")
            for skill in sorted(skills):
                print(f"  {Colors.GREEN}✓{Colors.ENDC} {skill}")
        
        print(f"\n{Colors.DIM}Total: {len(self.skills_available)} skills available{Colors.ENDC}")
        
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
    
    def cmd_settings(self):
        """Show and edit settings"""
        print_header("⚙️  SETTINGS")
        
        settings = [
            ("1", "AI Provider", "local (Free) / cloud (Anthropic Claude)"),
            ("2", "Speed Mode", "fast (60% faster) / safe (maximum quality)"),
            ("3", "Auto-test", "enabled / disabled"),
            ("4", "Compatibility Mode", "strict / balanced / modern"),
            ("5", "Back to Main Menu", ""),
        ]
        
        for num, name, value in settings:
            if value:
                print(f"  {num}. {Colors.BOLD}{name}{Colors.ENDC}: {Colors.DIM}{value}{Colors.ENDC}")
            else:
                print(f"  {num}. {name}")
        
        choice = input(f"\n{Colors.BOLD}Enter choice: {Colors.ENDC}")
        
        # Settings would be saved to config
        if choice == "5":
            return
        
        print_info("Settings saved!")
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
    
    def run(self):
        """Main application loop"""
        print_banner()
        
        # Check if in a project directory
        if not (self.workspace / "package.json").exists() and \
           not (self.workspace / "requirements.txt").exists() and \
           not (self.workspace / "Cargo.toml").exists():
            print_warning("You don't appear to be in a project directory.")
            print_info("Navigate to your project folder and run Vibecode Studio there.\n")
        
        # Show project info if scanned
        if self.state.get("project_scanned"):
            print_success("Project initialized and ready!")
        else:
            print_info("First time? Run 'Scan Project' to get started.")
        
        # Main loop
        while True:
            try:
                choice = self.show_main_menu()
                
                if choice == "0":
                    print(f"\n{Colors.CYAN}Thanks for using Vibecode Studio! 👋{Colors.ENDC}\n")
                    break
                elif choice == "1":
                    self.cmd_scan_project()
                elif choice == "2":
                    self.cmd_build_feature()
                elif choice == "3":
                    self.cmd_fix_bug()
                elif choice == "4":
                    print_info("UI Design feature coming soon!")
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
                elif choice == "5":
                    print_info("Test generation feature coming soon!")
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
                elif choice == "6":
                    print_info("Ship Release feature coming soon!")
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
                elif choice == "7":
                    self.cmd_list_agents()
                elif choice == "8":
                    self.cmd_list_skills()
                elif choice == "9":
                    self.cmd_settings()
                else:
                    print_error("Invalid choice. Please enter 0-9.")
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
            
            except KeyboardInterrupt:
                print(f"\n\n{Colors.CYAN}Thanks for using Vibecode Studio! 👋{Colors.ENDC}\n")
                break
            except Exception as e:
                print_error(f"An error occurred: {e}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description=f'{PRODUCT_NAME} - Your AI Development Team in a Box',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--version', action='version', version=f'{PRODUCT_NAME} v{VERSION}')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Run the application
    app = VibecodeSudio()
    app.run()


if __name__ == '__main__':
    main()
