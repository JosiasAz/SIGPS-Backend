from fastapi import APIRouter, Depends, HTTPException

from app.routers.deps import require_admin, require_staff
from app.schemas.ml import MLTrainRequest, MLTrainResponse, MLPredictRequest, MLPredictResponse
from app.ml.model import train_model, predict_priority

router = APIRouter(prefix="/ml", tags=["ML"])


@router.post("/train", response_model=MLTrainResponse)
def train(data: MLTrainRequest, _=Depends(require_admin)):
    model_name, acc = train_model(n_samples=data.n_samples)
    return MLTrainResponse(model_name=model_name, accuracy=acc)


@router.post("/predict", response_model=MLPredictResponse)
def predict(data: MLPredictRequest, _=Depends(require_staff)):
    try:
        prioridade, score = predict_priority(data.idade, data.renda, data.gastos)
        return MLPredictResponse(prioridade=prioridade, score=score)
    except FileNotFoundError:
        raise HTTPException(status_code=409, detail="Modelo não encontrado. Treine primeiro em /ml/train (admin).")