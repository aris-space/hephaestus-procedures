#!/bin/bash

# Download all PDFs from the latest GitHub release
gh release download -p "*" -D Downloads/procedures -R aris-space/hephaestus-procedures

# Create directories if they don't exist
mkdir -p "Downloads/procedures/01 Contingency Procedures"
mkdir -p "Downloads/procedures/01 Contingency Procedures/DACS"
mkdir -p "Downloads/procedures/01 Contingency Procedures/PSS"
mkdir -p "Downloads/procedures/01 Contingency Procedures/ENG"
mkdir -p "Downloads/procedures/02 Operating Procedures"
mkdir -p "Downloads/procedures/02 Operating Procedures/DACS"
mkdir -p "Downloads/procedures/02 Operating Procedures/PSS"
mkdir -p "Downloads/procedures/02 Operating Procedures/ENG"
mkdir -p "Downloads/procedures/03 Packing List"
mkdir -p "Downloads/procedures/guidelines"

# Move files to respective directories based on their filename
for file in Downloads/procedures/*.pdf; do
    if [[ $(basename "$file") == HEP_CP_DACS* ]]; then
        mv "$file" "Downloads/procedures/01 Contingency Procedures/DACS/"
    elif [[ $(basename "$file") == HEP_CP_PSS* ]]; then
        mv "$file" "Downloads/procedures/01 Contingency Procedures/PSS/"
    elif [[ $(basename "$file") == HEP_CP_ENG* ]]; then
        mv "$file" "Downloads/procedures/01 Contingency Procedures/ENG/"
    elif [[ $(basename "$file") == HEP_CP* ]]; then
        mv "$file" "Downloads/procedures/01 Contingency Procedures/"
    elif [[ $(basename "$file") == HEP_OP_DACS* ]]; then
        mv "$file" "Downloads/procedures/02 Operating Procedures/DACS/"
    elif [[ $(basename "$file") == HEP_OP_PSS* ]]; then
        mv "$file" "Downloads/procedures/02 Operating Procedures/PSS/"
    elif [[ $(basename "$file") == HEP_OP_ENG* ]]; then
        mv "$file" "Downloads/procedures/02 Operating Procedures/ENG/"
    elif [[ $(basename "$file") == HEP_OP_* ]]; then
        mv "$file" "Downloads/procedures/02 Operating Procedures/"
    elif [[ $(basename "$file") == HEP_PL* ]]; then
        mv "$file" "Downloads/procedures/03 Packing List/"
    elif [[ $(basename "$file") == HEP_GL* ]]; then
        mv "$file" "Downloads/procedures/guidelines/"
    elif [[ $(basename "$file") == HEP_TEMP* ]]; then
        rm "$file" 
    fi
done