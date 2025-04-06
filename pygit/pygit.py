import os
import sys
import shutil
import time
import hashlib
import json


def init(repo_dir=".pygit"):
    """
    Initialize a new pygit repository.

    This function creates the necessary directory structure for a pygit
    repository, including the `repo_dir/objects` and `repo_dir/refs/heads` 
    directories. It also creates a `repo_dir/HEAD` file that points to the 
    default branch (refs/heads/master).

    If the repository already exists, it does nothing (thanks to exist_ok=True).
    """
    # Create the necessary directories within the specified repo_dir
    os.makedirs(os.path.join(repo_dir, "objects"), exist_ok=True)
    os.makedirs(os.path.join(repo_dir, "refs", "heads"), exist_ok=True)
    
    # Write the HEAD file in the repo_dir
    with open(os.path.join(repo_dir, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    # Create an empty index file in the repo_dir if it doesn't exist
    index_path = os.path.join(repo_dir, "index")
    if not os.path.exists(index_path):
        with open(index_path, "w") as index_file:
            pass  # Create an empty index file
            
    print("Initialized empty pygit repository.")


def add(file_path, repo_dir=".pygit"):
    """
    Stage a file for commit by copying it to the staging area and updating the index.

    This function reads the specified file, generates a SHA-1 hash of its contents, 
    and copies the file to the staging area (`repo_dir/staging`). It also updates the 
    index (`repo_dir/index`) to record the file’s name and its corresponding hash.

    If the file is already staged, its entry in the index will be updated.
    """

    # Ensure the staging directory exists
    staging_dir = os.path.join(repo_dir, "staging")
    os.makedirs(staging_dir, exist_ok=True)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Read file content and generate blob hash
    with open(file_path, "rb") as f:
        content = f.read()
    blob_hash = hashlib.sha1(content).hexdigest()

    # Copy file to staging area
    dest_path = os.path.join(staging_dir, os.path.basename(file_path))
    shutil.copy(file_path, dest_path)

    # Update the index (no duplicate entries)
    index_path = os.path.join(repo_dir, "index")
    entries = {}
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            for line in f:
                name, hash_ = line.strip().split()
                entries[name] = hash_

    # Overwrite or add the entry
    entries[os.path.basename(file_path)] = blob_hash

    with open(index_path, "w") as f:
        for name, hash_ in entries.items():
            f.write(f"{name} {hash_}\n")

    print(f"File {file_path} staged for commit.")


def commit(message, repo_dir=".pygit"):
    """
    Create a new commit from the currently staged files.

    This function packages the staged files, generates a commit hash,
    saves the commit object to the repository, updates HEAD, and clears
    the staging area and index.
    """
    staged_files = get_staged_files(repo_dir=repo_dir)
    if not staged_files:
        print("Nothing to commit.")
        return

    parent = get_parent_commit(repo_dir=repo_dir)
    timestamp = time.time()

    commit_data = {
        "message": message,
        "timestamp": timestamp,
        "parent": parent,
        "files": staged_files,
    }

    commit_hash = generate_commit_hash(commit_data)
    save_commit(commit_hash, commit_data, repo_dir=repo_dir)
    update_head(commit_hash, repo_dir=repo_dir)
    clear_staging_area(repo_dir=repo_dir)

    print(f"Committed as {commit_hash}")


def get_staged_files(repo_dir=".pygit"):
    """Returns a list of (filename, hash) tuples representing the files staged for commit."""
    index_path = os.path.join(repo_dir, "index")
    if not os.path.exists(index_path):  # Ensure the index file exists
        return []
    with open(index_path, "r") as index_file:
        return [tuple(line.strip().split()) for line in index_file]


def clear_staging_area(repo_dir=".pygit"):
    """Clear the staging area by removing staged files and clearing the index."""

    staging_dir = os.path.join(repo_dir, "staging")
    index_path = os.path.join(repo_dir, "index")

    # Ensure the staging directory exists before listing its files
    if not os.path.isdir(staging_dir):
        os.makedirs(staging_dir)

    # Remove files from the staging area
    if os.path.isdir(staging_dir):
        for file in os.listdir(staging_dir):
            file_path = os.path.join(staging_dir, file)
            os.remove(file_path)

    # Clear the index (staged files list)
    if os.path.exists(index_path):
        os.remove(index_path)

    # Remove the staging directory if it is empty
    if not os.listdir(staging_dir):
        os.rmdir(staging_dir)



def hash_file(file_path):
    """Calculate the hash of the file contents."""
    hash_object = hashlib.sha1()  
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_object.update(chunk)
    return hash_object.hexdigest()


def get_parent_commit(repo_dir=".pygit"):
    """Returns the hash of the current HEAD commit, or None if no commits yet."""
    head_path = os.path.join(repo_dir, "HEAD")
    if not os.path.exists(head_path):
        return None

    with open(head_path, "r") as f:
        return f.read().strip()


def generate_commit_hash(commit_data):
    """Generate a SHA-1 hash based on the commit metadata."""
    commit_string = json.dumps(commit_data, sort_keys=True)
    return hashlib.sha1(commit_string.encode()).hexdigest()

def save_commit(commit_hash, commit_data, repo_dir=".pygit"):
    """Save the commit object as a JSON file in the .pygit/commits directory."""
    commit_dir = os.path.join(repo_dir, "commits")
    os.makedirs(commit_dir, exist_ok=True)

    commit_path = os.path.join(commit_dir, f"{commit_hash}.json")
    with open(commit_path, "w") as f:
        json.dump(commit_data, f, indent=2)

def update_head(commit_hash, repo_dir=".pygit"):
    """Updates the HEAD reference to point to the given commit hash."""
    head_path = os.path.join(repo_dir, "HEAD")
    with open(head_path, "w") as f:
        f.write(commit_hash)


if __name__ == "__main__":
    # Command: init
    if sys.argv[1] == "init":
        init()
    # Command: add
    elif sys.argv[1] == "add":
        if len(sys.argv) < 3:
            print("Error: You must specify a file to add.")
        else:
            file_path = sys.argv[2]
            try:
                add(file_path)
            except FileNotFoundError as e:
                print(e)
    # Command: commit
    elif sys.argv[1] == "commit":
        if "-m" in sys.argv:
            message_index = sys.argv.index("-m") + 1
            if message_index < len(sys.argv):
                message = sys.argv[message_index]
                commit(message)
            else:
                print("Error: Commit message must be provided after -m.")
        else:
            print("Error: -m flag is required to specify a commit message.")
