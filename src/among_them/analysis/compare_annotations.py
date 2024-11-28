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
    annotations = {}
    for item in data:
        text = item.get('text', '')
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
                         common_texts: Set[str]) -> Dict[str, float]:
    # Get all unique annotation labels
    all_annotations = get_all_unique_annotations(annotations1, annotations2)
    
    # Create binary matrices for each annotation type
    kappa_scores = {}
    
    for annotation in all_annotations:
        rater1_scores = []
        rater2_scores = []
        
        # Count occurrences to check if we have enough variation
        count_rater1 = 0
        count_rater2 = 0
        
        for text in common_texts:
            score1 = 1 if annotation in annotations1[text] else 0
            score2 = 1 if annotation in annotations2[text] else 0
            rater1_scores.append(score1)
            rater2_scores.append(score2)
            count_rater1 += score1
            count_rater2 += score2
        
        # Only calculate kappa if both raters used at least one positive and one negative label
        if (count_rater1 > 0 and count_rater1 < len(common_texts) and 
            count_rater2 > 0 and count_rater2 < len(common_texts)):
            try:
                kappa = cohen_kappa_score(rater1_scores, rater2_scores, labels=[0, 1])
                if not np.isnan(kappa):
                    kappa_scores[annotation] = kappa
            except:
                continue
    
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
            if not np.isnan(overall_kappa):
                kappa_scores['overall'] = overall_kappa
            else:
                kappa_scores['overall'] = 0.0
        except:
            kappa_scores['overall'] = 0.0
    else:
        kappa_scores['overall'] = 0.0
        
    return kappa_scores

def compare_annotations(file1_path: str, file2_path: str) -> Tuple[dict, Dict[str, float]]:
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
    
    # Calculate Cohen's Kappa scores
    kappa_scores = calculate_cohens_kappa(annotations1, annotations2, common_texts)
    
    # Analyze common texts
    for text in common_texts:
        annot1 = annotations1[text]
        annot2 = annotations2[text]
        
        if annot1 == annot2:
            comparison_results['matching_texts'].append({
                'text': text,
                'annotations': list(annot1)
            })
        else:
            comparison_results['different_annotations'].append({
                'text': text,
                'file1_annotations': list(annot1),
                'file2_annotations': list(annot2),
                'common_annotations': list(annot1 & annot2),
                'unique_to_file1': list(annot1 - annot2),
                'unique_to_file2': list(annot2 - annot1)
            })

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

    return comparison_results, kappa_scores

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
        "annotations_gemini_ev",
        "annotations_gemini_2_ev"
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
                comparison_results, kappa_scores = compare_annotations(
                    human_file_path, compare_file_path
                )
                
                # Add overall results
                results.append({
                    'filename': filename,
                    'comparison': f'human_vs_{compare_dir}',
                    'overall_kappa': kappa_scores.get('overall', 0.0),
                })
                
                # Add per-technique results
                for technique, score in kappa_scores.items():
                    if technique != 'overall':
                        results.append({
                            'filename': filename,
                            'comparison': f'human_vs_{compare_dir}',
                            'technique': technique,
                            'kappa': score,
                        })
    
    # Save results to CSV files
    overall_output = os.path.join(base_dir, 'annotation_comparison_overall.csv')
    technique_output = os.path.join(base_dir, 'annotation_comparison_by_technique.csv')
    
    # Write overall results
    overall_results = [r for r in results if 'technique' not in r]
    with open(overall_output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'comparison', 'overall_kappa'])
        writer.writeheader()
        writer.writerows(overall_results)
    
    # Write technique-specific results
    technique_results = [r for r in results if 'technique' in r]
    with open(technique_output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'comparison', 'technique', 'kappa'])
        writer.writeheader()
        writer.writerows(technique_results)
    
    print(f"Results have been saved to: {overall_output} and {technique_output}")

if __name__ == "__main__":
    main()
