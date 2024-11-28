import json
import os
from collections import defaultdict
from typing import Dict, List, Set, Tuple

def load_json_file(file_path: str) -> List[dict]:
    with open(file_path, 'r') as f:
        return json.load(f)

def get_annotations_by_text(data: List[dict]) -> Dict[str, Set[str]]:
    annotations = {}
    for item in data:
        text = item.get('text', '')
        annotation_list = item.get('annotation', [])
        annotations[text] = set(annotation_list)
    return annotations

def compare_annotations(file1_path: str, file2_path: str) -> Tuple[dict, float]:
    # Load both JSON files
    data1 = load_json_file(file1_path)
    data2 = load_json_file(file2_path)

    # Get annotations by text for both files
    annotations1 = get_annotations_by_text(data1)
    annotations2 = get_annotations_by_text(data2)

    # Compare annotations
    comparison_results = {
        'matching_texts': [],
        'different_annotations': [],
        'unique_to_file1': [],
        'unique_to_file2': []
    }

    # Find texts present in both files
    common_texts = set(annotations1.keys()) & set(annotations2.keys())
    
    # Analyze common texts
    total_comparisons = 0
    matching_annotations = 0
    
    for text in common_texts:
        annot1 = annotations1[text]
        annot2 = annotations2[text]
        
        if annot1 == annot2:
            comparison_results['matching_texts'].append({
                'text': text,
                'annotations': list(annot1)
            })
            matching_annotations += 1
        else:
            comparison_results['different_annotations'].append({
                'text': text,
                'file1_annotations': list(annot1),
                'file2_annotations': list(annot2),
                'common_annotations': list(annot1 & annot2),
                'unique_to_file1': list(annot1 - annot2),
                'unique_to_file2': list(annot2 - annot1)
            })
        total_comparisons += 1

    # Find texts unique to each file
    for text in set(annotations1.keys()) - common_texts:
        comparison_results['unique_to_file1'].append({
            'text': text,
            'annotations': list(annotations1[text])
        })

    for text in set(annotations2.keys()) - common_texts:
        comparison_results['unique_to_file2'].append({
            'text': text,
            'annotations': list(annotations2[text])
        })

    # Calculate agreement score
    agreement_score = matching_annotations / total_comparisons if total_comparisons > 0 else 0

    return comparison_results, agreement_score

def analyze_annotation_distribution(data: List[dict]) -> Dict[str, int]:
    distribution = defaultdict(int)
    for item in data:
        for annotation in item.get('annotation', []):
            distribution[annotation] += 1
    return dict(distribution)

def main():
    # Example usage
    base_dir = "data"
    
    # Define the annotation directories to compare
    dirs_to_compare = [
        "annotations_human",
        "annotations_4o_mini_ev",
        "annotations_gemini_ev"
    ]
    
    # Get all JSON files in the human annotations directory
    human_dir = os.path.join(base_dir, "annotations_human")
    human_files = [f for f in os.listdir(human_dir) if f.endswith('.json')]
    
    results = []
    
    # Compare each human annotation file with its counterparts in other directories
    for filename in human_files:
        human_file_path = os.path.join(human_dir, filename)
        
        for compare_dir in dirs_to_compare[1:]:  # Skip human directory
            compare_file_path = os.path.join(base_dir, compare_dir, filename)
            
            if os.path.exists(compare_file_path):
                comparison_results, agreement_score = compare_annotations(
                    human_file_path, compare_file_path
                )
                
                results.append({
                    'filename': filename,
                    'comparison': f'human_vs_{compare_dir}',
                    'agreement_score': agreement_score,
                    # 'details': comparison_results
                })
    
    # Save results to a file
    output_file = os.path.join(base_dir, 'annotation_comparison_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results have been saved to: {output_file}")

if __name__ == "__main__":
    main()
