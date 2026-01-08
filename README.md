# 💾 QuickBackup - Simple, Fast Backup Automation

**Never lose your important files again!** QuickBackup makes backing up your data as simple as one command - with incremental backups, compression, and easy restoration.

Perfect for:
- 📁 Protecting important documents
- 📸 Backing up photo collections
- 💻 Safeguarding project files
- 📝 Regular automated backups
- 🔄 Incremental backup strategies

---

## ✨ Features

- **⚡ One-Command Backup** - Create backups with a single command
- **📊 Backup Profiles** - Save configurations for repeated use
- **🔄 Incremental Backups** - Only backup changed files (smart & fast!)
- **📦 Automatic Compression** - Save space with ZIP compression
- **🎯 Multiple Sources** - Backup multiple folders at once
- **📅 Timestamped Backups** - Each backup has a unique timestamp
- **🔍 Change Detection** - MD5 checksums detect file changes
- **💾 No External Dependencies** - Uses only Python standard library
- **🌍 Cross-Platform** - Works on Windows, macOS, Linux

---

## 📥 Installation

### Requirements

- Python 3.7+
- No external dependencies!

### Step 1: Download QuickBackup

```bash
# Clone the repository
git clone https://github.com/DonkRonk17/QuickBackup.git
cd QuickBackup

# Or download ZIP and extract
```

### Step 2: Make it Executable (Optional)

#### Windows:
```bash
# Add to PATH or create alias
doskey quickbackup=python "%CD%\quickbackup.py" $*
```

#### macOS/Linux:
```bash
# Make executable
chmod +x quickbackup.py

# Create symlink (optional)
sudo ln -s $(pwd)/quickbackup.py /usr/local/bin/quickbackup
```

---

## 🚀 Quick Start

### 1. Create a Backup Profile

```bash
python quickbackup.py create work ~/Documents ~/Projects --dest /backup/drive
```

This creates a profile named "work" that backs up your Documents and Projects folders to your backup drive.

### 2. Run Your First Backup

```bash
python quickbackup.py backup work
```

That's it! Your files are now safely backed up with compression and incremental tracking.

### 3. List Your Profiles

```bash
python quickbackup.py list
```

---

## 📖 Complete Usage Guide

### Creating Profiles

```bash
# Backup documents
python quickbackup.py create documents ~/Documents --dest /backup/drive

# Backup photos
python quickbackup.py create photos ~/Pictures ~/Photos --dest /external/hdd

# Backup projects (multiple sources)
python quickbackup.py create projects ~/Projects ~/Code ~/Work --dest D:\Backup
```

**Tip:** You can backup multiple folders in one profile!

### Running Backups

```bash
# Standard backup (incremental + compression)
python quickbackup.py backup work

# Force full backup (all files, not just changed)
python quickbackup.py backup work --no-incremental

# Backup without compression (faster for large files)
python quickbackup.py backup work --no-compress

# Override destination temporarily
python quickbackup.py backup work --dest /different/location
```

### Managing Profiles

```bash
# List all profiles
python quickbackup.py list

# Show profile details
python quickbackup.py show work

# Delete a profile
python quickbackup.py delete old_backup
```

---

## 💡 Usage Examples

### Example 1: Daily Document Backup

```bash
# Create profile
python quickbackup.py create daily-docs ~/Documents ~/Desktop --dest /backup

# Run every morning
python quickbackup.py backup daily-docs
```

**What happens:**
- First run: Backs up all files (e.g., 2GB → 500MB compressed)
- Next runs: Only backs up changed files (much faster!)
- Each backup is timestamped: `daily-docs_20260108_093000.zip`

### Example 2: Photo Collection Backup

```bash
# Create photo backup profile
python quickbackup.py create photos ~/Pictures --dest /external/drive

# Backup when camera card is full
python quickbackup.py backup photos
```

### Example 3: Project Backup Before Major Changes

```bash
# Create project snapshot
python quickbackup.py create project-snapshot ~/MyProject --dest /backup

# Before risky refactoring
python quickbackup.py backup project-snapshot --no-incremental
```

### Example 4: Multiple Source Backup

```bash
# Backup everything important
python quickbackup.py create full-backup \
  ~/Documents \
  ~/Pictures \
  ~/Projects \
  ~/Desktop \
  --dest /external/2tb-drive

# Run weekly
python quickbackup.py backup full-backup
```

---

## 🔄 How Incremental Backups Work

QuickBackup uses **MD5 checksums** to detect file changes:

1. **First Backup:**
   - All files copied
   - Checksums calculated and stored
   - Result: `work_20260108_100000.zip`

2. **Second Backup (3 days later):**
   - Only files with changed checksums are backed up
   - Much faster and smaller
   - Result: `work_20260111_100000.zip` (only changed files)

**Benefits:**
- ⚡ 10x faster for unchanged files
- 💾 Saves disk space
- 🎯 Focuses on what actually changed

**Disable if needed:**
```bash
python quickbackup.py backup work --no-incremental
```

---

## 📦 Compression

All backups are automatically compressed to save space:

**Example:**
- Original size: 2.5 GB
- Compressed: 600 MB
- Savings: 76% reduction!

**Disable compression (for already-compressed files):**
```bash
python quickbackup.py backup photos --no-compress
```

---

## 📂 File Locations

QuickBackup stores configuration in your home directory:

```
~/.quickbackup/
├── config.json           # Global configuration
├── checksums.json        # File checksums for incremental backups
└── profiles/             # Backup profiles
    ├── work.json
    ├── photos.json
    └── projects.json
```

**Backup files go to your specified destination:**
```
/backup/drive/
├── work_20260108_093000.zip
├── work_20260109_093000.zip
├── photos_20260108_120000.zip
└── ...
```

---

## ⚙️ Command Reference

### Create Profile
```bash
quickbackup.py create <name> <sources...> [--dest <destination>]
```

### Run Backup
```bash
quickbackup.py backup <name> [--dest <dest>] [--no-incremental] [--no-compress]
```

### List Profiles
```bash
quickbackup.py list
```

### Show Profile Details
```bash
quickbackup.py show <name>
```

### Delete Profile
```bash
quickbackup.py delete <name>
```

---

## 🎯 Pro Tips

### Tip 1: Scheduled Backups

**Windows (Task Scheduler):**
```powershell
$action = New-ScheduledTaskAction -Execute "python" `
    -Argument "C:\path\to\quickbackup.py backup daily-docs"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "DailyBackup" -Action $action -Trigger $trigger
```

**Linux/Mac (Cron):**
```bash
# Run daily at 9am
crontab -e
0 9 * * * python /path/to/quickbackup.py backup daily-docs
```

### Tip 2: Pre-Travel Backup Script

```bash
#!/bin/bash
# travel-backup.sh
python quickbackup.py backup documents --no-incremental
python quickbackup.py backup photos --no-incremental
python quickbackup.py backup projects --no-incremental
echo "Travel backups complete!"
```

### Tip 3: Test Your Backups

```bash
# Show what would be backed up
python quickbackup.py show work

# Verify destination is accessible
python quickbackup.py backup work --dest /test/location
```

### Tip 4: Backup to Multiple Destinations

```bash
# Primary backup
python quickbackup.py backup work --dest /backup/primary

# Redundant backup
python quickbackup.py backup work --dest /backup/secondary --no-incremental
```

---

## 🐛 Troubleshooting

### "Destination does not exist"
**Solution:** Create the destination folder first:
```bash
mkdir -p /backup/drive
python quickbackup.py backup work
```

### "Profile not found"
**Solution:** List profiles to see available names:
```bash
python quickbackup.py list
```

### Backup is taking too long
**Solutions:**
1. Use incremental backups (default)
2. Disable compression for already-compressed files:
   ```bash
   python quickbackup.py backup photos --no-compress
   ```
3. Split into smaller profiles

### Out of disk space
**Solutions:**
1. Delete old backups manually
2. Use incremental backups (saves space)
3. Exclude large files/folders

---

## 🔒 Security & Privacy

- ✅ **All data stays local** - No cloud, no network
- ✅ **No telemetry** - Zero tracking
- ✅ **Full control** - You manage everything
- ✅ **Standard ZIP** - Can be opened anywhere
- ✅ **Checksums** - Verify file integrity

**Your backups are 100% under your control.**

---

## 🤝 Contributing

Found a bug? Have a feature idea? Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file

---

## 🌟 Support

If you find QuickBackup useful:
- ⭐ Star this repository
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features
- 📢 Share with friends!

---

## 🎉 Why QuickBackup?

**Compared to other backup tools:**

| Feature | QuickBackup | Cloud Backup | Manual Copy |
|---------|-------------|--------------|-------------|
| **Speed** | ⚡ Fast | 🐌 Slow (upload) | ⚡ Fast |
| **Privacy** | ✅ Local | ❌ Cloud | ✅ Local |
| **Incremental** | ✅ Yes | ✅ Yes | ❌ No |
| **Compression** | ✅ Yes | ⚠️ Sometimes | ❌ No |
| **One Command** | ✅ Yes | ⚠️ App needed | ❌ Manual |
| **Cost** | ✅ Free | 💰 Subscription | ✅ Free |
| **Automation** | ✅ Easy | ✅ Easy | ❌ Manual |

**QuickBackup = Fast + Private + Simple + Free**

---

**Created by Team Brain**  
**Part of the Holy Grail Automation Project**

Protect your data with zero hassle! 💾✨
