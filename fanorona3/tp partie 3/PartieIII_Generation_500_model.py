import numpy as np

# Définir la taille du plateau (3x3)
BOARD_SIZE = 3

# Fonction pour générer une configuration aléatoire du plateau
def generate_random_board():
    # Chaque case peut être vide (0), blanche (1) ou noire (-1)
    return np.random.choice([-1, 0, 1], size=(BOARD_SIZE, BOARD_SIZE))

# Fonction pour évaluer si une configuration est gagnante pour les blancs
def is_winning_position(board):
    # Heuristique simple : les blancs gagnent s'ils contrôlent au moins 6 intersections
    white_count = np.sum(board == 1)
    black_count = np.sum(board == -1)
    return white_count >= 6 and white_count > black_count

# Fonction pour évaluer si une configuration est perdante pour les blancs
def is_losing_position(board):
    # Heuristique simple : les blancs perdent s'ils contrôlent moins de 3 intersections
    white_count = np.sum(board == 1)
    black_count = np.sum(board == -1)
    return black_count >= 6 and black_count > white_count

# Générer 500 configurations gagnantes pour les blancs
winning_boards = []
while len(winning_boards) < 500:
    board = generate_random_board()
    if is_winning_position(board):
        winning_boards.append(board)

# Générer 500 configurations perdantes pour les blancs
losing_boards = []
while len(losing_boards) < 500:
    board = generate_random_board()
    if is_losing_position(board):
        losing_boards.append(board)

# Afficher les résultats
print(f"Nombre de configurations gagnantes générées : {len(winning_boards)}")
print(f"Nombre de configurations perdantes générées : {len(losing_boards)}")

# Exemple d'une configuration gagnante et perdante
if len(winning_boards) > 0 and len(losing_boards) > 0:
    print("\nExemple de configuration gagnante :")
    print(winning_boards[0])
    print("\nExemple de configuration perdante :")
    print(losing_boards[0])