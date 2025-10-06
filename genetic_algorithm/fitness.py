"""Módulo para a função de avaliação (fitness) do Algoritmo Genético."""

import math
from typing import List, Dict, Any


def _calculate_distance(p1: Dict[str, Any], p2: Dict[str, Any]) -> float:
    """Calcula a distância euclidiana entre duas cidades."""
    return math.sqrt(
        (p1["coords"][0] - p2["coords"][0]) ** 2
        + (p1["coords"][1] - p2["coords"][1]) ** 2
    )


def calculate_fitness(
    path: List[Dict[str, Any]], vehicle_params: Dict[str, float]
) -> float:
    """
    [cite_start]Calcula o custo total de uma rota, servindo como função de fitness. [cite: 19]
    O custo considera distância, tempo e penalidades por quebra de regras.
    """
    if not path:
        return float("inf")

    total_distance = 0.0
    current_time = 0.0
    time_penalty = 0.0

    # Assume que a rota começa no início da janela de tempo da primeira cidade
    if current_time < path[0]["start_time"]:
        current_time = float(path[0]["start_time"])

    n = len(path)
    for i in range(n):
        current_city = path[i]
        next_city = path[(i + 1) % n]

        distance = _calculate_distance(current_city, next_city)
        total_distance += distance
        travel_time = distance * vehicle_params["time_multiplier"]

        arrival_time = current_time + travel_time

        # [cite_start]Penalidade por atraso na entrega [cite: 36]
        if arrival_time > current_city["end_time"]:
            time_penalty += (arrival_time - current_city["end_time"]) * vehicle_params[
                "late_penalty_multiplier"
            ]

        # [cite_start]Tempo de espera se chegar cedo (respeitando a janela de tempo) [cite: 35]
        current_time = max(arrival_time, float(current_city["start_time"]))

    # [cite_start]Penalidade massiva por exceder a autonomia, tornando a rota inválida [cite: 33, 34]
    if total_distance > vehicle_params["max_range"]:
        return 1_000_000.0 + (total_distance - vehicle_params["max_range"])

    # [cite_start]Custos operacionais [cite: 32]
    cost_from_distance = total_distance * vehicle_params["cost_per_km"]
    cost_from_time = current_time * vehicle_params["cost_per_hour"]

    operational_cost = cost_from_distance + cost_from_time

    return operational_cost + time_penalty
