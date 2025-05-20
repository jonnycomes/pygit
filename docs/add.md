# Understanding the `add` Command

## Overview

The `add` command stages a file for commit by copying it into the staging area and updating the repository index with its content hash. This mirrors how Git prepares files for inclusion in the next commit.

## Usage

``` bash  
pygit add <filename>  
```

## What happens during `add`?

When you run `pygit add <filename>`, the following steps are performed:

### 1. Ensure the staging directory exists

- A directory named `staging` inside the `.pygit` repository is created if it doesn't already exist.
- This staging area will temporarily hold copies of the files to be committed.

### 2. Check that the file exists and is not ignored

- If the specified file does not exist, the command prints a message:
	```
	<filename> does not exist. Nothing added.
	```

- If the file matches any pattern in `.pygitignore` (or is inside `.pygit`), the command prints a message:
	```
	<filename> is ignored. Skipping.
	```
	and skips staging it.

### 3. Hash the file contents

- The file’s contents are read and hashed using a SHA-1 hashing strategy.
- This hash acts as a unique identifier for the file content, similar to how Git uses hashes to track file versions.

### 4. Copy the file to the staging directory

- A copy of the file is saved in the `.pygit/staging` directory.
- The copy uses the same filename as the original, not the hashed name. (Actual Git stores blobs by their hash, but pygit keeps things simpler for now.)

### 5. Update the index

- The `index` file in `.pygit` is loaded as a dictionary.
- The filename is used as the key, and the content hash as the value.
- This lets pygit track which version of the file has been staged for the next commit.
- The updated index is saved back to disk in JSON format.

### 6. Print confirmation message

- After successfully staging the file, the command prints:

``` bash  
Staged <filename>  
```

## Summary of files and changes

```
.pygit/
├── staging/
│   └── <filename>       # Copy of the file staged for commit
├── index                # Updated to include filename and its content hash

```


## Notes

- If the same file is added again after changes, it will be rehashed and re-copied to the staging area, and the index will be updated accordingly.
- pygit's staging mechanism is simplified: it does not yet support nested directories or track file paths beyond the base filename.
