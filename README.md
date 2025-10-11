[readme.md](https://github.com/user-attachments/files/22865319/readme.md)
# Otimizador de Rotas com Algoritmo Genético e IA

Este projeto é uma aplicação de otimização logística que utiliza um Algoritmo Genético para resolver o Problema do Caixeiro Viajante com Janelas de Tempo (VRPTW). A solução é visualizada em tempo real com Pygame e, ao final, um relatório detalhado da rota otimizada pode ser gerado por uma Inteligência Artificial (Google Gemini).

## Explicação da Implementação

A aplicação é modularizada para separar as diferentes responsabilidades do sistema, desde a interface gráfica até o núcleo do algoritmo genético e a comunicação com a API de IA.

### Núcleo do Algoritmo Genético
O coração do projeto é um Algoritmo Genético (AG) projetado para evoluir uma população de rotas candidatas em busca de uma solução de custo mínimo.

*   **População (`population.py`):** O processo começa com a geração de uma população inicial de rotas aleatórias. Para garantir a reprodutibilidade dos cenários, a geração das cidades (pontos de entrega) é fixa com base em uma semente.
*   **Função de Fitness (`fitness.py`):** Cada rota (indivíduo) na população é avaliada por uma função de fitness que calcula seu custo total. O custo não se baseia apenas na distância, mas também inclui:
    *   Custos operacionais por distância e tempo.
    *   Penalidades por atraso na entrega, caso a janela de tempo seja violada.
    *   Tempo de espera, caso o veículo chegue antes do início da janela de tempo.
    *   Uma penalidade massiva que torna a rota inválida se a distância total exceder a autonomia do veículo.
*   **Seleção (`selection.py`):** Para criar a próxima geração, os indivíduos mais aptos são selecionados através da **Seleção por Torneio**. Este método seleciona um subconjunto aleatório de indivíduos e escolhe o melhor deles, equilibrando a pressão seletiva e a diversidade.
*   **Cruzamento (`crossover.py`):** O **Order Crossover (OX)** é usado para combinar duas rotas "pais" e gerar um "filho". Este operador preserva uma subsequência de uma rota pai e preenche o restante com a ordem da outra, sendo eficaz para problemas baseados em permutação como o PCV.
*   **Mutação (`mutation.py`):** Para introduzir novidade e evitar que o algoritmo fique preso em mínimos locais, uma **mutação de troca (swap)** é aplicada com uma certa probabilidade. Ela simplesmente troca a posição de duas cidades aleatórias na rota.

### Interface Gráfica e Visualização (`screens.py`, `drawing.py`)
A interface foi construída com Pygame para fornecer feedback visual em tempo real sobre o processo de otimização.

*   **Telas (`screens.py`):** O módulo gerencia três telas principais:
    1.  Uma tela de configuração inicial para definir o número de cidades e gerações.
    2.  A tela principal de simulação, que exibe o mapa, as rotas (melhor global, melhor da geração e um indivíduo aleatório) e um gráfico de convergência do custo ao longo das gerações.
    3.  Uma tela final de resultados, que mostra a melhor solução encontrada e oferece a opção de gerar o relatório.
*   **Desenho (`drawing.py`):** Contém funções reutilizáveis para desenhar os pontos de entrega, as rotas na tela e o gráfico de fitness.

### Integração com IA (`client.py`, `prompts.py`)
Ao final da simulação, o usuário pode solicitar um relatório gerado por IA.

*   **Cliente LLM (`client.py`):** Este módulo utiliza a biblioteca `langchain_google_genai` para se comunicar com a API do Gemini. Ele envia os dados da rota otimizada para o modelo de linguagem.
*   **Prompts (`prompts.py`):** Armazena o template do prompt que instrui a IA sobre como formatar o relatório. O prompt pede um resumo, um checklist para o motorista e uma análise sobre riscos de atraso.

---

## Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências necessárias.


**1. Crie um ambiente virtual (Recomendado):**
Isso isola as dependências do seu projeto.

```bash
# Para Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Para Windows
python -m venv venv
.\venv\Scripts\activate
```

**2. Crie o arquivo `requirements.txt`:**
Crie um arquivo com o nome `requirements.txt` na raiz do projeto e adicione o seguinte conteúdo:

```
pygame
python-dotenv
langchain-google-genai
langchain
```

**3. Instale as bibliotecas:**
Execute o comando abaixo no terminal para instalar todas as bibliotecas de uma vez.

```bash
pip install -r requirements.txt
```

## Como Executar
Após a instalação, siga estes passos para rodar a aplicação.

**1. Configure sua chave de API:**

Crie um arquivo chamado `.env` na raiz do projeto.

Dentro deste arquivo, adicione sua chave de API do Gemini (veja a seção abaixo sobre como gerá-la):

```
GOOGLE_API_KEY="SUA_CHAVE_DE_API_VAI_AQUI"
```

**2. Execute o arquivo principal:**
Abra o terminal na pasta do projeto e execute o comando:

```bash
python main.py
```
(Nota: O arquivo principal de execução foi assumido como `main.py`. Se o seu tiver outro nome, substitua-o no comando.)

**3. Interaja com a Simulação:**

Na primeira tela, defina o Número de Cidades e o Máximo de Gerações.

Clique em "Iniciar" para começar a otimização.

Ao final, na tela de resultados, clique em "Gerar Relatório LLM" para criar o arquivo `rota_otimizada.html`.

## Geração da API KEY do Gemini
Para usar a funcionalidade de geração de relatórios, você precisa de uma chave de API do Google AI.

**1. Acesse o Google AI Studio:**

Vá para o site [Google AI Studio](https://aistudio.google.com/).

Faça login com sua conta do Google.

**2. Crie uma Chave de API:**

No menu à esquerda, clique em "Get API key".

Na página seguinte, clique em "Create API key in new project".

Sua chave de API será gerada e exibida na tela.

**3. Copie e Guarde sua Chave:**

Copie a chave gerada. Ela é um conjunto longo de caracteres.

**Importante:** Trate esta chave como uma senha. Não a compartilhe publicamente nem a envie para repositórios de código públicos.

**4. Adicione a Chave ao Projeto:**

Cole a chave que você copiou no arquivo `.env` que você criou na raiz do projeto, conforme mostrado na seção "Como Executar".
