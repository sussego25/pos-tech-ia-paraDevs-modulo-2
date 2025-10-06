"""Ponto de entrada principal da aplicação de otimização de rotas."""

import pygame
import sys
import random
from typing import List, Dict, Any

import config
from ui import screens, drawing
from genetic_algorithm import (
    population as ga_pop,
    fitness as ga_fit,
    selection as ga_sel,
    crossover as ga_cross,
    mutation as ga_mut,
)


def run_simulation(
    screen: pygame.Surface, all_deliveries: List[Dict[str, Any]], max_generations: int
):
    """Executa o loop principal do algoritmo genético e a visualização."""
    clock = pygame.time.Clock()

    # Geração da população inicial
    population = ga_pop.generate_random_population(
        all_deliveries, config.POPULATION_SIZE
    )

    best_fitness_overall = float("inf")
    best_solution_overall = None
    fitness_history = []

    for generation in range(max_generations):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None, None, None  # Sinaliza para sair

        # Avaliação da população
        evaluated_population = []
        for individual in population:
            fitness_score = ga_fit.calculate_fitness(individual, config.VEHICLE_PARAMS)
            evaluated_population.append(
                {"solution": individual, "fitness": fitness_score}
            )

        evaluated_population.sort(key=lambda ind: ind["fitness"])

        # Atualiza o melhor indivíduo global
        best_solution_generation = evaluated_population[0]["solution"]
        best_fitness_generation = evaluated_population[0]["fitness"]
        if best_fitness_generation < best_fitness_overall:
            best_fitness_overall = best_fitness_generation
            best_solution_overall = best_solution_generation

        fitness_history.append(best_fitness_overall)
        graph_width = config.SCREEN_WIDTH - config.GRAPH_AREA_X - 50
        if len(fitness_history) > graph_width:
            fitness_history.pop(0)

        # Criação da nova população
        new_population = [best_solution_generation]  # Elitismo
        while len(new_population) < config.POPULATION_SIZE:
            parent1 = ga_sel.tournament_selection(
                evaluated_population, k=config.TOURNAMENT_SIZE
            )
            parent2 = ga_sel.tournament_selection(
                evaluated_population, k=config.TOURNAMENT_SIZE
            )
            child = ga_cross.order_crossover(parent1, parent2)
            child = ga_mut.mutate(child, config.MUTATION_PROBABILITY)
            new_population.append(child)

        population = new_population

        # Desenho da tela de simulação
        screens.draw_simulation_screen(
            screen,
            all_deliveries,
            best_solution_generation,
            best_solution_overall,
            random.choice(population),
            generation,
            max_generations,
            best_fitness_overall,
            best_fitness_generation,
            fitness_history,
        )
        clock.tick(30)

    return best_solution_overall, best_fitness_overall, generation, all_deliveries


if __name__ == "__main__":
    pygame.init()
    settings = screens.settings_screen()

    if settings:
        num_cities, max_gens = settings
        main_screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(config.APP_CAPTION)

        all_deliveries = ga_pop.get_fixed_problem_set(num_cities)

        solution, fitness, gens, deliveries = run_simulation(
            main_screen, all_deliveries, max_gens
        )

        if solution:  # Apenas mostra os resultados se a simulação não foi interrompida
            screens.results_screen(main_screen, solution, fitness, gens, deliveries)

    pygame.quit()
    sys.exit()
