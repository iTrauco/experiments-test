import json
from pathlib import Path

def export_notebook(input_path):
    """Export working notebook to clean version."""
    input_path = Path(input_path)
    output_path = Path(str(input_path).replace('.working.ipynb', '.ipynb'))
    
    with open(input_path, 'r') as f:
        nb = json.load(f)
    
    # Filter tagged cells
    nb['cells'] = [
        clean_cell(cell) for cell in nb['cells']
        if 'export' in cell.get('metadata', {}).get('tags', [])

    ]
    
    with open(output_path, 'w') as f:
        json.dump(nb, f, indent=1)
    
    return output_path

def clean_cell(cell):
    """Remove outputs from a cell."""
    cell['outputs'] = []
    if 'execution_count' in cell:
        cell['execution_count'] = None
    return cell