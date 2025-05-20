import pytest
from pathlib import Path
from pygit.commands import add
from pygit.core.index import load_index
from pygit.core.hashing import hash_file

def test_add_stages_file(tmp_path):
    # Setup: create a temporary repo and a file to add
    repo_dir = tmp_path / ".pygit"
    repo_dir.mkdir()
    (repo_dir / "index").write_text("{}")  # initialize empty index

    file_to_add = tmp_path / "hello.txt"
    file_to_add.write_text("Hello, pygit!")

    # Act: run the add command
    add.run(file_to_add, repo_dir=repo_dir)

    # Assert: file is copied to staging
    staging_file = repo_dir / "staging" / "hello.txt"
    assert staging_file.exists()
    assert staging_file.read_text() == "Hello, pygit!"

    # Assert: index contains correct hash
    index = load_index(repo_dir)
    expected_hash = hash_file(file_to_add)
    assert index["hello.txt"] == expected_hash

def test_add_nonexistent_file_raises(tmp_path):
    repo_dir = tmp_path / ".pygit"
    repo_dir.mkdir()

    with pytest.raises(FileNotFoundError):
        add.run(tmp_path / "not_there.txt", repo_dir=repo_dir)
