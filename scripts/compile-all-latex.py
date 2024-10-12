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

def get_folder_hash(folder_path):
    """Calculate the combined hash of all files in a folder."""
    sha256 = hashlib.sha256()
    
    # Go through all files in the folder and hash them
    for root, _, files in os.walk(folder_path):
        for file in sorted(files):  # Sort to ensure consistent order
            file_path = os.path.join(root, file)
            # Exclude versions.json or other non-relevant files if needed
            if file == "versions.json":
                continue
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
    
    return sha256.hexdigest()

# Initialize git repo
repo = git.Repo(os.getcwd())

# Go through all subdirectories
for dirpath, _, filenames in os.walk(base_folder):
    if root_file not in filenames:
        # Skip if there's no `main.tex`
        continue
    
    # Get the custom filename and folder hash
    folder_hash = get_folder_hash(dirpath)
    custom_filename = get_custom_filename(os.path.join(dirpath, root_file))
    
    # Check if the folder has been modified
    relative_path = os.path.relpath(dirpath, base_folder)
    if relative_path not in versions:
        # New folder, set version to 01
        versions[relative_path] = {'version': '01', 'hash': folder_hash}
    else:
        # Compare hashes to detect changes
        previous_hash = versions[relative_path]['hash']
        if folder_hash != previous_hash:
            # Folder has changed, increment version
            current_version = int(versions[relative_path]['version'])
            new_version = f"{current_version + 1:02}"
            versions[relative_path] = {'version': new_version, 'hash': folder_hash}
    
    # Compile LaTeX
    command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{os.environ['GITHUB_WORKSPACE']}:/workspace",
        "-w",
        f"/workspace/{dirpath}",
        "texlive/texlive:latest",
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        f"{root_file}",
    ]
    subprocess.run(command, check=True)
    
    # Store the custom filename and version for later use
    version_number = versions[relative_path]['version']
    if custom_filename:
        with open(os.path.join(dirpath, 'file_info.txt'), 'w') as f:
            f.write(f"{custom_filename},{version_number}")

# Save the updated versions
with open(version_file, 'w') as f:
    json.dump(versions, f, indent=4)
