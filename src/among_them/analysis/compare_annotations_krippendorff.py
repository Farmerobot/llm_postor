import json
import os
import csv
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import numpy as np
import krippendorff

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

def calculate_label_agreement(annotations1: Dict[str, Set[str]], annotations2: Dict[str, Set[str]], 
                            common_texts: Set[str], technique: str) -> float:
    """
    Calculate label-wise agreement for a specific technique:
    Agreement = (Number of times both annotations agree on the label) / (Total number of texts)
    """
    agreement_count = sum(
        1 for text in common_texts 
        if (technique in annotations1[text]) == (technique in annotations2[text])
    )
    return agreement_count / len(common_texts) if common_texts else 0.0

def calculate_krippendorff_alpha(annotations1: Dict[str, Set[str]], annotations2: Dict[str, Set[str]], 
                              common_texts: Set[str]) -> float:
    """
    Calculate Krippendorff's alpha for multi-label annotations using matrix reshaping.
    Each text-label pair is treated as a separate coding decision.
    """
    # Get all unique annotation labels
    all_annotations = list(get_all_unique_annotations(annotations1, annotations2))
    common_texts = list(common_texts)
    
    # Create a 3D matrix: (texts x labels x annotators)
    num_texts = len(common_texts)
    num_labels = len(all_annotations)
    annotations_matrix = np.zeros((num_texts, num_labels, 2), dtype=int)
    
    # Fill the matrix
    for i, text in enumerate(common_texts):
        for j, label in enumerate(all_annotations):
            annotations_matrix[i, j, 0] = 1 if label in annotations1[text] else 0
            annotations_matrix[i, j, 1] = 1 if label in annotations2[text] else 0
    
    # Reshape to (labels x texts x annotators) format expected by krippendorff.alpha
    reliability_data = annotations_matrix.transpose(1, 0, 2).reshape(num_labels * num_texts, 2).T
    
    try:
        # Calculate Krippendorff's alpha with nominal metric (since we have binary data)
        alpha = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement='nominal')
        return float(alpha) if not np.isnan(alpha) else 0.0
    except:
        return 0.0

def compare_directories(dir1: str, dir2: str) -> Tuple[dict, float, dict, dict]:
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
    
    # Calculate overall Krippendorff's alpha
    overall_alpha = calculate_krippendorff_alpha(all_annotations1, all_annotations2, common_texts)
    
    # Calculate per-technique agreement
    all_techniques = get_all_unique_annotations(all_annotations1, all_annotations2)
    
    # Calculate both Krippendorff's alpha and label-wise agreement for each technique
    technique_alphas = {}
    technique_agreements = {}
    
    for technique in all_techniques:
        # Create single-technique annotations for alpha calculation
        tech_annotations1 = {text: {technique} if technique in annots else set() 
                           for text, annots in all_annotations1.items()}
        tech_annotations2 = {text: {technique} if technique in annots else set() 
                           for text, annots in all_annotations2.items()}
        tech_common_texts = set(tech_annotations1.keys()) & set(tech_annotations2.keys())
        
        # Calculate alpha for this technique
        tech_alpha = calculate_krippendorff_alpha(tech_annotations1, tech_annotations2, tech_common_texts)
        technique_alphas[technique] = tech_alpha
        
        # Calculate label-wise agreement for this technique
        agreement = calculate_label_agreement(all_annotations1, all_annotations2, tech_common_texts, technique)
        technique_agreements[technique] = agreement
    
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
    
    return comparison_results, overall_alpha, technique_alphas, technique_agreements

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
        comparison_results, overall_alpha, technique_alphas, technique_agreements = compare_directories(human_dir, comparison_dir)
        
        results.append({
            'comparison': f'human_vs_{compare_dir}',
            'overall_alpha': overall_alpha,
            'matching_texts': len(comparison_results['matching_texts']),
            'different_texts': len(comparison_results['different_annotations']),
            'unique_to_human': len(comparison_results['unique_to_dir1']),
            'unique_to_other': len(comparison_results['unique_to_dir2']),
            'matching_annotations': comparison_results['total_techniques']['matching'],
            'different_annotations': comparison_results['total_techniques']['different'],
            'unique_to_human_annotations': comparison_results['total_techniques']['unique_to_dir1'],
            'unique_to_other_annotations': comparison_results['total_techniques']['unique_to_dir2']
        })
        
        results_detailed.append({
            'comparison': f'human_vs_{compare_dir}',
            'overall_alpha': overall_alpha,
            'technique_alphas': technique_alphas,
            'technique_agreements': technique_agreements,
            'comparison_results': comparison_results
        })
    
    # Save results to CSV files
    output_file = os.path.join(base_dir, 'annotation_comparison_results.csv')
    output_detailed = os.path.join(base_dir, 'annotation_comparison_detailed.csv')
    
    # Save summary results
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['comparison', 'overall_alpha', 'matching_texts', 
                                             'different_texts', 'unique_to_human', 'unique_to_other', 
                                             'matching_annotations', 'different_annotations', 
                                             'unique_to_human_annotations', 'unique_to_other_annotations'])
        writer.writeheader()
        writer.writerows(results)
    
    # Save detailed results including per-technique metrics
    with open(output_detailed, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Comparison', 'Technique', 'Krippendorff Alpha', 'Label Agreement'])
        for result in results_detailed:
            comparison = result['comparison']
            for technique in result['technique_alphas'].keys():
                writer.writerow([
                    comparison,
                    technique,
                    result['technique_alphas'][technique],
                    result['technique_agreements'][technique]
                ])
    
    print(f"Results have been saved to: {output_file}")
    print(f"Detailed results have been saved to: {output_detailed}")

if __name__ == "__main__":
    main()
