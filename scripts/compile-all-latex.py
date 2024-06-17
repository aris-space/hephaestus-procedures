import os
import subprocess

# Define folders and files
base_folder = "src"
root_file = "main.tex"


# Go through all subdirectories
for dirpath, _, filenames in os.walk(base_folder):
    if not root_file in filenames:
        # Skip if there's no `main.tex`
        continue
    
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
