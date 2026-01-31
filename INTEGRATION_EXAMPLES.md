# QuickBackup - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

QuickBackup is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: QuickBackup + AgentHealth](#pattern-1-quickbackup--agenthealth)
2. [Pattern 2: QuickBackup + SynapseLink](#pattern-2-quickbackup--synapselink)
3. [Pattern 3: QuickBackup + TaskQueuePro](#pattern-3-quickbackup--taskqueuepro)
4. [Pattern 4: QuickBackup + MemoryBridge](#pattern-4-quickbackup--memorybridge)
5. [Pattern 5: QuickBackup + SessionReplay](#pattern-5-quickbackup--sessionreplay)
6. [Pattern 6: QuickBackup + ContextCompressor](#pattern-6-quickbackup--contextcompressor)
7. [Pattern 7: QuickBackup + ConfigManager](#pattern-7-quickbackup--configmanager)
8. [Pattern 8: QuickBackup + CollabSession](#pattern-8-quickbackup--collabsession)
9. [Pattern 9: Multi-Tool Backup Workflow](#pattern-9-multi-tool-backup-workflow)
10. [Pattern 10: Full Team Brain Backup Stack](#pattern-10-full-team-brain-backup-stack)

---

## Pattern 1: QuickBackup + AgentHealth

**Use Case:** Track backup operations as part of agent health monitoring

**Why:** Understand agent behavior and catch backup failures early

**Code:**

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from AgentHealth.agenthealth import AgentHealth
from QuickBackup.quickbackup import QuickBackup
from datetime import datetime

# Initialize both tools
health = AgentHealth()
backup = QuickBackup()

# Start health session for backup task
session_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
health.start_session("ATLAS", session_id=session_id)

try:
    # Log backup start
    health.heartbeat("ATLAS", status="backup_started")
    
    # Perform backup
    result = backup.backup("daily-docs")
    
    if result:
        # Log success
        health.heartbeat("ATLAS", status="backup_complete")
        print("[OK] Backup completed successfully")
    else:
        # Log failure
        health.log_error("ATLAS", "Backup failed: daily-docs")
        print("[X] Backup failed!")
        
except Exception as e:
    health.log_error("ATLAS", f"Backup exception: {str(e)}")
    raise
    
finally:
    health.end_session("ATLAS", session_id=session_id)
```

**Result:** Backup operations tracked in health monitoring system

---

## Pattern 2: QuickBackup + SynapseLink

**Use Case:** Notify Team Brain when backups complete or fail

**Why:** Keep team informed of backup status automatically

**Code:**

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from SynapseLink.synapselink import quick_send
from QuickBackup.quickbackup import QuickBackup
from datetime import datetime

backup = QuickBackup()

# Run backup
profile = "memory-core"
result = backup.backup(profile)

# Notify based on result
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

if result:
    quick_send(
        "TEAM",
        f"[QuickBackup] Backup Complete: {profile}",
        f"Profile: {profile}\n"
        f"Time: {timestamp}\n"
        f"Status: SUCCESS\n"
        f"Mode: Incremental",
        priority="NORMAL"
    )
    print("[OK] Backup complete, team notified")
else:
    quick_send(
        "FORGE,LOGAN",
        f"[QuickBackup] BACKUP FAILED: {profile}",
        f"Profile: {profile}\n"
        f"Time: {timestamp}\n"
        f"Status: FAILED\n"
        f"ACTION REQUIRED: Investigate immediately!",
        priority="HIGH"
    )
    print("[X] Backup failed, urgent notification sent")
```

**Result:** Team stays informed without manual status updates

---

## Pattern 3: QuickBackup + TaskQueuePro

**Use Case:** Manage backup operations as tracked tasks

**Why:** Track backup operations alongside other agent tasks

**Code:**

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from TaskQueuePro.taskqueuepro import TaskQueuePro
from QuickBackup.quickbackup import QuickBackup
from datetime import datetime

queue = TaskQueuePro()
backup = QuickBackup()

# Create backup task in queue
task_id = queue.create_task(
    title="Daily backup: memory-core",
    agent="ATLAS",
    priority=2,
    metadata={
        "tool": "QuickBackup",
        "profile": "memory-core",
        "type": "incremental"
    }
)

# Mark task as in-progress
queue.start_task(task_id)

try:
    # Execute backup
    result = backup.backup("memory-core")
    
    if result:
        # Complete task successfully
        queue.complete_task(
            task_id,
            result={
                "status": "success",
                "profile": "memory-core",
                "timestamp": datetime.now().isoformat()
            }
        )
        print("[OK] Task completed successfully")
    else:
        # Fail task
        queue.fail_task(task_id, error="Backup operation returned False")
        print("[X] Task failed")
        
except Exception as e:
    queue.fail_task(task_id, error=str(e))
    raise
```

**Result:** Centralized task tracking across all tools

---

## Pattern 4: QuickBackup + MemoryBridge

**Use Case:** Persist backup history in memory core

**Why:** Maintain long-term history of backup operations

**Code:**

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from MemoryBridge.memorybridge import MemoryBridge
from QuickBackup.quickbackup import QuickBackup
from datetime import datetime

memory = MemoryBridge()
backup = QuickBackup()

# Load backup history from memory
history = memory.get("quickbackup_history", default=[])

# Run backup
profile = "daily-docs"
result = backup.backup(profile)

# Record in history
history.append({
    "timestamp": datetime.now().isoformat(),
    "profile": profile,
    "status": "success" if result else "failed",
    "mode": "incremental"
})

# Keep last 100 entries (cleanup old history)
history = history[-100:]

# Save to memory
memory.set("quickbackup_history", history)
memory.sync()

# Report
print(f"Backup history: {len(history)} entries")
print(f"Last backup: {history[-1]}")
```

**Result:** Historical backup data persisted in memory core

---

## Pattern 5: QuickBackup + SessionReplay

**Use Case:** Record backup operations in session replays for debugging

**Why:** Replay backup operations when issues occur

**Code:**

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from SessionReplay.sessionreplay import SessionReplay
from QuickBackup.quickbackup import QuickBackup

replay = SessionReplay()
backup = QuickBackup()

# Start recording session
session_id = replay.start_session("ATLAS", task="System backup routine")
replay.log_input(session_id, "Starting daily backup routine")

# Run backups with replay tracking
profiles = ["docs", "projects", "configs"]

for profile in profiles:
    replay.log_input(session_id, f"Starting backup: {profile}")
    
    try:
        result = backup.backup(profile)
        status = "SUCCESS" if result else "FAILED"
        replay.log_output(session_id, f"Backup {profile}: {status}")
    except Exception as e:
        replay.log_error(session_id, f"Backup {profile} error: {str(e)}")

# End session
replay.log_output(session_id, "Daily backup routine complete")
replay.end_session(session_id, status="COMPLETED")

print(f"Session recorded: {session_id}")
```

**Result:** Full session replay available for debugging backup issues

---

## Pattern 6: QuickBackup + ContextCompressor

**Use Case:** Compress backup reports before sharing

**Why:** Save tokens when sharing large backup outputs

**Code:**

```python
import sys
from pathlib import Path
from io import StringIO
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from ContextCompressor.contextcompressor import ContextCompressor
from QuickBackup.quickbackup import QuickBackup

compressor = ContextCompressor()
backup = QuickBackup()

# Capture backup output
original_stdout = sys.stdout
sys.stdout = captured = StringIO()

# Run backup (output captured)
backup.backup("large-profile")

# Get captured output
backup_output = captured.getvalue()
sys.stdout = original_stdout

print(f"Original output: {len(backup_output)} characters")

# Compress if large
if len(backup_output) > 1000:
    compressed = compressor.compress_text(
        backup_output,
        query="backup status and file count",
        method="summary"
    )
    share_text = compressed.compressed_text
    print(f"Compressed: {len(share_text)} characters")
    print(f"Savings: {len(backup_output) - len(share_text)} characters")
else:
    share_text = backup_output

# Use compressed text for sharing/logging
print("\n--- Compressed Report ---")
print(share_text)
```

**Result:** 70-90% token savings on large backup reports

---

## Pattern 7: QuickBackup + ConfigManager

**Use Case:** Centralize backup configuration

**Why:** Share backup settings across tools and agents

**Code:**

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from ConfigManager.configmanager import ConfigManager
from QuickBackup.quickbackup import QuickBackup

config = ConfigManager()

# Load backup settings from central config
backup_settings = config.get("quickbackup", {
    "default_destination": "D:/Backup",
    "compression": True,
    "incremental": True,
    "profiles": {
        "daily-docs": {"sources": ["~/Documents"], "priority": 1},
        "projects": {"sources": ["~/Projects"], "priority": 2},
        "configs": {"sources": ["~/.config"], "priority": 3}
    }
})

# Initialize QuickBackup
backup = QuickBackup()

# Apply central configuration
if backup_settings.get("default_destination"):
    backup.config["default_destination"] = backup_settings["default_destination"]
    backup.save_config()

# Run backup with configured settings
profile = "daily-docs"
result = backup.backup(
    profile,
    compress=backup_settings.get("compression", True),
    incremental=backup_settings.get("incremental", True)
)

print(f"Backup using central config: {'SUCCESS' if result else 'FAILED'}")

# Update config with last backup time
backup_settings["last_backup"] = datetime.now().isoformat()
config.set("quickbackup", backup_settings)
config.save()
```

**Result:** Centralized configuration management

---

## Pattern 8: QuickBackup + CollabSession

**Use Case:** Coordinate backups during multi-agent sessions

**Why:** Prevent conflicts when multiple agents backup

**Code:**

```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from CollabSession.collabsession import CollabSession
from QuickBackup.quickbackup import QuickBackup

collab = CollabSession()
backup = QuickBackup()

# Create coordination session for backup
session_id = collab.start_session(
    "backup_coordination",
    participants=["ATLAS", "FORGE", "BOLT"]
)

# Lock the backup resource to prevent conflicts
profile = "memory-core"
resource_id = f"backup-{profile}"

collab.lock_resource(session_id, resource_id, "ATLAS")
print(f"[ATLAS] Locked resource: {resource_id}")

try:
    # Only this agent can backup memory-core now
    print(f"[ATLAS] Backing up: {profile}")
    result = backup.backup(profile)
    print(f"[ATLAS] Backup result: {'SUCCESS' if result else 'FAILED'}")
    
finally:
    # Release lock for other agents
    collab.unlock_resource(session_id, resource_id)
    print(f"[ATLAS] Released resource: {resource_id}")
    
    collab.end_session(session_id)
    print("[ATLAS] Coordination session ended")
```

**Result:** Safe concurrent backup usage across agents

---

## Pattern 9: Multi-Tool Backup Workflow

**Use Case:** Complete backup workflow using multiple tools

**Why:** Demonstrate real production backup scenario

**Code:**

```python
import sys
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

from TaskQueuePro.taskqueuepro import TaskQueuePro
from SessionReplay.sessionreplay import SessionReplay
from AgentHealth.agenthealth import AgentHealth
from SynapseLink.synapselink import quick_send
from QuickBackup.quickbackup import QuickBackup

# Initialize all tools
queue = TaskQueuePro()
replay = SessionReplay()
health = AgentHealth()
backup = QuickBackup()

# Create task in queue
task_id = queue.create_task(
    title="Daily system backup",
    agent="ATLAS",
    priority=1
)

# Start session replay
session_id = replay.start_session("ATLAS", task="Daily system backup")

# Start health monitoring
health.start_session("ATLAS", session_id=session_id)

try:
    # Begin task
    queue.start_task(task_id)
    replay.log_input(session_id, "Starting daily backup routine")
    
    # Run backups
    profiles = ["docs", "projects", "memory-core"]
    results = {}
    
    for profile in profiles:
        replay.log_input(session_id, f"Backing up: {profile}")
        health.heartbeat("ATLAS", status=f"backup:{profile}")
        
        result = backup.backup(profile)
        results[profile] = result
        
        status = "SUCCESS" if result else "FAILED"
        replay.log_output(session_id, f"{profile}: {status}")
    
    # Summarize
    all_success = all(results.values())
    
    if all_success:
        queue.complete_task(task_id, result={"status": "success", "profiles": list(results.keys())})
        replay.end_session(session_id, status="COMPLETED")
        health.end_session("ATLAS", session_id=session_id, status="success")
        
        quick_send("TEAM", "Daily Backup Complete", 
            f"All {len(profiles)} profiles backed up successfully at {datetime.now()}")
    else:
        failed = [p for p, r in results.items() if not r]
        queue.fail_task(task_id, error=f"Failed profiles: {failed}")
        replay.end_session(session_id, status="PARTIAL_FAILURE")
        health.end_session("ATLAS", session_id=session_id, status="partial")
        
        quick_send("FORGE,LOGAN", "Backup Partial Failure",
            f"Failed profiles: {failed}", priority="HIGH")
            
except Exception as e:
    queue.fail_task(task_id, error=str(e))
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    health.log_error("ATLAS", str(e))
    health.end_session("ATLAS", session_id=session_id, status="failed")
    
    quick_send("FORGE,LOGAN", "Backup System Error", str(e), priority="HIGH")
    raise
```

**Result:** Fully instrumented, coordinated backup workflow

---

## Pattern 10: Full Team Brain Backup Stack

**Use Case:** Ultimate integration - comprehensive backup system

**Why:** Production-grade backup operations

**Code:**

```python
#!/usr/bin/env python3
"""
Team Brain Comprehensive Backup System
Integrates all Team Brain tools for production-grade backups
"""

import sys
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Import all tools
from QuickBackup.quickbackup import QuickBackup
from ConfigManager.configmanager import ConfigManager
from TaskQueuePro.taskqueuepro import TaskQueuePro
from SessionReplay.sessionreplay import SessionReplay
from AgentHealth.agenthealth import AgentHealth
from MemoryBridge.memorybridge import MemoryBridge
from SynapseLink.synapselink import quick_send

class TeamBrainBackupSystem:
    """Comprehensive backup system using all Team Brain tools."""
    
    def __init__(self, agent_name="ATLAS"):
        self.agent = agent_name
        self.backup = QuickBackup()
        self.config = ConfigManager()
        self.queue = TaskQueuePro()
        self.replay = SessionReplay()
        self.health = AgentHealth()
        self.memory = MemoryBridge()
        
        # Load configuration
        self.settings = self.config.get("backup_system", {
            "profiles": ["docs", "projects", "memory-core", "configs"],
            "notify_on_success": True,
            "notify_on_failure": True,
            "track_history": True
        })
    
    def run_full_backup(self):
        """Run complete backup routine with full instrumentation."""
        
        timestamp = datetime.now()
        session_id = f"backup_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        # Create task
        task_id = self.queue.create_task(
            title=f"Full system backup {timestamp.date()}",
            agent=self.agent,
            priority=1
        )
        
        # Start session
        self.replay.start_session(self.agent, task="Full system backup")
        self.health.start_session(self.agent, session_id=session_id)
        self.queue.start_task(task_id)
        
        # Track results
        results = {}
        start_time = datetime.now()
        
        try:
            for profile in self.settings["profiles"]:
                self.replay.log_input(session_id, f"Backing up: {profile}")
                self.health.heartbeat(self.agent, status=f"backup:{profile}")
                
                result = self.backup.backup(profile)
                results[profile] = result
                
                self.replay.log_output(session_id, 
                    f"{profile}: {'SUCCESS' if result else 'FAILED'}")
            
            # Calculate summary
            duration = (datetime.now() - start_time).total_seconds()
            success_count = sum(1 for r in results.values() if r)
            total_count = len(results)
            all_success = success_count == total_count
            
            # Record in memory
            if self.settings["track_history"]:
                self._record_history(results, duration)
            
            # Complete task and sessions
            self._complete_sessions(
                task_id, session_id, results, duration, all_success
            )
            
            # Notify team
            self._notify_completion(results, duration, all_success)
            
            return all_success
            
        except Exception as e:
            self._handle_error(task_id, session_id, e)
            raise
    
    def _record_history(self, results, duration):
        """Record backup results in memory."""
        history = self.memory.get("backup_history", default=[])
        history.append({
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "duration": duration,
            "success": all(results.values())
        })
        history = history[-100:]  # Keep last 100
        self.memory.set("backup_history", history)
        self.memory.sync()
    
    def _complete_sessions(self, task_id, session_id, results, duration, success):
        """Complete all tracking sessions."""
        status = "COMPLETED" if success else "PARTIAL_FAILURE"
        
        self.queue.complete_task(task_id, result={
            "status": "success" if success else "partial",
            "results": results,
            "duration": duration
        })
        
        self.replay.end_session(session_id, status=status)
        self.health.end_session(self.agent, session_id=session_id)
    
    def _notify_completion(self, results, duration, success):
        """Notify team of backup completion."""
        failed = [p for p, r in results.items() if not r]
        
        if success and self.settings["notify_on_success"]:
            quick_send(
                "TEAM",
                "[Backup] Full System Backup Complete",
                f"All {len(results)} profiles backed up successfully\n"
                f"Duration: {duration:.1f}s\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                priority="NORMAL"
            )
        elif not success and self.settings["notify_on_failure"]:
            quick_send(
                "FORGE,LOGAN",
                "[Backup] BACKUP FAILURE",
                f"Failed profiles: {failed}\n"
                f"Successful: {len(results) - len(failed)}/{len(results)}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"ACTION REQUIRED!",
                priority="HIGH"
            )
    
    def _handle_error(self, task_id, session_id, error):
        """Handle critical errors."""
        self.queue.fail_task(task_id, error=str(error))
        self.replay.log_error(session_id, str(error))
        self.replay.end_session(session_id, status="FAILED")
        self.health.log_error(self.agent, str(error))
        self.health.end_session(self.agent, session_id=session_id)
        
        quick_send(
            "FORGE,LOGAN",
            "[Backup] CRITICAL ERROR",
            f"Backup system error: {str(error)}\n"
            f"Time: {datetime.now()}\n"
            f"IMMEDIATE ATTENTION REQUIRED!",
            priority="CRITICAL"
        )


# Usage
if __name__ == "__main__":
    system = TeamBrainBackupSystem(agent_name="ATLAS")
    success = system.run_full_backup()
    print(f"Backup system result: {'SUCCESS' if success else 'FAILURE'}")
```

**Result:** Production-grade backup system with full Team Brain integration

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✓ AgentHealth - Track backup operations
2. ✓ SynapseLink - Team notifications
3. ✓ SessionReplay - Debugging support

**Week 2 (Productivity):**
4. ☐ TaskQueuePro - Task management
5. ☐ MemoryBridge - History persistence
6. ☐ ConfigManager - Centralized config

**Week 3 (Advanced):**
7. ☐ ContextCompressor - Report optimization
8. ☐ CollabSession - Multi-agent coordination
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**

```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from QuickBackup.quickbackup import QuickBackup
```

**Module Not Found:**

```bash
# Check tool directory exists
ls ~/OneDrive/Documents/AutoProjects/QuickBackup/

# Verify main file
python -c "from quickbackup import QuickBackup; print('OK')"
```

**Configuration Issues:**

```python
# Reset QuickBackup config
from quickbackup import QuickBackup
backup = QuickBackup()
backup.config = {"default_destination": None}
backup.save_config()
```

---

**Last Updated:** January 30, 2026  
**Maintained By:** ATLAS (Team Brain)  
**For:** Logan Smith / Metaphy LLC
