# src/doenca.py

from enum import Enum

class Cor(Enum):
    """ Enum para as cores das doenças, cidades e cartas. """
    AZUL = "Azul"
    AMARELO = "Amarelo"
    PRETO = "Preto"
    VERMELHO = "Vermelho"

class Doenca:
    """ Representa uma das quatro doenças do jogo. """
    def __init__(self, cor: Cor):
        self.cor = cor
        self.erradicada = False
        self.cura_descoberta = False

    def __repr__(self):
        return f"Doenca(Cor.{self.cor.name}, Cura: {self.cura_descoberta})"