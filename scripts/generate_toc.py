# import json
# import sys
# import os
# import glob

# def generate_toc(notebook_path, update_in_place=False):
#     with open(notebook_path, 'r') as f:
#         nb = json.load(f)
    
#     headers = []
#     toc_cell_index = None
    
#     for i, cell in enumerate(nb['cells']):
#         if cell['cell_type'] == 'markdown':
#             content = ''.join(cell['source'])
            
#             # Check for TOC marker
#             if '<!-- TOC -->' in content:
#                 toc_cell_index = i
            
#             # Extract headers
#             for line in content.split('\n'):
#                 if line.startswith('#'):
#                     level = len(line.split(' ')[0])
#                     title = line.strip('#').strip()
#                     anchor = title.lower().replace(' ', '-').replace(':', '')
#                     headers.append((level, title, anchor))
    
#     # Generate TOC
#     toc_lines = ["<!-- TOC -->", "# Table of Contents", ""]
#     for level, title, anchor in headers:
#         if level > 1:  # Skip main title
#             indent = '  ' * (level - 2)
#             toc_lines.append(f"{indent}- [{title}](#{anchor})")
#     toc_lines.extend(["", "<!-- /TOC -->"])
    
#     if update_in_place and toc_cell_index is not None:
#         # Convert to notebook cell format (list of lines with \n)
#         nb['cells'][toc_cell_index]['source'] = [line + '\n' for line in toc_lines]
#         with open(notebook_path, 'w') as f:
#             json.dump(nb, f, indent=1)
#         return True
#     return False

# if __name__ == '__main__':
#     update = '--update' in sys.argv
    
#     # Check if --all flag is used
#     if '--all' in sys.argv:
#         notebooks = glob.glob('notebooks/*.ipynb')
#         updated = 0
#         for nb in notebooks:
#             if generate_toc(nb, update):
#                 print(f"Updated TOC in {nb}")
#                 updated += 1
#         print(f"\nProcessed {len(notebooks)} notebooks, updated {updated}")
#     else:
#         notebook = [arg for arg in sys.argv[1:] if not arg.startswith('--')][0]
#         if generate_toc(notebook, update):
#             print(f"Updated TOC in {notebook}")
#         else:
#             toc = generate_toc(notebook, False)


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
        return True, toc_lines
    
    return False, toc_lines

if __name__ == '__main__':
    update = '--update' in sys.argv
    
    # Check if --all flag is used
    if '--all' in sys.argv:
        notebooks = glob.glob('notebooks/*.ipynb')
        updated = 0
        for nb in notebooks:
            updated_status, toc = generate_toc(nb, update)
            if update and updated_status:
                print(f"✓ Updated TOC in {nb}")
                updated += 1
            elif not update:
                print(f"\n{'='*60}")
                print(f"Preview for: {nb}")
                print('='*60)
                print('\n'.join(toc))
        
        if update:
            print(f"\nProcessed {len(notebooks)} notebooks, updated {updated}")
    else:
        # Get notebook path from arguments
        notebook = [arg for arg in sys.argv[1:] if not arg.startswith('--')][0]
        updated_status, toc = generate_toc(notebook, update)
        
        if update:
            if updated_status:
                print(f"✓ Updated TOC in {notebook}")
            else:
                print(f"✗ No TOC marker found in {notebook}")
        else:
            # Preview mode
            print(f"TOC Preview for: {notebook}")
            print("="*60)
            print('\n'.join(toc))
            print("="*60)
            print("\nUse --update flag to write this TOC to the notebook")