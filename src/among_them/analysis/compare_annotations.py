import json
import os
import csv
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import numpy as np
from sklearn.metrics import cohen_kappa_score

def load_json_file(file_path: str) -> List[dict]:
    with open(file_path, 'r') as f:
        return json.load(f)

def get_annotations_by_text(data: List[dict]) -> Dict[str, Set[str]]:
    
    # Get path to technique_examples.json
    exclude_file = os.path.join('data', 'technique_examples.json')
    annotations = {}
    
    # Load texts to exclude if exclude_file is provided
    exclude_texts = set()
    if exclude_file and os.path.exists(exclude_file):
        with open(exclude_file, 'r') as f:
            exclude_data = json.load(f)
            exclude_texts = {item['text'] for item in exclude_data}
    
    for item in data:
        text = item.get('text', '')
        # Skip texts that are in the exclude file
        if text in exclude_texts:
            continue
        annotation_list = item.get('annotation', [])
        annotations[text] = set(annotation_list)
    return annotations

def get_all_unique_annotations(annotations1: Dict[str, Set[str]], annotations2: Dict[str, Set[str]]) -> Set[str]:
    all_annotations = set()
    for annots in annotations1.values():
        all_annotations.update(annots)
    for annots in annotations2.values():
        all_annotations.update(annots)
    return all_annotations

def calculate_cohens_kappa(annotations1: Dict[str, Set[str]], annotations2: Dict[str, Set[str]], 
                         common_texts: Set[str]) -> float:
    # Get all unique annotation labels
    all_annotations = get_all_unique_annotations(annotations1, annotations2)
    
    # Calculate overall kappa
    all_rater1_scores = []
    all_rater2_scores = []
    
    for text in common_texts:
        for annotation in all_annotations:
            all_rater1_scores.append(1 if annotation in annotations1[text] else 0)
            all_rater2_scores.append(1 if annotation in annotations2[text] else 0)
    
    # Check if we have enough variation in the overall scores
    unique_scores1 = len(set(all_rater1_scores))
    unique_scores2 = len(set(all_rater2_scores))
    
    if unique_scores1 > 1 and unique_scores2 > 1:
        try:
            overall_kappa = cohen_kappa_score(all_rater1_scores, all_rater2_scores, labels=[0, 1])
            return float(overall_kappa) if not np.isnan(overall_kappa) else 0.0
        except:
            return 0.0
    else:
        return 0.0

def compare_directories(dir1: str, dir2: str) -> Tuple[dict, float]:
    # Get all JSON files in both directories
    files1 = {f for f in os.listdir(dir1) if f.endswith('.json')}
    files2 = {f for f in os.listdir(dir2) if f.endswith('.json')}
    
    # Find common files
    common_files = files1 & files2
    
    # Collect all annotations
    all_annotations1 = {}  # text -> set of annotations
    all_annotations2 = {}
    
    for filename in common_files:
        file1_path = os.path.join(dir1, filename)
        file2_path = os.path.join(dir2, filename)
        
        # Load annotations from both files
        data1 = load_json_file(file1_path)
        data2 = load_json_file(file2_path)
        
        # Get annotations by text
        annotations1 = get_annotations_by_text(data1)
        annotations2 = get_annotations_by_text(data2)
        
        # Merge into all_annotations
        all_annotations1.update(annotations1)
        all_annotations2.update(annotations2)
    
    # Find texts present in both sets
    common_texts = set(all_annotations1.keys()) & set(all_annotations2.keys())
    
    # Calculate Cohen's Kappa for all annotations
    kappa_score = calculate_cohens_kappa(all_annotations1, all_annotations2, common_texts)
    
    # Prepare comparison results
    comparison_results = {
        'matching_texts': [],
        'different_annotations': [],
        'unique_to_dir1': [],
        'unique_to_dir2': [],
        'total_techniques': {
            'matching': 0,
            'different': 0,
            'unique_to_dir1': 0,
            'unique_to_dir2': 0
        }
    }
    
    # Analyze common texts
    for text in common_texts:
        annot1 = all_annotations1[text]
        annot2 = all_annotations2[text]
        
        if annot1 == annot2:
            comparison_results['matching_texts'].append({
                'text': text,
                'annotations': list(annot1)
            })
            comparison_results['total_techniques']['matching'] += len(annot1)
        else:
            common_annotations = annot1 & annot2
            unique_to_file1 = annot1 - annot2
            unique_to_file2 = annot2 - annot1
            
            comparison_results['different_annotations'].append({
                'text': text,
                'file1_annotations': list(annot1),
                'file2_annotations': list(annot2),
                'common_annotations': list(common_annotations),
                'unique_to_file1': list(unique_to_file1),
                'unique_to_file2': list(unique_to_file2)
            })
            comparison_results['total_techniques']['different'] += len(common_annotations)
            comparison_results['total_techniques']['unique_to_dir1'] += len(unique_to_file1)
            comparison_results['total_techniques']['unique_to_dir2'] += len(unique_to_file2)
    
    # Find texts unique to each directory
    for text in set(all_annotations1.keys()) - common_texts:
        annotations = all_annotations1[text]
        comparison_results['unique_to_dir1'].append({
            'text': text,
            'annotations': list(annotations)
        })
        comparison_results['total_techniques']['unique_to_dir1'] += len(annotations)
    
    for text in set(all_annotations2.keys()) - common_texts:
        annotations = all_annotations2[text]
        comparison_results['unique_to_dir2'].append({
            'text': text,
            'annotations': list(annotations)
        })
        comparison_results['total_techniques']['unique_to_dir2'] += len(annotations)
    
    return comparison_results, kappa_score

def save_results_to_json(results, filename):
    with open(filename, 'w') as json_file:
        json.dump(results, json_file, indent=4)

def main():
    # Example usage
    base_dir = "data"
    
    # Define the annotation directories to compare
    dirs_to_compare = [
        "annotations_human",
        "annotations",
    ]
    
    results = []
    results_detailed = []
    
    # Compare human annotations with each other directory
    human_dir = os.path.join(base_dir, dirs_to_compare[0])
    
    for compare_dir in dirs_to_compare[1:]:
        comparison_dir = os.path.join(base_dir, compare_dir)
        comparison_results, kappa_score = compare_directories(human_dir, comparison_dir)
        
        results.append({
            'comparison': f'human_vs_{compare_dir}',
            'kappa_score': kappa_score,
            'matching_texts': len(comparison_results['matching_texts']),
            'different_texts': len(comparison_results['different_annotations']),
            'unique_to_human': len(comparison_results['unique_to_dir1']),
            'unique_to_other': len(comparison_results['unique_to_dir2']),
            'matching_annotations': comparison_results['total_techniques']['matching'],
            'different_annotations': comparison_results['total_techniques']['different'],
            'unique_to_human_annotations': comparison_results['total_techniques']['unique_to_dir1'],
            'unique_to_other_annotations': comparison_results['total_techniques']['unique_to_dir2']
        })
        
        results_detailed.append(comparison_results)
    
    # Save results to CSV file
    output_file = os.path.join(base_dir, 'annotation_comparison_results.csv')
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['comparison', 'kappa_score', 'matching_texts', 
                                             'different_texts', 'unique_to_human', 'unique_to_other', 
                                             'matching_annotations', 'different_annotations', 'unique_to_human_annotations', 'unique_to_other_annotations'])
        writer.writeheader()
        writer.writerows(results)
    
    # Save detailed results to JSON file
    output_json_file = os.path.join(base_dir, 'annotation_comparison_detailed_results.json')
    save_results_to_json(results_detailed, output_json_file)
    
    print(f"Results have been saved to: {output_file}")
    print(f"Detailed results have been saved to: {output_json_file}")

if __name__ == "__main__":
    main()
