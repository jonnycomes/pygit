from pathlib import Path

def run(repo_dir=".pygit"):
    """
    Initialize a new pygit repository.
    """
    repo_path = Path(repo_dir)
    (repo_path / "objects").mkdir(parents=True, exist_ok=True)
    (repo_path / "refs" / "heads").mkdir(parents=True, exist_ok=True)

    (repo_path / "HEAD").write_text("ref: refs/heads/master\n")
    (repo_path / "index").write_text("{}")

    repo_root = repo_path.parent
    pygitignore_path = repo_root / ".pygitignore"
    if not pygitignore_path.exists():
        pygitignore_path.write_text("# Add files or directories to ignore, one per line\n")

    print("Initialized empty pygit repository.")
