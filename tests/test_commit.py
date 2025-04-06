import pytest
import os
import shutil
import time
import json
from pygit.pygit import (
    commit, 
    init, 
    add, 
    get_staged_files, 
    clear_staging_area, 
    get_parent_commit
    )

@pytest.fixture
def setup_repo(tmp_path):
    """Fixture to set up a temporary pygit repository for testing."""
    repo_dir = tmp_path / ".pygit"
    
    # Ensure critical directories exist
    os.makedirs(repo_dir / "staging", exist_ok=True)
    os.makedirs(repo_dir / "commits", exist_ok=True)
    os.makedirs(repo_dir / "refs" / "heads", exist_ok=True)
    os.makedirs(repo_dir / "objects", exist_ok=True)
    
    # Ensure the index file exists
    index_path = repo_dir / "index"
    if not index_path.exists():
        index_path.touch() 
    
    # Initialize repository
    init()
    
    yield repo_dir
    
    # Cleanup
    clear_staging_area(repo_dir)
    if index_path.exists():
        os.remove(index_path)


def test_commit_with_staged_files(setup_repo):
    """Test committing with staged files."""
    repo_dir = setup_repo
    file_path = str(repo_dir / "file1.txt")
    
    # Add a file and stage it
    with open(file_path, "w") as f:
        f.write("Test content")
    
    add(file_path, repo_dir=repo_dir)
    
    # Commit the staged file
    commit("Initial commit", repo_dir=repo_dir)
    
    # Check that the commit file exists
    commit_hash = get_parent_commit(repo_dir=repo_dir)  # Should be the commit we just made
    commit_path = repo_dir / "commits" / f"{commit_hash}.json"
    assert commit_path.exists()
    
    # Check the staged files list is empty after the commit
    staged_files = get_staged_files(repo_dir=repo_dir)
    assert not staged_files

def test_commit_empty_staging_area(setup_repo):
    """Test committing with an empty staging area."""
    repo_dir = setup_repo
    
    # Try to commit with no staged files
    commit("Empty commit", repo_dir=repo_dir)
    
    # Ensure nothing has changed (no commit file should be created)
    assert not os.listdir(repo_dir / "commits")

def test_commit_with_multi_word_message(setup_repo):
    """Test committing with a multi-word message."""
    repo_dir = setup_repo
    file_path = str(repo_dir / "file1.txt")
    
    # Add a file and stage it
    with open(file_path, "w") as f:
        f.write("Test content")
    
    add(file_path, repo_dir=repo_dir)
    
    # Commit with a multi-word message
    commit("Fixing bug in file1", repo_dir=repo_dir)
    
    # Check that the commit file exists
    commit_hash = get_parent_commit(repo_dir=repo_dir)
    commit_path = repo_dir / "commits" / f"{commit_hash}.json"
    assert commit_path.exists()
    
    # Check that the commit message was saved correctly
    with open(commit_path, "r") as f:
        commit_data = json.load(f)
    assert commit_data["message"] == "Fixing bug in file1"

def test_commit_index_and_staging_area_cleared(setup_repo):
    """Test that the staging area and index are cleared after a commit."""
    repo_dir = setup_repo
    file_path = str(repo_dir / "file1.txt")
    
    # Add and stage a file
    with open(file_path, "w") as f:
        f.write("Test content")
    
    add(file_path, repo_dir=repo_dir)
    
    # Check that the file is staged
    staged_files = get_staged_files(repo_dir=repo_dir)
    assert staged_files
    
    # Commit the file
    commit("Committing file1", repo_dir=repo_dir)
    
    
    # Check that the index is cleared
    index_path = os.path.join(repo_dir, "index")
    assert not os.path.exists(index_path)

    # Check that the staging area is cleared
    staging_dir = repo_dir / "staging"
    if os.path.exists(staging_dir):
        assert not os.listdir(staging_dir)  # Check if it is empty
    else:
        # Ensure the directory doesn't exist after clearing
        assert not os.path.isdir(staging_dir)


def test_commit_updates_head(setup_repo):
    """Test that the HEAD file is updated after a commit."""
    repo_dir = setup_repo
    file_path = str(repo_dir / "file1.txt")
    
    # Add and stage a file
    with open(file_path, "w") as f:
        f.write("Test content")
    
    add(file_path, repo_dir=repo_dir)
    
    # Commit the file
    commit("Committing file1", repo_dir=repo_dir)
    
    # Check that the HEAD file is updated
    head_path = os.path.join(repo_dir, "HEAD")
    with open(head_path, "r") as f:
        head_commit_hash = f.read().strip()
    
    commit_hash = get_parent_commit(repo_dir=repo_dir)
    assert head_commit_hash == commit_hash
