"""Módulo para centralizar todas as constantes e configurações da aplicação."""

import pygame

# --- GERAL ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
MAP_AREA_WIDTH = 800
GRAPH_AREA_X = MAP_AREA_WIDTH + 50
APP_CAPTION = "Otimização de Rotas com Algoritmo Genético"

# --- CORES ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
GRAY = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)
DARK_GRAY = (60, 60, 60)
COLOR_INACTIVE = pygame.Color("lightskyblue3")
COLOR_ACTIVE = pygame.Color("dodgerblue2")
PURPLE_BUTTON = (138, 43, 226)

# --- FONTES ---
pygame.font.init()
FONT_SMALL = pygame.font.SysFont("Consolas", 18)
FONT_MEDIUM = pygame.font.SysFont("Consolas", 24)
FONT_LARGE = pygame.font.SysFont("Consolas", 48)

# --- PARÂMETROS DO ALGORITMO GENÉTICO ---
POPULATION_SIZE = 100
MUTATION_PROBABILITY = 0.2
TOURNAMENT_SIZE = 5

# --- PARÂMETROS DO VEÍCULO ---
VEHICLE_PARAMS = {
    "max_range": 10000.0,
    "cost_per_km": 1.75,
    "cost_per_hour": 35.0,
    "time_multiplier": 0.1,  # Fator de conversão distância -> tempo
    "late_penalty_multiplier": 150,  # Penalidade por hora de atraso
}
