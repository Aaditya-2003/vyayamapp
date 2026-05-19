# predictor/correction/base.py
import numpy as np

class BaseCorrection:
    def __init__(self, landmarks):
        """
        landmarks = dict like {"left_knee": (x, y), "right_knee": (x, y)}
        """
        self.landmarks = landmarks

    def angle_between(self, p1, p2, p3):
        """Calculate angle at p2 formed by points (p1, p2, p3)."""
        a = np.array(p1) - np.array(p2)
        b = np.array(p3) - np.array(p2)
        angle = np.degrees(
            np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        )
        return round(angle, 2)

    def distance(self, p1, p2):
        """Euclidean distance between two joints."""
        return round(np.linalg.norm(np.array(p1) - np.array(p2)), 2)

    def is_symmetric(self, val1, val2, tolerance=10):
        """Check if two values are close within tolerance."""
        return abs(val1 - val2) <= tolerance
