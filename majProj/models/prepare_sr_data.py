import os
import tensorflow_datasets as tfds
import tensorflow as tf
from PIL import Image

# Parameters
MAX_IMAGES = 1000
HR_SIZE = (256, 256)  # High-resolution size
LR_SIZE = (64, 64)    # Low-resolution size
# Update paths to save in ../data/sr_hr and ../data/sr_lr relative to this script
HR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_hr'))
LR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/sr_lr'))

os.makedirs(HR_DIR, exist_ok=True)
os.makedirs(LR_DIR, exist_ok=True)

# Load dataset
raw_ds, _ = tfds.load(
    'resisc45',
    split='train',
    shuffle_files=True,
    as_supervised=True,
    with_info=True
)
ds = raw_ds.take(MAX_IMAGES)

print('Saving HR and LR image pairs...')
for i, (img, label) in enumerate(tfds.as_numpy(ds)):
    # Convert to PIL Image
    img_pil = Image.fromarray(img)
    # Ensure HR size
    img_hr = img_pil.resize(HR_SIZE, Image.BICUBIC)
    # Downsample to LR, then upsample back to HR size for input
    img_lr = img_hr.resize(LR_SIZE, Image.BICUBIC).resize(HR_SIZE, Image.BICUBIC)
    # Save images
    img_hr.save(os.path.join(HR_DIR, f'{i:04d}_hr.png'))
    img_lr.save(os.path.join(LR_DIR, f'{i:04d}_lr.png'))
    if (i+1) % 100 == 0:
        print(f'Saved {i+1} pairs')
print('Done!')
