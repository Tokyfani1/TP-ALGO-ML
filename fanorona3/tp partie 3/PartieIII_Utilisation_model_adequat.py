import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Définir la taille du plateau (3x3)
BOARD_SIZE = 3

# Fonction pour générer une configuration aléatoire du plateau
def generate_random_board():
    return np.random.choice([-1, 0, 1], size=(BOARD_SIZE, BOARD_SIZE))

# Fonction pour évaluer si une configuration est gagnante pour les blancs
def is_winning_position(board):
    white_count = np.sum(board == 1)
    black_count = np.sum(board == -1)
    return white_count >= 6 and white_count > black_count

# Fonction pour évaluer si une configuration est perdante pour les blancs
def is_losing_position(board):
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

# Créer un dataset avec les configurations et leurs labels
X = np.array(winning_boards + losing_boards).reshape(-1, BOARD_SIZE * BOARD_SIZE)  # Aplatir les plateaux
y = np.array([1] * 500 + [0] * 500)  # Labels : 1 pour gagnant, 0 pour perdant

# Diviser le dataset en ensembles d'entraînement (80%) et de test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner un modèle RandomForest pour prédire le score d'une position
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Évaluer le modèle sur l'ensemble de test
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Précision du modèle : {accuracy:.2f}")
print("\nRapport de classification :")
print(classification_report(y_test, y_pred))

# Fonction pour prédire le score d'une position donnée
def predict_position_score(board):
    # Aplatir le plateau en un vecteur
    board_flat = board.reshape(1, -1)
    # Prédire le score (1 pour gagnant, 0 pour perdant)
    return model.predict(board_flat)[0]

# Exemple d'utilisation
example_board = generate_random_board()
print("\nExemple de plateau :")
print(example_board)
score = predict_position_score(example_board)
if score == 1:
    print("Les blancs sont favorisés dans cette position.")
else:
    print("Les noirs sont favorisés dans cette position.")