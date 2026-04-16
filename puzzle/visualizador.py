# =============================================================================
# MÓDULO: visualizador.py
# Responsabilidade: animar a solução graficamente com Matplotlib
# =============================================================================

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_DISPONIVEL = True
except ImportError:
    MATPLOTLIB_DISPONIVEL = False


class Visualizador:
    """
    Renderiza e anima o tabuleiro do 8-Puzzle usando Matplotlib.

    Cada estado da solução é desenhado em sequência com delay
    configurável entre os passos para facilitar o acompanhamento visual.
    """

    # Paleta de cores
    COR_BLOCO  = "#4A90D9"   # peça com número
    COR_VAZIO  = "#AED6F1"   # espaço vazio — azul claro
    COR_TEXTO  = "white"
    COR_FUNDO  = "#1A252F"
    COR_TITULO = "#ECF0F1"

    def __init__(self, delay_segundos=1.5):
        """
        Parâmetro:
            delay_segundos: tempo de espera entre cada passo da animação
        """
        self.delay = delay_segundos

    def _desenhar_estado(self, ax, estado, titulo=""):
        """
        Renderiza um único estado do tabuleiro no eixo fornecido.

        Parâmetros:
            ax     : eixo Matplotlib onde o tabuleiro será desenhado
            estado : objeto EstadoPuzzle com o tabuleiro atual
            titulo : texto exibido acima do tabuleiro
        """
        ax.clear()
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_facecolor(self.COR_FUNDO)

        for l in range(3):
            for c in range(3):
                val = estado.tabuleiro[l][c]
                l_visual = 2 - l  # inverte eixo Y: linha 0 fica no topo

                cor = self.COR_VAZIO if val == 0 else self.COR_BLOCO

                # Desenha o bloco arredondado
                rect = patches.FancyBboxPatch(
                    (c + 0.05, l_visual + 0.05),
                    0.90, 0.90,
                    boxstyle="round,pad=0.05",
                    facecolor=cor,
                    edgecolor="white",
                    linewidth=2
                )
                ax.add_patch(rect)

                # Escreve o número dentro do bloco (espaço vazio não exibe nada)
                if val != 0:
                    ax.text(
                        c + 0.5, l_visual + 0.5,
                        str(val),
                        ha="center", va="center",
                        fontsize=28, fontweight="bold",
                        color=self.COR_TEXTO
                    )

        ax.set_title(titulo, fontsize=13, pad=10, color=self.COR_TITULO)

    def animar_solucao(self, caminho, algoritmo=""):
        """
        Exibe cada estado da solução em sequência animada.

        Parâmetros:
            caminho   : lista de EstadoPuzzle (estado inicial → objetivo)
            algoritmo : nome do algoritmo (exibido no título da janela)
        """
        if not MATPLOTLIB_DISPONIVEL:
            print("[Aviso] Matplotlib não disponível — não é possível animar.")
            return

        total = len(caminho) - 1
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor(self.COR_FUNDO)
        fig.canvas.manager.set_window_title(f"8-Puzzle — {algoritmo}")
        plt.tight_layout()

        print(f"\n[ Animação ] {total} movimentos  |  delay {self.delay}s por passo\n")

        for i, estado in enumerate(caminho):
            if i == 0:
                titulo = f"[{algoritmo}]  Estado Inicial"
            elif i == total:
                titulo = f"[{algoritmo}]  Resolvido em {total} movimentos!"
            else:
                titulo = f"[{algoritmo}]  Passo {i} / {total}"

            self._desenhar_estado(ax, estado, titulo)
            plt.pause(self.delay)

        print("Animação concluída. Feche a janela para encerrar.")
        plt.show()
