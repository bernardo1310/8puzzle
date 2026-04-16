# =============================================================================
# MÓDULO: gerador.py
# Responsabilidade: criar estados iniciais válidos e solucionáveis
# =============================================================================

import random
from .estado import EstadoPuzzle


class GeradorPuzzle:
    """
    Gera configurações iniciais do 8-Puzzle garantidamente solucionáveis.

    Nem toda permutação dos números 0-8 possui solução. A solucionabilidade
    é verificada pelo número de inversões na sequência:
        inversões pares -> estado tem solução
        inversões ímpares -> estado não tem solução
    """

    @staticmethod
    def gerar_aleatorio():
        """
        Retorna um EstadoPuzzle inicial aleatório e solucionável.

        Continua embaralhando até encontrar uma configuração válida.
        Na prática, cerca de 50% das permutações são solucionáveis,
        então raramente são necessárias mais de 2 tentativas.
        """
        while True:
            nums = list(range(9))
            random.shuffle(nums)
            if GeradorPuzzle._solucionavel(nums):
                tabuleiro = [nums[i * 3:(i + 1) * 3] for i in range(3)]
                return EstadoPuzzle(tabuleiro)

    @staticmethod
    def _solucionavel(nums):
        """
        Verifica se uma permutação é solucionável contando inversões.

        Uma inversão ocorre quando um número maior aparece antes de um
        número menor na sequência (desconsiderando o 0).

        Para o 8-Puzzle em grade 3x3, o estado é solucionável quando
        o número total de inversões é par.

        Parâmetro:
            nums: lista plana de 9 números (0 a 8)
        Retorna:
            True se solucionável, False caso contrário
        """
        sem_zero = [n for n in nums if n != 0]
        inversoes = sum(
            1
            for i in range(len(sem_zero))
            for j in range(i + 1, len(sem_zero))
            if sem_zero[i] > sem_zero[j]
        )
        return inversoes % 2 == 0
