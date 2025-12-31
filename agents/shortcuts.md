# Vibecode Command Reference (VOS 2.0)

**Production-Grade Multi-Agent CLI**

This reference documents all orchestrator commands for controlling the Vibecode Operating System. Commands are organized by workflow phase and include safety levels, expected outputs, and common usage patterns.

---

## Command Safety Levels

🟢 **SAFE** - Read-only, no filesystem changes  
🟡 **MODIFY** - Creates/edits files with validation  
🔴 **DANGEROUS** - Potential for significant changes  
⚠️ **EXPERIMENTAL** - Use with caution

---

## 0. Quick Reference (Most Common)

```bash
/scan              # Audit codebase
/plan <feature>    # Design feature
/build             # Implement approved plan
/test              # Run test suite
/fix               # Auto-fix last error
/review            # Quality gate check
/ship              # Prepare release
```

---

## 1. Discovery & Analysis (Phase A)

### /scan 🟢
**Agent:** 00 (Forensic)  
**Purpose:** Deep codebase audit - tech stack, security, architecture analysis  
**Safety:** Read-only  
**Output:** `audit_report.md`  
**Duration:** 30-90 seconds  
**Use when:** Starting new project, onboarding, or before major changes

```bash
/scan              # Full audit
/scan --quick      # Skip deep analysis (5-10s)
/scan --security   # Security-focused audit only
```

**What it checks:**
- Tech stack detection (languages, frameworks, versions)
- Project structure and architecture patterns
- Security vulnerabilities (dependencies, hardcoded secrets)
- Code quality metrics
- Missing documentation

**Example output:**
```text
📋 Audit Complete
Stack: React 18 + TypeScript + Vite
Security: ⚠️ 2 medium vulnerabilities found
Architecture: Component-based, decent separation
Recommendation: Update dependencies, add API layer
Report: .vibecode/audit_report.md
```

---

### /plan <description> 🟡
**Agent:** 01 (Architect)  
**Purpose:** Transform requirements into rigorous, enforceable contracts  
**Safety:** Creates `docs/vibecode_plan.md`  
**Duration:** 1-3 minutes  
**Use when:** Starting new feature, unclear requirements

```bash
/plan <feature>                  # Create new feature plan
/plan "user authentication"      # Quote multi-word features
/plan --refine                   # Update existing plan with feedback
/plan --review                   # Show current plan without changes
```

**What it does:**
- Proactive requirements gathering (asks clarifying questions)
- Creates detailed blueprint with acceptance criteria
- Defines file structure, interfaces, dependencies
- Estimates complexity and risks
- Produces enforceable contract for Agent 02

**Example output:**
```text
📐 Plan Generated

Feature: User Authentication
Complexity: Medium (3-5 days)
Files to Create: 8
Dependencies: bcrypt, jsonwebtoken
Risks: Session management complexity

Contract: docs/vibecode_plan.md
Ready for /build when approved
```

---

### /refine 🟡
**Agent:** 01 (Architect)  
**Purpose:** Update plan based on feedback without starting from scratch  
**Safety:** Modifies existing plan  
**Use when:** Plan needs adjustments after review

```bash
/refine                          # Interactive refinement
/refine "add password reset"     # Specific change request
/refine --rewrite                # Start plan from scratch
```

---

## 2. Implementation (Phase B)

### /build 🟡
**Agent:** 02 (Builder)  
**Purpose:** Execute approved plan with production-grade implementation  
**Safety:** Creates/modifies source files per contract  
**Duration:** 2-10 minutes depending on scope  
**Prerequisites:** Approved plan in `docs/vibecode_plan.md`

```bash
/build                    # Execute current plan
/build --dry-run          # Preview what will be created (no writes)
/build --tdd              # Test-first approach (write tests before code)
/build --resume           # Continue interrupted build
```

**What it does:**
- Reviews contract and validates feasibility
- Implements with TDD (tests first)
- Applies SOLID principles and best practices
- Adds observability (logging, metrics)
- Implements failure engineering (retries, circuit breakers)
- Ensures security by design (input validation, auth)
- Optimizes performance (O(n) analysis, caching)
- Prepares for production (health checks, feature flags)

**Example output:**
```text
🔨 Build Complete

Files Created:
  - src/lib/auth/login.ts (145 lines)
  - src/lib/auth/register.ts (98 lines)
  - src/lib/auth/session.ts (67 lines)
  - src/types/auth.ts (34 lines)

Tests Created:
  - src/lib/auth/login.test.ts (23 tests)
  - Coverage: 94%

Next: /vibe to apply design system
```

---

### /vibe 🟡
**Agent:** 03 (Designer)  
**Purpose:** Apply production-grade UX/UI with accessibility-first approach  
**Safety:** Modifies UI files  
**Duration:** 1-5 minutes  
**Prerequisites:** Functional code from /build

```bash
/vibe                     # Apply design system
/vibe --audit             # Design audit only (no changes)
/vibe --a11y              # Accessibility-focused pass
/vibe --responsive        # Responsive design focus
/vibe --dark-mode         # Add dark mode support
```

**What it does:**
- Ensures WCAG 2.1 AA compliance
- Implements true mobile-first responsive design
- Adds proper interaction states (hover, focus, loading, error)
- Applies design tokens and spacing system
- Ensures 60fps animations
- Fixes layout shift issues
- Optimizes touch targets (44×44px minimum)

**Example output:**
```text
🎨 Design Applied

Accessibility: ✅ WCAG AA compliant
Responsive: ✅ Mobile-first (320px-2560px)
Performance: ✅ 60fps animations
Touch Targets: ✅ All ≥44×44px

Files Modified:
  - src/components/LoginForm.tsx
  - src/components/Button.tsx
  - src/styles/tokens.ts

Next: /review for quality gate
```

---

### /code <description> 🟡
**Agent Chain:** 01 → 02 → 03  
**Purpose:** End-to-end feature implementation (plan → build → design)  
**Safety:** Full feature lifecycle  
**Duration:** 5-15 minutes  
**Use when:** Clear feature requirements, want full automation

```bash
/code "user profile page"        # Full feature chain
/code "dark mode" --skip-vibe    # Skip design phase
/code "API endpoint" --api-only  # Backend only (no UI)
```

**What it does:**
1. Agent 01 creates plan (with your approval)
2. Agent 02 implements code + tests
3. Agent 03 applies design system
4. Automatic handoff between phases

---

## 3. Quality Assurance (Phase C)

### /review 🟢
**Agent:** 04 (Reviewer)  
**Purpose:** Comprehensive code review with 10-phase inspection  
**Safety:** Read-only analysis  
**Duration:** 1-3 minutes  
**Use when:** Before merging, before shipping, after major changes

```bash
/review                   # Full 10-phase review
/review --security        # Security-focused review only
/review --performance     # Performance analysis only
/review --accessibility   # A11y compliance check
/review --quick           # Fast review (syntax, tests, security)
```

**What it checks:**
- Context review (does it match contract?)
- Security (OWASP Top 10, injection, XSS, auth)
- Performance (O(n) complexity, N+1 queries, React optimization)
- Code quality (type safety, error handling, maintainability)
- Testing (coverage, edge cases, flaky tests)
- Accessibility (WCAG AA, keyboard nav, ARIA)
- Observability (logging, metrics, tracing)
- Deployment safety (feature flags, migrations, rollback)
- Contract adherence
- Production readiness checklist

**Example output:**
```text
🔍 Review Complete

Status: ✅ APPROVED

Summary:
  ✅ Security: No critical issues
  ✅ Performance: Efficient algorithms
  ✅ Tests: 94% coverage (target: 80%)
  ✅ Accessibility: WCAG AA compliant
  ⚠️ Code Quality: 1 minor duplication

Warnings:
  - Similar fetch logic in users.ts and posts.ts
  - Recommendation: Extract to httpClient utility
  - Priority: Low (not blocking)

Ready for deployment.
Next: /ship to prepare release
```

---

### /test 🟢
**Agent:** 09 (Testing)  
**Purpose:** Generate comprehensive test suite and execute validation  
**Safety:** Creates test files, runs tests (no production code changes)  
**Duration:** 1-5 minutes generation + test execution time  
**Use when:** After /build, before /ship, when tests are missing

```bash
/test                     # Generate + run all tests
/test --generate          # Generate tests only (don't run)
/test --run               # Run existing tests only
/test --unit              # Unit tests only
/test --integration       # Integration tests only
/test --e2e               # E2E tests only
/test --coverage          # With coverage report
/test --watch             # Watch mode for TDD
```

**What it does:**
- Generates unit tests (70% of pyramid)
- Generates integration tests (20%)
- Generates E2E tests (10%)
- Tests edge cases and error conditions
- Security testing (injection, XSS)
- Performance testing
- Accessibility testing
- Runs full suite with coverage

**Example output:**
```text
🧪 Test Results

Generated:
  - 45 unit tests
  - 12 integration tests
  - 5 E2E tests

Execution:
  Tests: 62 passed, 62 total
  Duration: 8.4s
  
Coverage:
  Statements: 91% (target: 80%)
  Branches: 87%
  Functions: 89%
  Lines: 90%

✅ All tests passed
✅ Coverage threshold met

Next: /ship when ready to release
```

---

## 4. Operations & Runtime (Phase D)

### /run 🟡
**Agent:** 06 (Runtime)  
**Purpose:** Start development server with environment validation  
**Safety:** Starts background process  
**Duration:** 10-60 seconds  
**Use when:** Need to preview locally, verify app boots

```bash
/run                      # Start dev server
/run --port 3000          # Specific port
/run --prod               # Production build + preview
/run --debug              # Verbose logging
/run --kill               # Stop running server
```

**What it does:**
- Detects project type and toolchain
- Validates dependencies are installed
- Checks for port conflicts (auto-resolves)
- Starts server in background
- Discovers and reports URL
- Monitors for crashes

**Example output:**
```text
🚀 Server Started

Project: Next.js 14
Command: npm run dev
URL: http://localhost:3000
PID: 12345
Status: ✅ Healthy

Health Check: Passed
Build Time: 2.3s

Ready for development.
Press Ctrl+C to stop, or use /run --kill
```

---

### /fix 🟡
**Agent:** 07 (Medic)  
**Purpose:** Diagnose and repair errors with graduated escalation  
**Safety:** Surgical patches only (max 5 lines per attempt)  
**Duration:** 30s - 3 minutes  
**Use when:** Runtime error, test failure, build break

```bash
/fix                      # Fix last error
/fix --error "specific error message"
/fix --file <path>        # Fix specific file
/fix --rollback           # Undo last fix
/fix --history            # Show all fix attempts
```

**What it does:**
- Reads error stack trace
- Performs root cause analysis
- Applies minimal surgical fix (attempt 1: 5 lines max)
- Validates fix doesn't break other code
- Escalates if multiple attempts fail
- NEVER deletes code
- NEVER full-replaces large files

**Safety limits:**
- Attempt 1: Max 5 lines changed
- Attempt 2: Max 20 lines changed
- Attempt 3: Max 50 lines changed
- Attempt 4: Escalate to Architect
- Circuit breaker: Stops after 3 attempts on same error

**Example output:**
```text
🚑 Fix Applied

Error: "TypeError: Cannot read property 'map' of undefined"
File: src/components/UserList.tsx:42
Root Cause: items prop undefined on first render

Fix Strategy: Atomic (Attempt 1 of 5)
Lines Changed: 1

Before:
  return items.map(item => <Item key={item.id} />)

After:
  return (items ?? []).map(item => <Item key={item.id} />)

Validation: ✅ Syntax valid, tests passed
Status: RESOLVED

Next: Re-run your command to verify
```

---

### /ship 🟡
**Agent:** 08 (Shipper)  
**Purpose:** Prepare production-ready release with full validation  
**Safety:** Creates release artifacts, updates docs  
**Duration:** 2-5 minutes  
**Prerequisites:** Tests pass, review approved  
**Use when:** Ready to deploy or deliver to user

```bash
/ship                     # Full release preparation
/ship --check             # Pre-flight check only (no changes)
/ship --version <ver>     # Bump to specific version
/ship --major             # Major version bump (breaking)
/ship --minor             # Minor version bump (features)
/ship --patch             # Patch version bump (fixes)
/ship --skip-docs         # Skip documentation generation
```

**What it does (5 phases):**
1. **Validation:** Build, tests, lint, security scan, bundle size
2. **Cleanup:** Remove debris, format, optimize assets
3. **Documentation:** README, CHANGELOG, deployment guide, runbook
4. **Packaging:** Version bump, git tag, build artifacts
5. **Deployment Readiness:** Health checks, rollback plan, monitoring

**Example output:**
```text
📦 Release Ready: v1.0.0

Validation:
  ✅ Build: PASSED
  ✅ Tests: PASSED (94% coverage)
  ✅ Lint: PASSED
  ✅ Security: No critical issues
  ✅ Bundle: 385KB (target: 500KB)

Documentation:
  ✅ README.md: Updated
  ✅ CHANGELOG.md: Generated
  ✅ DEPLOYMENT.md: Created
  ✅ RUNBOOK.md: Created

Packaging:
  ✅ Version: Bumped to 1.0.0
  ✅ Git Tag: v1.0.0 created
  ✅ Artifacts: Generated in dist/

Next Steps:
  1. Deploy to staging: npm run deploy:staging
  2. Run smoke tests
  3. Deploy to production: npm run deploy:prod
  4. Monitor for 1 hour

Rollback: npm run rollback v0.9.5
```

---

## 5. System Commands

### /status 🟢
**Purpose:** System health and current state  
**Safety:** Read-only  
**Duration:** Instant

```bash
/status                   # Full system status
/status --agents          # Agent availability
/status --errors          # Recent errors
/status --performance     # Performance metrics
```

**Example output:**
```text
📊 Vibecode System Status

Active Agent: 02 (Builder)
Current Phase: Implementation
Task: Building user authentication
Progress: 65% (6/8 files)

Project Health: ✅ Healthy
  - Build: Passing
  - Tests: 62/62 passed (91% coverage)
  - Server: Running on :3000
  - Last Error: None

State File: .vibecode/state.json
Session Log: .vibecode/session_context.md (156 entries)
Circuit Breaker: Not triggered

Recent Activity:
  10:45 - Agent 01: Plan approved
  10:47 - Agent 02: Started build
  10:52 - Agent 02: 6/8 files complete
```

---

### /turbo ⚠️
**Purpose:** Fast iteration mode (RESTRICTED FOR SAFETY)  
**Safety:** DANGEROUS - skips planning and review  
**Use when:** Trivial changes only (typos, formatting, deps)

```bash
/turbo "fix typo in header"      # Single trivial change
/turbo --unsafe                  # Override safety (NOT RECOMMENDED)
```

**⚠️ SAFETY RESTRICTIONS:**

Turbo mode is **ONLY** allowed for:
- ✅ Syntax fixes (typos, semicolons)
- ✅ Dependency installation
- ✅ Code formatting (prettier, eslint --fix)
- ✅ Comment updates
- ✅ Import organization

Turbo mode is **FORBIDDEN** for:
- ❌ Logic changes
- ❌ New features
- ❌ Refactoring
- ❌ API changes
- ❌ Security-related code
- ❌ Database migrations

**Why restricted:** In 25 years of production engineering, "quick fixes without review" are the #1 cause of incidents.

---

### /rollback 🔴
**Agent:** 05 (Integrator)  
**Purpose:** Revert recent changes  
**Safety:** DANGEROUS - restores previous state  
**Use when:** Recent change broke something

```bash
/rollback                 # Interactive rollback
/rollback --last          # Revert last operation
/rollback --to <version>  # Revert to specific version
/rollback --show          # Show rollback history
```

**Example output:**
```text
⏪ Rollback Options

Recent Operations:
  1. [10:52] Agent 02: Created authentication system (8 files)
  2. [10:35] Agent 03: Applied design system (4 files)
  3. [10:20] Agent 02: Built user profile (3 files)

Select operation to revert (1-3): 1

Reverting: Authentication system
Files to remove: 8
Files to restore: 2

Confirm? (y/n)
```

---

### /inspect <path> 🟢
**Purpose:** Deep analysis of specific file or module  
**Safety:** Read-only

```bash
/inspect src/components/UserProfile.tsx
/inspect src/lib/auth --recursive
/inspect --dependencies              # Dependency tree
```

---

### /clean 🔴
**Purpose:** Remove generated files and caches  
**Safety:** DANGEROUS - deletes build artifacts

```bash
/clean                    # Interactive cleanup
/clean --cache            # Clear caches only
/clean --build            # Remove build artifacts
/clean --all              # Full clean (requires confirmation)
```

**What it removes:**
- `node_modules/` (if --all)
- `dist/`, `build/`, `.next/`
- `.turbo/`, `.cache/`
- `*.log` files
- `coverage/`

**What it NEVER removes:**
- Source code (`src/`)
- Configuration files
- `.vibecode/` state
- `.git/` history

---

## 6. Advanced Workflows

### Chaining Commands
```bash
# Full feature lifecycle
/plan "user auth" && /build && /vibe && /test && /review

# Fix and verify
/fix && /test && /run

# Ship pipeline
/test && /review && /ship
```

### Conditional Execution
```bash
/review && /ship              # Ship only if review passes
/test || /fix                 # Fix if tests fail
```

---

## 7. Troubleshooting Commands

### /diagnose 🟢
**Purpose:** Comprehensive system diagnostic  
**Use when:** Something is wrong but unclear what

```bash
/diagnose                     # Full diagnostic
/diagnose --build             # Build issues only
/diagnose --runtime           # Runtime issues only
/diagnose --tests             # Test issues only
```

**Checks:**
- Toolchain versions (Node, npm, Python)
- Dependency conflicts
- Port availability
- File permissions
- Environment variables
- Recent errors
- Agent circuit breakers

---

### /logs 🟢
**Purpose:** View system logs

```bash
/logs                         # Recent logs
/logs --agent 07              # Specific agent logs
/logs --error                 # Error logs only
/logs --tail                  # Follow logs live
```

---

## 8. Configuration Commands

### /config 🟡
**Purpose:** View/modify Vibecode configuration

```bash
/config                       # Show current config
/config --edit                # Edit interactively
/config --reset               # Reset to defaults
/config set turbo.enabled false
```

---

## 9. Command Aliases (Shortcuts)

```bash
# Discovery
/audit      → /scan
/design     → /plan

# Build
/code       → /build
/style      → /vibe
/make       → /code

# Quality
/qa         → /review
/check      → /review

# Operations
/start      → /run
/dev        → /run
/serve      → /run
/repair     → /fix
/heal       → /fix
/deploy     → /ship
/release    → /ship
```

---

## 10. Best Practices (25 Years of Lessons)

### ✅ DO:
- Run `/scan` before starting work on unfamiliar codebase
- Run `/review` before every `/ship`
- Run `/test` after every `/build`
- Use `/status` frequently to monitor progress
- Read agent outputs carefully - they contain important context
- Let agents ask clarifying questions (don't rush)

### ❌ DON'T:
- Use `/turbo` for anything non-trivial
- Skip `/review` to "save time"
- Ignore warnings in agent outputs
- Chain too many commands without checking results
- Assume `/fix` will always work (escalate after 3 attempts)
- Ship without running `/test`

### 🎯 Pro Tips:
- Use `--dry-run` flags to preview before executing
- Keep `.vibecode/state.json` and `.vibecode/session_context.md` under version control
- Review `audit_report.md` when onboarding new team members
- Use `/inspect` to understand unfamiliar code before modifying
- Check `/status --errors` when debugging mysterious issues

---

## 11. Emergency Procedures

### System is Unresponsive
```bash
/status                       # Check system health
/logs --error                 # Check for errors
/diagnose                     # Full diagnostic
```

### Agent Stuck in Loop
```bash
/status                       # Check circuit breaker
/rollback                     # Revert last operation
# Manual: Edit .vibecode/state.json, reset attempt_count
```

### Accidental Deletion
```bash
/rollback --last              # Revert immediately
# If not in history: git checkout -- <file>
```

### Build Completely Broken
```bash
/clean --build                # Remove build artifacts
/run                          # Try clean build
/fix                          # If errors persist
# If still broken: /rollback to last working state
```

---

## 12. Command Reference Summary

| Command | Agent | Safety | Duration | Purpose |
|---------|-------|--------|----------|---------|
| /scan | 00 | 🟢 | 30-90s | Audit codebase |
| /plan | 01 | 🟡 | 1-3m | Design feature |
| /refine | 01 | 🟡 | 1-2m | Update plan |
| /build | 02 | 🟡 | 2-10m | Implement code |
| /vibe | 03 | 🟡 | 1-5m | Apply design |
| /code | 01→02→03 | 🟡 | 5-15m | Full feature |
| /review | 04 | 🟢 | 1-3m | Quality gate |
| /test | 09 | 🟢 | 1-5m | Generate/run tests |
| /run | 06 | 🟡 | 10-60s | Start server |
| /fix | 07 | 🟡 | 30s-3m | Repair errors |
| /ship | 08 | 🟡 | 2-5m | Prepare release |
| /status | System | 🟢 | Instant | System health |
| /turbo | System | ⚠️ | Varies | Fast mode (restricted) |
| /rollback | 05 | 🔴 | 10-30s | Revert changes |
| /diagnose | System | 🟢 | 30s-2m | Troubleshooting |

---

## Version
**Vibecode OS:** 2.0  
**Last Updated:** 2025-12-30  
**Agents:** 10 (00-09)

---

**Remember:** These agents have 25 years of combined engineering experience embedded in them. Trust the process, read the outputs, and escalate when uncertain. Quality over speed. Safety over shortcuts.