# =============================================================================
# MÓDULO: estado.py
# Responsabilidade: representar e manipular o tabuleiro 3x3 do 8-Puzzle
# =============================================================================

import copy


class EstadoPuzzle:
    """
    Representa uma configuração do tabuleiro 3x3 do 8-Puzzle.

    O valor 0 indica o espaço vazio, que se move trocando de lugar com
    peças vizinhas (cima, baixo, esquerda, direita).

    Estado objetivo:
        1 2 3
        4 5 6
        7 8 0
    """

    ESTADO_OBJETIVO = [[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]]

    def __init__(self, tabuleiro):
        """
        Parâmetro:
            tabuleiro: lista de listas 3x3 com números de 0 a 8
        """
        self.tabuleiro = tabuleiro
        self.posicao_vazio = self._encontrar_vazio()

    def _encontrar_vazio(self):
        """Retorna (linha, coluna) do espaço vazio (número 0)."""
        for linha in range(3):
            for coluna in range(3):
                if self.tabuleiro[linha][coluna] == 0:
                    return (linha, coluna)

    def eh_objetivo(self):
        """Retorna True se o tabuleiro está na configuração objetivo."""
        return self.tabuleiro == self.ESTADO_OBJETIVO

    def gerar_vizinhos(self):
        """
        Gera todos os estados alcançáveis com exatamente um movimento.

        O espaço vazio pode se deslocar para cima, baixo, esquerda ou
        direita, desde que o destino esteja dentro do tabuleiro 3x3.
        A troca é feita via cópia profunda para preservar o estado atual.
        """
        vizinhos = []
        l, c = self.posicao_vazio

        # Deltas: (Δlinha, Δcoluna) para cada direção possível
        for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nl, nc = l + dl, c + dc
            if 0 <= nl < 3 and 0 <= nc < 3:
                novo = copy.deepcopy(self.tabuleiro)
                # Troca: o espaço vazio absorve a peça vizinha
                novo[l][c], novo[nl][nc] = novo[nl][nc], novo[l][c]
                vizinhos.append(EstadoPuzzle(novo))

        return vizinhos

    def como_tupla(self):
        """
        Serializa o tabuleiro em tupla imutável.
        Usado como chave em sets e dicts (controle de visitados).

        Exemplo: [[1,2,3],[4,5,6],[7,8,0]] → (1,2,3,4,5,6,7,8,0)
        """
        return tuple(n for linha in self.tabuleiro for n in linha)

    def __str__(self):
        """Representação visual no terminal."""
        linhas = []
        for linha in self.tabuleiro:
            celulas = " ".join(str(n) if n != 0 else "·" for n in linha)
            linhas.append(f"| {celulas} |")
        return "\n".join(linhas)
