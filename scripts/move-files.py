import os
import shutil
import json

# Define folders
base_folder = "src"
release_folder = "release"

# Load the versions from a JSON file
versions_file = 'versions.json'
if os.path.exists(versions_file):
    with open(versions_file, 'r') as vf:
        versions = json.load(vf)
else:
    raise FileNotFoundError("versions.json not found. Please ensure the versioning process is run first.")

# Ensure the release folder exists
if not os.path.exists(release_folder):
    os.makedirs(release_folder)

# Go through all subdirectories
for root, dirs, files in os.walk(base_folder):
    for file in files:
        if file != "main.pdf":
            # Skip file if it's not `main.pdf`
            continue
        
        # Get the relative path to use for version lookup
        relative_path = os.path.relpath(root, base_folder)
        
        # Check if a custom filename and version number is defined
        file_info_path = os.path.join(root, 'file_info.txt')
        if os.path.exists(file_info_path):
            # Read the custom filename and version from file_info.txt
            with open(file_info_path, 'r') as f:
                custom_filename, version_number = f.read().strip().split(',')
            new_filename = f"{custom_filename}_v{version_number}.pdf"
        else:
            # Use default naming with versioning from versions.json
            if relative_path in versions:
                version_number = versions[relative_path]['version']
            else:
                # If no version info exists, default to version 01
                version_number = '01'
            
            # Replace directory separators with hyphens for the filename
            new_filename = f"{relative_path.replace(os.sep, '-')}_v{version_number}.pdf"
        
        # Construct the old and new file paths
        old_path = os.path.join(root, file)
        new_path = os.path.join(release_folder, new_filename)
        
        # Move and rename the file
        shutil.move(old_path, new_path)
        print(f"Moved {old_path} to {new_path}")