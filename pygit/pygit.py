import os
import sys
import shutil
import time
import hashlib


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
    """Stage a file for commit by copying it to the staging area and adding it to the index."""
    
    # Ensure the staging directory exists
    staging_dir = os.path.join(repo_dir, "staging")
    os.makedirs(staging_dir, exist_ok=True)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Copy the file to the staging area
    dest_path = os.path.join(staging_dir, os.path.basename(file_path))
    shutil.copy(file_path, dest_path)

    # Calculate the file hash (could be a sha1 or sha256 hash)
    file_hash = hash_file(file_path)

    # Add the file and hash to the index
    index_path = os.path.join(repo_dir, "index")
    with open(index_path, "a") as index_file:
        index_file.write(f"{os.path.basename(file_path)} {file_hash}\n")
    
    print(f"File {file_path} staged for commit.")
    
def hash_file(file_path):
    """Calculate the hash of the file contents."""
    hash_object = hashlib.sha1()  # You can choose another hash method like sha256
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_object.update(chunk)
    return hash_object.hexdigest()




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


