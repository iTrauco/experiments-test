## Environment Validation

This cell validates the environment for model training. The system checks:
- GPU availability and memory for training
- YOLO framework installation
- Required training dependencies
- Access to annotation outputs


```python
import sys
import torch
import importlib
from pathlib import Path
import subprocess

print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

# check ultralytics
try:
    import ultralytics
    print(f"✓ ultralytics: {ultralytics.__version__}")
except ImportError:
    print("✗ ultralytics - Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
    import ultralytics
    print(f"✓ ultralytics: {ultralytics.__version__}")

# verify dirs
dirs = ['data/annotations/yolo_format', 'models', 'runs']
for dir_path in dirs:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    print(f"✓ {dir_path}")
```

    Python: 3.12.9 | packaged by Anaconda, Inc. | (main, Feb  6 2025, 18:56:27) [GCC 11.2.0]
    PyTorch: 2.7.1+cu126
    CUDA Available: True
    GPU: NVIDIA RTX A5500
    Memory: 23.5 GB
    ✓ ultralytics: 8.3.158
    ✓ data/annotations/yolo_format
    ✓ models
    ✓ runs


## Set Working Directory

This cell changes the working directory to the project root. This ensures:
- Model saves to correct location
- Training data paths resolve correctly
- Output runs are organized


```python

import os
from pathlib import Path

# set project root
project_root = Path('/home/trauco/experiments-test')

# change to root
os.chdir(project_root)
print(f"Project root: {os.getcwd()}")

# verify paths
for path in ['data/annotations/yolo_format', 'configs', 'models', 'runs']:
    exists = Path(path).exists()
    print(f"{'✓' if exists else '✗'} {path}")
```

    Project root: /home/trauco/experiments-test
    ✓ data/annotations/yolo_format
    ✓ configs
    ✓ models
    ✗ runs


## Load Annotation Configuration

This cell loads the annotation configuration from the previous workflow. The process:
- Finds the most recent annotation config
- Loads data paths and parameters
- Verifies annotation data exists
- Displays annotation summary


```python
import json
import glob
import yaml

# find annotation configs
config_files = sorted(glob.glob('configs/annotation_*.json'))

if not config_files:
    print("✗ No annotation configs found")
    print("Run annotation notebook first")
else:
    # load latest
    latest_config = config_files[-1]
    print(f"Loading: {latest_config}")
    
    with open(latest_config, 'r') as f:
        annotation_config = json.load(f)
    
    # show info
    print(f"\nAnnotation info:")
    print(f"  Timestamp: {annotation_config['timestamp']}")
    print(f"  Frame count: {annotation_config['frame_count']}")
    print(f"  YAML path: {annotation_config['yaml_path']}")
    
    # verify yaml exists
    if Path(annotation_config['yaml_path']).exists():
        print("✓ data.yaml found")
        with open(annotation_config['yaml_path'], 'r') as f:
            data_yaml = yaml.safe_load(f)
            print(f"  Classes: {data_yaml['names']}")
    else:
        print("✗ data.yaml not found")
```

    Loading: configs/annotation_20250623_021049.json
    
    Annotation info:
      Timestamp: 20250623_021049
      Frame count: 40
      YAML path: data/annotations/yolo_format/data.yaml
    ✓ data.yaml found
      Classes: {0: 'vehicle'}


## Configure Training Parameters

This cell sets up the training configuration. Parameters include:
- Model selection (YOLOv8/v9 variant)
- Training hyperparameters
- Hardware optimization settings
- Output paths for results


```python
# training params
train_params = {
    'model': 'yolov8x.pt',  # x-large model for best accuracy
    'data': annotation_config['yaml_path'],
    'epochs': 100,  # more epochs for better training
    'imgsz': 640,  # larger size for better detection
    'batch': 32,  # larger batch with your gpu
    'device': 0,  # gpu 0
    'project': 'runs/detect',
    'name': 'traffic_baseline_v8x',
    'exist_ok': True,
    'patience': 20,  # more patience for larger model
    'save': True,
    'plots': True,
    'amp': True,  # mixed precision for speed
    'cache': True  # cache images in ram
}

print("Training configuration:")
for key, value in train_params.items():
    print(f"  {key}: {value}")

# check gpu memory for batch size
if torch.cuda.is_available():
    gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"\nGPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {gpu_mem:.1f} GB")
    print(f"Using YOLOv8x - largest model")
```

    Training configuration:
      model: yolov8x.pt
      data: data/annotations/yolo_format/data.yaml
      epochs: 100
      imgsz: 640
      batch: 32
      device: 0
      project: runs/detect
      name: traffic_baseline_v8x
      exist_ok: True
      patience: 20
      save: True
      plots: True
      amp: True
      cache: True
    
    GPU: NVIDIA RTX A5500
    Memory: 23.5 GB
    Using YOLOv8x - largest model


## Train YOLO Model

This cell initiates model training. The training process:
- Downloads YOLOv8x pretrained weights if needed
- Loads annotated dataset
- Trains model with specified parameters
- Saves best weights and training metrics


```python
from ultralytics import YOLO

# init model
print("Initializing YOLOv8x model...")
model = YOLO(train_params['model'])

# start training
print("\nStarting training...")
print(f"Dataset: {train_params['data']}")
print(f"Training will save to: {train_params['project']}/{train_params['name']}")

# train
results = model.train(**train_params)

print("\n✓ Training complete!")
print(f"Best weights saved to: {results.save_dir}/weights/best.pt")
print(f"Results saved to: {results.save_dir}")
```

    Initializing YOLOv8x model...
    Downloading https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8x.pt to 'yolov8x.pt'...


    100%|█████████████████| 131M/131M [00:01<00:00, 112MB/s]


    
    Starting training...
    Dataset: data/annotations/yolo_format/data.yaml
    Training will save to: runs/detect/traffic_baseline_v8x
    Ultralytics 8.3.158 🚀 Python-3.12.9 torch-2.7.1+cu126 CUDA:0 (NVIDIA RTX A5500, 24090MiB)
    [34m[1mengine/trainer: [0magnostic_nms=False, amp=True, augment=False, auto_augment=randaugment, batch=32, bgr=0.0, box=7.5, cache=True, cfg=None, classes=None, close_mosaic=10, cls=0.5, conf=None, copy_paste=0.0, copy_paste_mode=flip, cos_lr=False, cutmix=0.0, data=data/annotations/yolo_format/data.yaml, degrees=0.0, deterministic=True, device=0, dfl=1.5, dnn=False, dropout=0.0, dynamic=False, embed=None, epochs=100, erasing=0.4, exist_ok=True, fliplr=0.5, flipud=0.0, format=torchscript, fraction=1.0, freeze=None, half=False, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, imgsz=640, int8=False, iou=0.7, keras=False, kobj=1.0, line_width=None, lr0=0.01, lrf=0.01, mask_ratio=4, max_det=300, mixup=0.0, mode=train, model=yolov8x.pt, momentum=0.937, mosaic=1.0, multi_scale=False, name=traffic_baseline_v8x, nbs=64, nms=False, opset=None, optimize=False, optimizer=auto, overlap_mask=True, patience=20, perspective=0.0, plots=True, pose=12.0, pretrained=True, profile=False, project=runs/detect, rect=False, resume=False, retina_masks=False, save=True, save_conf=False, save_crop=False, save_dir=runs/detect/traffic_baseline_v8x, save_frames=False, save_json=False, save_period=-1, save_txt=False, scale=0.5, seed=0, shear=0.0, show=False, show_boxes=True, show_conf=True, show_labels=True, simplify=True, single_cls=False, source=None, split=val, stream_buffer=False, task=detect, time=None, tracker=botsort.yaml, translate=0.1, val=True, verbose=True, vid_stride=1, visualize=False, warmup_bias_lr=0.1, warmup_epochs=3.0, warmup_momentum=0.8, weight_decay=0.0005, workers=8, workspace=None
    



    ---------------------------------------------------------------------------

    FileNotFoundError                         Traceback (most recent call last)

    File ~/miniconda/lib/python3.12/site-packages/ultralytics/engine/trainer.py:607, in BaseTrainer.get_dataset(self)
        601 elif self.args.data.rsplit(".", 1)[-1] in {"yaml", "yml"} or self.args.task in {
        602     "detect",
        603     "segment",
        604     "pose",
        605     "obb",
        606 }:
    --> 607     data = check_det_dataset(self.args.data)
        608     if "yaml_file" in data:


    File ~/miniconda/lib/python3.12/site-packages/ultralytics/data/utils.py:463, in check_det_dataset(dataset, autodownload)
        462     m += f"\nNote dataset download directory is '{DATASETS_DIR}'. You can update this in '{SETTINGS_FILE}'"
    --> 463     raise FileNotFoundError(m)
        464 t = time.time()


    FileNotFoundError: Dataset 'data/annotations/yolo_format/data.yaml' images not found, missing path '/home/trauco/experiments-test/data/annotations/yolo_format/images'
    Note dataset download directory is '/home/trauco/traffic-vision/datasets'. You can update this in '/home/trauco/.config/Ultralytics/settings.json'

    
    The above exception was the direct cause of the following exception:


    RuntimeError                              Traceback (most recent call last)

    Cell In[7], line 13
         10 print(f"Training will save to: {train_params['project']}/{train_params['name']}")
         12 # train
    ---> 13 results = model.train(**train_params)
         15 print("\n✓ Training complete!")
         16 print(f"Best weights saved to: {results.save_dir}/weights/best.pt")


    File ~/miniconda/lib/python3.12/site-packages/ultralytics/engine/model.py:791, in Model.train(self, trainer, **kwargs)
        788 if args.get("resume"):
        789     args["resume"] = self.ckpt_path
    --> 791 self.trainer = (trainer or self._smart_load("trainer"))(overrides=args, _callbacks=self.callbacks)
        792 if not args.get("resume"):  # manually set model only if not resuming
        793     self.trainer.model = self.trainer.get_model(weights=self.model if self.ckpt else None, cfg=self.model.yaml)


    File ~/miniconda/lib/python3.12/site-packages/ultralytics/engine/trainer.py:153, in BaseTrainer.__init__(self, cfg, overrides, _callbacks)
        151 self.model = check_model_file_from_stem(self.args.model)  # add suffix, i.e. yolo11n -> yolo11n.pt
        152 with torch_distributed_zero_first(LOCAL_RANK):  # avoid auto-downloading dataset multiple times
    --> 153     self.data = self.get_dataset()
        155 self.ema = None
        157 # Optimization utils init


    File ~/miniconda/lib/python3.12/site-packages/ultralytics/engine/trainer.py:611, in BaseTrainer.get_dataset(self)
        609             self.args.data = data["yaml_file"]  # for validating 'yolo train data=url.zip' usage
        610 except Exception as e:
    --> 611     raise RuntimeError(emojis(f"Dataset '{clean_url(self.args.data)}' error ❌ {e}")) from e
        612 if self.args.single_cls:
        613     LOGGER.info("Overriding class names with single class.")


    RuntimeError: Dataset 'data/annotations/yolo_format/data.yaml' error ❌ Dataset 'data/annotations/yolo_format/data.yaml' images not found, missing path '/home/trauco/experiments-test/data/annotations/yolo_format/images'
    Note dataset download directory is '/home/trauco/traffic-vision/datasets'. You can update this in '/home/trauco/.config/Ultralytics/settings.json'


## Fix YOLO Directory Structure

This cell reorganizes the extracted CVAT data into YOLO's expected structure:
- Creates images/ subdirectory for image files
- Creates labels/ subdirectory for annotation files
- Moves .jpg files to images/
- Moves .txt label files to labels/
- Preserves config files in root directory

YOLO requires this specific structure to loc


```python
import shutil
from pathlib import Path

# check current structure
yolo_dir = Path('data/annotations/yolo_format')
print("Current structure:")
for item in yolo_dir.iterdir():
    print(f"  {item.name}")

# create images dir if needed
images_dir = yolo_dir / 'images'
if not images_dir.exists():
    images_dir.mkdir()
    print(f"\n✓ Created: {images_dir}")
    
    # move image files
    moved = 0
    for img_file in yolo_dir.glob('*.jpg'):
        shutil.move(str(img_file), str(images_dir / img_file.name))
        moved += 1
    print(f"✓ Moved {moved} images to images/")

# also need labels dir
labels_dir = yolo_dir / 'labels'
if not labels_dir.exists():
    labels_dir.mkdir()
    print(f"✓ Created: {labels_dir}")
    
    # move label files
    moved = 0
    for txt_file in yolo_dir.glob('*.txt'):
        if txt_file.name not in ['classes.txt', 'obj.names']:
            shutil.move(str(txt_file), str(labels_dir / txt_file.name))
            moved += 1
    print(f"✓ Moved {moved} label files to labels/")

# verify
print("\nNew structure:")
for subdir in ['images', 'labels']:
    count = len(list((yolo_dir / subdir).glob('*')))
    print(f"  {subdir}/: {count} files")
```

    Current structure:
      data.yaml
      Train
    
    ✓ Created: data/annotations/yolo_format/images
    ✓ Moved 0 images to images/
    ✓ Created: data/annotations/yolo_format/labels
    ✓ Moved 0 label files to labels/
    
    New structure:
      images/: 0 files
      labels/: 0 files



```python

```
