import json
import os
import pandas as pd
from pathlib import Path

def combine_annotations():
    # Get the project root directory
    project_root = Path(__file__).parents[3]
    annotations_dir = project_root / "data" / "annotations"
    output_file = project_root / "data" / "combined_annotations.csv"

    # List to store all annotations
    all_annotations = []

    # Process each JSON file
    for json_file in annotations_dir.glob("*.json"):
        try:
            # Parse filename to get models
            filename = json_file.stem  # Get filename without extension
            models = filename.split("_vs_")
            impostor_model = models[0]  # First model is impostor
            crewmate_model = models[1].split("_")[0]  # Second model is crewmate, remove game number
            
            with open(json_file, 'r') as f:
                data = json.load(f)
                
            # Extract player names from the first message
            if data and "text" in data[0]:
                first_message = data[0]["text"]
                player_name = first_message.split("]:")[0].strip("[]")
            
            # Track the current speaker to determine their role
            for entry in data:
                text = entry["text"]
                current_speaker = text.split("]:")[0].strip("[]") if "]: " in text else player_name
                
                # Determine if the current speaker is impostor or crewmate based on the model order
                is_impostor = current_speaker == player_name
                
                all_annotations.append({
                    'text': text,
                    'annotation': '; '.join(entry['annotation']),
                    'source_file': json_file.name,
                    'speaker': current_speaker,
                    'model': impostor_model if is_impostor else crewmate_model,
                    'role': 'impostor' if is_impostor else 'crewmate'
                })
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(all_annotations)
    df.to_csv(output_file, index=False)
    print(f"Combined annotations saved to {output_file}")
    print(f"Total entries: {len(df)}")

if __name__ == "__main__":
    combine_annotations()