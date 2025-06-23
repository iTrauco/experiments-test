# Baseline ML Workflow Skeleton

**Repository** → [experiments-test](https://github.com/iTrauco/experiments-test)

A minimal engineering sandbox for isolating core machine learning workflow logic across notebooks.
Built to strip away noise and validate raw workflow mechanics.

---

## Table of Contents

* [Project Structure](#project-structure)
* [Scope](#scope)
* [Upstream Integration](#upstream-integration)
* [Reproducibility Framework](#reproducibility-framework)

  * [Environment Setup](#environment-setup)
  * [Environment Details](#environment-details)
  * [Environment Management](#environment-management)
* [References](#references)

---

## Project Structure

The following directory structure is created using the `setup_experiments_structure.sh` script:

```
experiments-test/
├── notebooks/
│   ├── 01_preprocessing.ipynb     # Preprocessing logic
│   ├── 02_training.ipynb          # Model training
│   └── 03_inference.ipynb         # Inference pipeline
├── data/
│   ├── raw/                       # Original recordings
│   ├── clips/                     # 60-second extracts
│   ├── frames/                    # Extracted frames
│   │   └── {camera_name}_{timestamp}/
│   └── annotations/              # CVAT outputs
├── configs/                       # JSON configs between notebooks
└── models/                        # Trained models
```

To generate this structure:

```bash
bash setup_experiments_structure.sh
```

---

## Scope

* Self-contained notebook logic
* Core workflow structure only
* No external orchestration
* No Python data science virtual environment dependency hell conflicts

## Upstream Integration

* Primary development repo → [traffic-vision-v0.4](https://github.com/iTrauco/traffic-vision-v0.4)
* Current unstable work lives in → [feature/experiments-framework](https://github.com/iTrauco/traffic-vision-v0.4/tree/feature/experiments-framework) — a chaotic prototype branch being deprecated.

This repo will drive a clean rebuild of workflow logic in the next iteration of `traffic-vision-v0.4`.

---

## Reproducibility Framework

### Environment Setup

This project uses a Conda environment to manage dependencies for reproducible analysis. Follow these steps to set up the environment:

#### Prerequisites

* Anaconda or Miniconda installed on your system
* Git for cloning the repository

#### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/iTrauco/experiments-test.git
   cd experiments-test
   ```

2. Create the Conda environment:

   ```bash
   conda create -n traffic-vision-env python=3.11 -y
   ```

3. Activate the environment:

   ```bash
   conda activate traffic-vision-env
   ```

4. Install baseline packages:

   ```bash
   conda install -c conda-forge jupyter numpy pandas matplotlib seaborn scikit-learn opencv -y
   ```

5. Install deep learning and computer vision packages:

   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   pip install ultralytics supervision
   ```

6. Launch Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

7. Access the notebook in your browser via the URL displayed in the terminal.

---

### Environment Details

The environment includes essential data science and computer vision packages:

* [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* [Jupyter Notebook](https://jupyter.org/documentation)
* [pandas](https://pandas.pydata.org/docs/) & [numpy](https://numpy.org/doc/stable/) for data manipulation
* [matplotlib](https://matplotlib.org/stable/index.html) & [seaborn](https://seaborn.pydata.org/) for visualization
* [scikit-learn](https://scikit-learn.org/stable/documentation.html) for traditional ML algorithms
* [OpenCV](https://docs.opencv.org/4.x/) for image and video processing
* [PyTorch](https://pytorch.org/docs/stable/index.html) for deep learning model development
* [Ultralytics](https://docs.ultralytics.com/) for YOLO object detection
* [Supervision](https://supervision.roboflow.com/) for object tracking utilities

---

### Environment Management

For collaborators who enhance the environment with additional packages:

```bash
# Export the updated environment
conda activate traffic-vision-env
conda env export > environment.yml
```

This ensures full reproducibility across systems by preserving all dependencies and versions.

---

---

**Author:** Christopher Trauco | [ORCID: 0009-0005-8113-6528](https://orcid.org/0009-0005-8113-6528)

---

## References

This repository includes citation tracking files located in the `references/` directory:

* [`citations.bib`](references/citations.bib)
* [`datasets.bib`](references/datasets.bib)
* [`software.bib`](references/software.bib)

These BibTeX files help manage research provenance and provide citation records for notebooks and datasets used in this project.
