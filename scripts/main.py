import os
import subprocess

def main():
    # Define the project root directory (this assumes the script is located in the scripts/ folder)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Navigate to the project root directory
    os.chdir(project_root)

    # Define the path to the main.py script relative to the project root
    main_path = os.path.join(project_root, "src", "llm_postor", "main.py")

    # Check if the demo_gui.py file exists
    if not os.path.exists(main_path):
        raise FileNotFoundError(f"File does not exist: {main_path}")

    # Run the Streamlit app with the correct path
    subprocess.run(["poetry", "run", "streamlit", "run", main_path], check=True)
