import json
import tempfile
from pathlib import Path
from pygit.commands import init, add, commit
from pygit.core.index import load_index
from pygit.core.repo import get_head_commit_hash

def test_commit_creates_commit_file_and_clears_index():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # 1. Initialize repo
        init.run(repo_dir=temp_path / ".pygit")

        # 2. Create and add a file
        file_path = temp_path / "hello.txt"
        file_path.write_text("Hello, pygit!")
        add.run(file_path, repo_dir=temp_path / ".pygit")

        # 3. Commit the file
        commit.run("Initial commit", repo_dir=temp_path / ".pygit")

        # 4. Check commit file exists
        head_hash = get_head_commit_hash(temp_path / ".pygit")
        commit_file = temp_path / ".pygit" / "commits" / f"{head_hash}.json"
        assert commit_file.exists(), "Commit file was not created"

        # 5. Validate commit contents
        data = json.loads(commit_file.read_text())
        assert data["message"] == "Initial commit"
        assert isinstance(data["timestamp"], float)
        assert isinstance(data["files"], dict)
        assert "hello.txt" in data["files"]

        # 6. Check index was cleared
        assert load_index(temp_path / ".pygit") == {}
