import joblib
from tensorflow.keras.models import load_model

model = load_model("predictor\models\pose_deep_model_balanced.keras")
label_encoder = joblib.load("predictor\models\label_encoder.pkl")
