from pathlib import Path
import joblib
from app.core.config import settings


def garantir_diretorio() -> Path:
    p = Path(settings.ML_MODEL_DIR)
    p.mkdir(parents=True, exist_ok=True)
    return p


def obter_caminho_modelo() -> Path:
    return garantir_diretorio() / settings.ML_MODEL_NAME


def salvar(objeto) -> str:
    caminho = obter_caminho_modelo()
    joblib.dump(objeto, caminho)
    return str(caminho)


def carregar():
    caminho = obter_caminho_modelo()
    if not caminho.exists():
        raise FileNotFoundError(str(caminho))
    return joblib.load(caminho)