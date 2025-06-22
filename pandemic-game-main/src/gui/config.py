# src/gui/config.py

import pygame

# --- Configurações da Janela (a "Câmera") ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Pandemic - Navegação com Câmera"

# --- Configurações do Mapa (o "Mundo" completo) ---
WORLD_WIDTH = 3000
WORLD_HEIGHT = 1800

# --- Controles ---
SCROLL_SPEED = 15 # Velocidade da rolagem do mapa com as setas

# --- Cores, Fontes e Cores dos Jogadores (sem alteração) ---
WHITE = (255, 255, 255); BLACK = (0, 0, 0); BLUE = (50, 50, 200); RED = (200, 50, 50); YELLOW = (200, 200, 50); GREY = (150, 150, 150); DARK_GREY = (50, 50, 50); GREEN = (50, 200, 50); PINK = (255, 105, 180)
PLAYER_COLORS = [(30, 144, 255), PINK, GREEN, WHITE]
FONT_FAMILY = "Arial"; FONT_SIZE_NORMAL = 24; FONT_SIZE_SMALL = 18

# --- UI Layout (ancorado na TELA, não no MUNDO) ---
ACTION_BUTTON_WIDTH = 180; ACTION_BUTTON_HEIGHT = 40
ACTION_BUTTONS_POS = {
    'treat_disease': pygame.Rect(20, SCREEN_HEIGHT - 160, ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT),
    'build_station': pygame.Rect(20, SCREEN_HEIGHT - 110, ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT),
    'discover_cure': pygame.Rect(220, SCREEN_HEIGHT - 160, ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT),
    'share_knowledge': pygame.Rect(220, SCREEN_HEIGHT - 110, ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT),
}

# --- Posições das Cidades (coordenadas no MUNDO de 2400x1600) ---
CITY_POSITIONS = {
    "São Francisco": (300, 475), "Chicago": (550, 450), "Montreal": (650, 450), "Nova Iorque": (650, 500), "Atlanta": (525, 600), "Washington": (625, 525), "Londres": (1265, 350), "Madri": (1250, 515), "Paris": (1300, 425),
    "Los Angeles": (300, 550), "Cidade do México": (400, 800), "Miami": (575, 700), "Bogotá": (600, 1000), "Lima": (600, 1200), "São Paulo": (850, 1350), "Lagos": (1325, 950), "Kinshasa": (1425, 1125), "Joanesburgo": (1500, 1450),
    "Argel": (1100, 550), "Istambul": (1250, 500), "Cairo": (1200, 580), "Moscou": (1350, 430), "Bagdá": (1380, 560), "Riad": (1350, 680), "Teerã": (1480, 510), "Karachi": (1500, 600),
    "Pequim": (1750, 450), "Xangai": (1780, 530), "Hong Kong": (1800, 650), "Tóquio": (2000, 480), "Osaka": (2010, 560), "Bangkok": (1650, 700), "Jacarta": (1680, 850), "Sydney": (1950, 1100),
}