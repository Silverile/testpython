import os
import cv2
import numpy as np
import h5py
from sklearn.model_selection import train_test_split
from HandRecognitionModel import build_model


# Check if processed data already exists
if os.path.exists('processed_images.h5'):
    # Load the processed images
    with h5py.File('processed_images.h5', 'r') as hf:
        loaded_images = hf['images'][:]
    print(f"Loaded {loaded_images.shape[0]} images from disk.")
else:
    # Your existing code to load and process images
    images = []
    dataset_directory = "/Users/cen69206/Downloads/Hands"
    count = 0
    for filename in os.listdir(dataset_directory):
        if filename.endswith(".jpg"):
            img_path = os.path.join(dataset_directory, filename)
            img = cv2.imread(img_path)
            img_resized = cv2.resize(img, (224, 224))
            img_normalized = img_resized / 255.0
            images.append(img_normalized)
            count += 1
            if count % 100 == 0:
                print(f"Processed {count} images.")
    images = np.array(images)

    # Save the processed images
    with h5py.File('processed_images.h5', 'w') as hf:
        hf.create_dataset('images', data=images)

    print(f"Processed and saved {images.shape[0]} images.")
# Load the processed images from the HDF5 file
with h5py.File('processed_images.h5', 'r') as hf:
    loaded_images = hf['images'][:]

# Split the data into training and test sets
X_train, X_test = train_test_split(loaded_images, test_size=0.2, random_state=42)

print(f"Number of training images: {X_train.shape[0]}")
print(f"Number of test images: {X_test.shape[0]}")
# Define the input shape based on one sample from the training set
input_shape = X_train[0].shape

# Build the model
model = build_model(input_shape)

# Fit the model to the training data
# Here, we're using 10 epochs and a batch size of 32 as an example.
# You can adjust these numbers based on your needs.
model.fit(X_train, epochs=10, batch_size=32, validation_data=(X_test,))

# Save the model for future use
model.save("hand_recognition_model.h5")