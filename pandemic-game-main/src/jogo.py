# src/jogo.py

from .mapa import Mapa
from .doenca import Doenca, Cor
from .baralho import Baralho
from .carta import CartaCidade, CartaDoenca, CartaEvento, CartaPersonagem
from .cidade import Cidade
from .jogador import Jogador
from .turno import Turno

class Jogo:
    def __init__(self, num_players: int): # <-- Aceita o número de jogadores
        print(f"==== INICIANDO JOGO PANDEMIC PARA {num_players} JOGADORES ====")
        self.num_players = num_players
        
        # 1. Define as cores (e doenças) ativas para o jogo
        if num_players == 2:
            self.active_colors = [Cor.AZUL, Cor.AMARELO]
        elif num_players == 3:
            self.active_colors = [Cor.AZUL, Cor.AMARELO, Cor.PRETO]
        else: # 4 jogadores
            self.active_colors = [Cor.AZUL, Cor.AMARELO, Cor.PRETO, Cor.VERMELHO]
        
        # 2. Cria apenas as doenças ativas
        self.doencas = {cor: Doenca(cor) for cor in self.active_colors}

        # 3. Inicializa um mapa apenas com as cidades das cores ativas
        self.mapa = self._inicializar_mapa(self.active_colors)
        
        # O resto da inicialização agora usa o mapa dinâmico
        cartas_cidade_jogador, cartas_cidade_infeccao = self._criar_cartas_cidade()
        self.baralho_jogador = Baralho("Jogador", cartas_cidade_jogador + self._criar_cartas_evento())
        self.baralho_infeccao = Baralho("Infecção", cartas_cidade_infeccao)

        # 4. Cria o número correto de jogadores com nomes genéricos
        nomes_jogadores = [f"Jogador {i+1}" for i in range(num_players)]
        self.jogadores = self._criar_jogadores(nomes_jogadores)
        self._distribuir_cartas_iniciais()

        self.turno_atual: Turno | None = None
        print("\n==== JOGO PRONTO PARA COMEÇAR ====")

    # Dentro da classe Jogo, no arquivo src/jogo.py

    def _inicializar_mapa(self, active_colors: list[Cor]) -> Mapa:
        mapa = Mapa()
        
        all_cities_data = [
            ("São Francisco", Cor.AZUL), ("Chicago", Cor.AZUL), ("Atlanta", Cor.AZUL), ("Montreal", Cor.AZUL), ("Washington", Cor.AZUL), ("Nova Iorque", Cor.AZUL), ("Madri", Cor.AZUL), ("Londres", Cor.AZUL), ("Paris", Cor.AZUL),
            ("Los Angeles", Cor.AMARELO), ("Cidade do México", Cor.AMARELO), ("Miami", Cor.AMARELO), ("Bogotá", Cor.AMARELO), ("Lima", Cor.AMARELO), ("São Paulo", Cor.AMARELO), ("Lagos", Cor.AMARELO), ("Kinshasa", Cor.AMARELO), ("Joanesburgo", Cor.AMARELO),
            ("Argel", Cor.PRETO), ("Cairo", Cor.PRETO), ("Istambul", Cor.PRETO), ("Moscou", Cor.PRETO), ("Bagdá", Cor.PRETO), ("Teerã", Cor.PRETO), ("Karachi", Cor.PRETO), ("Riad", Cor.PRETO),
            ("Pequim", Cor.VERMELHO), ("Xangai", Cor.VERMELHO), ("Hong Kong", Cor.VERMELHO), ("Tóquio", Cor.VERMELHO), ("Osaka", Cor.VERMELHO), ("Bangkok", Cor.VERMELHO), ("Jacarta", Cor.VERMELHO), ("Sydney", Cor.VERMELHO),
        ]
        
        # LISTA DE CONEXÕES ATUALIZADA
        all_connections = [
            ("São Francisco", "Chicago"), ("São Francisco", "Los Angeles"), ("São Francisco", "Tóquio"), 
            ("Chicago", "Atlanta"), ("Chicago", "Montreal"), ("Chicago", "Cidade do México"), 
            ("Montreal", "Nova Iorque"), ("Montreal", "Washington"), 
            ("Nova Iorque", "Londres"), ("Nova Iorque", "Madri"), 
            ("Atlanta", "Washington"), ("Atlanta", "Miami"), 
            ("Miami", "Bogotá"), 
            ("Los Angeles", "Cidade do México"), ("Los Angeles", "Sydney"), 
            ("Cidade do México", "Lima"), ("Cidade do México", "Bogotá"), 
            ("Bogotá", "São Paulo"), ("Bogotá", "Lima"), 
            ("São Paulo", "Lagos"), ("São Paulo", "Madri"), ("São Paulo", "Joanesburgo"),
            ("Londres", "Paris"), ("Londres", "Madri"), 
            ("Madri", "Argel"), 
            ("Paris", "Argel"), ("Paris", "Istambul"), 
            ("Argel", "Cairo"), 
            ("Cairo", "Bagdá"), ("Cairo", "Riad"), 
            ("Istambul", "Moscou"), ("Istambul", "Bagdá"), 
            ("Moscou", "Teerã"), 
            ("Bagdá", "Karachi"), ("Bagdá", "Teerã"), 
            ("Riad", "Karachi"), 
            ("Karachi", "Teerã"), 
            ("Tóquio", "Xangai"), ("Tóquio", "Osaka"), 
            ("Xangai", "Pequim"), ("Xangai", "Hong Kong"), 
            ("Hong Kong", "Bangkok"), ("Hong Kong", "Jacarta"), 
            ("Sydney", "Jacarta"),
            ("Lagos", "Kinshasa"),
            ("Kinshasa", "Joanesburgo"),
            # --- NOVAS CONEXÕES ESTRATÉGICAS ---
            ("Bangkok", "Karachi"),     # Conecta a região Vermelha com a Preta
            ("Hong Kong", "Pequim"),     # Uma rota interna importante na China
            ("Jacarta", "Bangkok"),      # Melhora a mobilidade no Sudeste Asiático
        ]

        cities_in_game = [c for c in all_cities_data if c[1] in active_colors]
        city_names_in_game = {c[0] for c in cities_in_game}

        for nome, cor in cities_in_game:
            mapa.adicionar_cidade(Cidade(nome, cor))

        valid_connections = [conn for conn in all_connections if conn[0] in city_names_in_game and conn[1] in city_names_in_game]

        for c1_nome, c2_nome in valid_connections:
            c1 = mapa.get_cidade(c1_nome)
            c2 = mapa.get_cidade(c2_nome)
            if c1 and c2:
                c1.adicionar_vizinho(c2)

        # A cidade inicial precisa existir no mapa de 2 jogadores, Atlanta (Azul) é segura.
        mapa.get_cidade("Atlanta").centro_pesquisa = True
        print(f"Mapa inicializado com {len(mapa.cidades)} cidades das cores: {[c.value for c in active_colors]}")
        return mapa
    
    # ... O resto do arquivo (criar cartas, jogadores, iniciar turno) pode permanecer o mesmo ...
    def _criar_cartas_cidade(self) -> tuple[list[CartaCidade], list[CartaDoenca]]:
        cartas_jogador = []
        cartas_infeccao = []
        for nome, cidade_obj in self.mapa.cidades.items():
            cartas_jogador.append(CartaCidade(nome, cidade_obj.cor))
            cartas_infeccao.append(CartaDoenca(nome, cidade_obj.cor))
        return cartas_jogador, cartas_infeccao

    def _criar_cartas_evento(self) -> list[CartaEvento]:
        return [CartaEvento("Ponte Aérea", "Mova qualquer peão para qualquer cidade.")]

    def _criar_jogadores(self, nomes: list[str]) -> list[Jogador]:
        personagens = [
            CartaPersonagem("Cientista", "Precisa de apenas 4 cartas para descobrir a cura."),
            CartaPersonagem("Médico", "Remove todos os cubos de uma doença ao tratar."),
            CartaPersonagem("Pesquisadora", "Pode dar qualquer carta para outro jogador na mesma cidade."),
            CartaPersonagem("Agente de Operações", "Pode construir um centro de pesquisa sem gastar a carta da cidade."),
        ]
        jogadores = []
        cidade_inicial = self.mapa.get_cidade("Atlanta")
        for i, nome in enumerate(nomes):
            jogador = Jogador(nome, personagens[i % len(personagens)])
            jogador.set_cidade_atual(cidade_inicial)
            jogadores.append(jogador)
        return jogadores

    def _distribuir_cartas_iniciais(self):
        print("\n--- Distribuindo cartas iniciais ---")
        # Regra do Pandemic: 4 jogadores -> 2 cartas; 3 jogadores -> 3 cartas; 2 jogadores -> 4 cartas
        num_cartas_map = {2: 4, 3: 3, 4: 2}
        num_cartas = num_cartas_map[self.num_players]
        
        for jogador in self.jogadores:
            for _ in range(num_cartas):
                carta = self.baralho_jogador.comprar()
                if carta: jogador.adicionar_carta_mao(carta)
            print(f"{jogador.nome} recebeu {num_cartas} cartas. Mão: {[c.nome for c in jogador.mao]}")

    def iniciar_novo_turno(self, jogador: Jogador):
        self.turno_atual = Turno(jogador, self)
        print(f"\n================ NOVO TURNO: {jogador.nome} ({jogador.personagem.nome}) ================")