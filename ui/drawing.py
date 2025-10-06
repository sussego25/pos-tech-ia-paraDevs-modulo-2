"""Módulo para funções de desenho com Pygame."""

import pygame
import math
from typing import List, Dict, Any, Tuple

import config


def draw_points(surface: pygame.Surface, points: List[Dict[str, Any]]) -> None:
    """Desenha os pontos de entrega na tela."""
    for point in points:
        pygame.draw.circle(surface, config.WHITE, point["coords"], 5)


def draw_route(
    surface: pygame.Surface, route: List[Dict[str, Any]], color: Tuple[int, int, int]
) -> None:
    """Desenha uma rota na tela."""
    if route and len(route) > 1:
        pygame.draw.lines(surface, color, True, [p["coords"] for p in route], 2)


def draw_graph(
    surface: pygame.Surface,
    fitness_history: List[float],
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    """Desenha o gráfico de convergência do fitness."""
    graph_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, config.GRAY, graph_rect, 2)

    if len(fitness_history) < 2:
        return

    max_fitness = max(fitness_history)
    min_fitness = min(fitness_history)
    padding_factor = 0.1

    if max_fitness == min_fitness:
        py = y + (height / 2)
        pygame.draw.line(surface, config.GREEN, (x, py), (x + width, py), 2)
    else:
        points = []
        effective_height = height * (1 - 2 * padding_factor)
        top_padding = height * padding_factor
        for i, fitness in enumerate(fitness_history):
            px = x + (i / (len(fitness_history) - 1)) * width
            normalized_fitness = (fitness - min_fitness) / (max_fitness - min_fitness)
            py = (
                y
                + top_padding
                + (effective_height - (normalized_fitness * effective_height))
            )
            points.append((px, py))
        if len(points) > 1:
            pygame.draw.lines(surface, config.GREEN, False, points, 2)

    max_text = config.FONT_SMALL.render(f"Max: {max_fitness:.0f}", True, config.WHITE)
    min_text = config.FONT_SMALL.render(f"Min: {min_fitness:.0f}", True, config.WHITE)
    surface.blit(max_text, (x + 5, y + 5))
    surface.blit(min_text, (x + 5, y + height - 25))


def draw_loading_animation(screen: pygame.Surface, center_pos: Tuple[int, int]) -> None:
    """Desenha uma animação de carregamento na tela."""
    overlay = pygame.Surface(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA
    )
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    loading_text = config.FONT_MEDIUM.render("Gerando Relatório...", True, config.WHITE)
    text_rect = loading_text.get_rect(center=(center_pos[0], center_pos[1] - 50))
    screen.blit(loading_text, text_rect)

    time_factor = (pygame.time.get_ticks() / 2) % 360
    num_dots = 8
    radius = 30
    for i in range(num_dots):
        angle = math.radians(time_factor + i * (360 / num_dots))
        alpha = 150 + 100 * math.sin(math.radians(pygame.time.get_ticks() / 2 + i * 45))
        dot_color = (200, 200, 255, alpha)
        dot_pos = (
            center_pos[0] + radius * math.cos(angle),
            center_pos[1] + radius * math.sin(angle),
        )

        dot_surface = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(dot_surface, dot_color, (6, 6), 6)
        screen.blit(dot_surface, (dot_pos[0] - 6, dot_pos[1] - 6))
