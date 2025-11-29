import os
import cv2
import numpy as np


def compute_blur(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    return cv2.Laplacian(img, cv2.CV_64F).var()


def compute_noise(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    return np.std(img)


def analyze_dataset(dataset_path):
    """
    Handles dataset structured like:
    dataset/
        train/
            0/
            1/
        test/
            0/
            1/
    OR any number of classes.
    """

    image_paths = []
    class_counts = {}

    # Loop over train and test folders
    for split in ["train", "test"]:
        split_path = os.path.join(dataset_path, split)
        if not os.path.exists(split_path):
            continue

        # Loop over class folders
        for cls in os.listdir(split_path):
            class_dir = os.path.join(split_path, cls)
            if not os.path.isdir(class_dir):
                continue

            # Count images in this class folder
            num_imgs = len([f for f in os.listdir(class_dir)
                            if f.lower().endswith((".jpg", ".jpeg", ".png"))])

            # Add to class count (sum train + test)
            class_counts[cls] = class_counts.get(cls, 0) + num_imgs

            # Add full image paths for blur/noise calc
            for img_file in os.listdir(class_dir):
                if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_paths.append(os.path.join(class_dir, img_file))

    # Calculate blur + noise scores
    blur_scores = [compute_blur(p) for p in image_paths]
    noise_scores = [compute_noise(p) for p in image_paths]

    # Avoid errors for empty datasets
    valid_blur = [x for x in blur_scores if x is not None]
    valid_noise = [x for x in noise_scores if x is not None]

    stats = {
        "size": len(image_paths),
        "class_dist": class_counts,
        "imbalance_ratio": (
            max(class_counts.values()) / min(class_counts.values())
            if len(class_counts) > 1 else 1
        ),
        "avg_blur": float(np.mean(valid_blur)) if valid_blur else 0.0,
        "avg_noise": float(np.mean(valid_noise)) if valid_noise else 0.0,
        "num_classes": len(class_counts)
    }

    return stats
