# src/cidade.py

from .doenca import Cor

class Cidade:
    """ Representa uma cidade no mapa do jogo. """
    def __init__(self, nome: str, cor: Cor):
        self.nome = nome
        self.cor = cor
        self.cubos = {c: 0 for c in Cor}
        self.vizinhos = set()
        self.centro_pesquisa = False

    def adicionar_vizinho(self, vizinho: 'Cidade'):
        """ Adiciona uma cidade à lista de vizinhos (conexão mútua). """
        if vizinho not in self.vizinhos:
            self.vizinhos.add(vizinho)
            vizinho.vizinhos.add(self)

    def adicionar_cubo(self, cor: Cor):
        """ Adiciona um cubo de doença na cidade. """
        if self.cubos[cor] < 3:
            self.cubos[cor] += 1
            print(f"Cubo {cor.value} adicionado em {self.nome}. Total: {self.cubos[cor]}")
        else:
            # Lógica de surto (outbreak) deveria ser chamada aqui
            print(f"SURTO em {self.nome} com a cor {cor.value}!")


    def remover_cubo(self, cor: Cor) -> bool:
        """ Remove um cubo de doença, se houver. """
        if self.cubos[cor] > 0:
            self.cubos[cor] -= 1
            print(f"Cubo {cor.value} removido de {self.nome}. Restantes: {self.cubos[cor]}")
            return True
        return False

    def __repr__(self):
        return f"Cidade('{self.nome}', Cor.{self.cor.name})"