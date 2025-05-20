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
    try:
        return path.resolve().is_relative_to(repo_path.resolve())
    except AttributeError:
        # Python < 3.9 fallback
        return repo_path.resolve() in path.resolve().parents

