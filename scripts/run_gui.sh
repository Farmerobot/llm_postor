#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to the project root (assuming this script is located inside `scripts/` directory)
cd "$SCRIPT_DIR/.."

# Activate the poetry environment
poetry shell

# Run the streamlit app from the `src` directory
cd src
streamlit run demo_gui.py
