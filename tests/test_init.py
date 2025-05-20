from pathlib import Path
from pygit.commands import init

def test_init_creates_repo_structure(tmp_path):
    repo_dir = tmp_path / ".pygit"

    # Run the init command
    init.run(repo_dir)

    # Check that .pygit directory was created
    assert repo_dir.exists()
    assert (repo_dir / "objects").is_dir()
    assert (repo_dir / "refs" / "heads").is_dir()

    # Check that HEAD and index files were created
    head_file = repo_dir / "HEAD"
    index_file = repo_dir / "index"

    assert head_file.exists()
    assert index_file.exists()

    # Check HEAD contents
    assert head_file.read_text() == "ref: refs/heads/master\n"
