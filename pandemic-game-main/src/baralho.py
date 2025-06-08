# src/baralho.py

import random
from .carta import Carta

class Baralho:
    """ Representa um baralho de cartas (de jogador ou de infecção). """
    def __init__(self, tipo: str, cartas: list[Carta]):
        self.tipo = tipo
        self.cartas_compra = cartas
        self.cartas_descarte = []
        self.embaralhar()

    def embaralhar(self):
        """ Embaralha o monte de compras. """
        random.shuffle(self.cartas_compra)
        print(f"Baralho de {self.tipo} foi embaralhado.")

    def comprar(self) -> Carta | None:
        """ Compra a carta do topo do baralho. """
        if len(self.cartas_compra) > 0:
            return self.cartas_compra.pop(0)
        return None

    def descartar(self, carta: Carta):
        """ Move uma carta para a pilha de descarte. """
        self.cartas_descarte.append(carta)

    def __len__(self):
        return len(self.cartas_compra)