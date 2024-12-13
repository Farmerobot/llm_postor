import json
import os
import random
from collections import defaultdict
from typing import Dict, List, Set

def load_all_annotations(directory: str) -> List[dict]:
    all_examples = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                examples = json.load(f)
                all_examples.extend(examples)
    return all_examples

def get_examples_by_technique(examples: List[dict]) -> Dict[str, List[dict]]:
    technique_examples = defaultdict(list)
    for example in examples:
        for technique in example['annotation']:
            technique_examples[technique].append({
                'text': example['text'],
                'annotation': example['annotation']
            })
    return technique_examples

def select_examples(technique_examples: Dict[str, List[dict]], n: int = 3) -> Dict[str, List[dict]]:
    selected = {}
    for technique, examples in technique_examples.items():
        # Select min(n, len(examples)) examples to handle cases where we have fewer than n examples
        selected[technique] = random.sample(examples, min(n, len(examples)))
    #return just the values
    return [example for examples in selected.values() for example in examples]

def main():
    # Directory containing the annotation files
    annotations_dir = '/Users/luncenok/PycharmProjects/mk-ai-agents/data/annotations_human'
    output_file = '/Users/luncenok/PycharmProjects/mk-ai-agents/data/technique_examples.json'
    
    # Load all examples
    all_examples = load_all_annotations(annotations_dir)
    
    # Group examples by technique
    technique_examples = get_examples_by_technique(all_examples)
    
    # Select 2 examples for each technique
    selected_examples = select_examples(technique_examples, 3)
    
    # Save to a new JSON file
    with open(output_file, 'w') as f:
        json.dump(selected_examples, f, indent=2)
    
    print(f"Created {output_file} with {len(selected_examples)} techniques")
    print("Number of examples:", len(selected_examples), "/", len(all_examples))

if __name__ == '__main__':
    main()
