"""
test_generate_log.py - Tests for generate_log() covering all rubric criteria:

1. generate_log() creates a file with the correct timestamped filename.
2. The filename follows the pattern log_YYYYMMDD.txt.
3. The file contents exactly match the input list provided.
4. A ValueError is raised when called with invalid (non-list) input.
5. An empty list still creates a valid (empty) log file without errors.
6. The function prints a confirmation message including the filename.
7. The log file is created in the expected directory and removed cleanly
   during test teardown.
"""

import os
import re
import sys
from datetime import datetime

import pytest

# Ensure the project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from generate_log import generate_log


EXPECTED_FILENAME = f"log_{datetime.now().strftime('%Y%m%d')}.txt"


@pytest.fixture
def cleanup_files():
    """
    Track files created during a test and remove them afterwards,
    ensuring clean teardown regardless of the test outcome.
    """
    created = []
    yield created
    for path in created:
        if os.path.exists(path):
            os.remove(path)


class TestGenerateLog:
    """Tests for the generate_log() function."""

    def test_creates_file_with_timestamped_filename(self, tmp_path, cleanup_files):
        """generate_log() should create a file with the correct timestamped name."""
        log_data = ["Event 1", "Event 2"]
        filepath = generate_log(log_data, directory=str(tmp_path))
        cleanup_files.append(filepath)

        assert os.path.exists(filepath)
        assert os.path.basename(filepath) == EXPECTED_FILENAME

    def test_filename_follows_pattern(self, tmp_path, cleanup_files):
        """The filename must match the pattern log_YYYYMMDD.txt."""
        filepath = generate_log(["Some event"], directory=str(tmp_path))
        cleanup_files.append(filepath)

        filename = os.path.basename(filepath)
        assert re.fullmatch(r"log_\d{8}\.txt", filename)

    def test_file_contents_match_input_list(self, tmp_path, cleanup_files):
        """The file contents should exactly match the input list, line by line."""
        log_data = ["Line A", "Line B", "Line C"]
        filepath = generate_log(log_data, directory=str(tmp_path))
        cleanup_files.append(filepath)

        with open(filepath, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]

        assert lines == log_data

    def test_raises_value_error_for_non_list_input(self, tmp_path):
        """generate_log() should raise ValueError for non-list input types."""
        with pytest.raises(ValueError):
            generate_log("not a list", directory=str(tmp_path))

        with pytest.raises(ValueError):
            generate_log({"key": "value"}, directory=str(tmp_path))

        with pytest.raises(ValueError):
            generate_log(12345, directory=str(tmp_path))

        with pytest.raises(ValueError):
            generate_log(None, directory=str(tmp_path))

    def test_empty_list_creates_valid_empty_file(self, tmp_path, cleanup_files):
        """An empty list should still create a valid, empty log file."""
        filepath = generate_log([], directory=str(tmp_path))
        cleanup_files.append(filepath)

        assert os.path.exists(filepath)
        with open(filepath, "r") as f:
            content = f.read()
        assert content == ""

    def test_prints_confirmation_message_with_filename(self, tmp_path, capsys, cleanup_files):
        """generate_log() should print a confirmation message including the filename."""
        filepath = generate_log(["Event"], directory=str(tmp_path))
        cleanup_files.append(filepath)

        captured = capsys.readouterr()
        filename = os.path.basename(filepath)

        assert "Log written" in captured.out
        assert filename in captured.out

    def test_file_created_and_removed_cleanly(self, tmp_path):
        """The log file should be created in the expected directory and removable cleanly."""
        filepath = generate_log(["Cleanup check"], directory=str(tmp_path))

        # File exists in the expected directory
        assert os.path.dirname(filepath) == str(tmp_path)
        assert os.path.exists(filepath)

        # Teardown: remove the file cleanly
        os.remove(filepath)
        assert not os.path.exists(filepath)
