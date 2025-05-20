from pathlib import Path

def get_repo_path(repo_dir: str) -> Path:
    return Path(repo_dir)

def get_parent_commit(repo_path: Path):
    head_file = repo_path / "HEAD"
    return head_file.read_text().strip() if head_file.exists() else None

def update_head(repo_path: Path, commit_hash: str):
    (repo_path / "HEAD").write_text(commit_hash)
