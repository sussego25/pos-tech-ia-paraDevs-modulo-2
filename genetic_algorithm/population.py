"""Módulo para geração e gerenciamento da população de indivíduos."""

import random
from typing import List, Dict, Any

import config


def get_fixed_problem_set(num_cities: int) -> List[Dict[str, Any]]:
    """Cria um conjunto fixo de entregas (cidades) com base em uma semente."""
    random.seed(42)  # Semente para garantir a reprodutibilidade dos problemas
    fixed_deliveries = []
    for i in range(num_cities):
        start_time = random.randint(8, 16)
        end_time = start_time + random.randint(1, 2)
        coords = (
            random.randint(50, config.MAP_AREA_WIDTH - 50),
            random.randint(50, config.SCREEN_HEIGHT - 50),
        )
        fixed_deliveries.append(
            {"id": i, "coords": coords, "start_time": start_time, "end_time": end_time}
        )
    return fixed_deliveries


def generate_random_population(
    cities: List[Dict[str, Any]], size: int
) -> List[List[Dict[str, Any]]]:
    """
    [cite_start]Gera uma população inicial de soluções (rotas) aleatórias. [cite: 15]
    """
    if not cities or len(cities) == 0 or size <= 0:
        return []
    return [random.sample(cities, len(cities)) for _ in range(size)]
