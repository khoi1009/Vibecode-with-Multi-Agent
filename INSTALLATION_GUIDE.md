# Vibecode Studio Installation Guide

Complete guide for installing Vibecode Studio globally on your system.

---

## 🚀 Quick Install (Recommended)

### Windows

```powershell
# Clone repository
git clone https://github.com/khoi1009/Vibecode-with-Multi-Agent.git
cd Vibecode-with-Multi-Agent

# Install globally
pip install -e .

# Verify installation
vibecode --version
vibe --version
```

### Linux/macOS

```bash
# Clone repository
git clone https://github.com/khoi1009/Vibecode-with-Multi-Agent.git
cd Vibecode-with-Multi-Agent

# Install globally
pip install -e .

# Verify installation
vibecode --version
vibe --version
```

---

## 📦 Installation Methods

### Method 1: Editable Install (Development Mode) - **RECOMMENDED**

Best for active development and getting updates:

```powershell
# Install in editable mode
pip install -e .

# Update anytime with git pull
git pull origin main
# Changes immediately available!
```

**Benefits:**
- ✅ Edit code and see changes immediately
- ✅ Easy to update (`git pull`)
- ✅ All 36 skills + automation scripts included
- ✅ Works from any directory

### Method 2: Standard Install

Install as a regular Python package:

```powershell
pip install .
```

**To update:**
```powershell
git pull origin main
pip install --upgrade .
```

### Method 3: Install from GitHub (Direct)

Install directly from GitHub without cloning:

```powershell
pip install git+https://github.com/khoi1009/Vibecode-with-Multi-Agent.git
```

**To update:**
```powershell
pip install --upgrade --force-reinstall git+https://github.com/khoi1009/Vibecode-with-Multi-Agent.git
```

### Method 4: Build Distribution Package

Create a distributable wheel:

```powershell
# Install build tools
pip install build wheel

# Build package
python -m build

# Install from wheel
pip install dist/vibecode_studio-1.0.0-py3-none-any.whl
```

---

## ✅ Verify Installation

After installation, verify everything works:

```powershell
# Check version
vibecode --version

# Should output:
# Vibecode Studio 1.0.0

# Test from any directory
cd C:\Projects\your-project
vibecode --task "Create a React component"

# Test short alias
vibe --task "Add authentication"

# Check skills are available
vibecode --list-skills
```

---

## 🎯 Usage After Installation

### From Any Project Directory

```powershell
# Navigate to any project
cd C:\Projects\my-ecommerce-site

# Use Vibecode Studio directly
vibecode --task "Add product search with filters"

# Or use the short alias
vibe --task "Optimize database queries"
```

### Skills Are Always Available

Your 36 premium skills (165+ reference docs + 26 automation scripts) are now available from **any project**:

```powershell
# Better Auth with OAuth
cd C:\Projects\user-portal
vibe --task "Add Google OAuth login" --skills better-auth

# Database optimization
cd C:\Projects\api-backend
vibe --task "Add connection pooling" --skills databases

# Media processing
cd C:\Projects\media-app
vibe --task "Batch resize user uploads" --skills media-processing
```

---

## 🔧 Configuration

### Skills Location

After installation, skills are located at:

**Editable Install:**
```
C:\Users\khoi1\Desktop\Vibecode with Multi Agent\skills\
```

**Standard Install:**
```
C:\Users\<username>\AppData\Local\Programs\Python\Python3X\Lib\site-packages\skills\
```

**Check skills directory:**
```powershell
python -c "import vibecode_studio; print(vibecode_studio.__file__)"
```

### Environment Variables (Optional)

Set custom skills directory:

```powershell
# Windows
$env:VIBECODE_SKILLS_DIR = "C:\Custom\Path\skills"

# Linux/macOS
export VIBECODE_SKILLS_DIR="/custom/path/skills"
```

---

## 📋 What Gets Installed

```
✅ vibecode command (CLI tool)
✅ vibe command (short alias)
✅ 36 premium skills
   ├── 165+ reference documentation files
   ├── 26 automation scripts
   └── All SKILL.md files
✅ Core orchestration system
✅ Multi-agent framework
✅ Intelligent skill loader
```

---

## 🆕 Updating Vibecode Studio

### Editable Install (Recommended)

```powershell
cd Vibecode-with-Multi-Agent
git pull origin main
# Immediately available - no reinstall needed!
```

### Standard Install

```powershell
cd Vibecode-with-Multi-Agent
git pull origin main
pip install --upgrade .
```

### Direct from GitHub

```powershell
pip install --upgrade --force-reinstall git+https://github.com/khoi1009/Vibecode-with-Multi-Agent.git
```

---

## 🚨 Troubleshooting

### Command Not Found

If `vibecode` or `vibe` not recognized:

**Windows:**
```powershell
# Check Python Scripts directory is in PATH
$env:PATH -split ";" | Select-String "Python.*Scripts"

# If missing, add to PATH:
[Environment]::SetEnvironmentVariable(
    "Path",
    $env:Path + ";C:\Users\<username>\AppData\Local\Programs\Python\Python3X\Scripts",
    [EnvironmentVariableTarget]::User
)
```

**Linux/macOS:**
```bash
# Check pip install location
pip show vibecode-studio

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Import Errors

```powershell
# Reinstall in editable mode
pip uninstall vibecode-studio
pip install -e .
```

### Skills Not Loading

```powershell
# Verify skills directory exists
python -c "from pathlib import Path; print((Path(__file__).parent / 'skills').exists())"

# Check skills are packaged
pip show -f vibecode-studio | Select-String "skills"
```

### Permission Issues (Windows)

```powershell
# Run PowerShell as Administrator
pip install -e . --user
```

### Permission Issues (Linux/macOS)

```bash
# Install for current user only
pip install -e . --user

# Or use sudo (not recommended)
sudo pip install -e .
```

---

## 🎉 Success!

After installation, you can:

✅ Run `vibecode` or `vibe` from **any directory**  
✅ Access all 36 premium skills globally  
✅ Use 165+ reference docs across all projects  
✅ Leverage 26 automation scripts anywhere  
✅ Switch between projects seamlessly  

**Example workflow:**

```powershell
# Morning: Work on e-commerce site
cd C:\Projects\ecommerce
vibe --task "Add Stripe payment" --skills payment-integration

# Afternoon: Work on blog platform
cd C:\Projects\blog
vibe --task "Add markdown editor" --skills frontend-design

# Evening: Work on API backend
cd C:\Projects\api
vibe --task "Add rate limiting" --skills backend-development

# All with the same globally installed Vibecode Studio! 🚀
```

---

## 🔗 Next Steps

- [Quick Start Guide](QUICKSTART_CLI.md) - Learn basic commands
- [Complete Documentation](DOCUMENTATION_INDEX.md) - Full reference
- [Skills Overview](skills/README.md) - See all 36 skills

---

## 💡 Tips

**Use Editable Install for Development:**
```powershell
pip install -e .
```
- Get updates instantly with `git pull`
- Modify skills and see changes immediately
- Best for active users

**Create Virtual Environment (Optional):**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -e .
```
- Isolated installation
- No conflicts with other packages

**Share with Team:**
```powershell
# Each team member installs once
git clone https://github.com/khoi1009/Vibecode-with-Multi-Agent.git
cd Vibecode-with-Multi-Agent
pip install -e .

# Everyone has access to same skills across all projects!
```

---

## 📞 Support

Issues? Check:
1. [GitHub Issues](https://github.com/khoi1009/Vibecode-with-Multi-Agent/issues)
2. [Documentation Index](DOCUMENTATION_INDEX.md)
3. [Quick Start Guide](QUICKSTART_CLI.md)

**Repository:** https://github.com/khoi1009/Vibecode-with-Multi-Agent
