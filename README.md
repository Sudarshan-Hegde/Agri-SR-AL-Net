# Agri-SR-AL-Net

A Joint Network of Super-Resolution and Active Learning for Agricultural Land Classification

## Overview
This project implements a novel approach combining Super-Resolution (SR) and Active Learning for improved agricultural land classification using remote sensing imagery. The system consists of two main components:

1. **Super-Resolution Network**: Enhances the quality of low-resolution satellite imagery
2. **Active Learning Classifier**: Efficiently learns to classify agricultural land types while minimizing the need for labeled data

## Project Structure
```
majProj/
├── models/
│   ├── active_learning_loop.py    # Active learning implementation
│   ├── train_classifier.py        # Classifier training
│   ├── train_sr_model.py         # Super-resolution model training
│   └── generate_sr_images.py      # Generate super-resolution images
├── data/
│   ├── prepare_sr_data.py        # Data preparation scripts
│   └── download_resisc45.py      # Dataset download script
```

## Features
- Super-resolution enhancement of low-resolution satellite imagery
- Active learning-based classification with uncertainty sampling
- Integration with RESISC45 dataset
- Dynamic model training with iterative improvement
- Efficient labeling strategy to minimize annotation costs

## Requirements
- Python 3.x
- TensorFlow 2.x
- Keras
- NumPy
- PIL
- TensorFlow Datasets

## Setup and Installation
1. Create a virtual environment:
   ```bash
   python -m venv majProj
   source majProj/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Prepare Dataset**:
   ```bash
   python data/download_resisc45.py
   python data/prepare_sr_data.py
   ```

2. **Train Super-Resolution Model**:
   ```bash
   python models/train_sr_model.py
   ```

3. **Run Active Learning Loop**:
   ```bash
   python models/active_learning_loop.py
   ```

## Model Architecture
- **Super-Resolution Network**: Convolutional neural network for image enhancement
- **Classifier**: CNN-based architecture with uncertainty-aware active learning
- **Active Learning Strategy**: Least confidence sampling for efficient data labeling

## Performance
- Improved classification accuracy through super-resolution enhancement
- Reduced annotation costs through active learning
- Progressive improvement in model performance across active learning rounds

## License
MIT License

## Authors
- Sudarshan Hegde
