import pygame
import random
import heapq
import csv
import time

class PuzzleGame:
    def __init__(self):
        pygame.init()
        # Refined visual constants
        self.TILE_SIZE = 100  # Slightly smaller tiles
        self.MARGIN = 50  # Reduced margin
        self.SCREEN_WIDTH = 800  # Smaller window
        self.SCREEN_HEIGHT = 600  # Smaller window
        
        # Enhanced color palette
        self.BACKGROUND_COLOR = (240, 248, 255)  # Soft light blue
        self.TILE_COLOR = (52, 152, 219)  # Vibrant blue
        self.TEXT_COLOR = (255, 255, 255)  # White
        self.ACCENT_COLOR = (44, 62, 80)  # Dark blue-gray
        self.HIGHLIGHT_COLOR = (231, 76, 60)  # Soft red for highlights
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Pygame setup with smoother rendering
        pygame.display.set_icon(pygame.Surface((32, 32), pygame.SRCALPHA))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Puzzle Challenge")
        self.clock = pygame.time.Clock()

        # Refined typography
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        self.INPUT_BACKGROUND = (240, 240, 250)
        self.INPUT_BORDER_COLOR = (100, 100, 150)

        

    def draw_gradient_background(self):
        # Softer, more elegant gradient
        for y in range(self.SCREEN_HEIGHT):
            r = int(240 - (y / self.SCREEN_HEIGHT) * 40)
            g = int(248 - (y / self.SCREEN_HEIGHT) * 30)
            b = int(255 - (y / self.SCREEN_HEIGHT) * 40)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.SCREEN_WIDTH, y))

    def draw_menu(self):
        self.draw_gradient_background()
        
        # Refined title with shadow effect
        title = self.font_large.render("Puzzle Challenge", True, self.ACCENT_COLOR)
        shadow = self.font_large.render("Puzzle Challenge", True, (200, 200, 220))
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 4))
        shadow_rect = shadow.get_rect(center=(self.SCREEN_WIDTH // 2 + 2, self.SCREEN_HEIGHT // 4 + 2))
        
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        buttons = [
            {"text": "8-Puzzle", "rect": pygame.Rect(self.SCREEN_WIDTH // 4 - 100, self.SCREEN_HEIGHT // 2, 200, 80), "size": 3},
            {"text": "15-Puzzle", "rect": pygame.Rect(3 * self.SCREEN_WIDTH // 4 - 100, self.SCREEN_HEIGHT // 2, 200, 80), "size": 4}
        ]

        for button in buttons:
            # Softer button design with hover-like effect
            pygame.draw.rect(self.screen, self.TILE_COLOR, button["rect"], border_radius=15)
            pygame.draw.rect(self.screen, self.ACCENT_COLOR, button["rect"], 3, border_radius=15)
            text = self.font_medium.render(button["text"], True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()
        return buttons
    def draw_input_field(self, input_box, user_input):
        # Clear the input area with a soft background
        pygame.draw.rect(self.screen, self.INPUT_BACKGROUND, input_box)
        
        # Draw input border
        pygame.draw.rect(self.screen, self.INPUT_BORDER_COLOR, input_box, 2, border_radius=10)
        
        # Placeholder text if input is empty
        if not user_input:
            placeholder = self.font_small.render("Enter le nombre de deplacement", True, (150, 150, 180))
            self.screen.blit(placeholder, (input_box.x + 10, input_box.y + 15))
        else:
            # Render user input
            txt_surface = self.font_small.render(user_input, True, self.ACCENT_COLOR)
            self.screen.blit(txt_surface, (input_box.x + 10, input_box.y + 15))

    def draw_puzzle(self, puzzle, n, remaining_moves=None):
        self.draw_gradient_background()
        for i in range(n):
            for j in range(n):
                value = puzzle[i * n + j]
                if value != 0:
                    rect = pygame.Rect(self.MARGIN + j * self.TILE_SIZE, 
                                       self.MARGIN + i * self.TILE_SIZE, 
                                       self.TILE_SIZE, self.TILE_SIZE)
                    pygame.draw.rect(self.screen, self.TILE_COLOR, rect, border_radius=15)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=15)
                    text = self.font_large.render(str(value), True, self.TEXT_COLOR)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
        moves_textx = self.font_medium.render(f"resolution automatique:touche S", True, self.ACCENT_COLOR)
        self.screen.blit(moves_textx, (200 , 0))
        if remaining_moves is not None:
            moves_text = self.font_medium.render(f"mouvement restant avant la prochaine swap: {remaining_moves}", True, self.ACCENT_COLOR)
            self.screen.blit(moves_text, (self.SCREEN_WIDTH // 2 - moves_text.get_width() // 2, self.SCREEN_HEIGHT - 100))

        pygame.display.flip()

    def generate_puzzle(self, n):
        puzzle = list(range(1, n * n)) + [0]
        while True:
            random.shuffle(puzzle)
            if self.is_solvable(puzzle, n):
                return puzzle

    def is_solvable(self, puzzle, n):
        inversions = sum(
            1 for i in range(len(puzzle)) 
            for j in range(i + 1, len(puzzle)) 
            if puzzle[i] and puzzle[j] and puzzle[i] > puzzle[j]
        )
        
        blank_row = puzzle.index(0) // n
        
        if n % 2 == 1:
            # For odd grid sizes (3x3)
            return inversions % 2 == 0
        else:
            # For even grid sizes (4x4)
            if (n - blank_row) % 2 == 1:
                return inversions % 2 == 0
            else:
                return inversions % 2 == 1

    def move_tile(self, puzzle, n, position, blank_pos):
        i, j = position
        bi, bj = blank_pos
        if abs(i - bi) + abs(j - bj) == 1:
            puzzle[bi * n + bj], puzzle[i * n + j] = puzzle[i * n + j], puzzle[bi * n + bj]
            return (i, j)
        return blank_pos

    def a_star_solver(self, initial_puzzle, n):
        start_time = time.time()
        start_state = tuple(initial_puzzle)
        target_state = tuple(range(1, n * n)) + (0,)

        open_set = [(0, start_state, start_state.index(0), 0, None)]
        closed_set = set()
        parent_map = {}

        while open_set:
            _, current_state, blank_pos, g_score, parent = heapq.heappop(open_set)

            if current_state in closed_set:
                continue

            closed_set.add(current_state)
            parent_map[current_state] = parent

            if current_state == target_state:
                path = []
                while current_state:
                    path.append(current_state)
                    current_state = parent_map[current_state]
                return path[::-1], len(path), time.time() - start_time, "Success"

            i, j = divmod(blank_pos, n)
            neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

            for ni, nj in neighbors:
                if 0 <= ni < n and 0 <= nj < n:
                    new_blank_pos = ni * n + nj
                    new_state = list(current_state)
                    new_state[blank_pos], new_state[new_blank_pos] = new_state[new_blank_pos], new_state[blank_pos]
                    new_state = tuple(new_state)

                    if new_state not in closed_set:
                        h_score = self.manhattan_distance(new_state, n)
                        f_score = g_score + 1 + h_score
                        heapq.heappush(open_set, (f_score, new_state, new_blank_pos, g_score + 1, current_state))

        return None, 0, time.time() - start_time, "Failed"

    def manhattan_distance(self, puzzle, n):
        distance = 0
        for index, value in enumerate(puzzle):
            if value != 0:
                target_x, target_y = divmod(value - 1, n)
                current_x, current_y = divmod(index, n)
                distance += abs(target_x - current_x) + abs(target_y - current_y)
        return distance

    def export_results_to_csv(self, results):
        with open("solver_results.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Execution Time (s)", "Moves", "Status"])
            writer.writerows(results)

    def is_solved(self, puzzle, n):
        # Check if puzzle matches the solved state
        return puzzle == list(range(1, n * n)) + [0]


    
    def show_win_message(self, n):
        # Draw gradient background
        self.draw_gradient_background()
        
        # Render congratulations text
        win_text = self.font_large.render("Bravo!", True, self.HIGHLIGHT_COLOR)
        subtitle = self.font_medium.render(f"{n}x{n} Puzzle Solved!", True, self.ACCENT_COLOR)
        
        # Position text in the center
        win_text_rect = win_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        subtitle_rect = subtitle.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(win_text, win_text_rect)
        self.screen.blit(subtitle, subtitle_rect)
        pygame.display.flip()
        
        # Wait for 3 seconds
        pygame.time.wait(3000)

    def run(self):
        # Game selection and initialization
        buttons = self.draw_menu()
        n, k = 0, 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            n = button["size"]
                            running = False
                            break
                

        # Input for move limit
        self.draw_gradient_background()
        description_text = self.font_small.render("Enter number of moves before tile exchange:", True, self.BLACK)
        description_rect = description_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(description_text, description_rect)

       

        input_box = pygame.Rect(self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 + 50, 300, 50)
        user_input = ""
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        k = int(user_input) if user_input.isdigit() else 0
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit() and len(user_input) < 3:
                        user_input += event.unicode
            self.screen.fill(self.WHITE)

            # Descriptive text
            description_text = self.font_small.render("veuillez entre le nombre de k:", True, self.ACCENT_COLOR)
            description_rect = description_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 80))
            self.screen.blit(description_text, description_rect)

            self.draw_input_field(input_box, user_input)
            pygame.display.flip()

        # Puzzle generation and game loop
        puzzle = self.generate_puzzle(n)
        blank_pos = divmod(puzzle.index(0), n)
        remaining_moves = k
        results = []
        selected_tiles = []
        game_paused = False

        running = True
        while running:
            selection_text = self.font_small.render("selectionne 2 tuiles pour echanger leur place", True, self.BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


                if self.is_solved(puzzle, n):
                # Export results before showing win message
                    self.export_results_to_csv(results)
                    
                    # Show win message
                    self.show_win_message(n)
                    
                    # Return to main menu
                    return self.run()

                # Tile movement logic
                if event.type == pygame.KEYDOWN and remaining_moves > 0 and not game_paused:
                    if event.key == pygame.K_UP and blank_pos[0] < n - 1:
                        blank_pos = self.move_tile(puzzle, n, (blank_pos[0] + 1, blank_pos[1]), blank_pos)
                        remaining_moves -= 1
                    elif event.key == pygame.K_DOWN and blank_pos[0] > 0:
                        blank_pos = self.move_tile(puzzle, n, (blank_pos[0] - 1, blank_pos[1]), blank_pos)
                        remaining_moves -= 1
                    elif event.key == pygame.K_LEFT and blank_pos[1] < n - 1:
                        blank_pos = self.move_tile(puzzle, n, (blank_pos[0], blank_pos[1] + 1), blank_pos)
                        remaining_moves -= 1
                    elif event.key == pygame.K_RIGHT and blank_pos[1] > 0:
                        blank_pos = self.move_tile(puzzle, n, (blank_pos[0], blank_pos[1] - 1), blank_pos)
                        remaining_moves -= 1

                # Pause and solve mechanics
                if remaining_moves == 0 and not game_paused and k > 0:
                    game_paused = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        game_paused = False
                        selected_tiles = []
                        remaining_moves = k
                        path, moves, execution_time, status = self.a_star_solver(puzzle, n)
                        if path:
                            for state in path:
                                self.draw_puzzle(list(state), n)
                                pygame.time.delay(300)
                            puzzle = list(path[-1])
                        results.append([execution_time, moves, status])

                # Tile swapping when paused
                if event.type == pygame.MOUSEBUTTONDOWN and game_paused:
                    x, y = event.pos
                    row = (y - self.MARGIN) // self.TILE_SIZE
                    col = (x - self.MARGIN) // self.TILE_SIZE

                    if 0 <= row < n and 0 <= col < n:
                        tile_pos = (row, col)
                        if puzzle[row * n + col] != 0:
                            selected_tiles.append(tile_pos)

                        if len(selected_tiles) == 2:
                            i1, j1 = selected_tiles[0]
                            i2, j2 = selected_tiles[1]
                            puzzle[i1 * n + j1], puzzle[i2 * n + j2] = puzzle[i2 * n + j2], puzzle[i1 * n + j1]
                            selected_tiles = []
                            remaining_moves = k
                            game_paused = False

            self.draw_puzzle(puzzle, n, remaining_moves)

            if game_paused:
                selection_text = self.font_small.render("selectionne 2 tuiles pour echanger leur place", True, self.BLACK)
                selection_text_rect = selection_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 30))
                self.screen.blit(selection_text, selection_text_rect)

            pygame.display.flip()

        # Export results
        self.export_results_to_csv(results)
        pygame.quit()

def main():
    game = PuzzleGame()
    game.run()

if __name__ == "__main__":
    main()