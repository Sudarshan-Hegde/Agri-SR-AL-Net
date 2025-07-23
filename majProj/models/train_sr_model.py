import os
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image

# Parameters
# Update paths to load from ../data/sr_hr and ../data/sr_lr relative to this script
HR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_hr'))
LR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_lr'))
IMG_SIZE = (256, 256)
BATCH_SIZE = 16
EPOCHS = 10  # You can increase for better results

# Helper to load images
def load_images_from_folder(folder, max_images=None):
    images = []
    files = sorted(os.listdir(folder))
    if max_images:
        files = files[:max_images]
    for filename in files:
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path).convert('RGB').resize(IMG_SIZE)
        img = np.array(img, dtype=np.float32) / 255.0
        images.append(img)
    return np.array(images)

print('Loading images...')
X = load_images_from_folder(LR_DIR)
y = load_images_from_folder(HR_DIR)
print(f'Loaded {X.shape[0]} image pairs.')

# SRCNN-like model
def build_srcnn():
    model = keras.Sequential([
        layers.Input(shape=(256, 256, 3)),
        layers.Conv2D(64, (9, 9), activation='relu', padding='same'),
        layers.Conv2D(32, (1, 1), activation='relu', padding='same'),
        layers.Conv2D(3, (5, 5), activation='sigmoid', padding='same'),
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

model = build_srcnn()
model.summary()

# Train
print('Training SRCNN model...')
history = model.fit(
    X, y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_split=0.1
)

# Save model
model.save(os.path.join(os.path.dirname(__file__), 'sr_model.h5'))
print('Model saved as sr_model.h5')
