import json
from pathlib import Path

def load_index(repo_path: Path):
    index_file = repo_path / "index"
    if not index_file.exists():
        return {}
    return dict(line.strip().split() for line in index_file.read_text().splitlines())

def save_index(repo_path: Path, index: dict):
    index_file = repo_path / "index"
    lines = [f"{k} {v}" for k, v in index.items()]
    index_file.write_text("\n".join(lines) + "\n")

def clear_index(repo_path: Path):
    (repo_path / "index").unlink(missing_ok=True)
    staging_dir = repo_path / "staging"
    if staging_dir.exists():
        for f in staging_dir.iterdir():
            f.unlink()
        staging_dir.rmdir()
