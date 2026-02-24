import numpy as np


def gerar_recursos(idade: int, renda: float, gastos: float) -> np.ndarray:
    proporcao = (gastos / renda) if renda > 0 else 0.0
    return np.array([[idade, renda, gastos, proporcao]], dtype=float)