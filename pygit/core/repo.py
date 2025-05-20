import fnmatch
from pathlib import Path

def get_repo_path(repo_dir: str) -> Path:
    return Path(repo_dir)

def get_parent_commit(repo_path: Path):
    head_file = repo_path / "HEAD"
    return head_file.read_text().strip() if head_file.exists() else None

def update_head(repo_path: Path, commit_hash: str):
    head_content = (repo_path / "HEAD").read_text().strip()
    if head_content.startswith("ref: "):
        ref_path = repo_path / head_content[5:]
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_text(commit_hash)
    else:
        # Detached HEAD
        (repo_path / "HEAD").write_text(commit_hash)

def get_head_commit_hash(repo_path: Path):
    head_ref = (repo_path / "HEAD").read_text().strip()
    if head_ref.startswith("ref: "):
        ref_path = repo_path / head_ref[5:]
        if ref_path.exists():
            return ref_path.read_text().strip()
    return None

def is_ignored(path: Path, repo_path: Path) -> bool:
    # Normalize and resolve paths
    path = path.resolve()
    repo_path = repo_path.resolve()
    repo_root = repo_path.parent
    pygitignore_path = repo_root / ".pygitignore"

    # Always ignore anything inside .pygit (the repo path)
    if repo_path in path.parents or path == repo_path:
        return True

    # Ignore the .pygitignore file itself
    if path == pygitignore_path.resolve():
        return True

    # If there's no .pygitignore, nothing else to ignore
    if not pygitignore_path.exists():
        return False

    patterns = load_ignore_patterns(pygitignore_path)

    try:
        rel_path = path.relative_to(repo_root)
    except ValueError:
        return False  # If path is outside the repo, don't ignore it

    # Match against each pattern using fnmatch
    return any(fnmatch.fnmatch(str(rel_path), pat) for pat in patterns)
    
def load_ignore_patterns(ignore_file: Path) -> list[str]:
    if not ignore_file.exists():
        return []
    with ignore_file.open() as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]
