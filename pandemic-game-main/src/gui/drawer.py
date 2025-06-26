# src/gui/drawer.py

import os
import pygame
from .config import *
from ..doenca import Cor

class Drawer:
    def __init__(self, world_surface):
        # Agora o Drawer conhece a superfície do MUNDO
        self.world_surface = world_surface
        self.font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_NORMAL)
        self.small_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_SMALL)
        self.color_map = {Cor.AZUL: BLUE, Cor.AMARELO: YELLOW, Cor.PRETO: GREY, Cor.VERMELHO: RED}

        # Carrega o mapa mundi
        self.background_image = pygame.image.load(os.path.join("assets", "mapa_mundi.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, (WORLD_WIDTH, WORLD_HEIGHT))

    def draw_world(self, mapa, jogadores):
        """ Desenha todos os elementos que pertencem ao mundo e devem rolar. """
        self.world_surface.blit(self.background_image, (0, 0))
        self._draw_connections(mapa)
        self._draw_cities(mapa)
        self._draw_players(jogadores)

    def draw_ui(self, screen, jogador_atual, acoes_validas, jogo):
        """ Desenha a interface do usuário (painéis, botões) que é fixa na tela. """
        self._draw_ui_panel(screen, jogador_atual, acoes_validas, jogo)

    def _draw_text(self, surface, text, position, font=None, color=WHITE):
        if font is None: font = self.font
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, position)

    def _draw_connections(self, mapa):
        drawn_connections = set()
        for city_name, city_obj in mapa.cidades.items():
            start_pos = CITY_POSITIONS[city_name]
            for vizinho in city_obj.vizinhos:
                connection = tuple(sorted((city_name, vizinho.nome)))
                if connection not in drawn_connections:
                    end_pos = CITY_POSITIONS[vizinho.nome]
                    # Lógica da Parábola
                    if connection == ("São Francisco", "Tóquio"):
                        points = []; curve_height = 200; num_segments = 30
                        for i in range(num_segments + 1):
                            t = i / num_segments
                            x = start_pos[0] * (1 - t) + end_pos[0] * t
                            y = start_pos[1] * (1 - t) + end_pos[1] * t
                            y -= curve_height * 4 * (t - t**2)
                            points.append((x, y))
                        pygame.draw.lines(self.world_surface, GREY, False, points, 2)
                    else:
                        pygame.draw.line(self.world_surface, GREY, start_pos, end_pos, 2)
                    drawn_connections.add(connection)

    def _draw_cities(self, mapa):
        for name, city_obj in mapa.cidades.items():
            pos = CITY_POSITIONS.get(name)
            if pos:
                pygame.draw.circle(self.world_surface, self.color_map[city_obj.cor], pos, 15)
                self._draw_text(self.world_surface, name, (pos[0] + 20, pos[1] - 10), font=self.small_font, color=BLUE)
                if city_obj.centro_pesquisa:
                    pygame.draw.rect(self.world_surface, WHITE, (pos[0]-7, pos[1]-7, 14, 14), 3)
                cube_offset_x, cube_offset_y = 0, 20
                for cor, count in city_obj.cubos.items():
                    if cor in self.color_map:
                        for i in range(count):
                            pygame.draw.rect(self.world_surface, self.color_map[cor], (pos[0] + cube_offset_x, pos[1] + cube_offset_y, 10, 10))
                            cube_offset_x += 12

    def _draw_players(self, jogadores):
        for i, jogador in enumerate(jogadores):
            if jogador.cidade_atual:
                pos = CITY_POSITIONS[jogador.cidade_atual.nome]
                player_pos = (pos[0] - 10 + i*10, pos[1] - 10 + i*10)
                pygame.draw.circle(self.world_surface, PLAYER_COLORS[i % len(PLAYER_COLORS)], player_pos, 8)
    
    def _draw_ui_panel(self, screen, jogador_atual, acoes_validas, jogo):
        panel_rect = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
        # Usamos uma superfície com alfa para transparência
        panel_surface = pygame.Surface((SCREEN_WIDTH, 200), pygame.SRCALPHA)
        panel_surface.fill((30, 30, 30, 220)) # Cor escura com 220 de alfa (0-255)
        screen.blit(panel_surface, (0, SCREEN_HEIGHT - 200))
        
        # Desenha os textos e botões sobre a tela
        self._draw_text(screen, f"Turno de: {jogador_atual.nome} ({jogador_atual.personagem.nome})", (20, SCREEN_HEIGHT - 190))
        self._draw_text(screen, f"Ações Restantes: {jogo.turno_atual.acoes_restantes}", (450, SCREEN_HEIGHT - 190))
        
        # Botões
        button_texts = {'treat_disease': '1. Tratar Doença', 'build_station': '2. Construir Centro', 'discover_cure': '3. Descobrir Cura', 'share_knowledge': '4. Compartilhar'}
        for action_name, rect in ACTION_BUTTONS_POS.items():
            color = GREEN if acoes_validas.get(action_name) else GREY
            pygame.draw.rect(screen, color, rect)
            self._draw_text(screen, button_texts[action_name], (rect.x + 10, rect.y + 5), font=self.small_font)

        # Mão
        self._draw_text(screen, "Mão:", (20, SCREEN_HEIGHT - 55))
        card_offset = 70
        for card in jogador_atual.mao:
            self._draw_text(screen, card.nome, (card_offset, SCREEN_HEIGHT - 30), font=self.small_font)
            card_offset += 140

        # Botão Finalizar
        end_turn_button = pygame.Rect(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 65, 200, 45)
        pygame.draw.rect(screen, GREY, end_turn_button)
        self._draw_text(screen, "Finalizar Turno", (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 55))