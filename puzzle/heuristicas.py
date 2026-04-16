# =============================================================================
# MÓDULO: heuristicas.py
# Responsabilidade: calcular os valores heurísticos usados nas buscas
# =============================================================================

from .estado import EstadoPuzzle


class Heuristicas:
    """
    Coleção de funções heurísticas para orientar a busca informada.

    Cada método recebe um EstadoPuzzle e retorna um inteiro estimando
    o custo restante até o estado objetivo.

    Todas as heurísticas implementadas são admissíveis, ou seja, nunca
    superestimam o custo real — o que garante otimalidade no A*.
    """

    @staticmethod
    def pecas_fora_do_lugar(estado):
        """
        Heurística de Hamming: conta quantas peças estão em posição errada.

        Para cada peça (exceto o espaço vazio 0), verifica se ela está na
        mesma célula do estado objetivo. Cada peça deslocada soma 1.

        Admissível: cada peça fora do lugar precisa de no mínimo 1 movimento.
        """
        objetivo = EstadoPuzzle.ESTADO_OBJETIVO
        fora = 0
        for l in range(3):
            for c in range(3):
                val = estado.tabuleiro[l][c]
                if val != 0 and val != objetivo[l][c]:
                    fora += 1
        return fora

    @staticmethod
    def manhattan(estado):
        """
        Distância de Manhattan: soma dos deslocamentos absolutos de cada peça.

        Para cada peça, calcula a distância horizontal + vertical entre sua
        posição atual e sua posição correta no objetivo.

        Exemplo: peça '5' deveria estar em (1,1); se estiver em (0,2):
            distância = |0−1| + |2−1| = 2

        Admissível e consistente (dominante sobre Hamming): um único
        movimento desloca cada peça no máximo 1 unidade de Manhattan.
        """
        total = 0
        for l in range(3):
            for c in range(3):
                val = estado.tabuleiro[l][c]
                if val != 0:
                    # Posição correta: número N ocupa o índice N-1 no objetivo
                    l_correta = (val - 1) // 3
                    c_correta = (val - 1) % 3
                    total += abs(l - l_correta) + abs(c - c_correta)
        return total

    @staticmethod
    def combinada(estado):
        """
        Heurística combinada usada pelo A*:
            h(x) = peças_fora_do_lugar(x) + manhattan(x)

        A soma de duas heurísticas admissíveis continua sendo admissível
        e tende a orientar melhor a busca do que cada uma isolada,
        reduzindo o número de estados expandidos.
        """
        return (Heuristicas.pecas_fora_do_lugar(estado)
                + Heuristicas.manhattan(estado))
