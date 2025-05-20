from pathlib import Path

def run(repo_dir=".pygit"):
    """
    Initialize a new pygit repository.
    """
    repo_path = Path(repo_dir)
    (repo_path / "objects").mkdir(parents=True, exist_ok=True)
    (repo_path / "refs" / "heads").mkdir(parents=True, exist_ok=True)

    (repo_path / "HEAD").write_text("ref: refs/heads/master\n")
    (repo_path / "index").touch(exist_ok=True)

    print("Initialized empty pygit repository.")
