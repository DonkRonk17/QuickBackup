#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuickBackup - Simple, Fast Backup Automation
=============================================
One-command backup of your important files with compression and incremental support.

Author: Team Brain / Forge
License: MIT
"""

import os
import sys
import json
import shutil
import hashlib
import zipfile
from pathlib import Path
from datetime import datetime
import argparse

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
    except:
        pass


class QuickBackup:
    """Main QuickBackup application class."""

    def __init__(self):
        """Initialize QuickBackup with config directory."""
        self.config_dir = Path.home() / ".quickbackup"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.profiles_dir = self.config_dir / "profiles"
        self.profiles_dir.mkdir(exist_ok=True)
        self.checksums_file = self.config_dir / "checksums.json"
        self.load_config()
        self.load_checksums()

    def load_config(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
                self.config = {"default_destination": None}
        else:
            self.config = {"default_destination": None}
            self.save_config()

    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"[X] Error saving config: {e}")

    def load_checksums(self):
        """Load file checksums for incremental backups."""
        if self.checksums_file.exists():
            try:
                with open(self.checksums_file, "r") as f:
                    self.checksums = json.load(f)
            except:
                self.checksums = {}
        else:
            self.checksums = {}

    def save_checksums(self):
        """Save file checksums."""
        try:
            with open(self.checksums_file, "w") as f:
                json.dump(self.checksums, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save checksums: {e}")

    def calculate_checksum(self, file_path):
        """Calculate MD5 checksum of a file."""
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            print(f"Warning: Could not calculate checksum for {file_path}: {e}")
            return None

    def has_file_changed(self, file_path, profile_name):
        """Check if file has changed since last backup."""
        file_str = str(file_path)
        checksum_key = f"{profile_name}:{file_str}"
        
        current_checksum = self.calculate_checksum(file_path)
        if current_checksum is None:
            return True
        
        if checksum_key in self.checksums:
            return self.checksums[checksum_key] != current_checksum
        
        return True

    def update_checksum(self, file_path, profile_name):
        """Update stored checksum for a file."""
        file_str = str(file_path)
        checksum_key = f"{profile_name}:{file_str}"
        checksum = self.calculate_checksum(file_path)
        if checksum:
            self.checksums[checksum_key] = checksum

    def create_profile(self, name, sources, destination=None):
        """Create a backup profile."""
        profile = {
            "name": name,
            "sources": [str(Path(s).resolve()) for s in sources],
            "destination": str(Path(destination).resolve()) if destination else None,
            "created": datetime.now().isoformat(),
            "last_backup": None,
        }

        profile_file = self.profiles_dir / f"{name}.json"
        
        try:
            with open(profile_file, "w") as f:
                json.dump(profile, f, indent=2)
            print(f"[OK] Profile '{name}' created")
            print(f"     Sources: {len(sources)} folder(s)")
            if destination:
                print(f"     Destination: {destination}")
            return True
        except Exception as e:
            print(f"[X] Error creating profile: {e}")
            return False

    def list_profiles(self):
        """List all backup profiles."""
        profiles = list(self.profiles_dir.glob("*.json"))
        
        if not profiles:
            print("No backup profiles found. Create one with: quickbackup create")
            return

        print(f"\n[{len(profiles)} profile(s)]\n")
        
        for profile_file in sorted(profiles):
            try:
                with open(profile_file) as f:
                    profile = json.load(f)
                
                name = profile.get("name", profile_file.stem)
                sources_count = len(profile.get("sources", []))
                last_backup = profile.get("last_backup", "Never")
                if last_backup != "Never":
                    last_backup = last_backup[:19]
                
                print(f"* {name}")
                print(f"  Sources: {sources_count} folder(s)")
                print(f"  Last backup: {last_backup}")
                print()
            except Exception as e:
                print(f"Warning: Could not read {profile_file.name}: {e}")

    def show_profile(self, name):
        """Show profile details."""
        profile_file = self.profiles_dir / f"{name}.json"
        
        if not profile_file.exists():
            print(f"[X] Profile '{name}' not found!")
            return False

        try:
            with open(profile_file) as f:
                profile = json.load(f)
            
            print(f"\n{'='*60}")
            print(f"Profile: {profile['name']}")
            print(f"{'='*60}")
            print(f"\nCreated: {profile.get('created', 'Unknown')[:19]}")
            print(f"Last Backup: {profile.get('last_backup', 'Never')[:19] if profile.get('last_backup') else 'Never'}")
            
            print(f"\nSources ({len(profile['sources'])}):")
            for source in profile['sources']:
                exists = "✓" if Path(source).exists() else "✗"
                print(f"  [{exists}] {source}")
            
            dest = profile.get('destination')
            if dest:
                dest_exists = "✓" if Path(dest).exists() else "✗"
                print(f"\nDestination:")
                print(f"  [{dest_exists}] {dest}")
            else:
                print(f"\nDestination: Not set (will prompt)")
            
            print(f"\n{'='*60}\n")
            return True
        except Exception as e:
            print(f"[X] Error reading profile: {e}")
            return False

    def backup(self, profile_name, destination=None, incremental=True, compress=True):
        """Perform backup using a profile."""
        profile_file = self.profiles_dir / f"{profile_name}.json"
        
        if not profile_file.exists():
            print(f"[X] Profile '{profile_name}' not found!")
            return False

        try:
            with open(profile_file) as f:
                profile = json.load(f)
        except Exception as e:
            print(f"[X] Error loading profile: {e}")
            return False

        # Determine destination
        if destination is None:
            destination = profile.get('destination')
            if destination is None:
                destination = self.config.get('default_destination')
            if destination is None:
                print("[X] No destination specified! Use --dest or set in profile")
                return False

        dest_path = Path(destination)
        if not dest_path.exists():
            print(f"[X] Destination does not exist: {destination}")
            return False

        # Create backup folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{profile_name}_{timestamp}"
        backup_dir = dest_path / backup_name
        
        print(f"\n[BACKUP] Starting backup '{profile_name}'")
        print(f"Destination: {backup_dir}")
        print(f"Incremental: {'Yes' if incremental else 'No'}")
        print(f"Compress: {'Yes' if compress else 'No'}\n")

        try:
            backup_dir.mkdir(parents=True)
        except Exception as e:
            print(f"[X] Could not create backup directory: {e}")
            return False

        # Backup each source
        total_files = 0
        total_size = 0
        skipped_files = 0

        for source in profile['sources']:
            source_path = Path(source)
            if not source_path.exists():
                print(f"[!] Skipping non-existent source: {source}")
                continue

            print(f"Backing up: {source}")
            
            if source_path.is_file():
                # Single file
                if not incremental or self.has_file_changed(source_path, profile_name):
                    try:
                        shutil.copy2(source_path, backup_dir / source_path.name)
                        total_files += 1
                        total_size += source_path.stat().st_size
                        if incremental:
                            self.update_checksum(source_path, profile_name)
                    except Exception as e:
                        print(f"  [X] Failed to copy {source_path.name}: {e}")
                else:
                    skipped_files += 1
            else:
                # Directory
                for root, dirs, files in os.walk(source_path):
                    root_path = Path(root)
                    rel_path = root_path.relative_to(source_path.parent)
                    dest_folder = backup_dir / rel_path
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    
                    for file in files:
                        file_path = root_path / file
                        
                        if not incremental or self.has_file_changed(file_path, profile_name):
                            try:
                                shutil.copy2(file_path, dest_folder / file)
                                total_files += 1
                                total_size += file_path.stat().st_size
                                if incremental:
                                    self.update_checksum(file_path, profile_name)
                            except Exception as e:
                                print(f"  [X] Failed to copy {file}: {e}")
                        else:
                            skipped_files += 1

        # Save checksums if incremental
        if incremental:
            self.save_checksums()

        # Compress if requested
        if compress and total_files > 0:
            print(f"\nCompressing backup...")
            zip_file = dest_path / f"{backup_name}.zip"
            
            try:
                with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(backup_dir):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(backup_dir)
                            zipf.write(file_path, arcname)
                
                # Remove uncompressed backup
                shutil.rmtree(backup_dir)
                
                zip_size = zip_file.stat().st_size
                compression_ratio = (1 - zip_size / total_size) * 100 if total_size > 0 else 0
                
                print(f"[OK] Compressed: {self.format_size(zip_size)} "
                      f"({compression_ratio:.1f}% reduction)")
                
            except Exception as e:
                print(f"[X] Compression failed: {e}")

        # Update profile
        profile['last_backup'] = datetime.now().isoformat()
        try:
            with open(profile_file, 'w') as f:
                json.dump(profile, f, indent=2)
        except:
            pass

        print(f"\n{'='*60}")
        print(f"[OK] Backup complete!")
        print(f"Files backed up: {total_files}")
        if incremental and skipped_files > 0:
            print(f"Files skipped (unchanged): {skipped_files}")
        print(f"Total size: {self.format_size(total_size)}")
        print(f"{'='*60}\n")
        
        return True

    def format_size(self, size_bytes):
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def delete_profile(self, name):
        """Delete a backup profile."""
        profile_file = self.profiles_dir / f"{name}.json"
        
        if not profile_file.exists():
            print(f"[X] Profile '{name}' not found!")
            return False

        try:
            profile_file.unlink()
            print(f"[OK] Profile '{name}' deleted")
            return True
        except Exception as e:
            print(f"[X] Error deleting profile: {e}")
            return False


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="QuickBackup - Simple, Fast Backup Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  quickbackup create work ~/Documents ~/Projects --dest /backup/drive
  quickbackup create photos ~/Pictures --dest /backup/drive
  quickbackup list
  quickbackup show work
  quickbackup backup work
  quickbackup backup work --no-incremental
  quickbackup backup work --no-compress --dest /other/location
  quickbackup delete old_profile
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create profile
    parser_create = subparsers.add_parser("create", help="Create backup profile")
    parser_create.add_argument("name", help="Profile name")
    parser_create.add_argument("sources", nargs="+", help="Folders/files to backup")
    parser_create.add_argument("--dest", help="Backup destination folder")

    # List profiles
    subparsers.add_parser("list", help="List all profiles")

    # Show profile
    parser_show = subparsers.add_parser("show", help="Show profile details")
    parser_show.add_argument("name", help="Profile name")

    # Backup
    parser_backup = subparsers.add_parser("backup", help="Run backup")
    parser_backup.add_argument("name", help="Profile name")
    parser_backup.add_argument("--dest", help="Override destination")
    parser_backup.add_argument("--no-incremental", action="store_true", help="Backup all files")
    parser_backup.add_argument("--no-compress", action="store_true", help="Don't compress")

    # Delete profile
    parser_delete = subparsers.add_parser("delete", help="Delete profile")
    parser_delete.add_argument("name", help="Profile name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    backup = QuickBackup()

    if args.command == "create":
        backup.create_profile(args.name, args.sources, args.dest)

    elif args.command == "list":
        backup.list_profiles()

    elif args.command == "show":
        backup.show_profile(args.name)

    elif args.command == "backup":
        backup.backup(
            args.name,
            destination=args.dest,
            incremental=not args.no_incremental,
            compress=not args.no_compress
        )

    elif args.command == "delete":
        backup.delete_profile(args.name)


if __name__ == "__main__":
    main()
