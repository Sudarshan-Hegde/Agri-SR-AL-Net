# Classifier training script for super-resolved images from RESISC45 dataset
#BASELINE / classifier trained on all data at once.("" WITHOUT THE CTIVE LARNING LOOP "")





import os
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image
import tensorflow_datasets as tfds

# Parameters
SR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_out'))
IMG_SIZE = (256, 256)
BATCH_SIZE = 16
EPOCHS = 10
NUM_CLASSES = 45  # RESISC45

# Load labels from TFDS (order matches sr_out/)
def get_labels(max_images=1000):
    ds, ds_info = tfds.load(
        'resisc45',
        split='train',
        shuffle_files=False,
        as_supervised=True,
        with_info=True
    )
    labels = []
    for i, (img, label) in enumerate(tfds.as_numpy(ds)):
        if i >= max_images:
            break
        labels.append(label)
    return np.array(labels)

# Load images
def load_images(folder, max_images=None):
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

print('Loading super-resolved images and labels...')
X = load_images(SR_DIR, max_images=1000)
y = get_labels(max_images=1000)
print(f'Loaded {X.shape[0]} images and {y.shape[0]} labels.')

# One-hot encode labels
y_cat = keras.utils.to_categorical(y, NUM_CLASSES)

# Build classifier
def build_classifier():
    model = keras.Sequential([
        layers.Input(shape=(256, 256, 3)),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(NUM_CLASSES, activation='softmax'),
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = build_classifier()
model.summary()

# Train
print('Training classifier...')
history = model.fit(
    X, y_cat,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_split=0.1
)

# Save model
model.save(os.path.join(os.path.dirname(__file__), 'classifier_model.h5'))
print('Classifier model saved as classifier_model.h5')
