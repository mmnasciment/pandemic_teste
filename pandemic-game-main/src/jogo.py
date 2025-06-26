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
            ("Argel", Cor.PRETO),
            ("Atlanta", Cor.AZUL),
            ("Bagdá", Cor.PRETO),
            ("Bangkok", Cor.VERMELHO),
            ("Bogotá", Cor.AMARELO),
            ("Buenos Aires", Cor.AMARELO),
            ("Cairo", Cor.PRETO),
            ("Chicago", Cor.AZUL),
            ("Cidade do México", Cor.AMARELO),
            ("Essen", Cor.AZUL),
            ("Hong Kong", Cor.VERMELHO),
            ("Istambul", Cor.PRETO),
            ("Jacarta", Cor.VERMELHO),
            ("Joanesburgo", Cor.AMARELO),
            ("Karachi", Cor.PRETO),
            ("Khartoum", Cor.AMARELO),
            ("Kinshasa", Cor.AMARELO),
            ("Lagos", Cor.AMARELO),
            ("Lima", Cor.AMARELO),
            ("Londres", Cor.AZUL),
            ("Los Angeles", Cor.AMARELO),
            ("Madri", Cor.AZUL),
            ("Miami", Cor.AMARELO),
            ("Milão", Cor.AZUL),
            ("Montreal", Cor.AZUL),
            ("Moscou", Cor.PRETO),
            ("Nova Iorque", Cor.AZUL),
            ("Osaka", Cor.VERMELHO),
            ("Paris", Cor.AZUL),
            ("Pequim", Cor.VERMELHO),
            ("Riad", Cor.PRETO),
            ("São Francisco", Cor.AZUL),
            ("Santiago", Cor.AMARELO),
            ("São Paulo", Cor.AMARELO),
            ("São Petersburgo", Cor.AZUL),
            ("Tóquio", Cor.VERMELHO),
            ("Sydney", Cor.VERMELHO),
            ("Teerã", Cor.PRETO),
            ("Xangai", Cor.VERMELHO),
            ("Washington", Cor.AZUL),
        ]
        
        # LISTA DE CONEXÕES ATUALIZADA
        all_connections = [
            ("Argel", "Cairo"), 
            ("Atlanta", "Washington"), ("Atlanta", "Miami"), 
            ("Bagdá", "Karachi"), ("Bagdá", "Teerã"), 
            ("Bogotá", "São Paulo"), ("Bogotá", "Lima"), 
            ("Buenos Aires", "São Paulo"), ("Buenos Aires", "Bogotá"),
            ("Cairo", "Bagdá"), ("Cairo", "Riad"), ("Cairo", "Istambul"),
            ("Chicago", "Atlanta"), ("Chicago", "Montreal"), ("Chicago", "Cidade do México"), ("Chicago", "Los Angeles"),
            ("Cidade do México", "Lima"), ("Cidade do México", "Bogotá"), ("Cidade do México", "Miami"), 
            ("Essen", "São Petersburgo"),
            ("Hong Kong", "Bangkok"), ("Hong Kong", "Jacarta"), 
            ("Istambul", "Moscou"), ("Istambul", "Bagdá"), 
            ("Karachi", "Teerã"), 
            ("Khartoum", "Lagos"), ("Khartoum", "Kinshasa"), ("Khartoum", "Joanesburgo"), ("Khartoum", "Cairo"),
            ("Kinshasa", "Joanesburgo"),
            ("Lagos", "Kinshasa"),
            ("Londres", "Paris"), ("Londres", "Madri"), 
            ("Los Angeles", "Cidade do México"), ("Los Angeles", "Sydney"), 
            ("Madri", "Argel"), 
            ("Miami", "Bogotá"), ("Miami", "Washington"),
            ("Milão", "Essen"), ("Milão", "Istambul"),
            ("Montreal", "Nova Iorque"), ("Montreal", "Washington"), 
            ("Moscou", "Teerã"), 
            ("Nova Iorque", "Londres"), ("Nova Iorque", "Madri"), ("Nova Iorque", "Washington"),
            ("Paris", "Argel"), ("Paris", "Milão"), ("Paris", "Essen"), ("Paris", "Madri"),
            ("Riad", "Karachi"), 
            ("Santiago", "Lima"),
            ("São Francisco", "Chicago"), ("São Francisco", "Los Angeles"), ("São Francisco", "Tóquio"), 
            ("São Paulo", "Lagos"), ("São Paulo", "Madri"), ("São Paulo", "Joanesburgo"),
            ("São Petersburgo", "Istambul"), ("São Petersburgo", "Moscou"),
            ("Sydney", "Jacarta"),
            ("Tóquio", "Xangai"), ("Tóquio", "Osaka"), 
            ("Xangai", "Pequim"), ("Xangai", "Hong Kong"), 
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