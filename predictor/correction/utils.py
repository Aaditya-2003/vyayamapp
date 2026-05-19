import numpy as np
import math

# MediaPipe indices
LEFT = "left"
RIGHT = "right"

# For readability
LM_ID = {
    "LEFT_SHOULDER": 11, "RIGHT_SHOULDER": 12,
    "LEFT_ELBOW": 13, "RIGHT_ELBOW": 14,
    "LEFT_WRIST": 15, "RIGHT_WRIST": 16,
    "LEFT_HIP": 23, "RIGHT_HIP": 24,
    "LEFT_KNEE": 25, "RIGHT_KNEE": 26,
    "LEFT_ANKLE": 27, "RIGHT_ANKLE": 28,
    "LEFT_HEEL": 29, "RIGHT_HEEL": 30,
    "LEFT_FOOT_INDEX": 31, "RIGHT_FOOT_INDEX": 32
}

def to_np(landmarks):
    """
    Convert list of dicts [{'x':..,'y':..,'z':..}, ...] to numpy array of shape (33, 2).
    We only use (x,y) for 2D geometry.
    """
    pts = np.array([[lm["x"], lm["y"]] for lm in landmarks], dtype=np.float32)
    return pts

def angle_3pts(a, b, c):
    """
    Angle (in degrees) at point B formed by A-B-C.
    a,b,c: np.array of shape (2,)
    """
    ba = a - b
    bc = c - b
    # Normalize
    if np.linalg.norm(ba) == 0 or np.linalg.norm(bc) == 0:
        return None
    cosang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosang = np.clip(cosang, -1.0, 1.0)
    return np.degrees(np.arccos(cosang))

def vector_angle_with_x(p1, p2):
    """
    Angle of vector p1->p2 with respect to +X axis (degrees).
    0 or 180 means horizontal, 90 means vertical.
    """
    v = p2 - p1
    if np.linalg.norm(v) == 0:
        return None
    ang = np.degrees(np.arctan2(v[1], v[0]))  # y, x
    # Normalize to [0, 180]
    ang = abs(ang)
    if ang > 180:
        ang = 360 - ang
    return ang

def within(value, target, tol):
    return value is not None and abs(value - target) <= tol

def rel_dist(a, b):
    """Euclidean dist between two 2D points."""
    return float(np.linalg.norm(a - b))
