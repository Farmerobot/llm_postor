import os
import subprocess

def run_gui():
    # Define the project root directory (this assumes the script is located in the scripts/ folder)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Navigate to the project root directory
    os.chdir(project_root)

    # Define the path to the demo_gui.py script relative to the project root
    demo_gui_path = os.path.join(project_root, "src", "llm_postor", "demo_gui.py")

    # Check if the demo_gui.py file exists
    if not os.path.exists(demo_gui_path):
        raise FileNotFoundError(f"File does not exist: {demo_gui_path}")

    # Run the Streamlit app with the correct path
    subprocess.run(["poetry", "run", "streamlit", "run", demo_gui_path], check=True)
