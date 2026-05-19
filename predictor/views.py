from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import numpy as np
import json
import joblib
import mediapipe as mp
from tensorflow.keras.models import load_model

# --- Pose metadata (basic info) ---
poses = [
    {'id': i, 'name': f'Pose {i}', 'image': f'predictor/images/pose{i}.jpg'}
    for i in range(1, 86)
]
pose_details = {
    1: {
        'name': 'Baddhakonasana',
        'instructions': (
            "Sit with your back straight. "
            "Bend your knees and bring the soles of your feet together. "
            "Hold your feet with your hands and gently press your knees toward the floor."
        ),
        'benefits': (
            "Improves hip flexibility, stimulates abdominal organs, relieves sciatica."
        ),
        'recommended_time': '30 seconds',
    },
    2: {
        'name': 'Agnistambhasana',
        'instructions': "Stack your shins on top of each other.",
        'benefits': "Opens hips and relieves tension.",
        'recommended_time': '30-60 seconds',
    },
}


# --- Load ML model + encoder ---
model = load_model("predictor/models/pose_deep_model_balanced.keras")
label_encoder = joblib.load("predictor/models/label_encoder.pkl")
mp_pose = mp.solutions.pose

REFERENCE_POSES_PATH = "predictor/correction/reference_poses.npy"
reference_poses = np.load(REFERENCE_POSES_PATH, allow_pickle=True).item()

# --- Helpers ---
def get_pose_embedding(landmarks):
    """Normalize landmarks based on hip center"""
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    base_x, base_y, base_z = hip['x'], hip['y'], hip['z']
    embedding = []
    for lm in landmarks:
        embedding.extend([lm['x'] - base_x, lm['y'] - base_y, lm['z'] - base_z])
    return np.array(embedding).reshape(1, -1)

# --- Views ---
@login_required
def pose_grid(request):
    return render(request, 'predictor/pose_grid.html', {'poses': poses})

@login_required
def pose_instructions(request, pose_id):
    if pose_id not in pose_details:
        raise Http404("Pose not found")

    pose = pose_details[pose_id]
    prev_id = pose_id - 1 if pose_id > 1 else None
    next_id = pose_id + 1 if pose_id < 85 else None

    return render(request, 'predictor/pose_instructions.html', {
        'pose_id': pose_id,
        'pose': pose,
        'prev_id': prev_id,
        'next_id': next_id,
    })

from django.http import JsonResponse
from predictor.correction.registry import get_corrector as get_correction_class


@login_required
def live_pose(request, pose_id):
    if pose_id not in pose_details:
        raise Http404("Pose not found")

    pose = pose_details[pose_id]
    predicted_pose = pose["name"]  # Link pose_id → name

    # Example landmarks for demo (replace with real ML output)
    landmarks_dict = {
        "left_knee": (100, 250),
        "right_knee": (140, 250),
        "left_ankle": (110, 320),
        "right_ankle": (130, 320),
        "hip": (120, 200),
        "shoulder": (120, 150),
        "ear": (120, 100),
    }

    CorrectionClass = get_correction_class(predicted_pose)
    feedback = []
    if CorrectionClass:
        correction = CorrectionClass(landmarks_dict)
        feedback = correction.check_alignment()

    return render(request, "predictor/live_pose.html", {
        "pose_id": pose_id,
        "pose": pose,
        "correction": feedback
    })

# --- Pose correction API ---
from predictor.correction.pose_correction import correct_agnistambhasana
from predictor.utils.correction_loader import get_correction_function

@csrf_exempt
def pose_correction_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"})

    data = json.loads(request.body)
    landmarks = data.get("landmarks")
    pose_name = data.get("pose_name")  # Get pose name from POST body

    if not landmarks:
        return JsonResponse({"error": "No landmarks provided"})
    if not pose_name:
        return JsonResponse({"error": "No pose name provided"})

    # Example: use pose_name to select correction function
    if pose_name == "Agnistambhasana":
        feedback = correct_agnistambhasana(landmarks)
    else:
        feedback = ["No correction available for this pose."]

    return JsonResponse({
        "predicted_pose": pose_name,
        "feedback": feedback
    })
