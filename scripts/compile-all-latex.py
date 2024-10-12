import os
import re
import subprocess
import json
import hashlib
import git

# Define folders and files
base_folder = "src"
root_file = "main.tex"
version_file = "versions.json"

# Load or initialize version tracking
if os.path.exists(version_file):
    with open(version_file, 'r') as f:
        versions = json.load(f)
else:
    versions = {}

def get_custom_filename(tex_file):
    """Extracts custom filename from a LaTeX file's comments."""
    with open(tex_file, 'r') as f:
        content = f.read()
    match = re.search(r'%\s*filename:\s*(\S+)', content)
    return match.group(1) if match else None

def get_file_hash(file_path):
    """Calculate the hash of a file to detect changes."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# Initialize git repo
repo = git.Repo(os.getcwd())

# Go through all subdirectories
for dirpath, _, filenames in os.walk(base_folder):
    if root_file not in filenames:
        # Skip if there's no `main.tex`
        continue

    # Get the custom filename and file hash
    tex_file_path = os.path.join(dirpath, root_file)
    custom_filename = get_custom_filename(tex_file_path)
    current_hash = get_file_hash(tex_file_path)

    # Check if the file has been modified
    relative_path = os.path.relpath(dirpath, base_folder)
    if relative_path not in versions:
        # New file, set version to 01
        versions[relative_path] = {'version': '01', 'hash': current_hash}
    else:
        # Compare hashes to detect changes
        previous_hash = versions[relative_path]['hash']
        if current_hash != previous_hash:
            # File has changed, increment version
            current_version = int(versions[relative_path]['version'])
            new_version = f"{current_version + 1:02}"
            versions[relative_path] = {'version': new_version, 'hash': current_hash}

    # Compile LaTeX
    try:
        subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", root_file],
            check=True,
            cwd=dirpath
        )
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {tex_file_path}: {e}")
        exit(1)

    # Store the custom filename and version for later use
    version_number = versions[relative_path]['version']
    if custom_filename:
        with open(os.path.join(dirpath, 'file_info.txt'), 'w') as f:
            f.write(f"{custom_filename},{version_number}")

# Save the updated versions
with open(version_file, 'w') as f:
    json.dump(versions, f, indent=4)
