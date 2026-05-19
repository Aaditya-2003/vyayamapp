from base import calculate_angle, feedback_message

def correct_pose(landmarks):
    """
    Correction logic for Agnistambhasana (Fire Log Pose)
    landmarks: dict of body points (x, y)
    """
    feedback = []

    # Check knee alignment (both knees should be stacked)
    left_knee = landmarks["LEFT_KNEE"]
    right_knee = landmarks["RIGHT_KNEE"]
    knee_diff = abs(left_knee[1] - right_knee[1])
    feedback.append(
        feedback_message(knee_diff < 30,
            "Good! Knees are aligned.",
            "Align both knees vertically for proper stacking."
        )
    )

    # Check hip opening (thigh and shin roughly at 90°)
    left_hip = landmarks["LEFT_HIP"]
    left_ankle = landmarks["LEFT_ANKLE"]
    angle = calculate_angle(left_hip, left_knee, left_ankle)
    feedback.append(
        feedback_message(80 <= angle <= 100,
            "Nice hip opening!",
            "Try adjusting your shin to form a 90° angle."
        )
    )

    # Check spine uprightness (shoulder over hips)
    left_shoulder = landmarks["LEFT_SHOULDER"]
    spine_tilt = abs(left_shoulder[0] - left_hip[0])
    feedback.append(
        feedback_message(spine_tilt < 25,
            "Great! Spine is upright.",
            "Keep your spine straight, avoid leaning sideways."
        )
    )

    return feedback
