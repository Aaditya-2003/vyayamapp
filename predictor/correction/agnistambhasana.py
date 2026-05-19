# predictor/correction/agnistambhasana.py
from .base import BaseCorrection

class AgnistambhasanaCorrection(BaseCorrection):
    def check_alignment(self):
        corrections = []

        # Rule 1: Shins stacked
        left_dist = self.distance(self.landmarks["left_knee"], self.landmarks["right_ankle"])
        right_dist = self.distance(self.landmarks["right_knee"], self.landmarks["left_ankle"])
        if left_dist > 40 or right_dist > 40:
            corrections.append("Stack your shins, align knees over ankles.")

        # Rule 2: Spine upright
        spine_angle = self.angle_between(
            self.landmarks["hip"], self.landmarks["shoulder"], self.landmarks["ear"]
        )
        if abs(spine_angle - 180) > 15:
            corrections.append("Keep your spine upright, avoid leaning forward.")

        # Rule 3: Knees symmetry
        knee_height_diff = abs(
            self.landmarks["left_knee"][1] - self.landmarks["right_knee"][1]
        )
        if knee_height_diff > 20:
            corrections.append("Balance both knees to same height.")

        return corrections
