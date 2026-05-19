import numpy as np

# ------------ JOINT ANGLE UTILITIES -----------------
def calc_angle(a, b, c):
    """
    Calculate the angle (in degrees) at point b, formed by points a-b-c.
    a, b, c: np.array([x, y])
    """
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return np.degrees(angle)

def get_joint_angles(landmarks_2d):
    """
    Compute main joint angles based on Mediapipe pose indices.
    Returns dict { joint_name: angle }
    """
    idxs = {
        "left_elbow": (11, 13, 15),
        "right_elbow": (12, 14, 16),
        "left_knee": (23, 25, 27),
        "right_knee": (24, 26, 28),
        "left_shoulder": (13, 11, 23),  # Elbow, Shoulder, Hip
        "right_shoulder": (14, 12, 24),
        # Add more as needed
    }
    angles = {}
    for joint, (a, b, c) in idxs.items():
        angles[joint] = calc_angle(landmarks_2d[a], landmarks_2d[b], landmarks_2d[c])
    return angles

# ------------ CORRECTION SUGGESTIONS GENERATOR --------------
def correction_feedback(
    user_landmarks,                     # shape (33, 2) np.array (x, y)
    predicted_pose_class,               # string label from your classifier
    reference_poses_path="reference_poses.npy",
    angle_threshold=12
):
    """
    Compare user pose vs. reference, and generate feedback for major joints.
    Returns: List of correction strings or a 'good job' message.
    """
    # Load saved reference poses
    reference_poses = np.load(reference_poses_path, allow_pickle=True).item()
    if predicted_pose_class not in reference_poses:
        return ["Reference pose unavailable for this class."]

    ref_flat = reference_poses[predicted_pose_class]  # shape (66,)
    ref_xs = ref_flat[:33]
    ref_ys = ref_flat[33:]
    ref_landmarks_2d = np.stack([ref_xs, ref_ys], axis=1).astype(np.float32)  # (33, 2)

    # Compute joint angles
    user_angles = get_joint_angles(user_landmarks)
    ref_angles = get_joint_angles(ref_landmarks_2d)

    feedback = []
    for joint in user_angles:
        user_ang = user_angles[joint]
        ref_ang = ref_angles[joint]
        diff = user_ang - ref_ang
        if abs(diff) > angle_threshold:
            if "elbow" in joint or "knee" in joint:
                if diff < 0:
                    feedback.append(f"Straighten your {joint.replace('_', ' ')} more.")
                else:
                    feedback.append(f"Bend your {joint.replace('_', ' ')} a bit.")
            if "shoulder" in joint:
                if diff > 0:
                    feedback.append(f"Lower your {joint.replace('_', ' ')}.")
                else:
                    feedback.append(f"Raise your {joint.replace('_', ' ')}.")
        # You can add more logic/messages per joint as needed!

    if not feedback:
        feedback = ["Pose alignment looks good! Well done."]

    return feedback

# ------------ USAGE EXAMPLE ------------
# user_landmarks: np.array shape (33, 2), current user pose (x, y) from Mediapipe
# predicted_pose_class: string, classifier result

# Example:
# user_landmarks = np.array([[...], ...])  # (33, 2)
# predicted_pose_class = "Triangle"
# corrections = correction_feedback(user_landmarks, predicted_pose_class, "reference_poses.npy")
# for msg in corrections:
#     print(msg)
import importlib

def get_correction_function(pose_name):
    try:
        module = importlib.import_module(f"predictor.pose_corrections.{pose_name}")
        return module.correct_pose
    except ModuleNotFoundError:
        return None
