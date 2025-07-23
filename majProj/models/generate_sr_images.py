import os
import numpy as np
from tensorflow import keras
from PIL import Image

# Paths
LR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_lr'))
SR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_out'))
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'sr_model.h5')
IMG_SIZE = (256, 256)

os.makedirs(SR_DIR, exist_ok=True)

# Load model
model = keras.models.load_model(MODEL_PATH, compile=False)

# Helper to load images
def load_images_from_folder(folder):
    images = []
    files = sorted(os.listdir(folder))
    for filename in files:
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path).convert('RGB').resize(IMG_SIZE)
        img = np.array(img, dtype=np.float32) / 255.0
        images.append((filename, img))
    return images

print('Loading LR images...')
lr_images = load_images_from_folder(LR_DIR)

print('Generating super-resolved images...')
for filename, img in lr_images:
    sr_img = model.predict(np.expand_dims(img, axis=0))[0]
    sr_img = np.clip(sr_img * 255.0, 0, 255).astype(np.uint8)
    sr_pil = Image.fromarray(sr_img)
    sr_pil.save(os.path.join(SR_DIR, filename.replace('_lr', '_sr')))
print('Super-resolved images saved to sr_out/')
