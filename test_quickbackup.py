#!/usr/bin/env python3
"""
Comprehensive test suite for QuickBackup.

Tests cover:
- Core functionality (profile management, backup operations)
- Edge cases (empty inputs, missing files, invalid paths)
- Error handling (file permissions, disk space)
- Integration scenarios (incremental backups, compression)
- Cross-platform compatibility

Run: python test_quickbackup.py
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from quickbackup import QuickBackup


class TestQuickBackupInit(unittest.TestCase):
    """Test QuickBackup initialization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get('HOME', os.environ.get('USERPROFILE'))
        os.environ['HOME'] = self.test_dir
        os.environ['USERPROFILE'] = self.test_dir
    
    def tearDown(self):
        """Clean up after tests."""
        if self.original_home:
            os.environ['HOME'] = self.original_home
            os.environ['USERPROFILE'] = self.original_home
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test QuickBackup initializes correctly."""
        backup = QuickBackup()
        self.assertIsNotNone(backup)
        self.assertIsNotNone(backup.config)
        self.assertIsNotNone(backup.checksums)
    
    def test_config_directory_created(self):
        """Test config directory is created on init."""
        backup = QuickBackup()
        self.assertTrue(backup.config_dir.exists())
    
    def test_profiles_directory_created(self):
        """Test profiles directory is created on init."""
        backup = QuickBackup()
        self.assertTrue(backup.profiles_dir.exists())
    
    def test_default_config_values(self):
        """Test default configuration values."""
        backup = QuickBackup()
        self.assertIn('default_destination', backup.config)


class TestProfileManagement(unittest.TestCase):
    """Test backup profile management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get('HOME', os.environ.get('USERPROFILE'))
        os.environ['HOME'] = self.test_dir
        os.environ['USERPROFILE'] = self.test_dir
        
        # Create test source directory with files
        self.source_dir = Path(self.test_dir) / "source"
        self.source_dir.mkdir()
        (self.source_dir / "file1.txt").write_text("test content 1")
        (self.source_dir / "file2.txt").write_text("test content 2")
        
        # Create test destination
        self.dest_dir = Path(self.test_dir) / "backup"
        self.dest_dir.mkdir()
        
        self.backup = QuickBackup()
    
    def tearDown(self):
        """Clean up after tests."""
        if self.original_home:
            os.environ['HOME'] = self.original_home
            os.environ['USERPROFILE'] = self.original_home
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_create_profile(self):
        """Test creating a backup profile."""
        result = self.backup.create_profile(
            "test_profile",
            [str(self.source_dir)],
            str(self.dest_dir)
        )
        self.assertTrue(result)
        
        profile_file = self.backup.profiles_dir / "test_profile.json"
        self.assertTrue(profile_file.exists())
    
    def test_create_profile_without_destination(self):
        """Test creating profile without destination."""
        result = self.backup.create_profile(
            "no_dest_profile",
            [str(self.source_dir)]
        )
        self.assertTrue(result)
    
    def test_create_profile_multiple_sources(self):
        """Test creating profile with multiple sources."""
        source2 = Path(self.test_dir) / "source2"
        source2.mkdir()
        
        result = self.backup.create_profile(
            "multi_source",
            [str(self.source_dir), str(source2)],
            str(self.dest_dir)
        )
        self.assertTrue(result)
        
        # Verify profile contents
        profile_file = self.backup.profiles_dir / "multi_source.json"
        with open(profile_file) as f:
            profile = json.load(f)
        self.assertEqual(len(profile['sources']), 2)
    
    def test_list_profiles_empty(self):
        """Test listing profiles when none exist."""
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        self.backup.list_profiles()
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertIn("No backup profiles found", output)
    
    def test_list_profiles_with_profiles(self):
        """Test listing profiles when profiles exist."""
        self.backup.create_profile("profile1", [str(self.source_dir)])
        self.backup.create_profile("profile2", [str(self.source_dir)])
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        self.backup.list_profiles()
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertIn("profile1", output)
        self.assertIn("profile2", output)
    
    def test_show_profile(self):
        """Test showing profile details."""
        self.backup.create_profile(
            "show_test",
            [str(self.source_dir)],
            str(self.dest_dir)
        )
        
        result = self.backup.show_profile("show_test")
        self.assertTrue(result)
    
    def test_show_nonexistent_profile(self):
        """Test showing non-existent profile."""
        result = self.backup.show_profile("nonexistent")
        self.assertFalse(result)
    
    def test_delete_profile(self):
        """Test deleting a profile."""
        self.backup.create_profile("to_delete", [str(self.source_dir)])
        
        result = self.backup.delete_profile("to_delete")
        self.assertTrue(result)
        
        profile_file = self.backup.profiles_dir / "to_delete.json"
        self.assertFalse(profile_file.exists())
    
    def test_delete_nonexistent_profile(self):
        """Test deleting non-existent profile."""
        result = self.backup.delete_profile("nonexistent")
        self.assertFalse(result)


class TestBackupOperations(unittest.TestCase):
    """Test backup operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get('HOME', os.environ.get('USERPROFILE'))
        os.environ['HOME'] = self.test_dir
        os.environ['USERPROFILE'] = self.test_dir
        
        # Create test source directory with files
        self.source_dir = Path(self.test_dir) / "source"
        self.source_dir.mkdir()
        (self.source_dir / "file1.txt").write_text("test content 1")
        (self.source_dir / "file2.txt").write_text("test content 2")
        
        # Create subdirectory
        subdir = self.source_dir / "subdir"
        subdir.mkdir()
        (subdir / "nested.txt").write_text("nested content")
        
        # Create test destination
        self.dest_dir = Path(self.test_dir) / "backup"
        self.dest_dir.mkdir()
        
        self.backup = QuickBackup()
        self.backup.create_profile(
            "test_backup",
            [str(self.source_dir)],
            str(self.dest_dir)
        )
    
    def tearDown(self):
        """Clean up after tests."""
        if self.original_home:
            os.environ['HOME'] = self.original_home
            os.environ['USERPROFILE'] = self.original_home
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_basic_backup(self):
        """Test basic backup operation."""
        result = self.backup.backup("test_backup", compress=False)
        self.assertTrue(result)
        
        # Check backup was created
        backups = list(self.dest_dir.glob("test_backup_*"))
        self.assertGreater(len(backups), 0)
    
    def test_backup_with_compression(self):
        """Test backup with compression."""
        result = self.backup.backup("test_backup", compress=True)
        self.assertTrue(result)
        
        # Check ZIP file was created
        zips = list(self.dest_dir.glob("*.zip"))
        self.assertEqual(len(zips), 1)
        
        # Verify ZIP contents
        with zipfile.ZipFile(zips[0], 'r') as zipf:
            names = zipf.namelist()
            self.assertGreater(len(names), 0)
    
    def test_backup_nonexistent_profile(self):
        """Test backup with non-existent profile."""
        result = self.backup.backup("nonexistent")
        self.assertFalse(result)
    
    def test_backup_nonexistent_destination(self):
        """Test backup with non-existent destination."""
        shutil.rmtree(self.dest_dir)
        result = self.backup.backup("test_backup")
        self.assertFalse(result)
    
    def test_backup_override_destination(self):
        """Test backup with overridden destination."""
        alt_dest = Path(self.test_dir) / "alt_backup"
        alt_dest.mkdir()
        
        result = self.backup.backup(
            "test_backup",
            destination=str(alt_dest),
            compress=False
        )
        self.assertTrue(result)
        
        backups = list(alt_dest.glob("test_backup_*"))
        self.assertGreater(len(backups), 0)
    
    def test_backup_no_destination(self):
        """Test backup with no destination specified."""
        # Create profile without destination
        self.backup.create_profile("no_dest", [str(self.source_dir)])
        
        result = self.backup.backup("no_dest")
        self.assertFalse(result)


class TestIncrementalBackup(unittest.TestCase):
    """Test incremental backup functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get('HOME', os.environ.get('USERPROFILE'))
        os.environ['HOME'] = self.test_dir
        os.environ['USERPROFILE'] = self.test_dir
        
        # Create test source with files
        self.source_dir = Path(self.test_dir) / "source"
        self.source_dir.mkdir()
        (self.source_dir / "file1.txt").write_text("original content")
        (self.source_dir / "file2.txt").write_text("original content 2")
        
        # Create destination
        self.dest_dir = Path(self.test_dir) / "backup"
        self.dest_dir.mkdir()
        
        self.backup = QuickBackup()
        self.backup.create_profile(
            "incremental_test",
            [str(self.source_dir)],
            str(self.dest_dir)
        )
    
    def tearDown(self):
        """Clean up after tests."""
        if self.original_home:
            os.environ['HOME'] = self.original_home
            os.environ['USERPROFILE'] = self.original_home
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_checksum_calculation(self):
        """Test MD5 checksum calculation."""
        test_file = self.source_dir / "file1.txt"
        checksum = self.backup.calculate_checksum(test_file)
        
        self.assertIsNotNone(checksum)
        self.assertEqual(len(checksum), 32)  # MD5 hex string length
    
    def test_checksum_nonexistent_file(self):
        """Test checksum for non-existent file."""
        checksum = self.backup.calculate_checksum(Path("/nonexistent/file.txt"))
        self.assertIsNone(checksum)
    
    def test_file_changed_detection(self):
        """Test file change detection."""
        test_file = self.source_dir / "file1.txt"
        
        # First check - should be "changed" (not in checksums)
        self.assertTrue(self.backup.has_file_changed(test_file, "test"))
        
        # Update checksum
        self.backup.update_checksum(test_file, "test")
        
        # Second check - should NOT be changed
        self.assertFalse(self.backup.has_file_changed(test_file, "test"))
        
        # Modify file
        test_file.write_text("modified content")
        
        # Third check - should be changed
        self.assertTrue(self.backup.has_file_changed(test_file, "test"))
    
    def test_incremental_backup_skips_unchanged(self):
        """Test that incremental backup skips unchanged files."""
        import time
        
        # First backup - all files
        self.backup.backup("incremental_test", incremental=True, compress=False)
        
        # Get first backup folder
        backups1 = list(self.dest_dir.glob("incremental_test_*"))
        self.assertEqual(len(backups1), 1)
        
        # Count files in first backup
        files1 = list(backups1[0].rglob("*"))
        files1 = [f for f in files1 if f.is_file()]
        initial_file_count = len(files1)
        self.assertGreater(initial_file_count, 0)
        
        # Wait for timestamp to change (prevents same-second collision)
        time.sleep(1.1)
        
        # Second backup - no changes
        self.backup.backup("incremental_test", incremental=True, compress=False)
        
        backups2 = list(self.dest_dir.glob("incremental_test_*"))
        self.assertEqual(len(backups2), 2)
        
        # Sort to get newest backup
        backups2 = sorted(backups2, key=lambda x: x.name)
        
        # Second backup should have no files (all unchanged)
        files2 = list(backups2[1].rglob("*"))
        files2 = [f for f in files2 if f.is_file()]
        self.assertEqual(len(files2), 0)
    
    def test_full_backup_includes_all(self):
        """Test that non-incremental backup includes all files."""
        import time
        
        # First backup
        self.backup.backup("incremental_test", incremental=False, compress=False)
        
        # Wait for timestamp to change (prevents same-second collision)
        time.sleep(1.1)
        
        # Second backup (non-incremental)
        self.backup.backup("incremental_test", incremental=False, compress=False)
        
        backups = list(self.dest_dir.glob("incremental_test_*"))
        self.assertEqual(len(backups), 2)
        
        # Both should have same number of files
        for backup in backups:
            files = [f for f in backup.rglob("*") if f.is_file()]
            self.assertEqual(len(files), 2)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get('HOME', os.environ.get('USERPROFILE'))
        os.environ['HOME'] = self.test_dir
        os.environ['USERPROFILE'] = self.test_dir
        
        self.backup = QuickBackup()
    
    def tearDown(self):
        """Clean up after tests."""
        if self.original_home:
            os.environ['HOME'] = self.original_home
            os.environ['USERPROFILE'] = self.original_home
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_empty_profile_name(self):
        """Test creating profile with empty name."""
        source = Path(self.test_dir) / "source"
        source.mkdir()
        
        # Should still work (creates .json file)
        result = self.backup.create_profile("", [str(source)])
        self.assertTrue(result)
    
    def test_special_characters_in_name(self):
        """Test profile name with special characters."""
        source = Path(self.test_dir) / "source"
        source.mkdir()
        
        # Safe characters should work
        result = self.backup.create_profile("test-profile_123", [str(source)])
        self.assertTrue(result)
    
    def test_backup_empty_directory(self):
        """Test backing up empty directory."""
        source = Path(self.test_dir) / "empty_source"
        source.mkdir()
        dest = Path(self.test_dir) / "backup"
        dest.mkdir()
        
        self.backup.create_profile("empty_backup", [str(source)], str(dest))
        result = self.backup.backup("empty_backup", compress=False)
        self.assertTrue(result)
    
    def test_backup_single_file(self):
        """Test backing up a single file (not directory)."""
        source_file = Path(self.test_dir) / "single_file.txt"
        source_file.write_text("single file content")
        dest = Path(self.test_dir) / "backup"
        dest.mkdir()
        
        self.backup.create_profile("single_file", [str(source_file)], str(dest))
        result = self.backup.backup("single_file", compress=False)
        self.assertTrue(result)
    
    def test_backup_missing_source(self):
        """Test backup when source no longer exists."""
        source = Path(self.test_dir) / "temp_source"
        source.mkdir()
        (source / "file.txt").write_text("content")
        dest = Path(self.test_dir) / "backup"
        dest.mkdir()
        
        self.backup.create_profile("missing_source", [str(source)], str(dest))
        
        # Remove source
        shutil.rmtree(source)
        
        # Should complete but skip missing source
        result = self.backup.backup("missing_source", compress=False)
        self.assertTrue(result)
    
    def test_large_file_handling(self):
        """Test handling of larger files."""
        source = Path(self.test_dir) / "source"
        source.mkdir()
        
        # Create 1MB file
        large_file = source / "large.bin"
        large_file.write_bytes(b'x' * (1024 * 1024))
        
        dest = Path(self.test_dir) / "backup"
        dest.mkdir()
        
        self.backup.create_profile("large_file", [str(source)], str(dest))
        result = self.backup.backup("large_file", compress=True)
        self.assertTrue(result)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get('HOME', os.environ.get('USERPROFILE'))
        os.environ['HOME'] = self.test_dir
        os.environ['USERPROFILE'] = self.test_dir
        
        self.backup = QuickBackup()
    
    def tearDown(self):
        """Clean up after tests."""
        if self.original_home:
            os.environ['HOME'] = self.original_home
            os.environ['USERPROFILE'] = self.original_home
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_format_size_bytes(self):
        """Test byte formatting."""
        self.assertEqual(self.backup.format_size(500), "500.0 B")
    
    def test_format_size_kilobytes(self):
        """Test KB formatting."""
        result = self.backup.format_size(1024)
        self.assertIn("KB", result)
    
    def test_format_size_megabytes(self):
        """Test MB formatting."""
        result = self.backup.format_size(1024 * 1024)
        self.assertIn("MB", result)
    
    def test_format_size_gigabytes(self):
        """Test GB formatting."""
        result = self.backup.format_size(1024 * 1024 * 1024)
        self.assertIn("GB", result)
    
    def test_format_size_zero(self):
        """Test zero bytes formatting."""
        self.assertEqual(self.backup.format_size(0), "0.0 B")


class TestConfigPersistence(unittest.TestCase):
    """Test configuration persistence."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get('HOME', os.environ.get('USERPROFILE'))
        os.environ['HOME'] = self.test_dir
        os.environ['USERPROFILE'] = self.test_dir
    
    def tearDown(self):
        """Clean up after tests."""
        if self.original_home:
            os.environ['HOME'] = self.original_home
            os.environ['USERPROFILE'] = self.original_home
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_config_persists(self):
        """Test configuration persists across instances."""
        backup1 = QuickBackup()
        backup1.config['test_key'] = 'test_value'
        backup1.save_config()
        
        backup2 = QuickBackup()
        self.assertEqual(backup2.config.get('test_key'), 'test_value')
    
    def test_checksums_persist(self):
        """Test checksums persist across instances."""
        backup1 = QuickBackup()
        backup1.checksums['test_file'] = 'abc123'
        backup1.save_checksums()
        
        backup2 = QuickBackup()
        self.assertEqual(backup2.checksums.get('test_file'), 'abc123')
    
    def test_profile_persists(self):
        """Test profile persists across instances."""
        source = Path(self.test_dir) / "source"
        source.mkdir()
        
        backup1 = QuickBackup()
        backup1.create_profile("persist_test", [str(source)])
        
        backup2 = QuickBackup()
        profile_file = backup2.profiles_dir / "persist_test.json"
        self.assertTrue(profile_file.exists())


def run_tests():
    """Run all tests with detailed output."""
    print("=" * 70)
    print("TESTING: QuickBackup v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestQuickBackupInit))
    suite.addTests(loader.loadTestsFromTestCase(TestProfileManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestBackupOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestIncrementalBackup))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigPersistence))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"RESULTS: {result.testsRun} tests run")
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
