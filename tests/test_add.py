import os
import shutil
import pytest
from pygit.pygit import add 


def test_add(tmpdir):
    # Create a temporary directory to simulate the repo
    repo_dir = tmpdir.mkdir(".pygit")
    staging_dir = repo_dir.mkdir("staging")  # This is where files will be staged

    # Create a dummy file to add
    file_path = tmpdir.join("file.txt")
    file_path.write("This is a test file.")

    # Call the add function to stage the file
    add(str(file_path), repo_dir=str(repo_dir))

    # Check that the file is now in the staging directory
    staged_file = staging_dir.join("file.txt")
    assert staged_file.exists()  # The file should be staged

    # Optionally, check the file content
    with open(staged_file, 'r') as f:
        content = f.read()
    assert content == "This is a test file."  # The content should match


def test_add_file_not_found(tmpdir):
    # Create a temporary directory to simulate the repo
    repo_dir = tmpdir.mkdir(".pygit")

    # Call add with a non-existent file
    nonexistent_file = tmpdir.join("nonexistent.txt")

    # Test that FileNotFoundError is raised
    with pytest.raises(FileNotFoundError):
        add(str(nonexistent_file), repo_dir=str(repo_dir))