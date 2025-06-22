# main.py

from src.gui.game_controller import GameController

def get_player_count():
    """ Pede e valida o número de jogadores no terminal. """
    while True:
        try:
            num_str = input("Quantos jogadores irão jogar (2-4)? ")
            num_players = int(num_str)
            if 2 <= num_players <= 4:
                return num_players
            else:
                print("Número inválido. Por favor, escolha entre 2 e 4.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

if __name__ == '__main__':
    # 1. Pega o número de jogadores antes de qualquer outra coisa
    player_count = get_player_count()
    
    # 2. Inicia a GUI, passando o número de jogadores para o controlador
    print(f"Iniciando um jogo para {player_count} jogadores...")
    game_controller = GameController(num_players=player_count)
    game_controller.run()