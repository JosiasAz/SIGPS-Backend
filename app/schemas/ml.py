from pydantic import BaseModel


class MLTrainRequest(BaseModel):
    n_samples: int = 300


class MLTrainResponse(BaseModel):
    ml_model_name: str
    accuracy: float


class MLPredictRequest(BaseModel):
    idade: int
    renda: float
    gastos: float


class MLPredictResponse(BaseModel):
    prioridade: int
    score: float