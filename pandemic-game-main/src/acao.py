# src/acao.py

from abc import ABC, abstractmethod
from .jogador import Jogador
from .doenca import Doenca, Cor
from .carta import CartaCidade

class Acao(ABC):
    """ Interface para todas as ações possíveis do jogador. """
    @abstractmethod
    def executa(self, jogador: Jogador, **kwargs):
        """
        O polimorfismo acontece aqui. Cada subclasse implementará sua lógica.
        **kwargs permite passar argumentos variáveis (destino, cor, etc).
        """
        pass

class Mover(Acao):
    def executa(self, jogador: Jogador, **kwargs):
        destino = kwargs.get('destino')
        if not destino:
            print("Erro: Cidade de destino não especificada.")
            return

        # Lógica de mover por Automóvel/Barco (para cidades vizinhas)
        if destino in jogador.cidade_atual.vizinhos:
            jogador.set_cidade_atual(destino)
            print(f"{jogador.nome} moveu-se para {destino.nome}.")
        else:
            print(f"Movimento inválido: {destino.nome} não é vizinha de {jogador.cidade_atual.nome}.")

class ConstruirCentro(Acao):
    def executa(self, jogador: Jogador, **kwargs):
        cidade = jogador.cidade_atual
        if cidade.centro_pesquisa:
            print(f"Erro: {cidade.nome} já possui um centro de pesquisa.")
            return

        carta_da_cidade = next((c for c in jogador.mao if isinstance(c, CartaCidade) and c.nome == cidade.nome), None)
        if carta_da_cidade:
            cidade.centro_pesquisa = True
            jogador.descartar_carta(carta_da_cidade.nome)
            # O descarte real deve ser gerenciado pela classe Jogo/Turno
            print(f"Centro de pesquisa construído em {cidade.nome}!")
        else:
            print(f"Erro: Você precisa da carta de {cidade.nome} para construir um centro aqui.")

class TratarDoenca(Acao):
    def executa(self, jogador: Jogador, **kwargs):
        cor_doenca = kwargs.get('cor')
        if not cor_doenca:
            print("Erro: Cor da doença a ser tratada não especificada.")
            return

        if jogador.cidade_atual.remover_cubo(cor_doenca):
            print(f"{jogador.nome} tratou a doença {cor_doenca.value} em {jogador.cidade_atual.nome}.")
        else:
            print(f"Não há cubos da doença {cor_doenca.value} em {jogador.cidade_atual.nome}.")

class DesenvolverCura(Acao):
    def executa(self, jogador: Jogador, **kwargs):
        doenca = kwargs.get('doenca')
        cartas_para_cura = kwargs.get('cartas')

        if not doenca or not cartas_para_cura:
            print("Argumentos inválidos para desenvolver cura.")
            return

        if not jogador.cidade_atual.centro_pesquisa:
            print(f"Erro: É preciso estar em uma cidade com Centro de Pesquisa.")
            return

        if len(cartas_para_cura) >= 5: # Simplificado para 5
            doenca.cura_descoberta = True
            for carta in cartas_para_cura:
                jogador.descartar_carta(carta.nome)
            print(f"🎉 A CURA PARA A DOENÇA {doenca.cor.value} FOI DESCOBERTA! 🎉")
        else:
            print("Não há cartas suficientes para descobrir a cura.")

class Compartilhar(Acao):
    def executa(self, jogador: Jogador, **kwargs):
        outro_jogador = kwargs.get('outro_jogador')
        carta_para_dar = kwargs.get('carta')

        if not outro_jogador or not carta_para_dar:
            print("Argumentos inválidos para compartilhar.")
            return

        if jogador.cidade_atual == outro_jogador.cidade_atual:
            if carta_para_dar.nome == jogador.cidade_atual.nome:
                jogador.mao.remove(carta_para_dar)
                outro_jogador.adicionar_carta_mao(carta_para_dar)
                print(f"{jogador.nome} deu a carta '{carta_para_dar.nome}' para {outro_jogador.nome}.")
            else:
                print("Só é possível compartilhar a carta da cidade em que vocês estão.")
        else:
            print("Jogadores precisam estar na mesma cidade para compartilhar cartas.")