# src/carta.py

from abc import ABC
from .doenca import Cor

class Carta(ABC):
    """ Classe base abstrata para todas as cartas do jogo. """
    def __init__(self, nome: str):
        self.nome = nome

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.nome}')"

class CartaCidade(Carta):
    """ Uma carta que representa uma cidade específica. """
    def __init__(self, nome: str, cor: Cor):
        super().__init__(nome)
        self.cor = cor

class CartaEvento(Carta):
    """ Uma carta de evento especial. """
    def __init__(self, nome: str, descricao: str):
        super().__init__(nome)
        self.descricao = descricao

class CartaEpidemia(Carta):
    """ A carta de Epidemia. """
    def __init__(self):
        super().__init__("Epidemia")

class CartaPersonagem(Carta):
    """ Carta que define o papel (personagem) do jogador. """
    def __init__(self, nome: str, habilidade: str):
        super().__init__(nome)
        self.habilidade = habilidade

class CartaDoenca(CartaCidade):
    """ Uma carta do baralho de infecção. É funcionalmente uma carta de cidade. """
    pass