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
EPOCHS = 5  # Fewer epochs per round for speed
NUM_CLASSES = 45
INIT_LABELED = 100
QUERY_BATCH = 50
ROUNDS = 10

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

print('Loading data...')
X = load_images(SR_DIR, max_images=1000)
y = get_labels(max_images=1000)
y_cat = keras.utils.to_categorical(y, NUM_CLASSES)

# Split into initial labeled and unlabeled pool
idxs = np.arange(len(X))
np.random.shuffle(idxs)
labeled_idxs = idxs[:INIT_LABELED].tolist()
unlabeled_idxs = idxs[INIT_LABELED:].tolist()

for round in range(ROUNDS):
    print(f'\n=== Active Learning Round {round+1} ===')
    # Train classifier on current labeled set
    model = build_classifier()
    model.fit(
        X[labeled_idxs], y_cat[labeled_idxs],
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_split=0.1,
        verbose=2
    )
    # Predict on unlabeled pool
    probs = model.predict(X[unlabeled_idxs], batch_size=BATCH_SIZE)
    uncertainty = 1 - np.max(probs, axis=1)  # Least confident
    # Select QUERY_BATCH most uncertain samples
    query_idxs = np.argsort(uncertainty)[-QUERY_BATCH:]
    new_labeled = [unlabeled_idxs[i] for i in query_idxs]
    # Update pools
    labeled_idxs.extend(new_labeled)
    unlabeled_idxs = [i for i in unlabeled_idxs if i not in new_labeled]
    print(f'Labeled set size: {len(labeled_idxs)} | Unlabeled pool size: {len(unlabeled_idxs)}')
    # Optionally, evaluate on all data
    loss, acc = model.evaluate(X, y_cat, verbose=0)
    print(f'Current model accuracy on all data: {acc:.4f}')

# Save final model
model.save(os.path.join(os.path.dirname(__file__), 'classifier_active_learning.h5'))
print('Final active learning classifier saved as classifier_active_learning.h5')
