from pathlib import Path
from pygit.commands import init

def test_init_creates_repo_structure(tmp_path):
    # Create a fake repo root
    repo_root = tmp_path
    repo_dir = repo_root / ".pygit"

    # Simulate a working directory by calling init from inside the test directory
    # We use init.run(repo_dir), which will create .pygitignore in repo_root
    init.run(repo_dir)

    # Assert pygit structure
    assert repo_dir.exists()
    assert (repo_dir / "objects").is_dir()
    assert (repo_dir / "refs" / "heads").is_dir()

    head_file = repo_dir / "HEAD"
    index_file = repo_dir / "index"
    assert head_file.exists()
    assert index_file.exists()
    assert head_file.read_text() == "ref: refs/heads/master\n"

    # Assert .pygitignore is created in the repo root
    pygitignore_file = repo_root / ".pygitignore"
    assert pygitignore_file.exists()
    assert "# Add files or directories to ignore" in pygitignore_file.read_text()