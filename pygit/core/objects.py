import json
import hashlib
from pathlib import Path
from typing import Optional

def generate_commit_hash(commit_data):
    data_str = json.dumps(commit_data, sort_keys=True)
    return hashlib.sha1(data_str.encode()).hexdigest()

def save_commit(repo_path: Path, commit_hash: str, commit_data: dict):
    commits_dir = repo_path / "commits"
    commits_dir.mkdir(exist_ok=True)
    (commits_dir / f"{commit_hash}.json").write_text(json.dumps(commit_data, indent=2))

def load_commit_tree(repo_path: Path, commit_hash: Optional[str]) -> dict:
    if not commit_hash:
        return {}
    commit_path = repo_path / "commits" / f"{commit_hash}.json"
    if not commit_path.exists():
        return {}
    commit = json.loads(commit_path.read_text())
    return commit.get("files", {})
