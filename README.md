# 8-Puzzle — Resolvedor com Múltiplos Algoritmos

Resolve o clássico 8-Puzzle (matriz 3x3) com três algoritmos de busca,
exibindo métricas de desempenho e animação gráfica via Matplotlib.

## Estrutura do Projeto

```
8puzzle/
├── main.py                  # Ponto de entrada — orquestra o fluxo
└── puzzle/
    ├── __init__.py          # Exportações do pacote
    ├── estado.py            # Classe EstadoPuzzle (tabuleiro 3x3)
    ├── heuristicas.py       # Hamming, Manhattan e Combinada
    ├── solver.py            # BFS, Hamming e A*
    ├── visualizador.py      # Animação com Matplotlib
    └── gerador.py           # Geração de estados solucionáveis
```

## Instalação

```bash
pip install matplotlib
```

## Uso

```bash
# Menu interativo (escolha na hora)
python main.py

# Forçar algoritmo específico
python main.py --algo bfs
python main.py --algo hamming
python main.py --algo astar

# Sem janela gráfica (exibe no terminal)
python main.py --algo astar --no-gui
```

## Algoritmos

| Algoritmo | Estratégia | Ótimo? |
|-----------|-----------|--------|
| **BFS** | Fila FIFO, sem heurística | ✓ Sim |
| **Hamming** | Heap por peças fora do lugar `h(x)` | ✗ Não garante |
| **A\*** | `f(x) = g(x) + Hamming(x) + Manhattan(x)` | ✓ Sim |

## Métricas Exibidas

- Número de movimentos na solução
- Estados expandidos (nós processados)
- Tempo de execução em segundos
- Valores de Hamming e Manhattan no estado inicial
