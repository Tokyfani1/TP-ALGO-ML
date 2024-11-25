import pygame
import sys
import random
import heapq
import math
from typing import List, Tuple

# Initialisation de pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puzzle Game")

# Couleurs
WHITE = (255, 255, 255)
DARK_BLUE = (20, 30, 70)
LIGHT_BLUE = (70, 130, 180)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
HIGHLIGHT_GREEN = (39, 174, 96)
HIGHLIGHT_RED = (192, 57, 43)
SHADOW = (30, 30, 30)
GOLD = (255, 215, 0)

# Police
FONT = pygame.font.Font(pygame.font.match_font("comicsansms"), 16)
LARGE_FONT = pygame.font.Font(pygame.font.match_font("comicsansms"), 50)
TITLE_FONT = pygame.font.Font(pygame.font.match_font("comicsansms"), 72)

# Variables du jeu
TILE_SIZE = 90
MARGIN = 5

class ParticleSystem:
    def __init__(self):
        self.particles: List[dict] = []
    
    def create_particle(self, x: int, y: int, color: Tuple[int, int, int]):
        particle = {
            'x': x,
            'y': y,
            'dx': random.uniform(-2, 2),
            'dy': random.uniform(-2, 2),
            'lifetime': 60,
            'color': color,
            'size': random.randint(3, 6)
        }
        self.particles.append(particle)
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        for particle in self.particles:
            alpha = min(255, particle['lifetime'] * 4)
            color = (*particle['color'], alpha)
            surf = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (particle['size']//2, particle['size']//2), particle['size']//2)
            surface.blit(surf, (particle['x'] - particle['size']//2, particle['y'] - particle['size']//2))

class Button:
    def __init__(self, x, y, width, height, text, base_color, highlight_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.highlight_color = highlight_color
        self.is_hovered = False
        self.animation_progress = 0
    
    def draw(self, surface):
        if self.is_hovered:
            self.animation_progress = min(1, self.animation_progress + 0.1)
        else:
            self.animation_progress = max(0, self.animation_progress - 0.1)
        
        current_color = tuple(
            int(self.base_color[i] + (self.highlight_color[i] - self.base_color[i]) * self.animation_progress)
            for i in range(3)
        )
        
        shadow_rect = self.rect.inflate(4, 4)
        pygame.draw.rect(surface, SHADOW, shadow_rect, border_radius=10)
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        
        text_surf = FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
        if self.animation_progress > 0:
            shine_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            shine_alpha = int(128 * self.animation_progress)
            pygame.draw.rect(shine_surf, (255, 255, 255, shine_alpha), shine_surf.get_rect(), border_radius=8)
            surface.blit(shine_surf, self.rect)

def manhattan_distance(board, size):
    """Calculate the Manhattan distance heuristic for the puzzle."""
    distance = 0
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            if value == 0:
                continue
            
            # Calculate target position
            target_row = (value - 1) // size
            target_col = (value - 1) % size
            
            # Add Manhattan distance
            distance += abs(i - target_row) + abs(j - target_col)
    return distance

def board_to_tuple(board):
    """Convert board to hashable tuple for tracking states."""
    return tuple(tuple(row) for row in board)

def solve_puzzle(puzzle_game):
    """
    Solve the puzzle using A* algorithm.
    Returns a list of moves to solve the puzzle.
    """
    initial_board = [row[:] for row in puzzle_game.board]
    goal_board = [[0 for _ in range(puzzle_game.size)] for _ in range(puzzle_game.size)]
    
    # Populate goal board
    value = 1
    for i in range(puzzle_game.size):
        for j in range(puzzle_game.size):
            if value < puzzle_game.size * puzzle_game.size:
                goal_board[i][j] = value
                value += 1
    goal_board[puzzle_game.size-1][puzzle_game.size-1] = 0
    
    # Priority queue for A* search
    heap = [(0, initial_board, [])]
    visited = set()
    
    while heap:
        _, current_board, moves = heapq.heappop(heap)
        
        # Check if solved
        if current_board == goal_board:
            return moves
        
        # Convert board to hashable tuple for visited tracking
        board_tuple = board_to_tuple(current_board)
        if board_tuple in visited:
            continue
        visited.add(board_tuple)
        
        # Find empty tile
        empty_pos = None
        for i in range(puzzle_game.size):
            for j in range(puzzle_game.size):
                if current_board[i][j] == 0:
                    empty_pos = (i, j)
                    break
            if empty_pos:
                break
        
        # Try all possible moves
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_i, new_j = empty_pos[0] + di, empty_pos[1] + dj
            
            if 0 <= new_i < puzzle_game.size and 0 <= new_j < puzzle_game.size:
                # Create a copy of the current board and swap tiles
                new_board = [row[:] for row in current_board]
                new_board[empty_pos[0]][empty_pos[1]] = new_board[new_i][new_j]
                new_board[new_i][new_j] = 0
                
                # Calculate priority (f = g + h)
                g_cost = len(moves) + 1
                h_cost = manhattan_distance(new_board, puzzle_game.size)
                priority = g_cost + h_cost
                
                # Add to heap with priority
                new_moves = moves + [(new_i, new_j)]
                heapq.heappush(heap, (priority, new_board, new_moves))
    
    return None  # No solution found

def add_solve_button(game, screen):
    """Add a solve button to the puzzle game."""
    solve_button = Button(
        SCREEN_WIDTH - 110, 
        10, 
        100, 
        40, 
        "Solve", 
        GOLD, 
        (255, 223, 0)
    )
    return solve_button


class PuzzleTile:
    def __init__(self, value, size):
        self.value = value
        self.size = size
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.target_pos = (0, 0)
        self.current_pos = [0, 0]
        self.moving = False
        self.move_speed = 0.2
        
    def update(self):
        if self.moving:
            dx = self.target_pos[0] - self.current_pos[0]
            dy = self.target_pos[1] - self.current_pos[1]
            
            if abs(dx) < 0.1 and abs(dy) < 0.1:
                self.current_pos = list(self.target_pos)
                self.moving = False
            else:
                self.current_pos[0] += dx * self.move_speed
                self.current_pos[1] += dy * self.move_speed
        
        self.rect.topleft = self.current_pos
    
    def draw(self, surface):
        if self.value == 0:  # Empty tile
            return
            
        pygame.draw.rect(surface, LIGHT_BLUE, self.rect, border_radius=8)
        text = FONT.render(str(self.value), True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

class PuzzleGame:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.tiles = []
        self.moves = 0
        self.particle_system = ParticleSystem()
        self.shuffle_moves = 100
        self.game_won = False
        self.initialize_board()
        
    def initialize_board(self):
        # Create tiles
        value = 1
        for i in range(self.size):
            for j in range(self.size):
                if value < self.size * self.size:
                    tile = PuzzleTile(value, self.size)
                    self.tiles.append(tile)
                    self.board[i][j] = value
                value += 1
                
        # Set initial positions
        self.update_tile_positions()
        self.shuffle()
    
    def update_tile_positions(self):
        board_width = self.size * (TILE_SIZE + MARGIN)
        board_height = self.size * (TILE_SIZE + MARGIN)
        start_x = (SCREEN_WIDTH - board_width) // 2
        start_y = (SCREEN_HEIGHT - board_height) // 2
        
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                if value != 0:
                    tile = self.get_tile_by_value(value)
                    if tile:
                        new_pos = (
                            start_x + j * (TILE_SIZE + MARGIN),
                            start_y + i * (TILE_SIZE + MARGIN)
                        )
                        tile.target_pos = new_pos
                        if not hasattr(tile, 'current_pos') or tile.current_pos == [0, 0]:
                            tile.current_pos = list(new_pos)
                        tile.moving = True
    
    def get_tile_by_value(self, value):
        for tile in self.tiles:
            if tile.value == value:
                return tile
        return None
    
    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j
        return None
    
    def get_valid_moves(self):
        empty_i, empty_j = self.find_empty()
        valid_moves = []
        
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_i, new_j = empty_i + di, empty_j + dj
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                valid_moves.append((new_i, new_j))
        
        return valid_moves
    
    def shuffle(self):
        for _ in range(self.shuffle_moves):
            valid_moves = self.get_valid_moves()
            if valid_moves:
                i, j = random.choice(valid_moves)
                self.make_move(i, j)
        self.moves = 0
    
    def make_move(self, i, j):
        empty_i, empty_j = self.find_empty()
        if abs(i - empty_i) + abs(j - empty_j) == 1:  # Adjacent to empty space
            # Swap tiles
            self.board[empty_i][empty_j] = self.board[i][j]
            self.board[i][j] = 0
            self.moves += 1
            self.update_tile_positions()
            
            # Create particles at the moved tile
            tile = self.get_tile_by_value(self.board[empty_i][empty_j])
            if tile:
                for _ in range(5):
                    self.particle_system.create_particle(
                        tile.rect.centerx,
                        tile.rect.centery,
                        LIGHT_BLUE
                    )
            
    def is_solved(self):
        value = 1
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    return self.board[i][j] == 0
                if self.board[i][j] != value:
                    return False
                value += 1
        return True
    
    def update(self):
        any_moving = False
        for tile in self.tiles:
            tile.update()
            if tile.moving:
                any_moving = True
        self.particle_system.update()
        return any_moving
    
    def draw(self, surface):
        # Draw board background
        board_width = self.size * (TILE_SIZE + MARGIN)
        board_height = self.size * (TILE_SIZE + MARGIN)
        board_rect = pygame.Rect(
            (SCREEN_WIDTH - board_width) // 2,
            (SCREEN_HEIGHT - board_height) // 2,
            board_width,
            board_height
        )
        pygame.draw.rect(surface, DARK_BLUE, board_rect, border_radius=10)
        
        # Draw tiles
        for tile in self.tiles:
            tile.draw(surface)
        
        # Draw particles
        self.particle_system.draw(surface)
        
        # Draw moves counter
        moves_text = FONT.render(f"Moves: {self.moves}", True, WHITE)
        surface.blit(moves_text, (10, 10))
        
        # Draw victory message
        if self.game_won:
            victory_text = LARGE_FONT.render("Victory!", True, GOLD)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, 50))
            surface.blit(victory_text, text_rect)

def game_loop(size):
    clock = pygame.time.Clock()
    game = PuzzleGame(size)
    
    # Bouton retour
    back_button = Button(10, SCREEN_HEIGHT - 60, 100, 40, "Retour", RED, HIGHLIGHT_RED)
    
    # Bouton de résolution
    solve_button = add_solve_button(game, screen)
    solve_solution = None
    current_solve_move_index = 0
    
    while True:
        screen.fill(DARK_BLUE)
        
        # Gestion des événements
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Gestion du bouton retour
                if back_button.rect.collidepoint(event.pos):
                    return "menu"
                
                # Gestion du bouton de résolution
                if solve_button.rect.collidepoint(event.pos):
                    solve_solution = solve_puzzle(game)
                    current_solve_move_index = 0
                
                # Gestion des clics sur les tuiles
                if not game.game_won and solve_solution is None:
                    board_width = size * (TILE_SIZE + MARGIN)
                    board_height = size * (TILE_SIZE + MARGIN)
                    board_x = (SCREEN_WIDTH - board_width) // 2
                    board_y = (SCREEN_HEIGHT - board_height) // 2
                    
                    # Convertir la position du clic en coordonnées de la grille
                    x, y = event.pos
                    j = (x - board_x) // (TILE_SIZE + MARGIN)
                    i = (y - board_y) // (TILE_SIZE + MARGIN)
                    
                    if 0 <= i < size and 0 <= j < size:
                        game.make_move(i, j)
        
        # Résolution automatique étape par étape
        if solve_solution is not None:
            if current_solve_move_index < len(solve_solution):
                i, j = solve_solution[current_solve_move_index]
                game.make_move(i, j)
                current_solve_move_index += 1
                pygame.time.delay(200)  # Petit délai entre les mouvements
            elif not game.is_solved():
                game.game_won = True
        
        # Mise à jour
        game.update()
        
        # Mise à jour du survol des boutons
        mouse_pos = pygame.mouse.get_pos()
        back_button.is_hovered = back_button.rect.collidepoint(mouse_pos)
        solve_button.is_hovered = solve_button.rect.collidepoint(mouse_pos)
        
        # Dessin
        game.draw(screen)
        back_button.draw(screen)
        solve_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

class MainMenu:
    def __init__(self):
        self.particle_system = ParticleSystem()
        self.buttons = [
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 30, 200, 60, "Jouer", GREEN, HIGHLIGHT_GREEN),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 60, "Quitter", RED, HIGHLIGHT_RED)
        ]
        self.title_angle = 0
        self.title_scale = 1.0
        
    def run(self):
        clock = pygame.time.Clock()
        title_text = "Puzzle Game"
        
        while True:
            current_time = pygame.time.get_ticks()
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                   for i, button in enumerate(self.buttons):
                        if button.rect.collidepoint(event.pos):
                            if i == 0:  # Bouton Jouer
                                return "game"
                            elif i == 1:  # Bouton Quitter
                                pygame.quit()
                                sys.exit()
            
            # Update
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_hovered = button.rect.collidepoint(mouse_pos)
                
            self.particle_system.update()
            
            # Animation du titre
            self.title_angle = math.sin(current_time / 1000.0) * 5  # Oscillation entre -5 et 5 degrés
            self.title_scale = 1.0 + math.sin(current_time / 800.0) * 0.1  # Oscillation entre 0.9 et 1.1
            
            # Draw
            screen.fill(DARK_BLUE)
            
            # Dessin des particules d'arrière-plan
            if random.random() < 0.1:  # 10% de chance de créer une nouvelle particule
                self.particle_system.create_particle(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT),
                    LIGHT_BLUE
                )
            self.particle_system.draw(screen)
            
            # Dessin du titre avec rotation et échelle
            title_surf = TITLE_FONT.render("Puzzle Game", True, WHITE)
            rotated_surf = pygame.transform.rotozoom(title_surf, self.title_angle, self.title_scale)
            title_rect = rotated_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
            screen.blit(rotated_surf, title_rect)
            
            # Dessin des boutons
            for button in self.buttons:
                button.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)

class DifficultyMenu:
    def __init__(self):
        self.particle_system = ParticleSystem()
        button_y = SCREEN_HEIGHT // 2 - 100
        self.buttons = []
        
        # Ajouter uniquement les boutons pour 3x3 et 4x4
        for i, size in enumerate([3, 4]):  
            self.buttons.append(
                Button(
                    SCREEN_WIDTH // 2 - 100,
                    button_y + i * 80,
                    200,
                    60,
                    f"{size}x{size}",
                    GREEN,
                    HIGHLIGHT_GREEN
                )
            )
        
        # Bouton retour
        self.buttons.append(
            Button(
                SCREEN_WIDTH // 2 - 100,
                button_y + 2 * 80,  # Ajustez la position pour le bouton "Retour"
                200,
                60,
                "Retour",
                RED,
                HIGHLIGHT_RED
            )
        )    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.rect.collidepoint(event.pos):
                            if i < 3:  # Boutons de difficulté
                                return ("play", i + 3)  # Retourne la taille du puzzle (3, 4, ou 5)
                            else:  # Bouton retour
                                return ("menu", None)
            
            # Update
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_hovered = button.rect.collidepoint(mouse_pos)
                
            self.particle_system.update()
            
            # Draw
            screen.fill(DARK_BLUE)
            
            # Particules d'arrière-plan
            if random.random() < 0.1:
                self.particle_system.create_particle(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT),
                    LIGHT_BLUE
                )
            self.particle_system.draw(screen)
            
            # Titre
            title = LARGE_FONT.render("Sélectionnez la difficulté", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
            screen.blit(title, title_rect)
            
            # Boutons
            for button in self.buttons:
                button.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)

def main():
    current_screen = "menu"
    main_menu = MainMenu()
    difficulty_menu = DifficultyMenu()
    
    while True:
        if current_screen == "menu":
            current_screen = main_menu.run()
        elif current_screen == "game":
            current_screen = difficulty_menu.run()
        elif isinstance(current_screen, tuple):
            action, size = current_screen
            if action == "play":
                current_screen = game_loop(size)
            elif action == "menu":
                current_screen = "menu"

if __name__ == "__main__":
    main()