# 💾 QuickBackup - Usage Examples

A comprehensive collection of real-world examples for QuickBackup.

## Quick Navigation

- [Example 1: Basic Profile Setup](#example-1-basic-profile-setup)
- [Example 2: First Backup](#example-2-first-backup)
- [Example 3: Multiple Source Folders](#example-3-multiple-source-folders)
- [Example 4: Incremental Backup Workflow](#example-4-incremental-backup-workflow)
- [Example 5: Full Backup (Non-Incremental)](#example-5-full-backup-non-incremental)
- [Example 6: Backup Without Compression](#example-6-backup-without-compression)
- [Example 7: Override Destination](#example-7-override-destination)
- [Example 8: Managing Multiple Profiles](#example-8-managing-multiple-profiles)
- [Example 9: Scheduled Backup Automation](#example-9-scheduled-backup-automation)
- [Example 10: Team Brain Integration](#example-10-team-brain-integration)
- [Example 11: Disaster Recovery Workflow](#example-11-disaster-recovery-workflow)
- [Example 12: Pre-Migration Backup](#example-12-pre-migration-backup)

---

## Example 1: Basic Profile Setup

**Scenario:** You want to set up a backup profile for your Documents folder.

**Steps:**

```bash
# Create a backup profile for Documents
python quickbackup.py create documents ~/Documents --dest /backup/drive
```

**Expected Output:**

```
[OK] Profile 'documents' created
     Sources: 1 folder(s)
     Destination: /backup/drive
```

**Verify the profile:**

```bash
python quickbackup.py show documents
```

**Expected Output:**

```
============================================================
Profile: documents
============================================================

Created: 2026-01-30T10:00:00
Last Backup: Never

Sources (1):
  [✓] /home/user/Documents

Destination:
  [✓] /backup/drive

============================================================
```

**What You Learned:**
- How to create a backup profile
- Profile stores source and destination paths
- Use `show` to verify profile configuration

---

## Example 2: First Backup

**Scenario:** Run your first backup after creating a profile.

**Steps:**

```bash
# Run backup for the documents profile
python quickbackup.py backup documents
```

**Expected Output:**

```
[BACKUP] Starting backup 'documents'
Destination: /backup/drive/documents_20260130_100500
Incremental: Yes
Compress: Yes

Backing up: /home/user/Documents

Compressing backup...
[OK] Compressed: 45.6 MB (68.2% reduction)

============================================================
[OK] Backup complete!
Files backed up: 1,247
Total size: 143.2 MB
============================================================
```

**Result:**
- A timestamped ZIP file: `documents_20260130_100500.zip`
- File saved to `/backup/drive/`

**What You Learned:**
- Backups are automatically timestamped
- Compression saves significant space
- Incremental mode is enabled by default

---

## Example 3: Multiple Source Folders

**Scenario:** Backup multiple important folders in one profile.

**Steps:**

```bash
# Create profile with multiple sources
python quickbackup.py create full-backup \
    ~/Documents \
    ~/Pictures \
    ~/Projects \
    ~/Desktop \
    --dest /external/backup
```

**Expected Output:**

```
[OK] Profile 'full-backup' created
     Sources: 4 folder(s)
     Destination: /external/backup
```

**Run the backup:**

```bash
python quickbackup.py backup full-backup
```

**Expected Output:**

```
[BACKUP] Starting backup 'full-backup'
Destination: /external/backup/full-backup_20260130_103000
Incremental: Yes
Compress: Yes

Backing up: /home/user/Documents
Backing up: /home/user/Pictures
Backing up: /home/user/Projects
Backing up: /home/user/Desktop

Compressing backup...
[OK] Compressed: 2.3 GB (54.1% reduction)

============================================================
[OK] Backup complete!
Files backed up: 15,847
Total size: 5.0 GB
============================================================
```

**What You Learned:**
- One profile can backup multiple source folders
- All sources are combined into one backup archive
- Great for comprehensive backups

---

## Example 4: Incremental Backup Workflow

**Scenario:** Efficiently backup only changed files over multiple days.

**Day 1 - Initial Backup:**

```bash
python quickbackup.py backup documents
```

**Output (Day 1):**

```
[BACKUP] Starting backup 'documents'
...
============================================================
[OK] Backup complete!
Files backed up: 1,247
Total size: 143.2 MB
============================================================
```

**Day 2 - Only 5 files changed:**

```bash
python quickbackup.py backup documents
```

**Output (Day 2):**

```
[BACKUP] Starting backup 'documents'
...
============================================================
[OK] Backup complete!
Files backed up: 5
Files skipped (unchanged): 1,242
Total size: 85.0 KB
============================================================
```

**Benefits:**
- **Day 1:** 143.2 MB → 45.6 MB compressed
- **Day 2:** Only 85 KB (just changed files!)
- **Time saved:** 95%+ faster on subsequent backups

**What You Learned:**
- Incremental backups only process changed files
- MD5 checksums detect file modifications
- Massive time and space savings over time

---

## Example 5: Full Backup (Non-Incremental)

**Scenario:** Force a complete backup of all files, ignoring change detection.

**Steps:**

```bash
# Full backup (all files, regardless of changes)
python quickbackup.py backup documents --no-incremental
```

**Expected Output:**

```
[BACKUP] Starting backup 'documents'
Destination: /backup/drive/documents_20260130_140000
Incremental: No
Compress: Yes

Backing up: /home/user/Documents

Compressing backup...
[OK] Compressed: 45.6 MB (68.2% reduction)

============================================================
[OK] Backup complete!
Files backed up: 1,247
Total size: 143.2 MB
============================================================
```

**When to Use:**
- Before major system changes
- Creating archival snapshots
- When you want a complete backup regardless of checksums

**What You Learned:**
- `--no-incremental` forces full backup
- Useful for milestone backups or archives

---

## Example 6: Backup Without Compression

**Scenario:** Backup already-compressed files (like photos/videos) without extra compression.

**Steps:**

```bash
# Create photo backup profile
python quickbackup.py create photos ~/Pictures --dest /external/drive

# Backup without compression (faster for media files)
python quickbackup.py backup photos --no-compress
```

**Expected Output:**

```
[BACKUP] Starting backup 'photos'
Destination: /external/drive/photos_20260130_150000
Incremental: Yes
Compress: No

Backing up: /home/user/Pictures

============================================================
[OK] Backup complete!
Files backed up: 3,456
Total size: 8.7 GB
============================================================
```

**Result:**
- A folder `photos_20260130_150000/` with all files (not zipped)
- Faster backup for already-compressed content

**What You Learned:**
- `--no-compress` skips ZIP compression
- Better for JPEG, PNG, MP4, ZIP files
- Results in a folder instead of ZIP file

---

## Example 7: Override Destination

**Scenario:** Temporarily backup to a different location than the profile default.

**Steps:**

```bash
# Profile has default destination set
python quickbackup.py show documents

# Override for this backup only
python quickbackup.py backup documents --dest /usb-drive/emergency-backup
```

**Expected Output:**

```
[BACKUP] Starting backup 'documents'
Destination: /usb-drive/emergency-backup/documents_20260130_160000
Incremental: Yes
Compress: Yes

...

============================================================
[OK] Backup complete!
Files backed up: 1,247
Total size: 143.2 MB
============================================================
```

**What You Learned:**
- `--dest` overrides profile destination
- Useful for one-time backups to different drives
- Profile's default destination remains unchanged

---

## Example 8: Managing Multiple Profiles

**Scenario:** Set up and manage multiple backup profiles for different purposes.

**Create multiple profiles:**

```bash
# Daily documents
python quickbackup.py create daily-docs ~/Documents --dest /backup/daily

# Weekly full backup
python quickbackup.py create weekly-full ~/Documents ~/Pictures ~/Projects --dest /backup/weekly

# Project-specific
python quickbackup.py create my-project ~/Projects/MyProject --dest /backup/projects
```

**List all profiles:**

```bash
python quickbackup.py list
```

**Expected Output:**

```
[3 profile(s)]

* daily-docs
  Sources: 1 folder(s)
  Last backup: 2026-01-30T09:00:00

* my-project
  Sources: 1 folder(s)
  Last backup: Never

* weekly-full
  Sources: 3 folder(s)
  Last backup: 2026-01-28T18:00:00
```

**Delete an old profile:**

```bash
python quickbackup.py delete my-project
```

**Expected Output:**

```
[OK] Profile 'my-project' deleted
```

**What You Learned:**
- Create multiple profiles for different backup strategies
- `list` shows all profiles with status
- `delete` removes profiles you no longer need

---

## Example 9: Scheduled Backup Automation

**Scenario:** Set up automated daily backups.

### Windows Task Scheduler

**Create a batch file `daily_backup.bat`:**

```batch
@echo off
cd C:\Users\logan\OneDrive\Documents\AutoProjects\QuickBackup
python quickbackup.py backup daily-docs
python quickbackup.py backup projects
```

**PowerShell command to schedule:**

```powershell
$action = New-ScheduledTaskAction -Execute "cmd.exe" `
    -Argument "/c C:\Backups\daily_backup.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "DailyBackup" -Action $action -Trigger $trigger
```

### Linux/macOS Cron

**Edit crontab:**

```bash
crontab -e
```

**Add entry for 9 AM daily:**

```cron
0 9 * * * /usr/bin/python3 /path/to/quickbackup.py backup daily-docs >> /var/log/backup.log 2>&1
```

### Python Script Wrapper

```python
#!/usr/bin/env python3
"""Automated backup script for Team Brain."""

import subprocess
from datetime import datetime

profiles = ["daily-docs", "projects", "configs"]

for profile in profiles:
    print(f"[{datetime.now()}] Backing up {profile}...")
    subprocess.run(["python", "quickbackup.py", "backup", profile])

print("All backups complete!")
```

**What You Learned:**
- Automate backups with OS schedulers
- Run multiple profile backups in sequence
- Log backup results for monitoring

---

## Example 10: Team Brain Integration

**Scenario:** Integrate QuickBackup with Team Brain tools for coordinated backups.

### With SynapseLink (Notification)

```python
from pathlib import Path
import sys
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects/QuickBackup"))
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects/SynapseLink"))

from quickbackup import QuickBackup
from synapselink import quick_send

# Initialize backup
backup = QuickBackup()

# Run backup
result = backup.backup("daily-docs")

# Notify team
if result:
    quick_send(
        "TEAM",
        "Backup Complete: daily-docs",
        f"Backup completed successfully at {datetime.now()}",
        priority="NORMAL"
    )
else:
    quick_send(
        "FORGE,LOGAN",
        "Backup FAILED: daily-docs",
        "Backup failed - please investigate!",
        priority="HIGH"
    )
```

### With SessionReplay (Tracking)

```python
from quickbackup import QuickBackup
from sessionreplay import SessionReplay

replay = SessionReplay()
backup = QuickBackup()

# Start session
session_id = replay.start_session("ATLAS", task="System backup")
replay.log_input(session_id, "Starting daily backup routine")

# Run backups
profiles = ["docs", "projects", "configs"]
for profile in profiles:
    replay.log_input(session_id, f"Backing up {profile}")
    result = backup.backup(profile)
    replay.log_output(session_id, f"Backup {profile}: {'SUCCESS' if result else 'FAILED'}")

# End session
replay.end_session(session_id, status="COMPLETED")
```

### With TaskQueuePro (Task Management)

```python
from quickbackup import QuickBackup
from taskqueuepro import TaskQueuePro

queue = TaskQueuePro()
backup = QuickBackup()

# Create backup task
task_id = queue.create_task(
    title="Daily system backup",
    agent="ATLAS",
    priority=2,
    metadata={"backup_profile": "daily-docs"}
)

# Execute
queue.start_task(task_id)
result = backup.backup("daily-docs")

# Complete task
if result:
    queue.complete_task(task_id, result={"status": "success"})
else:
    queue.fail_task(task_id, error="Backup failed")
```

**What You Learned:**
- Integrate QuickBackup with Team Brain ecosystem
- Send notifications on backup completion
- Track backups in task management system

---

## Example 11: Disaster Recovery Workflow

**Scenario:** Prepare for and recover from system disasters.

### Pre-Disaster: Create Comprehensive Backups

```bash
# Create a disaster recovery profile
python quickbackup.py create disaster-recovery \
    ~/Documents \
    ~/Pictures \
    ~/Projects \
    ~/Desktop \
    ~/.config \
    --dest /external/disaster-recovery

# Run full backup before travel/risky changes
python quickbackup.py backup disaster-recovery --no-incremental
```

### Post-Disaster: Recovery Steps

**1. List available backups:**

```bash
ls -la /external/disaster-recovery/
```

**Output:**

```
disaster-recovery_20260125_180000.zip  # Before trip
disaster-recovery_20260120_090000.zip  # Weekly backup
disaster-recovery_20260115_090000.zip  # 2 weeks ago
```

**2. Extract recovery backup:**

```bash
# Extract to recovery location
unzip disaster-recovery_20260125_180000.zip -d ~/recovery/
```

**3. Restore files:**

```bash
# Copy back to original locations
cp -r ~/recovery/Documents/* ~/Documents/
cp -r ~/recovery/Pictures/* ~/Pictures/
# etc.
```

### Best Practices:

```bash
# Before risky changes
python quickbackup.py backup disaster-recovery --no-incremental

# Regular backups (incremental)
python quickbackup.py backup disaster-recovery

# Verify backup exists
python quickbackup.py show disaster-recovery
```

**What You Learned:**
- Create comprehensive disaster recovery profiles
- Use `--no-incremental` for complete snapshots before risks
- Recovery is simple: extract ZIP and copy files back

---

## Example 12: Pre-Migration Backup

**Scenario:** Backup everything before migrating to a new computer or OS.

### Step 1: Create Migration Profile

```bash
python quickbackup.py create migration \
    ~/Documents \
    ~/Pictures \
    ~/Music \
    ~/Videos \
    ~/Projects \
    ~/Desktop \
    ~/.config \
    ~/.ssh \
    --dest /external/migration
```

### Step 2: Full Backup

```bash
# Complete backup of everything
python quickbackup.py backup migration --no-incremental
```

**Expected Output:**

```
[BACKUP] Starting backup 'migration'
Destination: /external/migration/migration_20260130_180000
Incremental: No
Compress: Yes

Backing up: /home/user/Documents
Backing up: /home/user/Pictures
Backing up: /home/user/Music
Backing up: /home/user/Videos
Backing up: /home/user/Projects
Backing up: /home/user/Desktop
Backing up: /home/user/.config
Backing up: /home/user/.ssh

Compressing backup...
[OK] Compressed: 45.2 GB (38.5% reduction)

============================================================
[OK] Backup complete!
Files backed up: 125,847
Total size: 73.5 GB
============================================================
```

### Step 3: Verify

```bash
# Verify backup was created
ls -la /external/migration/

# Check the profile shows last backup
python quickbackup.py show migration
```

### Step 4: On New System

```bash
# Copy backup to new system
# Extract and restore

unzip migration_20260130_180000.zip -d ~/migrated-files/
```

**What You Learned:**
- Create comprehensive migration backups
- Include hidden config directories (`.config`, `.ssh`)
- Full backup ensures nothing is missed
- Migration profile can be reused for future migrations

---

## Tips & Best Practices

### Naming Conventions

```bash
# Good profile names
daily-docs          # Clear purpose
project-xyz         # Specific project
weekly-full         # Backup frequency
pre-travel          # Situational

# Avoid
backup1             # Unclear
test                # Will be forgotten
asdf                # Meaningless
```

### Backup Strategy Recommendations

| Profile | Frequency | Mode | When |
|---------|-----------|------|------|
| `daily-docs` | Daily | Incremental | Morning |
| `weekly-full` | Weekly | Full | Weekend |
| `pre-travel` | As needed | Full | Before trips |
| `project-X` | Per session | Incremental | After work |

### Storage Recommendations

```bash
# Local SSD (fast access)
--dest /backup/local/

# External HDD (large capacity)
--dest /media/external/

# Network share (offsite)
--dest /mnt/nas/backups/
```

---

## Troubleshooting Examples

### Profile Not Found

```bash
$ python quickbackup.py backup missing-profile
[X] Profile 'missing-profile' not found!

# Solution: List available profiles
$ python quickbackup.py list
```

### Destination Not Accessible

```bash
$ python quickbackup.py backup documents
[X] Destination does not exist: /disconnected/drive

# Solution: Mount the drive or override destination
$ python quickbackup.py backup documents --dest /available/path
```

### Source Folder Removed

```bash
$ python quickbackup.py backup old-project
[!] Skipping non-existent source: /home/user/OldProject
...
[OK] Backup complete!
Files backed up: 0

# Solution: Update or delete the profile
$ python quickbackup.py delete old-project
```

---

## Summary

| Example | Key Feature | Command |
|---------|-------------|---------|
| Basic Setup | Create profile | `create NAME SOURCE --dest DEST` |
| First Backup | Run backup | `backup NAME` |
| Multi-Source | Multiple folders | `create NAME SRC1 SRC2 SRC3` |
| Incremental | Changed files only | `backup NAME` (default) |
| Full Backup | All files | `backup NAME --no-incremental` |
| No Compression | Media files | `backup NAME --no-compress` |
| Override Dest | Temp destination | `backup NAME --dest PATH` |
| List Profiles | View all | `list` |
| Show Details | Inspect profile | `show NAME` |
| Delete Profile | Remove profile | `delete NAME` |

---

**Built with ❤️ by ATLAS (Team Brain)**  
**For: Logan Smith / Metaphy LLC**
