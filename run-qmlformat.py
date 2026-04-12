#!/usr/bin/env python
import argparse
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

def get_formatted_code(file_path):
    """
    Use qmlformat to get the formatted code for a given file.
    """
    try:
        result = subprocess.run(
            ["qmlformat-qt5", file_path],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout
    except subprocess.CalledProcessError:
        print(f"Error: Could not process {file_path}")
        return False

def is_formatted(file_path):
    """
    Handles the formatting check for a single file.
    Returns True if formatted, False otherwise.
    """
    try:
        result = get_formatted_code(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        return result == original_content
    except subprocess.CalledProcessError:
        print(f"Error: Could not process {file_path}")
        return False

def format_file(file_path, max_retries=5):
    """
    Formats the file until two consecutive passes produce the same result.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        current_content = f.read()

    for i in range(max_retries):
        new_content = get_formatted_code(file_path)
        if new_content == current_content:
            return True

        current_content = new_content

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    return False

def main():
    github_workspace = os.environ.get('GITHUB_WORKSPACE')
    if github_workspace:
        os.chdir(github_workspace)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-f',
        '--fix',
        action='store_true',
        help='format the QML files instead of just checking')
    args = parser.parse_args()

    files = get_qml_files()

    if not files:
        print("No QML files found.")
        return

    if args.fix:
        print("Formatting files")
        for f in files:
            format_file(f)

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