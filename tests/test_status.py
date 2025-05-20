import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from pygit.commands import status

@pytest.fixture
def mock_repo(tmp_path):
    repo_path = tmp_path / ".pygit"
    repo_path.mkdir()
    (repo_path / "HEAD").write_text("ref: refs/heads/main")
    ref_path = repo_path / "refs/heads"
    ref_path.mkdir(parents=True)
    (ref_path / "main").write_text("abc123")
    return tmp_path, repo_path

@patch("pygit.commands.status.load_index")
@patch("pygit.commands.status.load_commit_tree")
@patch("pygit.commands.status.get_head_commit_hash")
@patch("pygit.commands.status.get_repo_path")
@patch("pygit.commands.status.get_working_directory_files")
def test_status_output(mock_working, mock_repo_path, mock_head, mock_commit_tree, mock_index, mock_repo, capsys):

    tmp_path, repo_path = mock_repo
    mock_repo_path.return_value = repo_path
    mock_head.return_value = "abc123"
    
    # Set up index, committed tree, and working dir states
    mock_index.return_value = {
        "file1.txt": "hash1",
        "file2.txt": "hash2",
        "file3.txt": "hash3"
    }
    
    mock_commit_tree.return_value = {
        "file1.txt": "hash1",
        "file2.txt": "oldhash"
    }

    mock_working.return_value = {
        "file2.txt": "hash2",       # modified (diff from index)
        "file3.txt": "hash3",       # clean
        "file4.txt": "hash4"        # untracked
    }

    # Run status
    status.run()
    
    captured = capsys.readouterr()
    output = captured.out

    assert "staged:   file2.txt" in output
    assert "staged:   file3.txt" in output
    assert "untracked: file4.txt" in output

    # These should *not* appear:
    assert "modified: file2.txt" not in output
    assert "file1.txt" not in output  # shouldn't appear at all


@patch("pygit.commands.status.get_working_directory_files")
@patch("pygit.commands.status.is_ignored", return_value=False)
@patch("pygit.commands.status.hash_file", return_value="fakehash")
def test_get_working_directory_files(mock_hash, mock_ignored, mock_get_files, tmp_path):
    # Setup files
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")

    repo_path = tmp_path / ".pygit"
    repo_path.mkdir()

    # Patch Path('.') to return tmp_path
    with patch("pygit.commands.status.Path", return_value=tmp_path):
        files = status.get_working_directory_files(repo_path)

    assert all(k.endswith(".txt") for k in files)
    assert all(v == "fakehash" for v in files.values())
