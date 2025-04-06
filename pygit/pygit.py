import os
import sys
import shutil
import time
import hashlib
import json


def init():
    """
    Initialize a new pygit repository.

    This function creates the necessary directory structure for a pygit
    repository, including the `.pygit/objects` and `.pygit/refs/heads` 
    directories. It also creates a `.pygit/HEAD` file that points to the 
    default branch (refs/heads/master).

    If the repository already exists, it does nothing (thanks to exist_ok=True).
    """
    os.makedirs(".pygit/objects", exist_ok=True)
    os.makedirs(".pygit/refs/heads", exist_ok=True)
    with open(".pygit/HEAD", "w") as f:
        f.write("ref: refs/heads/master\n")
    print("Initialized empty pygit repository.")



def add(file_path, repo_dir=".pygit"):
    """Stage a file for commit by copying it to the staging area and updating the index."""

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


def get_staged_files(repo_dir=".pygit"):
    """Returns a list of files currently staged for commit."""
    
    staged_files = []
    index_path = os.path.join(repo_dir, "index")
    
    if os.path.exists(index_path):
        with open(index_path, "r") as index_file:
            staged_files = [line.split()[0] for line in index_file.readlines()]
    
    return staged_files

def clear_staging_area(repo_dir=".pygit"):
    """Clear the staging area by removing staged files and clearing the index."""
    
    staging_dir = os.path.join(repo_dir, "staging")
    index_path = os.path.join(repo_dir, "index")
    
    # Remove files from the staging area
    for file in os.listdir(staging_dir):
        file_path = os.path.join(staging_dir, file)
        os.remove(file_path)
    
    # Clear the index (staged files list)
    if os.path.exists(index_path):
        os.remove(index_path)
    
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


