import tempfile
from pathlib import Path
import json
from pygit.core.objects import generate_commit_hash, save_commit

def test_generate_commit_hash_deterministic_and_differs_with_data():
    commit1 = {"message": "first", "timestamp": 12345, "parent": None, "files": {"file.txt": "abc123"}}
    commit2 = {"message": "second", "timestamp": 12345, "parent": None, "files": {"file.txt": "abc123"}}
    
    hash1 = generate_commit_hash(commit1)
    hash2 = generate_commit_hash(commit1)  # same data, should be same hash
    hash3 = generate_commit_hash(commit2)  # different message, different hash
    
    assert hash1 == hash2
    assert hash1 != hash3

def test_save_commit_creates_file_with_correct_content():
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        commit_data = {"message": "test commit", "files": {}}
        commit_hash = generate_commit_hash(commit_data)
        
        save_commit(repo_path, commit_hash, commit_data)
        
        commit_file = repo_path / "commits" / f"{commit_hash}.json"
        assert commit_file.exists()
        
        content = json.loads(commit_file.read_text())
        assert content == commit_data
