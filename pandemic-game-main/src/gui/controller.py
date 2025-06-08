# src/gui/controller.py

import pygame
import sys
from collections import Counter
from .config import *
from .drawer import Drawer
from ..jogo import Jogo
from ..acao import Mover, TratarDoenca, ConstruirCentro, DesenvolverCura
from ..carta import CartaCidade

class GameController:
    def __init__(self, num_players: int):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # Superfície maior onde o mapa do jogo será desenhado
        self.world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        
        self.jogo = Jogo(num_players=num_players)
        # O Drawer agora desenha no world_surface, não na tela diretamente
        self.drawer = Drawer(self.world_surface)
        self.running = True
        
        self.city_rects = { name: pygame.Rect(pos[0]-15, pos[1]-15, 30, 30) for name, pos in CITY_POSITIONS.items() if name in self.jogo.mapa.cidades }
        
        # Posição inicial da câmera (canto superior esquerdo)
        self.camera_x, self.camera_y = 0, 0

        self.id_jogador_atual = 0
        self.jogo.iniciar_novo_turno(self.jogo.jogadores[self.id_jogador_atual])
        self.acoes_validas = {}

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        # Eventos únicos (como fechar a janela ou clicar)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(event.pos)

        # Eventos contínuos (teclas pressionadas para rolagem suave)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_x -= SCROLL_SPEED
        if keys[pygame.K_RIGHT]:
            self.camera_x += SCROLL_SPEED
        if keys[pygame.K_UP]:
            self.camera_y -= SCROLL_SPEED
        if keys[pygame.K_DOWN]:
            self.camera_y += SCROLL_SPEED

        # Limita a câmera para não sair dos limites do mundo
        self.camera_x = max(0, min(self.camera_x, WORLD_WIDTH - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))

    def _handle_mouse_click(self, mouse_pos):
        # TRADUZ A COORDENADA DO MOUSE (TELA) PARA A COORDENADA DO MUNDO
        world_mouse_pos = (mouse_pos[0] + self.camera_x, mouse_pos[1] + self.camera_y)

        # Checa cliques nos botões de ação (eles estão na TELA, não no MUNDO)
        for action_name, rect in ACTION_BUTTONS_POS.items():
            if rect.collidepoint(mouse_pos) and self.acoes_validas.get(action_name):
                action_handler = getattr(self, f"_handle_action_{action_name}", None)
                if action_handler: action_handler()
                return

        # Checa cliques no mapa (usando a coordenada do MUNDO)
        for name, rect in self.city_rects.items():
            if rect.collidepoint(world_mouse_pos):
                self._handle_map_click(name)
                return

        # Botão de finalizar turno (também na TELA)
        end_turn_button = pygame.Rect(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 65, 200, 45)
        if end_turn_button.collidepoint(mouse_pos):
            self._end_turn()

    def _draw(self):
        """ Nova pipeline de desenho com câmera. """
        jogador_atual = self.jogo.jogadores[self.id_jogador_atual]
        
        # 1. O Drawer desenha todo o MUNDO (mapa, cidades, jogadores) na sua superfície
        self.drawer.draw_world(self.jogo.mapa, self.jogo.jogadores)

        # 2. Limpa a TELA
        self.screen.fill(DARK_GREY)
        
        # 3. Copia a parte do MUNDO que a câmera está vendo para a TELA
        camera_rect = pygame.Rect(self.camera_x, self.camera_y, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.blit(self.world_surface, (0, 0), camera_rect)

        # 4. O Drawer desenha a UI (que não se move) DIRETAMENTE na TELA
        self.drawer.draw_ui(self.screen, jogador_atual, self.acoes_validas)
        
        # 5. Atualiza a tela para mostrar o resultado
        pygame.display.flip()

    # O resto dos métodos (_update, _handle_map_click, _end_turn, etc.) permanece igual
    def _handle_map_click(self, city_name):
        jogador_atual = self.jogo.jogadores[self.id_jogador_atual]
        cidade_clicada = self.jogo.mapa.get_cidade(city_name)
        if cidade_clicada in jogador_atual.cidade_atual.vizinhos:
            self.jogo.turno_atual.realizar_acao(Mover(), destino=cidade_clicada)
    def _handle_action_treat_disease(self):
        jogador_atual = self.jogo.jogadores[self.id_jogador_atual]
        cor_a_tratar = next(cor for cor, count in jogador_atual.cidade_atual.cubos.items() if count > 0)
        self.jogo.turno_atual.realizar_acao(TratarDoenca(), cor=cor_a_tratar)
    def _handle_action_build_station(self):
        self.jogo.turno_atual.realizar_acao(ConstruirCentro())
    def _handle_action_discover_cure(self):
        jogador_atual = self.jogo.jogadores[self.id_jogador_atual]
        card_colors = Counter(c.cor for c in jogador_atual.mao if isinstance(c, CartaCidade))
        cartas_necessarias = 4 if jogador_atual.personagem.nome == "Cientista" else 5
        for cor, qtd in card_colors.items():
            if qtd >= cartas_necessarias:
                cartas_para_cura = [c for c in jogador_atual.mao if isinstance(c, CartaCidade) and c.cor == cor][:cartas_necessarias]
                doenca_correspondente = self.jogo.doencas[cor]
                self.jogo.turno_atual.realizar_acao(DesenvolverCura(), doenca=doenca_correspondente, cartas=cartas_para_cura)
                return
    def _handle_action_share_knowledge(self): print("Ação: Compartilhar Conhecimento (ainda não implementado)")
    def _end_turn(self):
        self.jogo.turno_atual.finalizar_turno()
        self.id_jogador_atual = (self.id_jogador_atual + 1) % len(self.jogo.jogadores)
        self.jogo.iniciar_novo_turno(self.jogo.jogadores[self.id_jogador_atual])
    def _update(self):
        self.acoes_validas = {}
        if self.jogo.turno_atual.acoes_restantes <= 0: return
        jogador = self.jogo.jogadores[self.id_jogador_atual]
        cidade = jogador.cidade_atual
        if any(count > 0 for count in cidade.cubos.values()): self.acoes_validas['treat_disease'] = True
        if not cidade.centro_pesquisa and any(c.nome == cidade.nome for c in jogador.mao if isinstance(c, CartaCidade)): self.acoes_validas['build_station'] = True
        if cidade.centro_pesquisa:
            card_colors = Counter(c.cor for c in jogador.mao if isinstance(c, CartaCidade))
            cartas_necessarias = 4 if jogador.personagem.nome == "Cientista" else 5
            if any(qtd >= cartas_necessarias for qtd in card_colors.values()): self.acoes_validas['discover_cure'] = True