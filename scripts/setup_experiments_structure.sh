#!/bin/bash

# target dir
TARGET_DIR=~/experiments-test

# check dir
if [ -d "$TARGET_DIR" ]; then
  echo "using existing dir: $TARGET_DIR"
else
  echo "creating dir: $TARGET_DIR"
  mkdir -p "$TARGET_DIR"
fi

# cd in
cd "$TARGET_DIR" || exit 1

# make dirs
mkdir -p notebooks data/{raw,clips,frames/sample_camera_20250622,annotations} configs models

# readmes
echo "Notebooks for preprocessing, training, and inference." > notebooks/README.md
echo "Directory for raw original recordings." > data/raw/README.md
echo "Directory for 60-second extracted clips." > data/clips/README.md
echo "Directory for extracted frames." > data/frames/README.md
echo "Directory for annotation outputs." > data/annotations/README.md
echo "Configuration files for workflows." > configs/README.md
echo "Trained machine learning models." > models/README.md

# base notebook
cat <<EOF > notebooks/01_preprocessing.ipynb
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## IN DEVELOPMENT..."
   ]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
EOF

# copy notebooks
cp notebooks/01_preprocessing.ipynb notebooks/02_training.ipynb
cp notebooks/01_preprocessing.ipynb notebooks/03_inference.ipynb

# done
echo "ready: $TARGET_DIR"
