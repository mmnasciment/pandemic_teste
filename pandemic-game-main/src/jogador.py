# src/jogador.py

from .carta import Carta, CartaPersonagem
from .cidade import Cidade

class Jogador:
    """ Representa um jogador no jogo. """
    def __init__(self, nome: str, personagem: CartaPersonagem):
        self.nome = nome
        self.personagem = personagem
        self.mao = []  # Mão de cartas do jogador
        self.cidade_atual: Cidade | None = None

    def set_cidade_atual(self, cidade: Cidade):
        self.cidade_atual = cidade

    def adicionar_carta_mao(self, carta: Carta):
        self.mao.append(carta)

    def descartar_carta(self, nome_carta: str) -> Carta | None:
        """ Descarta uma carta da mão pelo seu nome. """
        carta_a_descartar = next((c for c in self.mao if c.nome == nome_carta), None)
        if carta_a_descartar:
            self.mao.remove(carta_a_descartar)
            return carta_a_descartar
        return None

    def __repr__(self):
        return f"Jogador('{self.nome}', Personagem: {self.personagem.nome})"