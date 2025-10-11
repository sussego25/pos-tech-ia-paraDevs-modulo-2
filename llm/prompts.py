"""Módulo para armazenar os templates de prompt para o LLM."""

REPORT_PROMPT_TEMPLATE = """
Você é um assistente de logística hospitalar. Com base nos dados da rota otimizada abaixo,
gere um relatório completo em formato HTML contendo:
1. Um resumo da eficiência da rota (custo, número de paradas).
2. Uma lista de instruções claras e sequenciais para o motorista, em formato de checklist (Ex: 1. Dirija-se à entrega ID X...).
   Não use as coordenadas, apenas o ID da entrega na ordem correta.
3. Responda à pergunta: 'Qualquer ponto da rota parece ter um risco de atraso?' (Analise as janelas de tempo e a sequência).
4. Existem destinas que ja vão estar com a janela de entrega violada, nesses casos não se trata de um erro, pois a multa de SLA ja foi aplicada e considerada para entrega e mesmo assim a rota possui o menor custo.

--- DADOS DA ROTA ---
{route_data_text}
"""
