from pathlib import Path
from pygit.core.repo import get_repo_path, get_head_commit_hash, is_ignored
from pygit.core.index import load_index
from pygit.core.objects import load_commit_tree
from pygit.core.hashing import hash_file

def run():
    repo_path = get_repo_path(".pygit")
    index = load_index(repo_path)
    head_commit_hash = get_head_commit_hash(repo_path)
    committed = load_commit_tree(repo_path, head_commit_hash)
    working = get_working_directory_files(repo_path)

    staged = [f for f, h in index.items() if f not in committed or committed.get(f) != h]
    modified = [f for f, h in working.items() if f in index and index[f] != h]
    untracked = [f for f in working if f not in index]

    if staged:
        print("Changes to be committed:")
        for f in staged:
            print(f"  staged:   {f}")
    else:
        print("No changes to be committed.")

    if modified:
        print("\nChanges not staged for commit:")
        for f in modified:
            print(f"  modified: {f}")

    if untracked:
        print("\nUntracked files:")
        for f in untracked:
            print(f"  untracked: {f}")

def get_working_directory_files(repo_path: Path) -> dict:
    files = {}
    for path in Path(".").rglob("*"):
        if path.is_file() and not is_ignored(path, repo_path):
            files[str(path)] = hash_file(path)
    return files

