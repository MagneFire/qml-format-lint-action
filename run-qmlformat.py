#!/usr/bin/env python
import subprocess
import glob
import os
import sys

def get_qml_files(directory="."):
    """
    Handles file discovery. 
    Returns a list of paths to .qml files.
    """
    pattern = os.path.join(directory, "**/*.qml")
    return glob.glob(pattern, recursive=True)

def is_formatted(file_path):
    """
    Handles the formatting check for a single file.
    Returns True if formatted, False otherwise.
    """
    try:
        result = subprocess.run(
            ["qmlformat-qt5", file_path],
            capture_output=True,
            text=True,
            check=True
        )

        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        return result.stdout == original_content

    except subprocess.CalledProcessError:
        print(f"Error: Could not process {file_path}")
        return False

def main():
    github_workspace = os.environ.get('GITHUB_WORKSPACE')
    if github_workspace:
        os.chdir(github_workspace)

    files = get_qml_files()

    if not files:
        print("No QML files found.")
        return

    print(f"Checking {len(files)} files...")
    unformatted = [f for f in files if not is_formatted(f)]

    if unformatted:
        print(f"FAILED: {len(unformatted)} files need formatting:")
        for f in unformatted:
            print(f"  - {f}")
        sys.exit(1)

    print("SUCCESS: All files are formatted.")
    sys.exit(0)

if __name__ == "__main__":
    main()