"""Módulo para operadores de cruzamento (crossover) do Algoritmo Genético."""

import random
from typing import List, Dict, Any


def order_crossover(
    p1: List[Dict[str, Any]], p2: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Realiza o Order Crossover (OX).
    [cite_start]Preserva uma subsequência de um pai e preenche o restante com a ordem do outro. [cite: 26, 27]
    """
    length = len(p1)
    if length < 2:
        return p1

    start, end = sorted(random.sample(range(length), 2))

    child_middle = p1[start:end]
    child_middle_ids = {c["id"] for c in child_middle}

    child_rest = [item for item in p2 if item["id"] not in child_middle_ids]

    return child_rest[:start] + child_middle + child_rest[start:]
