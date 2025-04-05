import os
import sys

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


if __name__ == "__main__":
    if sys.argv[1] == "init":
        init()
