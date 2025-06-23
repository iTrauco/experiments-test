import json
import sys
import os
import glob

def generate_toc(notebook_path, update_in_place=False):
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    headers = []
    toc_cell_index = None
    
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            
            # Check for TOC marker
            if '<!-- TOC -->' in content:
                toc_cell_index = i
            
            # Extract headers
            for line in content.split('\n'):
                if line.startswith('#'):
                    level = len(line.split(' ')[0])
                    title = line.strip('#').strip()
                    anchor = title.lower().replace(' ', '-').replace(':', '')
                    headers.append((level, title, anchor))
    
    # Generate TOC
    toc_lines = ["<!-- TOC -->", "# Table of Contents", ""]
    for level, title, anchor in headers:
        if level > 1:  # Skip main title
            indent = '  ' * (level - 2)
            toc_lines.append(f"{indent}- [{title}](#{anchor})")
    toc_lines.extend(["", "<!-- /TOC -->"])
    
    if update_in_place and toc_cell_index is not None:
        # Convert to notebook cell format (list of lines with \n)
        nb['cells'][toc_cell_index]['source'] = [line + '\n' for line in toc_lines]
        with open(notebook_path, 'w') as f:
            json.dump(nb, f, indent=1)
        return True
    return False

if __name__ == '__main__':
    update = '--update' in sys.argv
    
    # Check if --all flag is used
    if '--all' in sys.argv:
        notebooks = glob.glob('notebooks/*.ipynb')
        updated = 0
        for nb in notebooks:
            if generate_toc(nb, update):
                print(f"Updated TOC in {nb}")
                updated += 1
        print(f"\nProcessed {len(notebooks)} notebooks, updated {updated}")
    else:
        notebook = [arg for arg in sys.argv[1:] if not arg.startswith('--')][0]
        if generate_toc(notebook, update):
            print(f"Updated TOC in {notebook}")
        else:
            toc = generate_toc(notebook, False)