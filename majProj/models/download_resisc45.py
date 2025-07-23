import tensorflow_datasets as tfds

# Limit the number of images to load
MAX_IMAGES = 1000

# Download and prepare the RESISC45 dataset
dataset, ds_info = tfds.load(
    'resisc45',
    split='train',
    shuffle_files=True,
    as_supervised=True,
    with_info=True
)
ds = dataset.take(MAX_IMAGES)

print(f"Dataset '{ds_info.name}' loaded successfully.")
print(f"Number of examples in subset: {MAX_IMAGES}")
print(f"Number of classes: {ds_info.features['label'].num_classes}")
