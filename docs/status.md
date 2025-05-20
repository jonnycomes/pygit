# Understanding the `status` Command

## Overview

The `status` command shows the current state of your working directory and staging area. It helps you understand which files are ready to be committed, which have been modified but not staged, and which are untracked.

This mirrors the behavior of `git status`, offering a concise summary of pending changes in your pygit repository.

## Usage

```
pygit status
```

## What does `status` show?

When you run the `status` command, pygit compares three versions of each file:

1. **The committed version** – the latest version stored in the repository's current `HEAD` commit.
2. **The index (staging area)** – the version that will be committed next.
3. **The working directory** – the current version of the file on disk.

Based on these comparisons, it groups files into three categories:

### 1. Changes to be committed

- These files are staged and will be included in the next commit.
- This typically means the version in the index differs from the version in the last commit.
- Output example:

```
Changes to be committed:
  staged:   example.txt
```

### 2. Changes not staged for commit

- These files exist in the index but have been modified since being staged.
- You need to run `pygit add` again to stage the updated version.
- Output example:

```
Changes not staged for commit:
  modified: notes.md
```

### 3. Untracked files

- These files are in the working directory but not tracked by pygit (i.e., not in the index).
- You can begin tracking them with `pygit add`.
- Output example:

```
Untracked files:
  untracked: newfile.py
```

## How it works internally

The `status` command performs the following steps:

1. **Load repository state**:
   - Retrieves the repository path (`.pygit`)
   - Loads the current index and HEAD commit tree

2. **Hash working directory files**:
   - Recursively scans the working directory (excluding ignored files)
   - Computes content hashes for each file

3. **Compare file states**:
   - Identifies:
     - **Staged** files: in index but different from HEAD commit
     - **Modified** files: in working directory and index, but hashes differ
     - **Untracked** files: in working directory but not in index

4. **Print status summary**:
   - Outputs the status of each relevant file grouped by category

## Example output

```
Changes to be committed:
  staged:   script.py
  staged:   README.md

Changes not staged for commit:
  modified: config.json

Untracked files:
  untracked: todo.txt
```
