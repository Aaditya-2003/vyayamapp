import math

def calculate_angle(a, b, c):
    """Calculate the angle between three points a, b, c (each a dict with x, y)."""
    ba = (a['x'] - b['x'], a['y'] - b['y'])
    bc = (c['x'] - b['x'], c['y'] - b['y'])
    cosine_angle = (ba[0]*bc[0] + ba[1]*bc[1]) / (math.sqrt(ba[0]**2 + ba[1]**2) * math.sqrt(bc[0]**2 + bc[1]**2))
    angle = math.degrees(math.acos(cosine_angle))
    return angle

def correct_agnistambhasana(landmarks):
    """
    landmarks: list of dicts [{x:..., y:..., z:...}, ...]
    Returns feedback list.
    """
    feedback = []

    # Example check: Back should be straight (angle between shoulders & hips)
    left_shoulder = landmarks[11]
    left_hip = landmarks[23]
    left_knee = landmarks[25]
    
    angle_back = calculate_angle(left_shoulder, left_hip, left_knee)
    if angle_back < 165:  
        feedback.append("Keep your back straight.")
    
    # Example check: Knees aligned
    right_knee = landmarks[26]
    if abs(left_knee['y'] - right_knee['y']) > 0.05:
        feedback.append("Align your knees evenly.")

    if not feedback:
        feedback.append("Perfect! Hold the pose.")

    return feedback

def correct_baddhakonasana(landmarks):
    feedback = []

    # Check back alignment (shoulder-hip vertical)
    if not is_back_straight(landmarks):
        feedback.append("Keep your back straight.")

    # Check knees (they should be close to the floor)
    if not are_knees_low(landmarks):
        feedback.append("Gently press your knees toward the floor.")

    if not feedback:
        feedback.append("Great posture! Keep holding.")
    return feedback
