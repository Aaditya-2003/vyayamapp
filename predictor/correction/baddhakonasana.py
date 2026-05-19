# predictor/correction/baddhakonasana.py
from .base import BaseCorrection

class BaddhakonasanaCorrection(BaseCorrection):
    def check_alignment(self):
        corrections = []

        # Rule 1: Knees toward the floor
        left_knee_height = self.landmarks["left_knee"][1]
        right_knee_height = self.landmarks["right_knee"][1]
        hip_height = self.landmarks["hip"][1]

        if left_knee_height - hip_height > 50 or right_knee_height - hip_height > 50:
            corrections.append("Gently press your knees down toward the floor.")

        # Rule 2: Spine upright
        spine_angle = self.angle_between(
            self.landmarks["hip"], self.landmarks["shoulder"], self.landmarks["ear"]
        )
        if abs(spine_angle - 180) > 15:
            corrections.append("Keep your spine tall and upright.")

        # Rule 3: Feet together
        feet_distance = self.distance(self.landmarks["left_ankle"], self.landmarks["right_ankle"])
        if feet_distance > 40:
            corrections.append("Bring your feet closer together, soles touching.")

        return corrections
