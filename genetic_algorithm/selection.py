"""Módulo para operadores de seleção do Algoritmo Genético."""

import random
from typing import List, Dict, Any


def tournament_selection(
    population_with_fitness: List[Dict], k: int = 5
) -> List[Dict[str, Any]]:
    """
    [cite_start]Seleciona o melhor indivíduo de um subconjunto aleatório (torneio) da população. [cite: 22, 23]
    [cite_start]Este método equilibra a pressão seletiva e a diversidade. [cite: 24]
    """
    tournament_contenders = random.sample(population_with_fitness, k)
    winner = min(tournament_contenders, key=lambda ind: ind["fitness"])
    return winner["solution"]
