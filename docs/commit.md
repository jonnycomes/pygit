# Understanding the `commit` Command

## Overview

The `commit` command records a snapshot of the current staged files and saves them as a new commit object in the repository. Each commit contains metadata such as a message, timestamp, parent commit reference, and a snapshot of the staged file hashes.

## Usage

``` bash  
pygit commit -m "Your commit message here"  
```

## What happens during `commit`?

When you run the `commit` command, the following steps occur:

### 1. Load the index

- The index file is loaded to determine which files have been staged.
- If the index is empty, no commit is made and the message `Nothing to commit.` is printed.

### 2. Construct the commit data

- A commit dictionary is created containing:
  - `message`: The user-provided commit message.
  - `timestamp`: The current Unix timestamp.
  - `parent`: The hash of the previous commit (from `HEAD`).
  - `files`: A snapshot of the current index (filename to hash mapping).

### 3. Generate a commit hash

- A hash is computed from the commit data using a consistent hashing strategy.
- This hash becomes the identifier for the new commit object.

### 4. Save the commit

- The commit object is saved to the `objects` directory under its hash filename.

### 5. Update `HEAD`

- The `HEAD` reference is updated to point to the new commit hash.
- If `HEAD` is pointing to a branch (like `master`), that branch is updated.

### 6. Clear the index

- After the commit is completed, the index and the staging area are cleared.
- This prepares the repository for staging the next set of changes.

### 7. Print confirmation message

- The final message indicates the commit was successful:

``` bash  
Committed as <commit_hash>  
```

## Summary of files and changes


```
.pygit/
├── HEAD                       # Updated to point to new commit hash
├── index                      # Emptied after commit
├── objects/
│   └── <commit_hash>          # New file storing the serialized commit data
├── staging/                   # Removed after clearing index (if empty)
└── refs/
    └── heads/
        └── master             # Updated with the new commit hash (if on master)
```