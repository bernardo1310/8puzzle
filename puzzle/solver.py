# =============================================================================
# MÓDULO: solver.py
# Responsabilidade: executar os algoritmos de busca e coletar métricas
# =============================================================================

import heapq
import time
from collections import deque

from .heuristicas import Heuristicas


class PuzzleSolver:
    """
    Resolve o 8-Puzzle com três algoritmos distintos.

    Métricas coletadas após cada execução:
        self.estados_expandidos  — nós retirados da fila e processados
        self.tempo_busca         — segundos gastos na busca

    Todos os métodos retornam a lista de EstadoPuzzle do início ao fim,
    ou None se não houver solução.
    """

    def __init__(self):
        self.estados_expandidos = 0
        self.tempo_busca = 0.0

    def _resetar_metricas(self):
        """Zera as métricas antes de cada nova busca."""
        self.estados_expandidos = 0
        self.tempo_busca = 0.0

    # ------------------------------------------------------------------
    # BUSCA EM LARGURA (BFS)
    # ------------------------------------------------------------------
    def bfs(self, estado_inicial):
        """
        Busca em Largura (Breadth-First Search).

        Explora o espaço de estados nível a nível usando uma fila FIFO,
        garantindo a solução com o menor número de movimentos possível.

        Sem heurística — examina todos os vizinhos de um nível antes
        de avançar para o próximo. Ótimo, porém pode ser lento em
        puzzles com muitos movimentos necessários.

        Complexidade: O(b^d), onde b ≈ 2,7 (ramo médio) e d = profundidade.
        """
        self._resetar_metricas()
        inicio = time.time()

        # Fila FIFO: cada entrada é (estado_atual, caminho_até_aqui)
        fila = deque()
        fila.append((estado_inicial, [estado_inicial]))
        visitados = {estado_inicial.como_tupla()}

        while fila:
            estado_atual, caminho = fila.popleft()
            self.estados_expandidos += 1

            if estado_atual.eh_objetivo():
                self.tempo_busca = time.time() - inicio
                return caminho

            for vizinho in estado_atual.gerar_vizinhos():
                chave = vizinho.como_tupla()
                if chave not in visitados:
                    visitados.add(chave)
                    fila.append((vizinho, caminho + [vizinho]))

        self.tempo_busca = time.time() - inicio
        return None

    # ------------------------------------------------------------------
    # BUSCA POR HAMMING (peças fora do lugar)
    # ------------------------------------------------------------------
    def hamming(self, estado_inicial):
        """
        Busca gulosa com heurística de Hamming.

        Ordena a fila de prioridade pelo número de peças que ainda estão
        fora de sua posição correta, sem considerar o custo acumulado g(x).

        f(x) = h_hamming(x)   — busca puramente gulosa.

        Tende a ser mais rápida que BFS em muitos casos, porém não
        garante solução ótima (pode encontrar um caminho mais longo).
        """
        self._resetar_metricas()
        inicio = time.time()

        h0 = Heuristicas.pecas_fora_do_lugar(estado_inicial)
        contador = 0  # desempate no heap quando prioridades são iguais

        # Heap: (prioridade, contador_desempate, estado, caminho)
        heap = [(h0, contador, estado_inicial, [estado_inicial])]
        visitados = set()

        while heap:
            _, _, estado_atual, caminho = heapq.heappop(heap)
            chave = estado_atual.como_tupla()

            if chave in visitados:
                continue
            visitados.add(chave)
            self.estados_expandidos += 1

            if estado_atual.eh_objetivo():
                self.tempo_busca = time.time() - inicio
                return caminho

            for vizinho in estado_atual.gerar_vizinhos():
                chave_viz = vizinho.como_tupla()
                if chave_viz not in visitados:
                    h = Heuristicas.pecas_fora_do_lugar(vizinho)
                    contador += 1
                    heapq.heappush(heap, (h, contador, vizinho, caminho + [vizinho]))

        self.tempo_busca = time.time() - inicio
        return None

    # ------------------------------------------------------------------
    # A* — BUSCA INFORMADA COMBINADA (Hamming + Manhattan)
    # ------------------------------------------------------------------
    def astar(self, estado_inicial):
        """
        Algoritmo A* com heurística combinada (Hamming + Manhattan).

        Combina custo acumulado e estimativa do esforço restante:

            f(x) = g(x) + h(x)

        onde:
            g(x) = movimentos realizados até o estado x
            h(x) = Hamming(x) + Manhattan(x)  (heurística combinada)

        A combinação de duas heurísticas admissíveis permanece admissível
        e orienta melhor a busca, reduzindo estados expandidos em relação
        a usar cada heurística separada.

        Ótimo e completo quando a heurística é admissível.
        """
        self._resetar_metricas()
        inicio = time.time()

        h0 = Heuristicas.combinada(estado_inicial)
        g0 = 0
        contador = 0

        # Heap: (f, g, contador_desempate, estado, caminho)
        heap = [(g0 + h0, g0, contador, estado_inicial, [estado_inicial])]
        visitados = set()

        while heap:
            f, g, _, estado_atual, caminho = heapq.heappop(heap)
            chave = estado_atual.como_tupla()

            if chave in visitados:
                continue
            visitados.add(chave)
            self.estados_expandidos += 1

            if estado_atual.eh_objetivo():
                self.tempo_busca = time.time() - inicio
                return caminho

            for vizinho in estado_atual.gerar_vizinhos():
                chave_viz = vizinho.como_tupla()
                if chave_viz not in visitados:
                    g_novo = g + 1
                    h_novo = Heuristicas.combinada(vizinho)
                    contador += 1
                    heapq.heappush(heap,
                        (g_novo + h_novo, g_novo, contador, vizinho, caminho + [vizinho]))

        self.tempo_busca = time.time() - inicio
        return None
