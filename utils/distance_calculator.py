# /utils/distance_calculator.py
"""Módulo com funções de utilidade para cálculos matemáticos."""

import math
from typing import Dict, Any


def calculate_distance(p1: Dict[str, Any], p2: Dict[str, Any]) -> float:
    """Calcula a distância euclidiana entre duas cidades."""
    return math.sqrt(
        (p1["coords"][0] - p2["coords"][0]) ** 2
        + (p1["coords"][1] - p2["coords"][1]) ** 2
    )
