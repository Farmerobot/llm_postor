import os
import subprocess

def run_gui():
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the project root (assuming this file is inside `src/llm_poster/`)
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    os.chdir(project_root)
    
    # Run the Streamlit app in the Poetry environment
    try:
        subprocess.run(["streamlit", "run", "src/demo_gui.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit app: {e}")
        exit(1)
