# 🎯 Vibecode Studio - Installation & Usage Quick Reference

**Install once, use everywhere!**

---

## ⚡ Quick Install

```powershell
# 1. Clone repository
git clone https://github.com/khoi1009/Vibecode-with-Multi-Agent.git

# 2. Enter directory
cd Vibecode-with-Multi-Agent

# 3. Install globally (editable mode - recommended)
pip install -e .

# 4. Verify
vibecode --version
vibe --version
```

**Done!** Now use from any project on your system.

---

## 🚀 Usage

### From Any Project Directory

```powershell
# Navigate to ANY project
cd C:\Projects\my-ecommerce-site
cd C:\Projects\blog-platform
cd C:\Projects\api-backend

# Use Vibecode Studio
vibecode --task "Add user authentication with OAuth"
vibe --task "Optimize database queries"
vibecode --task "Create React component with tests"
```

### With Specific Skills

```powershell
# Better Auth
cd C:\Projects\user-portal
vibe --task "Add Google OAuth login" --skills better-auth

# Databases
cd C:\Projects\api-backend
vibe --task "Add connection pooling and caching" --skills databases

# Media Processing  
cd C:\Projects\media-app
vibe --task "Batch resize and optimize images" --skills media-processing

# Web Frameworks
cd C:\Projects\nextjs-site
vibe --task "Add server actions with Zod validation" --skills web-frameworks
```

---

## 📚 What You Have Access To

After installation, **all** projects can use:

✅ **36 Premium Skills**  
✅ **165+ Reference Documentation Files**  
✅ **26 Automation Scripts** with full source code  
✅ **15.9x Enhanced AI Context** (1,485% more content)  
✅ **Multi-Agent Orchestration**

**Top Skills:**
- `better-auth` - Authentication with OAuth (8.6x content)
- `databases` - Database optimization (17.9x content)
- `media-processing` - Media automation (33.1x content)
- `web-frameworks` - Next.js, React, etc (12.7x content)
- `ai-multimodal` - AI processing (22.4x content)
- `devops` - Cloud deployment (11.8x content)
- `ui-styling` - Tailwind, shadcn (9.9x content)
- `backend-development` - APIs, servers (28.1x content)
- `threejs` - 3D graphics (24.8x content)
- `frontend-design` - UI/UX (11.0x content)

[See all 36 skills →](skills/)

---

## 🔄 Updating

### Editable Install (Recommended)

```powershell
cd Vibecode-with-Multi-Agent
git pull origin main
# Changes immediately available - no reinstall!
```

### Standard Install

```powershell
cd Vibecode-with-Multi-Agent
git pull origin main
pip install --upgrade .
```

---

## 💡 Real-World Examples

### Authentication Task

```powershell
cd C:\Projects\saas-platform
vibe --task "Add email/password authentication with password reset functionality" --skills better-auth

# AI uses:
# - SKILL.md (7KB)
# - 4 reference docs (46KB)
# - better_auth_init.py script (16KB)
# Total: 63KB context (8.6x enhancement!)
# Result: Complete auth setup in minutes instead of hours
```

### Database Optimization

```powershell
cd C:\Projects\high-traffic-api
vibe --task "Optimize database queries and add connection pooling for PostgreSQL" --skills databases

# AI uses:
# - SKILL.md (8KB)
# - 8 reference docs (120KB) 
# - db_performance_check.py, db_backup.py scripts
# Total: 137KB context (17.9x enhancement!)
# Result: Production-ready optimization with monitoring
```

### Media Processing

```powershell
cd C:\Projects\photo-sharing-app
vibe --task "Batch resize user uploads to multiple sizes (thumbnail, medium, large)" --skills media-processing

# AI uses:
# - SKILL.md (3KB)
# - 9 reference docs (96KB)
# - batch_resize.py, media_convert.py scripts (12KB)
# Total: 108KB context (33.1x enhancement!)
# Result: Working automation script ready to use
```

---

## 🎯 Key Benefits

### 1. **Install Once, Use Everywhere**
No need to clone repo for each project. Install globally, access from any directory.

### 2. **All Skills Available Globally**
Your expensive skills investment (36 skills, 165+ docs, 26 scripts) available to every project.

### 3. **Auto-Update (Editable Mode)**
```powershell
git pull  # Get updates instantly!
```

### 4. **15.9x More Context**
Enhanced skill loader provides 1.1MB context vs 69KB basic (1,485% increase).

### 5. **Working Code Examples**
26 automation scripts with full source code:
- `better_auth_init.py` - Auth setup wizard
- `db_backup.py` - Database backup automation
- `cloudflare_deploy.py` - Cloud deployment
- `batch_resize.py` - Image processing
- `nextjs_init.py` - Framework bootstrapping
- And 21 more!

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** | Complete installation guide with troubleshooting |
| [README.md](README.md) | Project overview with A/B test results |
| [QUICKSTART_CLI.md](QUICKSTART_CLI.md) | Quick start guide (5 min) |
| [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) | Master documentation index |
| [Skills Folder](skills/) | All 36 premium skills |

---

## 🚨 Troubleshooting

### Command Not Found After Install

**Windows:**
```powershell
# Add Python Scripts to PATH
$env:PATH += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python3X\Scripts"
# Or restart terminal
```

**Linux/macOS:**
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
# Or restart terminal
```

### Import Errors

```powershell
# Reinstall in editable mode
pip uninstall vibecode-studio
pip install -e .
```

### Skills Not Loading

```powershell
# Verify installation
pip show vibecode-studio

# Check skills directory
python -c "import vibecode_studio; print(vibecode_studio.__file__)"
```

---

## ✅ Verification Checklist

After installation, verify everything works:

```powershell
# 1. Check version
vibecode --version
# Should output: Vibecode Studio 1.0.0

# 2. Check commands work
vibe --help

# 3. Test from different directory
cd C:\Projects\test-project
vibecode --task "Hello test"

# 4. Verify skills accessible
vibecode --list-skills
```

If all checks pass: ✅ **You're ready to use Vibecode Studio across all projects!**

---

## 🎉 Success!

You now have Vibecode Studio installed globally with:

✅ `vibecode` and `vibe` commands available system-wide  
✅ 36 premium skills accessible from any project  
✅ 165+ reference docs providing 15.9x more AI context  
✅ 26 automation scripts with working code  
✅ Multi-agent orchestration for complex tasks  

**No more:**
- ❌ Cloning repo for each project
- ❌ Wasting 90% of skills investment
- ❌ Missing reference documentation
- ❌ Ignoring automation scripts

**Your workflow:**
```powershell
# Morning: E-commerce project
cd C:\Projects\shop
vibe --task "Add Stripe checkout"

# Afternoon: Blog platform
cd C:\Projects\blog
vibe --task "Add markdown editor"

# Evening: API backend
cd C:\Projects\api
vibe --task "Add rate limiting"

# All with the same Vibecode Studio installation! 🚀
```

---

**Repository:** https://github.com/khoi1009/Vibecode-with-Multi-Agent  
**Issues:** https://github.com/khoi1009/Vibecode-with-Multi-Agent/issues
