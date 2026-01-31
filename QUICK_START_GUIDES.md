# QuickBackup - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to backup Memory Core and session data

### Step 1: Installation Check

```bash
# Navigate to QuickBackup
cd C:\Users\logan\OneDrive\Documents\AutoProjects\QuickBackup

# Verify QuickBackup is available
python quickbackup.py --help
```

**Expected:** Help message with available commands

### Step 2: Create Memory Core Backup Profile

```bash
# Create backup profile for Memory Core
python quickbackup.py create memory-core "D:\BEACON_HQ\MEMORY_CORE_V2" --dest "D:\Backup\BEACON"
```

**Expected Output:**

```
[OK] Profile 'memory-core' created
     Sources: 1 folder(s)
     Destination: D:\Backup\BEACON
```

### Step 3: First Backup - Protect the Memory Core!

```bash
# Run full backup (first time)
python quickbackup.py backup memory-core --no-incremental
```

**Expected Output:**

```
[BACKUP] Starting backup 'memory-core'
...
[OK] Backup complete!
Files backed up: XXX
Total size: XX MB
```

### Step 4: Daily Incremental Backup

```bash
# Run incremental backup (only changed files)
python quickbackup.py backup memory-core
```

### Forge Workflow Integration

**Session Start Routine:**

```python
# Add to your session start
from pathlib import Path
import sys
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects/QuickBackup"))

from quickbackup import QuickBackup

def forge_session_start():
    """Forge session start routine - backup Memory Core."""
    backup = QuickBackup()
    
    print("[FORGE] Checking Memory Core backup...")
    result = backup.backup("memory-core")
    
    if result:
        print("[FORGE] Memory Core backup complete")
    else:
        print("[FORGE] WARNING: Memory Core backup failed!")
    
    return result
```

### Forge-Specific Profiles

```bash
# Synapse backup (communications)
python quickbackup.py create synapse "D:\BEACON_HQ\MEMORY_CORE_V2\03_INTER_AI_COMMS" --dest "D:\Backup\BEACON"

# AutoProjects backup (all tools)
python quickbackup.py create autotools "C:\Users\logan\OneDrive\Documents\AutoProjects" --dest "D:\Backup\BEACON"

# Full Beacon HQ backup
python quickbackup.py create beacon-full "D:\BEACON_HQ" --dest "D:\Backup\BEACON"
```

### Next Steps for Forge

1. Run `backup memory-core` at the start of each session
2. Create full backup before major system changes
3. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for team coordination
4. Set up SynapseLink notifications for backup status

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to backup before building tools

### Step 1: Installation Check

```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\QuickBackup
python quickbackup.py --help
```

### Step 2: Create Tool Backup Profile

```bash
# Create backup profile for AutoProjects
python quickbackup.py create tool-builds "C:\Users\logan\OneDrive\Documents\AutoProjects" --dest "D:\Backup\Atlas"
```

### Step 3: Pre-Build Backup Workflow

**Before starting any tool build:**

```bash
# Full backup before risky changes
python quickbackup.py backup tool-builds --no-incremental
```

**After successful build:**

```bash
# Incremental backup to capture new work
python quickbackup.py backup tool-builds
```

### Atlas Build Integration

```python
from quickbackup import QuickBackup

backup = QuickBackup()

def atlas_pre_build(tool_name):
    """Create backup before building a tool."""
    print(f"[ATLAS] Pre-build backup for {tool_name}")
    return backup.backup("tool-builds", incremental=False)

def atlas_post_build(tool_name):
    """Incremental backup after successful build."""
    print(f"[ATLAS] Post-build backup for {tool_name}")
    return backup.backup("tool-builds", incremental=True)

# Usage during tool build
if atlas_pre_build("NewTool"):
    # ... build the tool ...
    if build_successful:
        atlas_post_build("NewTool")
```

### Atlas-Specific Profiles

```bash
# Current project backup
python quickbackup.py create current-project "." --dest "../_project_backups"

# Specific tool backup
python quickbackup.py create quickbackup-dev "C:\...\AutoProjects\QuickBackup" --dest "D:\Backup\Atlas"
```

### Next Steps for Atlas

1. Create pre-build backup before every tool build
2. Add backup to Holy Grail Protocol checklist
3. Read [EXAMPLES.md](EXAMPLES.md) for more patterns
4. Integrate with SessionReplay for tracking

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to backup Linux configurations and dotfiles

### Step 1: Linux Installation

```bash
# Clone from GitHub (if not already present)
git clone https://github.com/DonkRonk17/QuickBackup.git
cd QuickBackup

# Verify installation
python3 quickbackup.py --help
```

### Step 2: Create Linux Config Profile

```bash
# Backup dotfiles and configs
python3 quickbackup.py create linux-config \
    ~/.bashrc \
    ~/.zshrc \
    ~/.gitconfig \
    ~/.config \
    --dest /backup/linux
```

### Step 3: First Backup

```bash
# Run backup
python3 quickbackup.py backup linux-config
```

### Clio Workflow Integration

**Session Start Script:**

```bash
#!/bin/bash
# clio_startup.sh

echo "[CLIO] Starting session..."

# Backup configs before work
python3 ~/QuickBackup/quickbackup.py backup linux-config

echo "[CLIO] Config backup complete"
```

### Clio-Specific Profiles

```bash
# Dotfiles only
python3 quickbackup.py create dotfiles ~/.bashrc ~/.zshrc ~/.gitconfig --dest /backup/dotfiles

# SSH keys (important!)
python3 quickbackup.py create ssh-keys ~/.ssh --dest /backup/secure

# Development configs
python3 quickbackup.py create dev-configs ~/.config/Code ~/.config/cursor --dest /backup/dev

# System configs (may need sudo for some)
python3 quickbackup.py create system-backup /etc/nginx /etc/apache2 --dest /backup/system
```

### Platform-Specific Notes

- Use `python3` instead of `python`
- Paths use forward slashes: `/home/user/`
- Create backup destination: `mkdir -p /backup/linux`
- Some system configs may require elevated permissions

### Next Steps for Clio

1. Create daily cron job for automatic backups
2. Test SSH key backup/restore procedure
3. Read [CHEAT_SHEET.txt](CHEAT_SHEET.txt) for CLI reference
4. Set up ABIOS integration for startup backups

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform backup usage

### Step 1: Platform Detection

```python
import platform
print(f"Running on: {platform.system()}")
# Expected: Windows, Linux, or Darwin (macOS)
```

### Step 2: Cross-Platform Profile Setup

```python
from pathlib import Path
import sys

# Add QuickBackup to path (adjust for platform)
if platform.system() == "Windows":
    sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects/QuickBackup"))
else:
    sys.path.append(str(Path.home() / "AutoProjects/QuickBackup"))

from quickbackup import QuickBackup

backup = QuickBackup()

# Create platform-appropriate profile
if platform.system() == "Windows":
    backup.create_profile("cross-platform",
        [str(Path.home() / "Documents")],
        str(Path("D:/Backup"))
    )
elif platform.system() == "Linux":
    backup.create_profile("cross-platform",
        [str(Path.home() / "Documents")],
        str(Path("/backup"))
    )
elif platform.system() == "Darwin":  # macOS
    backup.create_profile("cross-platform",
        [str(Path.home() / "Documents")],
        str(Path("/Volumes/Backup"))
    )
```

### Step 3: Run Cross-Platform Backup

```python
# Works on any platform
backup.backup("cross-platform")
```

### Platform-Specific Commands

**Windows:**

```bash
python quickbackup.py backup cross-platform --dest D:\Backup
```

**Linux:**

```bash
python3 quickbackup.py backup cross-platform --dest /backup
```

**macOS:**

```bash
python3 quickbackup.py backup cross-platform --dest /Volumes/Backup
```

### Cross-Platform Validation

```python
def validate_backup_cross_platform():
    """Test backup works on current platform."""
    backup = QuickBackup()
    
    # Create test profile
    test_source = Path.home() / "test_backup_source"
    test_dest = Path.home() / "test_backup_dest"
    
    test_source.mkdir(exist_ok=True)
    test_dest.mkdir(exist_ok=True)
    (test_source / "test.txt").write_text("test content")
    
    # Create and run backup
    backup.create_profile("cross-platform-test", 
        [str(test_source)], 
        str(test_dest)
    )
    
    result = backup.backup("cross-platform-test")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_source)
    
    print(f"Cross-platform test: {'PASS' if result else 'FAIL'}")
    return result
```

### Next Steps for Nexus

1. Test on all three platforms (Windows, Linux, macOS)
2. Verify ZIP files can be opened cross-platform
3. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for platform-specific notes
4. Report any platform-specific issues

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to automate batch backups

### Step 1: Verify Free Access

```bash
# No API key required!
cd C:\Users\logan\OneDrive\Documents\AutoProjects\QuickBackup
python quickbackup.py --help
```

### Step 2: Create Batch Backup Script

**batch_backup.py:**

```python
#!/usr/bin/env python3
"""Batch backup script for Bolt executor."""

from quickbackup import QuickBackup
from datetime import datetime

def run_all_backups():
    """Run backups for all configured profiles."""
    backup = QuickBackup()
    
    profiles = ["daily-docs", "projects", "configs", "memory-core"]
    results = {}
    
    print(f"[BOLT] Starting batch backup at {datetime.now()}")
    
    for profile in profiles:
        print(f"\n[BOLT] Backing up: {profile}")
        try:
            result = backup.backup(profile)
            results[profile] = "SUCCESS" if result else "FAILED"
        except Exception as e:
            results[profile] = f"ERROR: {e}"
    
    print("\n" + "="*50)
    print("[BOLT] Batch Backup Summary")
    print("="*50)
    for profile, status in results.items():
        print(f"  {profile}: {status}")
    
    return results

if __name__ == "__main__":
    run_all_backups()
```

### Step 3: Schedule Automation

**Windows Task Scheduler:**

```powershell
$action = New-ScheduledTaskAction -Execute "python" `
    -Argument "C:\...\QuickBackup\batch_backup.py"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "BoltDailyBackup" -Action $action -Trigger $trigger
```

**Linux Cron:**

```bash
crontab -e
# Add: 0 9 * * * python3 /path/to/batch_backup.py >> /var/log/backup.log 2>&1
```

### Bolt Batch Operations

```bash
# Backup multiple profiles in sequence
python quickbackup.py backup daily-docs
python quickbackup.py backup projects
python quickbackup.py backup configs

# Or use the batch script
python batch_backup.py
```

### Cost Considerations

- QuickBackup has **ZERO API costs** (local tool)
- Batch operations are **FREE**
- Automation saves time without cost increase
- No rate limits or quotas

### Next Steps for Bolt

1. Create batch backup script for all important profiles
2. Set up scheduled task for daily backups
3. Test backup restoration procedure
4. Report any issues via Synapse

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/QuickBackup/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message ATLAS (builder)

---

## 🎯 COMMON COMMANDS SUMMARY

| Task | Command |
|------|---------|
| Create profile | `python quickbackup.py create NAME SOURCE --dest DEST` |
| Run backup | `python quickbackup.py backup NAME` |
| Full backup | `python quickbackup.py backup NAME --no-incremental` |
| List profiles | `python quickbackup.py list` |
| Show profile | `python quickbackup.py show NAME` |
| Delete profile | `python quickbackup.py delete NAME` |

---

**Last Updated:** January 30, 2026  
**Maintained By:** ATLAS (Team Brain)  
**For:** Logan Smith / Metaphy LLC
