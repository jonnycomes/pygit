import os
import shutil
import pytest

from pygit.pygit import init, add, get_staged_files, clear_staging_area

REPO_DIR = ".pygit"
STAGING_DIR = os.path.join(REPO_DIR, "staging")
INDEX_PATH = os.path.join(REPO_DIR, "index")


def test_add(tmpdir):
    # Create a temporary directory to simulate the repo
    repo_dir = tmpdir.mkdir(".pygit")
    staging_dir = repo_dir.mkdir("staging")  # This is where files will be staged

    # Create a dummy file to add
    file_path = tmpdir.join("file.txt")
    file_path.write("This is a test file.")

    # Call the add function to stage the file
    add(str(file_path), repo_dir=str(repo_dir))

    # Check that the file is now in the staging directory
    staged_file = staging_dir.join("file.txt")
    assert staged_file.exists()  # The file should be staged

    # Optionally, check the file content
    with open(staged_file, 'r') as f:
        content = f.read()
    assert content == "This is a test file."  # The content should match


def test_add_file_not_found(tmpdir):
    # Create a temporary directory to simulate the repo
    repo_dir = tmpdir.mkdir(".pygit")

    # Call add with a non-existent file
    nonexistent_file = tmpdir.join("nonexistent.txt")

    # Test that FileNotFoundError is raised
    with pytest.raises(FileNotFoundError):
        add(str(nonexistent_file), repo_dir=str(repo_dir))



@pytest.fixture
def setup_repo(tmp_path, monkeypatch):
    # Change working directory to the temp path
    monkeypatch.chdir(tmp_path)
    init()

    # Create a sample file
    test_file = tmp_path / "example.txt"
    test_file.write_text("Hello, pygit!")

    yield test_file

    # Clean up
    shutil.rmtree(tmp_path)


def test_add_creates_staged_file_and_index_entry(setup_repo):
    test_file = setup_repo
    add(str(test_file))

    # Check that the file was copied to staging
    staged_file_path = os.path.join(STAGING_DIR, "example.txt")
    assert os.path.exists(staged_file_path)

    # Check that the index file exists and contains correct entry
    assert os.path.exists(INDEX_PATH)
    with open(INDEX_PATH) as f:
        index_contents = f.read()
    assert "example.txt" in index_contents


def test_get_staged_files_returns_correct_list(setup_repo):
    test_file = setup_repo
    add(str(test_file))

    staged = get_staged_files()
    assert staged == ["example.txt"]


def test_clear_staging_area_removes_staging_and_index(setup_repo):
    test_file = setup_repo
    add(str(test_file))

    clear_staging_area()

    # Staging directory should still exist but be empty
    assert os.path.isdir(STAGING_DIR)
    assert len(os.listdir(STAGING_DIR)) == 0

    # Index should be gone
    assert not os.path.exists(INDEX_PATH)

def test_adding_same_file_twice_only_once_in_index(setup_repo):
    test_file = setup_repo
    add(str(test_file))
    add(str(test_file))  # Add same file again

    # Check index has only one entry for the file
    with open(INDEX_PATH) as f:
        lines = f.read().splitlines()
    filenames = [line.split()[0] for line in lines]
    assert filenames.count("example.txt") == 1


    # Only one staged file exists
    staged_files = os.listdir(STAGING_DIR)
    assert staged_files.count("example.txt") == 1


def test_staging_multiple_files(tmp_path, monkeypatch):
    # Setup repo
    monkeypatch.chdir(tmp_path)
    init()

    # Create two files
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("First file")
    file2.write_text("Second file")

    # Add both
    add(str(file1))
    add(str(file2))

    # Verify both in staging
    assert set(os.listdir(STAGING_DIR)) == {"file1.txt", "file2.txt"}

    # Verify both in index
    with open(INDEX_PATH) as f:
        index_entries = f.read().splitlines()
    filenames = {line.split()[0] for line in index_entries}
    assert filenames == {"file1.txt", "file2.txt"}

