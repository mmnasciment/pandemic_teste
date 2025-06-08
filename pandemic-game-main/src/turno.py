# src/turno.py

from .jogador import Jogador
from .acao import Acao
from .carta import CartaEpidemia

# Usamos 'forward reference' com aspas pois Jogo é importado em um escopo que causa dependência circular
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .jogo import Jogo


class Turno:
    """ Gerencia as fases de um turno de um jogador. """
    def __init__(self, jogador_atual: Jogador, jogo: 'Jogo'):
        self.jogador_atual = jogador_atual
        self.jogo = jogo
        self.acoes_restantes = 4

    def realizar_acao(self, acao: Acao, **kwargs):
        """ Executa uma ação, decrementando o contador de ações. """
        if self.acoes_restantes > 0:
            print(f"\n--- Ação {5 - self.acoes_restantes} de {self.jogador_atual.nome} ---")
            acao.executa(self.jogador_atual, **kwargs)
            self.acoes_restantes -= 1
            print(f"Ações restantes: {self.acoes_restantes}")
        else:
            print("Não há mais ações disponíveis neste turno.")

    def finalizar_turno(self):
        """ Executa as fases de final de turno: comprar e infectar. """
        print("\n--- Fim do Turno: Comprando Cartas ---")
        self._comprar_cartas_jogador()
        print("\n--- Fim do Turno: Fase de Infecção ---")
        self._infectar_cidades()

    def _comprar_cartas_jogador(self):
        for _ in range(2):
            carta = self.jogo.baralho_jogador.comprar()
            if carta:
                if isinstance(carta, CartaEpidemia):
                    print("🚨 EPIDEMIA! 🚨")
                    # Lógica de epidemia deve ser chamada aqui
                else:
                    self.jogador_atual.adicionar_carta_mao(carta)
                    print(f"{self.jogador_atual.nome} comprou a carta {carta.nome}.")
            else:
                print("Fim do baralho de jogador. Derrota!")
                # Lógica de fim de jogo
                
    def _infectar_cidades(self):
        taxa_infeccao = 2 # Simplificado
        for _ in range(taxa_infeccao):
            carta_infeccao = self.jogo.baralho_infeccao.comprar()
            if carta_infeccao:
                cidade_a_infectar = self.jogo.mapa.get_cidade(carta_infeccao.nome)
                if cidade_a_infectar:
                    print(f"Infectando {cidade_a_infectar.nome}...")
                    cidade_a_infectar.adicionar_cubo(cidade_a_infectar.cor)
                self.jogo.baralho_infeccao.descartar(carta_infeccao)