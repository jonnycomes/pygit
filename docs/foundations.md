# Foundations of Version Control

## Overview

This document explains the foundational concepts behind Git — and by extension, pygit. It covers the key components and terminology you need to understand to follow the logic of how Git (and pygit) work under the hood.

This guide is not a manual for a specific command, but a bird’s-eye view of how all the parts fit together.

---

## Key Concepts

### Repository

A **repository** is a collection of all your project's version history. In Git, this is usually stored in a `.git/` folder. In pygit, we use a `.pygit/` folder.

The repository contains:

- Objects representing file contents and commits  
- References (branches)  
- The current `HEAD` pointer  
- The index (staging area)

---

### Working Directory

The **working directory** is where you edit files. It’s your actual project folder.

**Example:**  
If you have a file called `hello.txt` and you edit it in your code editor, that change is made in the working directory.

---

### Index (Staging Area)

The **index** (or staging area) is a place where you prepare changes before committing them.

When you run:
```
pygit add hello.txt
```

it adds the file’s content hash to the index and copies the file into `.pygit/staging/`.

The index tracks which versions of files are ready to be committed.  
This lets you control what gets committed, even if you have other changes in your working directory.

---

### Commit

A **commit** is a snapshot of the staged files at a point in time.

Each commit records:

- A message describing the change  
- A timestamp  
- The set of files (as stored in the index)  
- A reference to the parent commit (unless it’s the first commit)

Commits are **immutable**. Once you create one, it’s saved as an object (in `.pygit/objects/` in pygit) and referenced by a **hash** (its ID).

---

### HEAD

`HEAD` is a pointer to the current commit (or the current branch, which then points to a commit).

In pygit:

`.pygit/HEAD` contains something like:  
```  
ref: refs/heads/master  
```

This means "the current branch is `master`," and `.pygit/refs/heads/master` contains the hash of the most recent commit on that branch.

This chain of references lets Git (or pygit) know where you are in the project history.

---

### Branch

A **branch** is just a named pointer to a commit.  
In Git, branches live in `.git/refs/heads/`.

In pygit, they live in `.pygit/refs/heads/`.

When you commit, the branch pointer (like `master`) gets updated to point to the new commit.

`HEAD` points to the current branch, which points to the latest commit.

---

### Object Store

The **object store** is where all content is stored, hashed by their contents.  
In Git, these are blobs, trees, and commits.

In pygit, we simplify this by storing commits and file blobs as JSON files named by their SHA-1 hash.

**For example:**

A file called `hello.txt` with content `"Hello, world!"` might be hashed as `abc123...`

That content gets stored as `.pygit/objects/abc123...`

---

## Example Flow

Let’s say you do the following:

```
pygit init  
```  
Creates `.pygit/`, including `HEAD`, `refs/`, `index`, and `objects/`.

You create a file: `hello.txt`

```
pygit add hello.txt  
```  
- Hashes the file’s content  
- Copies the file into `.pygit/staging/`  
- Updates index with the file name and its hash

```
pygit commit -m "Initial commit"  
```  
- Reads the index  
- Creates a commit object with your message, timestamp, and file info  
- Stores it in `.pygit/objects/` under a hash  
- Updates the `master` branch to point to this commit  
- Clears the index

Now your project has a versioned snapshot.

---

## Summary

| Term              | What it means                            | Where it lives in pygit               |
|-------------------|-------------------------------------------|----------------------------------------|
| Working Directory | Your current project files                | On disk                                |
| Index             | Staging area for next commit              | `.pygit/index`                         |
| Commit            | Snapshot of staged files + metadata       | `.pygit/objects/<hash>`                |
| HEAD              | Pointer to current branch/commit          | `.pygit/HEAD`                          |
| Branch            | Named reference to a commit               | `.pygit/refs/heads/<branch>`           |
| Object Store      | Stores hashed file and commit contents    | `.pygit/objects/`                      |


