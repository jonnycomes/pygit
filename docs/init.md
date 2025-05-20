# Understanding the `init` Command

## Overview

The `init` command initializes a new pygit repository by creating the essential directory structure and files needed to track and manage version control data. This setup closely mirrors the structure of a Git repository but is simplified for pygit.

## Usage

```bash
pygit init
```

## What happens during `init`?

When you run the `init` command, it performs the following steps inside the specified repository directory (default is `.pygit`):

### 1. Create the `objects` directory

- The `objects` directory is created to store all the objects (commits, blobs, trees) in the repository.
- This directory will eventually hold files representing the data tracked by pygit, named by their SHA-1 hashes.

### 2. Create the `refs/heads` directory

- The `refs` directory holds references to commits, primarily branches.
- Inside `refs`, the `heads` subdirectory is created to store branch pointers.
- For example, the current branch `master` will have its commit hash stored here.

### 3. Create the `HEAD` file

- The `HEAD` file is created at the root of the repository.
- It contains the reference `"ref: refs/heads/master\n"`, meaning the repository starts on the `master` branch.
- `HEAD` points to the current branch or commit, allowing pygit to know which commit is currently checked out.

### 4. Create an empty `index` file

- The `index` file is initialized as an empty JSON object `{}`.
- It will be used to keep track of staged files and their content hashes.
- This index file allows commands like `add` and `commit` to know what changes are staged for the next commit.

### 5. Create a `.pygitignore` file (if it does not exist)

- The `.pygitignore` file is created in the root directory of the repository (the parent of the `.pygit` directory).
- This file allows you to list files and directories that pygit should ignore.
- If the file already exists, it will not be overwritten.
- The file is initialized with a helpful comment:
  
```
# Add files or directories to ignore, one per line
```

### 6. Print confirmation message

- After the setup completes, the command prints:
```
Initialized empty pygit repository.
```

## Summary of directory structure after `init`

```
.pygitignore             # File listing ignored files/directories
.pygit/
├── HEAD                 # File containing "ref: refs/heads/master\n"
├── index                # File containing "{}" (empty JSON object)
├── objects/             # Empty directory for storing Git objects (blobs, commits, trees)
└── refs/
    └── heads/           # Empty directory to store branch references (e.g., master)
```

