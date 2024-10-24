    #!/bin/bash

    # Get the directory of the current script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Navigate to the project root (assuming this script is located inside `scripts/` directory)
    cd "$SCRIPT_DIR/.."

    # Run the Streamlit app in the Poetry environment
    poetry run streamlit run src/demo_gui.py
