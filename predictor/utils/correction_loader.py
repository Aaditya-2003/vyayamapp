import importlib

def get_correction_function(pose_name):
    try:
        module = importlib.import_module(f"predictor.pose_corrections.{pose_name}")
        return module.correct_pose
    except ModuleNotFoundError:
        return None
