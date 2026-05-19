from .agnistambhasana import AgnistambhasanaCorrection
from .baddhakonasana import BaddhakonasanaCorrection
# Register all pose correctors here
_CORRECTORS = {
    "agnistambhasana": AgnistambhasanaCorrection,
     "Baddhakonasana": BaddhakonasanaCorrection,
    # "baddhakonasana": BaddhakonasanaCorrector,  # add later
    # ...
}

def get_corrector(pose_key: str):
    pose_key = pose_key.strip().lower()
    cls = _CORRECTORS.get(pose_key)
    if not cls:
        return None
    return cls()
