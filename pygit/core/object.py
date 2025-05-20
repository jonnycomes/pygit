import json
import hashlib
from pathlib import Path

def generate_commit_hash(commit_data):
    data_str = json.dumps(commit_data, sort_keys=True)
    return hashlib.sha1(data_str.encode()).hexdigest()

def save_commit(repo_path: Path, commit_hash: str, commit_data: dict):
    commits_dir = repo_path / "commits"
    commits_dir.mkdir(exist_ok=True)
    (commits_dir / f"{commit_hash}.json").write_text(json.dumps(commit_data, indent=2))
