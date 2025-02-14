class Noeud:
    # Définir les lignes gagnantes comme une constante de classe
    LIGNES_GAGNANTES = [
        0b111000000,  # Ligne 1
        0b000111000,  # Ligne 2
        0b000000111,  # Ligne 3
        0b100100100,  # Colonne 1
        0b010010010,  # Colonne 2
        0b001001001,  # Colonne 3
        0b100010001,  # Diagonale principale
        0b001010100   # Diagonale secondaire
    ]

    def __init__(self, white=0, black=0, joueur_actuel="B"):
        """
        Initialise un état du jeu Fanorona Telo avec des bitboards.
        """
        self.white = white & 0b111111111  # S'assurer que seuls les 9 bits sont utilisés
        self.black = black & 0b111111111
        self.empty = ~(white | black) & 0b111111111
        self.joueur_actuel = joueur_actuel
        
        # Conversion du plateau en liste pour faciliter la gestion
        self.board = ['.'] * 9
        for i in range(9):
            if self.white & (1 << i):
                self.board[i] = 'B'
            elif self.black & (1 <<i):
                self.board[i] = 'N'
                
        # Table de connexion - pour chaque position, liste des positions connectées
        self.connected = [
            [1, 3, 4],       # 0
            [0, 2, 3, 4, 5], # 1
            [1, 4, 5],       # 2
            [0, 1, 4, 6, 7], # 3
            [0, 1, 2, 3, 5, 6, 7, 8], # 4 (centre)
            [1, 2, 4, 7, 8], # 5
            [3, 4, 7],       # 6
            [3, 4, 5, 6, 8], # 7
            [4, 5, 7]        # 8
        ]

    def get_successors(self):
        """
        Génère tous les successeurs possibles de l'état actuel.
        """
        successors = []
        pieces = self.white if self.joueur_actuel == "B" else self.black
        
        for pos in range(9):
            if pieces & (1 << pos):  # Si la pièce appartient au joueur actuel
                for target in self.connected[pos]:
                    if self.empty & (1 << target):  # Case cible vide
                        new_white = self.white
                        new_black = self.black
                        
                        if self.joueur_actuel == "B":
                            # Retirer la pièce de sa position actuelle
                            new_white &= ~(1 << pos)
                            # Placer la pièce à la nouvelle position
                            new_white |= (1 << target)
                        else:
                            new_black &= ~(1 << pos)
                            new_black |= (1 <<target)
                        
                        # Créer un nouvel état
                        new_node = Noeud(new_white, new_black, "N" if self.joueur_actuel == "B" else "B")
                        successors.append(new_node)
        
        return successors

    def is_winner(self, joueur):
        """
        Vérifie si un joueur a gagné dans l'état actuel.
        """
        pieces = self.white if joueur == "B" else self.black
        
        for ligne in self.LIGNES_GAGNANTES:
            if (pieces & ligne) == ligne:
                return True
                
        return False

    def evaluate(self):
        """
        Évalue l'état actuel du plateau.
        """
        # Vérifier si l'un des joueurs a gagné
        if self.is_winner("B"):
            return 1000
        elif self.is_winner("N"):
            return -1000
        
        # Compter le nombre de pièces pour chaque joueur dans des positions stratégiques
        score = 0
        
        # Valeurs positionnelles (centre et coins sont plus importants)
        position_values = [
            3, 1, 3,  # Première ligne
            1, 4, 1,  # Deuxième ligne
            3, 1, 3   # Troisième ligne
        ]
        
        # Évaluer pour les blancs (positif)
        for i in range(9):
            if self.white & (1 << i):
                score += position_values[i]
        
        # Évaluer pour les noirs (négatif)
        for i in range(9):
            if self.black & (1 << i):
                score -= position_values[i]
        
        # Compter combien de lignes potentielles chaque joueur peut former
        for ligne in self.LIGNES_GAGNANTES:
            white_pieces = bin(self.white & ligne).count('1')
            black_pieces = bin(self.black & ligne).count('1')
            
            # Si la ligne contient uniquement des pièces blanches
            if white_pieces > 0 and black_pieces == 0:
                score += white_pieces
            
            # Si la ligne contient uniquement des pièces noires
            if black_pieces > 0 and white_pieces == 0:
                score -= black_pieces
        
        return score

    def minimax(self, depth, maximizing_player):
        """
        Algorithme Minimax classique.
        """
        # Conditions de terminaison
        if depth == 0:
            return self.evaluate()
        
        if self.is_winner("B"):
            return 1000
        
        if self.is_winner("N"):
            return -1000
        
        successors = self.get_successors()
        if not successors:
            return self.evaluate()
        
        if maximizing_player:
            max_eval = float('-inf')
            for successor in successors:
                eval = successor.minimax(depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for successor in successors:
                eval = successor.minimax(depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        """
        Algorithme Alpha-Beta Pruning.
        """
        # Conditions de terminaison
        if depth == 0:
            return self.evaluate()
        
        if self.is_winner("B"):
            return 1000
        
        if self.is_winner("N"):
            return -1000
        
        successors = self.get_successors()
        if not successors:
            return self.evaluate()
        
        if maximizing_player:
            max_eval = float('-inf')
            for successor in successors:
                eval = successor.alpha_beta(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for successor in successors:
                eval = successor.alpha_beta(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move_minimax(self, depth):
        """
        Trouve le meilleur coup possible pour le joueur actuel avec Minimax.
        """
        successors = self.get_successors()
        if not successors:
            return None
        
        best_move = None
        best_value = float('-inf') if self.joueur_actuel == "B" else float('inf')
        
        for successor in successors:
            value = successor.minimax(depth - 1, self.joueur_actuel != "B")
            
            if (self.joueur_actuel == "B" and value > best_value) or \
               (self.joueur_actuel == "N" and value < best_value):
                best_value = value
                best_move = successor
        
        return best_move

    def find_best_move_alpha_beta(self, depth):
        """
        Trouve le meilleur coup possible pour le joueur actuel avec Alpha-Beta Pruning.
        """
        successors = self.get_successors()
        if not successors:
            return None
        
        best_move = None
        best_value = float('-inf') if self.joueur_actuel == "B" else float('inf')
        alpha, beta = float('-inf'), float('inf')
        
        for successor in successors:
            value = successor.alpha_beta(depth - 1, alpha, beta, self.joueur_actuel != "B")
            
            if (self.joueur_actuel == "B" and value > best_value) or \
               (self.joueur_actuel == "N" and value < best_value):
                best_value = value
                best_move = successor
            
            if self.joueur_actuel == "B":
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)
        
        return best_move

    def print_board(self):
        """
        Affiche l'état actuel du plateau.
        """
        print(f"{self.board[0]} {self.board[1]} {self.board[2]}")
        print(f"{self.board[3]} {self.board[4]} {self.board[5]}")
        print(f"{self.board[6]} {self.board[7]} {self.board[8]}")
        print(f"Joueur actuel: {self.joueur_actuel}")
        print(f"Blancs: {bin(self.white)}, Noirs: {bin(self.black)}")


def create_bitboard_from_string(board_str):
    """
    Crée un bitboard à partir d'une représentation chaîne de caractères.
    """
    white = 0
    black = 0
    
    # Remplacer les espaces et les retours à la ligne
    board_str = board_str.replace("\n", "").replace(" ", "")
    
    for i, c in enumerate(board_str):
        if c == 'B':
            white |= (1 <<i)
        elif c == 'N':
            black |= (1 <<i)
    
    return white, black


if __name__ == "__main__":
    # Créer un état initial à partir d'une représentation lisible
    board_str = """
    B N .
    . N .
    B N B
    """
    white, black = create_bitboard_from_string(board_str)
    noeud_initial = Noeud(white, black, "B")
    
    print("État initial:")
    noeud_initial.print_board()

    print("\n=== Test de get_successors() ===")
    successors = noeud_initial.get_successors()
    print(f"Nombre de successeurs : {len(successors)}")
    for i, successor in enumerate(successors):
        print(f"Successeur {i + 1}:")
        successor.print_board()
        print()

    print("=== Test de is_winner() ===")
    test_cases = [
        # Blancs gagnent (ligne horizontale)
        Noeud(*create_bitboard_from_string("B B B\n. . .\nN N N"), "N"),
        # Noirs gagnent (ligne horizontale)
        Noeud(*create_bitboard_from_string("N N N\n. . .\nB B B"), "B"),
        # État non terminal
        Noeud(*create_bitboard_from_string("B N .\n. N .\nB N B"), "B")
    ]

    for i, test_case in enumerate(test_cases):
        print(f"Test case {i + 1}:")
        test_case.print_board()
        if test_case.is_winner("B"):
            print("Les blancs ont gagné !")
        elif test_case.is_winner("N"):
            print("Les noirs ont gagné !")
        else:
            print("Aucun gagnant.")
        print(f"Evaluation: {test_case.evaluate()}")
        print()

    print("=== Recherche du meilleur coup avec Minimax ===")
    depth = 6 # Augmenter la profondeur pour des meilleurs résultats
    best_move_minimax = noeud_initial.find_best_move_minimax(depth)

    if best_move_minimax:
        print("Meilleur coup trouvé avec Minimax :")
        best_move_minimax.print_board()
    else:
        print("Aucun coup possible avec Minimax.")

    print("\n=== Recherche du meilleur coup avec Alpha-Beta ===")
    best_move_alpha_beta = noeud_initial.find_best_move_alpha_beta(depth)

    if best_move_alpha_beta:
        print("Meilleur coup trouvé avec Alpha-Beta :")
        best_move_alpha_beta.print_board()
    else:
        print("Aucun coup possible avec Alpha-Beta.")