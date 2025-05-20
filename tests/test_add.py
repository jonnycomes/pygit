import pytest
from pathlib import Path
from pygit.commands import add
from pygit.core.index import load_index
from pygit.core.hashing import hash_file

def test_add_stages_file(tmp_path, capsys):
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

    # Output should mention the staged file
    captured = capsys.readouterr()
    assert "Staged hello.txt" in captured.out

def test_add_nonexistent_file_prints_message(tmp_path, capsys):
    repo_dir = tmp_path / ".pygit"
    repo_dir.mkdir()

    missing_file = tmp_path / "not_there.txt"
    add.run(missing_file, repo_dir=repo_dir)

    captured = capsys.readouterr()
    assert "does not exist" in captured.out

def test_add_ignored_file_skips(tmp_path, capsys):
    # Setup: .pygitignore contains hello.txt
    repo_dir = tmp_path / ".pygit"
    repo_dir.mkdir()
    (repo_dir / "index").write_text("{}")
    (tmp_path / ".pygitignore").write_text("hello.txt\n")

    file_to_add = tmp_path / "hello.txt"
    file_to_add.write_text("Hello, ignored!")

    add.run(file_to_add, repo_dir=repo_dir)

    # Should not appear in staging or index
    assert not (repo_dir / "staging" / "hello.txt").exists()
    index = load_index(repo_dir)
    assert "hello.txt" not in index

    captured = capsys.readouterr()
    assert "is ignored" in captured.out