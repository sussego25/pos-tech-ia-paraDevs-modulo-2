"""Módulo para renderizar as diferentes telas da aplicação."""

import pygame
import threading
from typing import List, Dict, Any

import config
from ui import drawing
from llm import client, prompts


def settings_screen():
    """Renderiza e gerencia a tela de configurações iniciais."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Configuração da Simulação")
    clock = pygame.time.Clock()

    input_box_cities = pygame.Rect(config.SCREEN_WIDTH / 2 - 100, 250, 200, 40)
    input_box_gens = pygame.Rect(config.SCREEN_WIDTH / 2 - 100, 350, 200, 40)
    start_button = pygame.Rect(config.SCREEN_WIDTH / 2 - 100, 450, 200, 50)

    color_cities = config.COLOR_INACTIVE
    color_gens = config.COLOR_INACTIVE
    active_box = None
    text_cities = "40"
    text_gens = "5000"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_cities.collidepoint(event.pos):
                    active_box = "cities"
                elif input_box_gens.collidepoint(event.pos):
                    active_box = "gens"
                else:
                    active_box = None

                color_cities = (
                    config.COLOR_ACTIVE
                    if active_box == "cities"
                    else config.COLOR_INACTIVE
                )
                color_gens = (
                    config.COLOR_ACTIVE
                    if active_box == "gens"
                    else config.COLOR_INACTIVE
                )

                if start_button.collidepoint(event.pos):
                    try:
                        num_cities = int(text_cities) if text_cities else 40
                        max_gens = int(text_gens) if text_gens else 5000
                        return num_cities, max_gens
                    except ValueError:
                        print("Erro: Por favor, insira valores numéricos válidos.")

            if event.type == pygame.KEYDOWN:
                if active_box == "cities":
                    if event.key == pygame.K_BACKSPACE:
                        text_cities = text_cities[:-1]
                    elif event.unicode.isdigit():
                        text_cities += event.unicode
                elif active_box == "gens":
                    if event.key == pygame.K_BACKSPACE:
                        text_gens = text_gens[:-1]
                    elif event.unicode.isdigit():
                        text_gens += event.unicode

        screen.fill(config.BLACK)
        title_surf = config.FONT_LARGE.render(
            "Configurar Simulação", True, config.WHITE
        )
        screen.blit(
            title_surf, title_surf.get_rect(center=(config.SCREEN_WIDTH / 2, 100))
        )

        # Labels e caixas de texto
        screen.blit(
            config.FONT_MEDIUM.render("Número de Cidades:", True, config.WHITE),
            (input_box_cities.x, input_box_cities.y - 30),
        )
        pygame.draw.rect(screen, color_cities, input_box_cities, 2)
        screen.blit(
            config.FONT_MEDIUM.render(text_cities, True, config.WHITE),
            (input_box_cities.x + 10, input_box_cities.y + 5),
        )

        screen.blit(
            config.FONT_MEDIUM.render("Máximo de Gerações:", True, config.WHITE),
            (input_box_gens.x, input_box_gens.y - 30),
        )
        pygame.draw.rect(screen, color_gens, input_box_gens, 2)
        screen.blit(
            config.FONT_MEDIUM.render(text_gens, True, config.WHITE),
            (input_box_gens.x + 10, input_box_gens.y + 5),
        )

        # Botão Iniciar
        pygame.draw.rect(screen, config.GREEN, start_button)
        start_text_surf = config.FONT_MEDIUM.render("Iniciar", True, config.BLACK)
        screen.blit(
            start_text_surf, start_text_surf.get_rect(center=start_button.center)
        )

        pygame.display.flip()
        clock.tick(30)


def draw_simulation_screen(
    screen,
    all_deliveries,
    best_gen,
    best_overall,
    random_ind,
    generation,
    max_gens,
    fitness_overall,
    fitness_gen,
    history,
):
    """Desenha a tela principal de simulação a cada frame."""
    screen.fill(config.BLACK)

    # Mapa e rotas
    drawing.draw_points(screen, all_deliveries)
    if random_ind:
        drawing.draw_route(screen, random_ind, config.DARK_GRAY)
    if best_gen:
        drawing.draw_route(screen, best_gen, config.LIGHT_GRAY)
    if best_overall:
        drawing.draw_route(screen, best_overall, config.GREEN)

    # Divisor
    pygame.draw.line(
        screen,
        config.WHITE,
        (config.MAP_AREA_WIDTH + 20, 0),
        (config.MAP_AREA_WIDTH + 20, config.SCREEN_HEIGHT),
        2,
    )

    # Painel de informações
    screen.blit(
        config.FONT_MEDIUM.render("Otimização em Tempo Real", True, config.WHITE),
        (config.GRAPH_AREA_X, 20),
    )
    screen.blit(
        config.FONT_SMALL.render(
            f"Geração: {generation}/{max_gens}", True, config.WHITE
        ),
        (config.GRAPH_AREA_X, 70),
    )
    screen.blit(
        config.FONT_SMALL.render(
            f"Menor Custo (Global): {fitness_overall:.2f}", True, config.GREEN
        ),
        (config.GRAPH_AREA_X, 100),
    )
    screen.blit(
        config.FONT_SMALL.render(
            f"Custo (Geração Atual): {fitness_gen:.2f}", True, config.LIGHT_GRAY
        ),
        (config.GRAPH_AREA_X, 130),
    )

    # Gráfico
    graph_width = config.SCREEN_WIDTH - config.GRAPH_AREA_X - 50
    drawing.draw_graph(screen, history, config.GRAPH_AREA_X, 180, graph_width, 300)

    pygame.display.flip()


def results_screen(
    screen, best_solution, best_fitness, total_generations, all_deliveries
):
    """Renderiza e gerencia a tela final de resultados."""
    pygame.display.set_caption("Resultados da Otimização")
    llm_button = pygame.Rect(config.GRAPH_AREA_X, 520, 300, 50)

    feedback_text = ""
    feedback_time = 0
    filename = "rota_otimizada.html"
    is_loading = False
    llm_thread = None
    thread_result = {"html_report": None, "error": None}

    def worker_generate_report(prompt, data, result_dict):
        try:
            report = client.generate_report_from_llm(prompt, data)
            result_dict["html_report"] = report
        except Exception as e:
            result_dict["error"] = e

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if llm_button.collidepoint(event.pos) and not is_loading:
                    is_loading = True
                    route_data_text = f"Custo Total: R$ {best_fitness:.2f}\n"
                    route_data_text += f"Número de Paradas: {len(best_solution)}\n"
                    route_data_text += "Ordem de visita (ID da entrega -> Coordenadas -> Janela de Horário):\n"
                    for i, city in enumerate(best_solution):
                        route_data_text += f"{i+1}. ID {city['id']} -> Coords {city['coords']} -> Horário: {city['start_time']}h-{city['end_time']}h\n"

                    thread_result = {"html_report": None, "error": None}
                    llm_thread = threading.Thread(
                        target=worker_generate_report,
                        args=(
                            prompts.REPORT_PROMPT_TEMPLATE,
                            route_data_text,
                            thread_result,
                        ),
                    )
                    llm_thread.start()

        if is_loading and llm_thread and not llm_thread.is_alive():
            is_loading = False
            if thread_result["error"]:
                feedback_text = f"Erro na API: {thread_result['error']}"
            elif thread_result["html_report"]:
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(thread_result["html_report"])
                    feedback_text = f"Relatório salvo em '{filename}'"
                except Exception as e:
                    feedback_text = f"Erro ao salvar: {e}"
            feedback_time = pygame.time.get_ticks()
            llm_thread = None

        # Desenho
        screen.fill(config.BLACK)
        drawing.draw_points(screen, all_deliveries)
        if best_solution:
            drawing.draw_route(screen, best_solution, config.GREEN)

        pygame.draw.line(
            screen,
            config.WHITE,
            (config.MAP_AREA_WIDTH + 20, 0),
            (config.MAP_AREA_WIDTH + 20, config.SCREEN_HEIGHT),
            2,
        )

        screen.blit(
            config.FONT_MEDIUM.render("Resultados da Otimização", True, config.WHITE),
            (config.GRAPH_AREA_X, 20),
        )
        screen.blit(
            config.FONT_MEDIUM.render("Melhor Custo Encontrado:", True, config.WHITE),
            (config.GRAPH_AREA_X, 100),
        )
        screen.blit(
            config.FONT_LARGE.render(f"R$ {best_fitness:.2f}", True, config.GREEN),
            (config.GRAPH_AREA_X, 130),
        )

        pygame.draw.rect(
            screen,
            config.PURPLE_BUTTON if not is_loading else config.DARK_GRAY,
            llm_button,
        )
        llm_text_surf = config.FONT_MEDIUM.render(
            "Gerar Relatório LLM", True, config.WHITE
        )
        screen.blit(llm_text_surf, llm_text_surf.get_rect(center=llm_button.center))

        if feedback_text and pygame.time.get_ticks() - feedback_time < 3000:
            feedback_surf = config.FONT_SMALL.render(feedback_text, True, config.GREEN)
            screen.blit(feedback_surf, (llm_button.x, llm_button.y + 60))

        if is_loading:
            drawing.draw_loading_animation(
                screen, (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
            )

        screen.blit(
            config.FONT_SMALL.render(
                "Pressione qualquer tecla para sair.", True, config.GRAY
            ),
            (config.GRAPH_AREA_X, config.SCREEN_HEIGHT - 50),
        )

        pygame.display.flip()
