import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow import keras

# Paths
LR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_lr'))
SR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_out'))
HR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_hr'))
CLASSIFIER_PATH = os.path.join(os.path.dirname(__file__), 'classifier_active_learning.h5')
IMG_SIZE = (256, 256)
NUM_CLASSES = 45
N_SAMPLES = 10  # Number of images to visualize

# Load classifier
classifier = keras.models.load_model(CLASSIFIER_PATH, compile=False)

# Helper to load images
def load_image(path):
    img = Image.open(path).convert('RGB').resize(IMG_SIZE)
    return np.array(img, dtype=np.float32) / 255.0

def get_label_names():
    # Hardcoded for RESISC45
    return [
        'airplane', 'airport', 'baseball_diamond', 'basketball_court', 'beach', 'bridge', 'chaparral', 'church',
        'circular_farmland', 'cloud', 'commercial_area', 'dense_residential', 'desert', 'forest', 'freeway',
        'golf_course', 'ground_track_field', 'harbor', 'industrial_area', 'intersection', 'island', 'lake',
        'meadow', 'medium_residential', 'mobile_home_park', 'mountain', 'overpass', 'palace', 'parking_lot',
        'railway', 'railway_station', 'rectangular_farmland', 'river', 'roundabout', 'runway', 'sea_ice',
        'ship', 'snowberg', 'sparse_residential', 'stadium', 'storage_tank', 'tennis_court', 'terrace',
        'thermal_power_station', 'wetland', 'windmill'
    ]

label_names = get_label_names()

# Visualize LR, SR, HR side by side
files = sorted(os.listdir(LR_DIR))[:N_SAMPLES]
plt.figure(figsize=(12, 4*N_SAMPLES))
for i, fname in enumerate(files):
    lr_img = load_image(os.path.join(LR_DIR, fname))
    sr_img = load_image(os.path.join(SR_DIR, fname.replace('_lr', '_sr')))
    hr_img = load_image(os.path.join(HR_DIR, fname.replace('_lr', '_hr')))
    # Classification prediction
    pred = classifier.predict(np.expand_dims(sr_img, axis=0))[0]
    pred_label = np.argmax(pred)
    pred_name = label_names[pred_label]
    confidence = float(pred[pred_label])
    # True label from filename index
    true_idx = int(fname.split('_')[0])
    true_name = label_names[true_idx // (1000//NUM_CLASSES)] if NUM_CLASSES == 45 else str(true_idx)
    correct = (pred_label == (true_idx // (1000//NUM_CLASSES)))
    # Plot
    for j, (img, title) in enumerate(zip([lr_img, sr_img, hr_img], ['LR', 'SR', 'HR'])):
        plt.subplot(N_SAMPLES, 3, i*3+j+1)
        plt.imshow(img)
        plt.axis('off')
        if title == 'SR':
            plt.title(f"{title}\nPred: {pred_name}\nConf: {confidence:.2f}\nTrue: {true_name}\n{'Correct' if correct else 'Wrong'}", fontsize=10)
        else:
            plt.title(title)
plt.tight_layout()
plt.show()
