import os
import subprocess


def main():
    # Define the project root directory
    # (this assumes the script is located in the scripts/ folder)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(project_root)
    tournament_path = os.path.join(project_root, "src", "llm_postor", "tournament.py")

    if not os.path.exists(tournament_path):
        raise FileNotFoundError(f"File does not exist: {tournament_path}")

    # Run the Streamlit app with the correct path
    subprocess.run(["poetry", "run", "python3", tournament_path], check=True)


if __name__ == "__main__":
    main()
