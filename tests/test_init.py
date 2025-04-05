import os
import shutil
from pygit import init

def test_init_creates_repository_structure(tmp_path):
    """
    Test that init() creates the correct pygit directory structure.
    """
    # Change to a temporary directory for testing
    os.chdir(tmp_path)

    # Run the init function
    init()

    # Define expected structure
    assert (tmp_path / ".pygit").is_dir()
    assert (tmp_path / ".pygit" / "objects").is_dir()
    assert (tmp_path / ".pygit" / "refs" / "heads").is_dir()

    head_file = tmp_path / ".pygit" / "HEAD"
    assert head_file.is_file()

    with open(head_file, "r") as f:
        assert f.read().strip() == "ref: refs/heads/master"
