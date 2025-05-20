import time
from pygit.core.index import load_index, clear_index
from pygit.core.commit_utils import generate_commit_hash, save_commit
from pygit.core.repo import get_repo_path, get_parent_commit, update_head

def run(message, repo_dir=".pygit"):
    """
    Commit staged changes.
    """
    repo_path = get_repo_path(repo_dir)
    index = load_index(repo_path)

    if not index:
        print("Nothing to commit.")
        return

    commit_data = {
        "message": message,
        "timestamp": time.time(),
        "parent": get_parent_commit(repo_path),
        "files": index,
    }

    commit_hash = generate_commit_hash(commit_data)
    save_commit(repo_path, commit_hash, commit_data)
    update_head(repo_path, commit_hash)
    clear_index(repo_path)

    print(f"Committed as {commit_hash}")
