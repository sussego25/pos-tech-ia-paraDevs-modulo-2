"""Módulo para operadores de mutação do Algoritmo Genético."""

import random
import copy
from typing import List, Dict, Any


def mutate(solution: List[Dict[str, Any]], probability: float) -> List[Dict[str, Any]]:
    """
    [cite_start]Realiza uma mutação de troca (swap) em uma solução com uma dada probabilidade. [cite: 28]
    [cite_start]A mutação introduz novidade na população, evitando estagnação. [cite: 29]
    """
    mutated_solution = copy.deepcopy(solution)
    if random.random() < probability:
        if len(solution) < 2:
            return solution

        idx1, idx2 = random.sample(range(len(solution)), 2)
        mutated_solution[idx1], mutated_solution[idx2] = (
            mutated_solution[idx2],
            mutated_solution[idx1],
        )

    return mutated_solution
