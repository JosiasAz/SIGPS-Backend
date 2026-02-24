from dataclasses import dataclass
from typing import Tuple
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from app.ml.storage import salvar, carregar
from app.ml.features import gerar_recursos


@dataclass
class ModeloEmpacotado:
    modelo: LogisticRegression


def _gerar_dados_ficticios(n: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(42)
    idade = rng.integers(18, 75, size=n)
    renda = rng.normal(3500, 1700, size=n).clip(500, 25000)
    gastos = rng.normal(2200, 1400, size=n).clip(0, 30000)
    prop = gastos / renda
    # classe 1: "prioridade alta" (apenas baseline para TCC)
    y = ((prop > 0.8) | (idade > 65)).astype(int)
    X = np.column_stack([idade, renda, gastos, prop]).astype(float)
    return X, y


def treinar_IA(n_amostras: int = 300) -> Tuple[str, float]:
    n = max(80, int(n_amostras))
    X, y = _gerar_dados_ficticios(n)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=7, stratify=y)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(Xtr, ytr)

    precisao = float(accuracy_score(yte, clf.predict(Xte)))
    empacotado = ModeloEmpacotado(modelo=clf)
    caminho = salvar(empacotado)
    return caminho.split("/")[-1], precisao


def prever_prioridade(idade: int, renda: float, gastos: float) -> tuple[int, float]:
    empacotado: ModeloEmpacotado = carregar()
    X = gerar_recursos(idade, renda, gastos)
    proba = empacotado.modelo.predict_proba(X)[0]
    pontuacao = float(proba[1])  # prob de classe 1 (alta)
    prioridade = int(round(pontuacao * 100))
    return prioridade, pontuacao