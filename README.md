# pygit

**pygit** is a personal project to help me learn about Git internals by implementing a simplified version of Git in Python. This project is for educational purposes and is not intended to be a fully-featured Git alternative.

## Goals

The main goal of **pygit** is to provide hands-on experience with how Git works under the hood. By building it from scratch, I aim to better understand Git's data structures, workflows, and underlying mechanics.


## Installation

To get started with **pygit**, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pygit.git
   cd pygit
   ```

2. Install the package in editable mode:

   ```bash
   pip install --editable .
   ```

## Features

### `init`

Create a new `.pygit` directory with the necessary structure for tracking commits.

```bash
pygit init
```

[Read about `init`](docs/init.md)

---

### `add`

Add one or more files to the staging area.

```bash
pygit add path/to/your/file.txt
```

[Read about `add`](docs/add.md)

---

### `commit`

Save a snapshot of the current state of the staged files with a commit message.

```bash
pygit commit -m "Your commit message"
```

[Read about `commit`](docs/commit.md)

