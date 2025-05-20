import json
from pathlib import Path

def load_index(repo_path: Path) -> dict:
    """
    Load the index file as a dictionary of filename to hash.
    If the index file does not exist, return an empty dictionary.
    """
    index_file = repo_path / "index"
    if not index_file.exists():
        return {}
    return json.loads(index_file.read_text())

def save_index(repo_path: Path, index: dict) -> None:
    """
    Save the index dictionary to the index file in JSON format.
    """
    index_file = repo_path / "index"
    index_file.write_text(json.dumps(index, indent=2))

def clear_index(repo_path: Path):
    (repo_path / "index").unlink(missing_ok=True)
    staging_dir = repo_path / "staging"
    if staging_dir.exists():
        for f in staging_dir.iterdir():
            f.unlink()
        staging_dir.rmdir()
