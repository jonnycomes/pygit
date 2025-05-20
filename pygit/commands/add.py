from pathlib import Path
import shutil
from pygit.core.index import load_index, save_index
from pygit.core.hashing import hash_file

def run(file_path, repo_dir=".pygit"):
    """
    Stage a file for commit.
    """
    file_path = Path(file_path)
    repo_path = Path(repo_dir)
    staging_dir = repo_path / "staging"
    staging_dir.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    file_hash = hash_file(file_path)
    shutil.copy(file_path, staging_dir / file_path.name)

    index = load_index(repo_path)
    index[file_path.name] = file_hash
    save_index(repo_path, index)

    print(f"Staged {file_path.name}")
