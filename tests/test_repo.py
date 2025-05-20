import tempfile
from pathlib import Path
from pygit.core.repo import get_repo_path, get_parent_commit, update_head, get_head_commit_hash

def test_get_repo_path_returns_path_object():
    path_str = "/tmp/testrepo"
    path_obj = get_repo_path(path_str)
    assert isinstance(path_obj, Path)
    assert str(path_obj) == path_str

def test_get_parent_commit_reads_head_content():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        head_file = repo_path / "HEAD"
        head_file.write_text("abc123\n")
        assert get_parent_commit(repo_path) == "abc123"

        head_file.unlink()
        assert get_parent_commit(repo_path) is None

def test_update_head_writes_to_ref_and_head_directly():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        # Setup HEAD to point to a ref
        head_file = repo_path / "HEAD"
        ref_file = repo_path / "refs" / "heads" / "master"
        ref_file.parent.mkdir(parents=True, exist_ok=True)
        head_file.write_text("ref: refs/heads/master\n")

        update_head(repo_path, "commit123")
        assert ref_file.read_text() == "commit123"

        # Now test detached HEAD case (HEAD content is not a ref)
        head_file.write_text("detachedhash")
        update_head(repo_path, "commit456")
        assert head_file.read_text() == "commit456"

def test_get_head_commit_hash_returns_correct_hash_or_none():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        head_file = repo_path / "HEAD"
        ref_file = repo_path / "refs" / "heads" / "master"
        ref_file.parent.mkdir(parents=True, exist_ok=True)

        head_file.write_text("ref: refs/heads/master\n")
        ref_file.write_text("commit789\n")
        assert get_head_commit_hash(repo_path) == "commit789"

        ref_file.unlink()
        assert get_head_commit_hash(repo_path) is None

        # Also test detached head returns None
        head_file.write_text("detachedhash")
        assert get_head_commit_hash(repo_path) is None
