import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions par défaut
TILE_SIZE = 100  # Taille des tuiles
MARGIN = 50  # Marge autour de la grille
WIDTH, HEIGHT = 0, 0
WINDOW = None  # La fenêtre sera initialisée dynamiquement

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (0, 102, 204)
RED = (204, 0, 0)
GREEN = (0, 255, 0)

def initialize_window(n):
    """
    Initialise la fenêtre en fonction de la taille du puzzle choisi.
    """
    global WIDTH, HEIGHT, WINDOW
    WIDTH = HEIGHT = TILE_SIZE * n + MARGIN * 2
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption(f"{n * n - 1}-Puzzle")

def draw_menu():
    """
    Affiche un menu pour que l'utilisateur choisisse entre 8-puzzle et 15-puzzle.
    """
    WINDOW.fill(WHITE)

    font = pygame.font.Font(None, 60)
    title = font.render("Choisissez votre puzzle :", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    WINDOW.blit(title, title_rect)

    # Bouton pour 8-puzzle
    button_8 = pygame.Rect(WIDTH // 4 - 75, HEIGHT // 2, 150, 50)
    pygame.draw.rect(WINDOW, BLUE, button_8)
    text_8 = font.render("8-puzzle", True, WHITE)
    text_8_rect = text_8.get_rect(center=button_8.center)
    WINDOW.blit(text_8, text_8_rect)

    # Bouton pour 15-puzzle
    button_15 = pygame.Rect(3 * WIDTH // 4 - 75, HEIGHT // 2, 150, 50)
    pygame.draw.rect(WINDOW, RED, button_15)
    text_15 = font.render("15-puzzle", True, WHITE)
    text_15_rect = text_15.get_rect(center=button_15.center)
    WINDOW.blit(text_15, text_15_rect)

    pygame.display.flip()

    return button_8, button_15

def generate_puzzle(n):
    """
    Génère un puzzle avec des cases numérotées de 1 à n*n-1, et un espace vide représenté par 0.
    """
    puzzle = list(range(1, n * n)) + [0]
    while True:
        random.shuffle(puzzle)
        if is_solvable(puzzle, n):
            break
    return puzzle

def is_solvable(puzzle, n):
    """
    Vérifie si le puzzle est solvable.
    """
    inversions = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:
                inversions += 1

    if n % 2 == 1:  # Grille impaire
        return inversions % 2 == 0
    else:  # Grille paire
        blank_row = (puzzle.index(0) // n)
        return (inversions + blank_row) % 2 == 0

def draw_puzzle(window, puzzle, n, remaining_moves=None):
    """
    Dessine le puzzle sur la fenêtre avec le nombre de déplacements restants (optionnel).
    """
    window.fill(WHITE)
    for i in range(n):
        for j in range(n):
            value = puzzle[i * n + j]
            if value != 0:  # Case vide
                rect = pygame.Rect(MARGIN + j * TILE_SIZE, MARGIN + i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(window, GREY, rect)
                pygame.draw.rect(window, BLACK, rect, 2)

                font = pygame.font.Font(None, 80)
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                window.blit(text, text_rect)

    # Afficher le nombre de déplacements restants
    if remaining_moves is not None:
        font = pygame.font.Font(None, 60)
        moves_text = font.render(f"restes: {remaining_moves}", True, GREEN)
        window.blit(moves_text, (WIDTH // 2 - moves_text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

def move_tile(puzzle, n, position, blank_pos):
    """
    Permet de déplacer une tuile si elle est adjacente à la case vide.
    """
    i, j = position
    bi, bj = blank_pos
    if abs(i - bi) + abs(j - bj) == 1:  # Vérifie si le mouvement est valide
        puzzle[bi * n + bj], puzzle[i * n + j] = puzzle[i * n + j], puzzle[bi * n + bj]
        return (i, j)  # Nouvelle position de la case vide
    return blank_pos

def swap_tiles(puzzle, n):
    """
    Permet d'échanger deux tuiles aléatoires dans le puzzle.
    """
    non_zero_tiles = [i for i, value in enumerate(puzzle) if value != 0]
    tile1, tile2 = random.sample(non_zero_tiles, 2)
    puzzle[tile1], puzzle[tile2] = puzzle[tile2], puzzle[tile1]

# === Main ===
def main():
    global WINDOW

    global WIDTH, HEIGHT
    WIDTH, HEIGHT = 600, 400
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

    running = True
    n = 0

    while running:
        button_8, button_15 = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_8.collidepoint(event.pos):
                    n = 3
                    running = False
                elif button_15.collidepoint(event.pos):
                    n = 4
                    running = False

    # Demander à l'utilisateur d'entrer la valeur de k
    font = pygame.font.Font(None, 60)
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    user_input = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    k = int(user_input) if user_input.isdigit() else 0
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        WINDOW.fill(WHITE)
        pygame.draw.rect(WINDOW, BLUE, input_box)
        txt_surface = font.render(user_input, True, BLACK)
        input_box.w = max(200, txt_surface.get_width()+10)
        WINDOW.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.display.flip()

    # Initialiser la fenêtre du puzzle et générer le puzzle
    initialize_window(n)
    puzzle = generate_puzzle(n)
    blank_pos = divmod(puzzle.index(0), n)
    
    remaining_moves = k
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and remaining_moves > 0:
                if event.key == pygame.K_UP and blank_pos[0] < n - 1:
                    blank_pos = move_tile(puzzle, n, (blank_pos[0] + 1, blank_pos[1]), blank_pos)
                    remaining_moves -= 1  # Décrémenter le nombre de déplacements
                elif event.key == pygame.K_DOWN and blank_pos[0] > 0:
                    blank_pos = move_tile(puzzle, n, (blank_pos[0] - 1, blank_pos[1]), blank_pos)
                    remaining_moves -= 1
                elif event.key == pygame.K_LEFT and blank_pos[1] < n - 1:
                    blank_pos = move_tile(puzzle, n, (blank_pos[0], blank_pos[1] + 1), blank_pos)
                    remaining_moves -= 1
                elif event.key == pygame.K_RIGHT and blank_pos[1] > 0:
                    blank_pos = move_tile(puzzle, n, (blank_pos[0], blank_pos[1] - 1), blank_pos)
                    remaining_moves -= 1

        # Lorsque le nombre de déplacements atteint 0, échanger deux tuiles
        if remaining_moves == 0:
            swap_tiles(puzzle, n)
            remaining_moves = k  # Réinitialiser le nombre de déplacements

        draw_puzzle(WINDOW, puzzle, n, remaining_moves)
        pygame.time.delay(100)

    pygame.quit()

if __name__ == "__main__":
    main()
