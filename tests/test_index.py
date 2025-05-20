import json
import tempfile
from pathlib import Path
from pygit.core.index import load_index, save_index, clear_index

def test_load_index_returns_empty_if_missing():
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        index = load_index(repo_path)
        assert index == {}

def test_save_and_load_index():
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        sample_index = {"file1.txt": "abc123", "file2.txt": "def456"}
        
        save_index(repo_path, sample_index)
        loaded_index = load_index(repo_path)
        
        assert loaded_index == sample_index
        # Ensure it's valid JSON on disk
        index_path = repo_path / "index"
        with open(index_path) as f:
            assert json.load(f) == sample_index

def test_clear_index_removes_index_and_staging_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        
        # Create dummy index file
        index_path = repo_path / "index"
        index_path.write_text(json.dumps({"file.txt": "abc123"}))

        # Create dummy staging files
        staging_dir = repo_path / "staging"
        staging_dir.mkdir()
        (staging_dir / "file.txt").write_text("temp content")
        
        assert index_path.exists()
        assert any(staging_dir.iterdir())

        clear_index(repo_path)

        assert not index_path.exists()
        assert not staging_dir.exists()
