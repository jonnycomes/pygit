import tempfile
from pathlib import Path
from pygit.core.hashing import hash_file

def test_hash_file_consistent_and_differs_for_different_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        file1 = temp_path / "file1.txt"
        file1.write_text("Hello, pygit!")

        file2 = temp_path / "file2.txt"
        file2.write_text("Hello, pygit!!")

        # Hash of file1 twice should be identical
        h1a = hash_file(file1)
        h1b = hash_file(file1)
        assert h1a == h1b

        # Hash of file1 and file2 should differ
        h2 = hash_file(file2)
        assert h1a != h2

        # Known hash for the exact content of file1
        import hashlib
        expected_hash = hashlib.sha1(b"Hello, pygit!").hexdigest()
        assert h1a == expected_hash
