from pathlib import Path
import shutil
import sys
from pygit.core.index import load_index, save_index
from pygit.core.hashing import hash_file
from pygit.core.repo import is_ignored 

def run(file_path, repo_dir=".pygit"):
    """
    Stage a file for commit, unless it's ignored or missing.
    """
    file_path = Path(file_path)
    repo_path = Path(repo_dir)

    if not file_path.exists():
        print(f"'{file_path}' does not exist. Nothing added.")
        return

    if is_ignored(file_path, repo_path):
        print(f"'{file_path}' is ignored. Skipping.")
        return

    staging_dir = repo_path / "staging"
    staging_dir.mkdir(parents=True, exist_ok=True)

    file_hash = hash_file(file_path)
    shutil.copy(file_path, staging_dir / file_path.name)

    index = load_index(repo_path)
    index[file_path.name] = file_hash
    save_index(repo_path, index)

    print(f"Staged {file_path.name}")