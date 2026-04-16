#!/usr/bin/env python3
# =============================================================================
# ARQUIVO PRINCIPAL: main.py
# Responsabilidade: orquestrar o fluxo completo do sistema 8-Puzzle
# =============================================================================
#
# Uso:
#   python main.py                  → menu interativo para escolher algoritmo
#   python main.py --algo bfs       → força Busca em Largura
#   python main.py --algo hamming   → força heurística de Hamming
#   python main.py --algo astar     → força A* combinado
#   python main.py --no-gui         → exibe solução no terminal (sem janela)
#
# Dependências: matplotlib  →  pip install matplotlib
# =============================================================================

import argparse

try:
    import matplotlib
    MATPLOTLIB_DISPONIVEL = True
except ImportError:
    MATPLOTLIB_DISPONIVEL = False

from puzzle import EstadoPuzzle, Heuristicas, PuzzleSolver, Visualizador, GeradorPuzzle


# Mapeamento das opções de algoritmo
ALGORITMOS = {
    "bfs":     ("Busca em Largura (BFS)",        lambda s: s.bfs),
    "hamming": ("Hamming — Peças Fora do Lugar", lambda s: s.hamming),
    "astar":   ("A* — Hamming + Manhattan",      lambda s: s.astar),
}


def escolher_algoritmo_interativo():
    """Exibe menu no terminal e retorna a chave do algoritmo escolhido."""
    print("\nEscolha o algoritmo de busca:")
    print("  1 — Busca em Largura (BFS)")
    print("  2 — Hamming (peças fora do lugar)")
    print("  3 — A* combinado (Hamming + Manhattan)")

    mapa = {"1": "bfs", "2": "hamming", "3": "astar"}
    while True:
        op = input("\nOpção [1/2/3]: ").strip()
        if op in mapa:
            return mapa[op]
        print("Opção inválida. Digite 1, 2 ou 3.")


def exibir_solucao_terminal(caminho):
    """Imprime cada passo da solução no terminal."""
    total = len(caminho) - 1
    for i, estado in enumerate(caminho):
        if i == 0:
            label = "Estado Inicial"
        elif i == total:
            label = "Estado Final (Objetivo)"
        else:
            label = f"Passo {i} / {total}"
        print(f"\n{label}:")
        print(estado)


def exibir_metricas(solver, estado_inicial, solucao):
    """Exibe as métricas de desempenho da busca no terminal."""
    print("=" * 54)
    if solucao:
        print(f"  Resultado         : Solução encontrada ✓")
        print(f"  Movimentos        : {len(solucao) - 1}")
        print(f"  Estados expandidos: {solver.estados_expandidos}")
        print(f"  Tempo de busca    : {solver.tempo_busca:.4f} segundos")
        print(f"  Hamming inicial   : "
              f"{Heuristicas.pecas_fora_do_lugar(estado_inicial)} peças")
        print(f"  Manhattan inicial : "
              f"{Heuristicas.manhattan(estado_inicial)}")
    else:
        print("  Resultado: Nenhuma solução encontrada.")
    print("=" * 54)


def main():
    parser = argparse.ArgumentParser(
        description="Resolve o 8-Puzzle com BFS, Hamming ou A*."
    )
    parser.add_argument(
        "--algo", choices=["bfs", "hamming", "astar"],
        help="Algoritmo: bfs | hamming | astar  (padrão: menu interativo)"
    )
    parser.add_argument(
        "--no-gui", action="store_true",
        help="Exibe a solução no terminal sem abrir janela gráfica"
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------ Banner
    print("=" * 54)
    print("   RESOLVEDOR DE 8-PUZZLE — MÚLTIPLOS ALGORITMOS")
    print("=" * 54)

    # ------------------------------------------------ Escolha do algoritmo
    chave = args.algo if args.algo else escolher_algoritmo_interativo()
    nome_algo, fn_algo = ALGORITMOS[chave]

    # ------------------------------------------------ Gerar estado inicial
    print("\nGerando estado inicial aleatório...")
    estado_inicial = GeradorPuzzle.gerar_aleatorio()

    print(f"\nEstado Inicial:")
    print(estado_inicial)

    print(f"\nEstado Objetivo:")
    print(EstadoPuzzle(EstadoPuzzle.ESTADO_OBJETIVO))

    # ------------------------------------------------ Executar busca
    print(f"\nAlgoritmo: {nome_algo}")
    print("Executando busca...\n")

    solver = PuzzleSolver()
    solucao = fn_algo(solver)(estado_inicial)

    # ------------------------------------------------ Exibir métricas
    exibir_metricas(solver, estado_inicial, solucao)

    if not solucao:
        return

    # ------------------------------------------------ Visualização
    if MATPLOTLIB_DISPONIVEL and not args.no_gui:
        print("\nAbrindo visualização gráfica...")
        viz = Visualizador(delay_segundos=1.5)
        viz.animar_solucao(solucao, algoritmo=nome_algo)
    else:
        if not MATPLOTLIB_DISPONIVEL:
            print("\n[Aviso] Matplotlib não disponível — exibindo no terminal.")
        else:
            print("\n[Modo sem GUI] Exibindo solução no terminal.")
        exibir_solucao_terminal(solucao)

    print("\n" + "=" * 54)
    print("   Execução concluída com sucesso!")
    print("=" * 54)


if __name__ == "__main__":
    main()
