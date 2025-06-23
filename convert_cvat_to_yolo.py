#!/usr/bin/env python3
"""
Convert CVAT JSON annotations to YOLO format
Matches your existing training workflow structure
"""

import json
import shutil
from pathlib import Path
from collections import defaultdict

def convert_cvat_to_yolo(json_file, output_dir, image_width=480, image_height=270):
    """
    Convert CVAT JSON annotations to YOLO format
    
    Args:
        json_file: Path to CVAT annotations JSON
        output_dir: Output directory for YOLO format files
        image_width: Image width in pixels (default 480 for traffic cam)
        image_height: Image height in pixels (default 270 for traffic cam)
    """
    
    # Load CVAT annotations
    with open(json_file, 'r') as f:
        cvat_data = json.load(f)
    
    # Create output directories
    output_path = Path(output_dir)
    images_dir = output_path / 'images'
    labels_dir = output_path / 'labels'
    
    # Clean and create directories
    if output_path.exists():
        shutil.rmtree(output_path)
    
    output_path.mkdir(parents=True)
    images_dir.mkdir()
    labels_dir.mkdir()
    
    # Group annotations by frame
    frames_annotations = defaultdict(list)
    
    for shape in cvat_data['shapes']:
        if shape['type'] == 'rectangle':
            frame_num = shape['frame']
            points = shape['points']  # [x1, y1, x2, y2]
            
            # Convert to YOLO format (class_id, center_x, center_y, width, height)
            # All normalized to 0-1
            x1, y1, x2, y2 = points
            
            # Calculate center and dimensions
            center_x = (x1 + x2) / 2.0 / image_width
            center_y = (y1 + y2) / 2.0 / image_height  
            width = abs(x2 - x1) / image_width
            height = abs(y2 - y1) / image_height
            
            # Class ID 0 for vehicle (YOLO uses 0-based indexing)
            class_id = 0
            
            yolo_annotation = f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}"
            frames_annotations[frame_num].append(yolo_annotation)
    
    # Copy images from annotation images directory
    source_images = Path('data/annotations/images')
    if source_images.exists():
        for img_file in source_images.glob('*.jpg'):
            shutil.copy2(img_file, images_dir / img_file.name)
    
    # Create label files for each frame
    created_labels = 0
    for frame_num, annotations in frames_annotations.items():
        # Create label file name matching image name
        label_file = labels_dir / f"frame_{frame_num:04d}.txt"
        
        with open(label_file, 'w') as f:
            f.write('\n'.join(annotations) + '\n')
        
        created_labels += 1
    
    # Create data.yaml file
    data_yaml = {
        'path': str(output_path.absolute()),
        'train': 'images',
        'val': 'images',  # Using same for initial training
        'names': {0: 'vehicle'}
    }
    
    import yaml
    with open(output_path / 'data.yaml', 'w') as f:
        yaml.dump(data_yaml, f)
    
    return {
        'frames_with_annotations': len(frames_annotations),
        'total_annotations': len(cvat_data['shapes']),
        'output_dir': str(output_path),
        'created_labels': created_labels
    }

if __name__ == '__main__':
    # Convert the annotations
    result = convert_cvat_to_yolo(
        json_file='annotations_api.json',
        output_dir='data/annotations/yolo_format',
        image_width=480,  # Traffic camera resolution
        image_height=270
    )
    
    print("CVAT to YOLO Conversion Complete!")
    print(f"✓ Frames with annotations: {result['frames_with_annotations']}")
    print(f"✓ Total annotations: {result['total_annotations']}")
    print(f"✓ Created label files: {result['created_labels']}")
    print(f"✓ Output directory: {result['output_dir']}")
    print(f"✓ Ready for YOLO training!")
    
    # Verify structure
    output_path = Path(result['output_dir'])
    images_count = len(list((output_path / 'images').glob('*.jpg')))
    labels_count = len(list((output_path / 'labels').glob('*.txt')))
    
    print(f"\nDirectory structure:")
    print(f"  images/: {images_count} files")
    print(f"  labels/: {labels_count} files")
    print(f"  data.yaml: {'✓' if (output_path / 'data.yaml').exists() else '✗'}")