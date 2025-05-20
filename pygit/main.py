import sys
from pygit.commands import init, add, commit, status

def main():
    if len(sys.argv) < 2:
        print("Usage: pygit [init|add|commit]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init.run()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: You must specify a file to add.")
        else:
            add.run(sys.argv[2])
    elif command == "commit":
        if "-m" in sys.argv:
            idx = sys.argv.index("-m") + 1
            if idx < len(sys.argv):
                commit.run(sys.argv[idx])
            else:
                print("Error: No commit message provided.")
        else:
            print("Error: -m flag is required to specify a commit message.")
    elif command == "status":
        status.run()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()