import pandas as pd
import numpy as np

# Load your dataset
df = pd.read_csv("../data/pose_data_balanced.csv")

# Identify landmark columns
NUM_KEYPOINTS = 33
x_columns = [f"x_{i}" for i in range(NUM_KEYPOINTS)]
y_columns = [f"y_{i}" for i in range(NUM_KEYPOINTS)]
landmark_columns = x_columns + y_columns

# Compute mean (reference) landmarks for each class
reference_poses = {}  # Dictionary of pose_class: mean_landmarks
for pose_class in df['class'].unique():
    class_samples = df[df['class'] == pose_class][landmark_columns].values
    mean_landmarks = np.mean(class_samples, axis=0)  # Shape: (66,)
    reference_poses[pose_class] = mean_landmarks

# Optionally: Save reference poses for later use
np.save("../data/reference_poses.npy", reference_poses)
