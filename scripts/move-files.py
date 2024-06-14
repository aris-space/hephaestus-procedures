import os
import shutil


# Define folders
base_folder = "src"
release_folder = "release"

# Ensure the release folder exists
if not os.path.exists(release_folder):
    os.makedirs(release_folder)

# Go through all subdirectories
for root, dirs, files in os.walk(base_folder):
    for file in files:
        if file != "main.pdf":
            # Skip file if it's not `main.pdf`
            continue

        # Construct the original file path
        old_path = os.path.join(root, file)

        # Create the new file name with '-' instead of '/'
        relative_path = os.path.relpath(root, base_folder)
        new_filename = relative_path.replace(os.sep, "-")

        # Add the '.pdf' extension to the new filename
        new_filename += ".pdf"

        # Construct the new file path
        new_path = os.path.join(release_folder, new_filename)

        # Move and rename the file
        shutil.move(old_path, new_path)
        print(f"Moved {old_path} to {new_path}")
