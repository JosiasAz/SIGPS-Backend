from pathlib import Path
import joblib
from app.core.config import settings


def ensure_dir() -> Path:
    p = Path(settings.ML_MODEL_DIR)
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_model_path() -> Path:
    return ensure_dir() / settings.ML_MODEL_NAME


def save(obj) -> str:
    path = get_model_path()
    joblib.dump(obj, path)
    return str(path)


def load():
    path = get_model_path()
    if not path.exists():
        raise FileNotFoundError(str(path))
    return joblib.load(path)