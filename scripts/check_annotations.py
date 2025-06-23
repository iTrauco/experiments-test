#!/usr/bin/env python3
import os
from pathlib import Path
import json
from datetime import datetime

def check_annotations():
    # output file
    output = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # project root
    project_root = Path('/home/trauco/experiments-test')
    annotations_dir = project_root / 'data' / 'annotations'
    
    output.append(f"Annotation Directory Diagnostic Report")
    output.append(f"Generated: {timestamp}")
    output.append("="*60)
    
    # check main dir
    output.append(f"\nAnnotations directory: {annotations_dir}")
    output.append(f"Exists: {annotations_dir.exists()}")
    
    if annotations_dir.exists():
        # scan all subdirs
        output.append("\nDirectory tree:")
        for root, dirs, files in os.walk(annotations_dir):
            level = root.replace(str(annotations_dir), '').count(os.sep)
            indent = ' ' * 2 * level
            output.append(f"{indent}{os.path.basename(root)}/")
            
            # show subdirs
            subindent = ' ' * 2 * (level + 1)
            for d in dirs:
                output.append(f"{subindent}{d}/")
            
            # show files
            for f in files:
                file_path = Path(root) / f
                size = file_path.stat().st_size
                output.append(f"{subindent}{f} ({size} bytes)")
        
        # specific checks
        output.append("\n" + "="*60)
        output.append("Specific locations:")
        
        # check each expected location
        locations = [
            'images',
            'labels', 
            'yolo_format',
            'yolo_format/images',
            'yolo_format/labels',
            'yolo_format/Train',
            'cvat_exports'
        ]
        
        for loc in locations:
            full_path = annotations_dir / loc
            output.append(f"\n{loc}:")
            output.append(f"  Exists: {full_path.exists()}")
            
            if full_path.exists():
                # count files by type
                jpg_files = list(full_path.glob('*.jpg'))
                txt_files = list(full_path.glob('*.txt'))
                other_files = [f for f in full_path.glob('*') if f.suffix not in ['.jpg', '.txt'] and f.is_file()]
                
                output.append(f"  JPG files: {len(jpg_files)}")
                output.append(f"  TXT files: {len(txt_files)}")
                output.append(f"  Other files: {len(other_files)}")
                
                # list first few files
                if jpg_files:
                    output.append("  Sample JPGs:")
                    for f in jpg_files[:3]:
                        output.append(f"    - {f.name}")
                
                if txt_files:
                    output.append("  Sample TXTs:")
                    for f in txt_files[:3]:
                        output.append(f"    - {f.name}")
    
    # write report
    report_path = project_root / f'annotations_diagnostic_{timestamp}.txt'
    with open(report_path, 'w') as f:
        f.write('\n'.join(output))
    
    print(f"✓ Diagnostic report saved to: {report_path}")
    
    # also print to console
    print("\n" + '\n'.join(output))

if __name__ == '__main__':
    check_annotations()