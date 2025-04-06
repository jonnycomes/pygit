import os
import json
import hashlib
import time
import tempfile
from pathlib import Path

import pytest

from pygit.pygit import (
    get_staged_files,
    get_parent_commit,
    generate_commit_hash,
    save_commit,
    update_head,
)

@pytest.fixture
def repo_dir(tmp_path):
    pygit = tmp_path / ".pygit"
    pygit.mkdir()
    
    # Ensure essential directories exist
    (pygit / "index").parent.mkdir(parents=True, exist_ok=True)
    (pygit / "commits").mkdir(parents=True, exist_ok=True)
    return pygit


def test_get_staged_files(repo_dir):
    index = repo_dir / "index"
    index.write_text("file1.txt abc123\nfile2.txt def456\n")

    result = get_staged_files(repo_dir=repo_dir)
    assert ("file1.txt", "abc123") in result
    assert ("file2.txt", "def456") in result
    assert len(result) == 2

def test_get_parent_commit_none(repo_dir):
    # HEAD doesn't exist yet
    result = get_parent_commit(repo_dir=repo_dir)
    assert result is None

def test_get_parent_commit_existing(repo_dir):
    head = repo_dir / "HEAD"
    head.write_text("deadbeef12345678")
    result = get_parent_commit(repo_dir=repo_dir)
    assert result == "deadbeef12345678"

def test_generate_commit_hash_is_stable():
    commit_data = {
        "message": "Initial commit",
        "timestamp": 1234567890.0,
        "parent": None,
        "files": [("file1.txt", "abc123")]
    }
    hash1 = generate_commit_hash(commit_data)
    hash2 = generate_commit_hash(commit_data)
    assert hash1 == hash2
    assert isinstance(hash1, str)
    assert len(hash1) == 40  # SHA-1 hex digest

def test_save_commit(repo_dir):
    commit_data = {
        "message": "Test commit",
        "timestamp": 1234567890.0,
        "parent": None,
        "files": [("file1.txt", "abc123")]
    }
    commit_hash = generate_commit_hash(commit_data)

    save_commit(commit_hash, commit_data, repo_dir=repo_dir)

    commit_path = repo_dir / "commits" / f"{commit_hash}.json"
    assert commit_path.exists()

    with open(commit_path) as f:
        saved_data = json.load(f)
    assert saved_data == {
        "message": "Test commit",
        "timestamp": 1234567890.0,
        "parent": None,
        "files": [["file1.txt", "abc123"]]
    }

def test_update_head(repo_dir):
    commit_hash = "cafebabe1234"
    update_head(commit_hash, repo_dir=repo_dir)

    head_path = repo_dir / "HEAD"
    assert head_path.exists()
    assert head_path.read_text() == commit_hash


