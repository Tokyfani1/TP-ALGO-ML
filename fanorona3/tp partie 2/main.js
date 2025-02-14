// Game board representation
var tab = [
    [1, 1, 1],
    [0, 0, 0],
    [2, 2, 2]
];

// Track which pieces have been moved
var movedPieces = {
    player1: new Set(),
    player2: new Set()
};

var position = document.querySelectorAll(".position");
var turn = document.querySelector(".container");
var player = "p1";

// Add click event listeners to all positions
for(var elmt of position) {
    var temp,
        from;

    elmt.addEventListener("click", function(e) {
        if(!turn.classList.contains("moving")) {
            if(turn.classList.contains("player1")) {
                if(this.classList.contains("p1")) {
                    from = this.id;
                    this.classList.remove("p1");
                    this.classList.add("active-p1");
                    temp = this; 
                    turn.classList.add("moving");
                }
                else {
                    alert("Sélectionner un pion rouge!");
                }
            }
            else if(turn.classList.contains("player2")) {
                // AI move
                makeAIMove();
            }
        }
        else {
            if(turn.classList.contains("player1")) {
                if(this != temp) {
                    if(!this.classList.contains("p1") && !this.classList.contains("p2") && isValid(from, this.id)) {
                        moveTo(from, this.id);
                        movedPieces.player1.add(from); // Track moved piece
                        this.classList.add("p1");
                        temp.classList.remove("active-p1"); 
                        turn.classList.remove("moving");
                        turn.classList.remove("player1");
                        turn.classList.add("player2");
                        
                        if(gameOver(1) && movedPieces.player1.size >= 3){
                            alert("Rouge a gagné");
                            window.location.reload();
                        } else {
                            // Trigger AI move after player's move
                            setTimeout(makeAIMove, 500);
                        }
                    }
                    else {
                        alert("Sélectionner une zone vide adjacente!");
                    }
                }
                else {
                    this.classList.add("p1");
                    this.classList.remove("active-p1");
                    turn.classList.remove("moving");
                }
            }
        }
    }, false);
}

// Move validation function
function isValid(id1, id2) {
    var start = id1.split("-")[1];
    var end = id2.split("-")[1];

    // Center position
    if(start === "11")
        return true;

    // Corner positions
    if(start === "00") {
        if(end === "01" || end === "10" || end === "11")
            return true;
    }
    if(start === "02") {
        if(end === "01" || end === "12" || end === "11")
            return true;
    }
    if(start === "20") {
        if(end === "21" || end === "10" || end === "11")
            return true;
    }
    if(start === "22") {
        if(end === "21" || end === "12" || end === "11")
            return true;
    }

    // Edge positions
    if(start === "01") {
        if(end === "00" || end === "02" || end === "11")
            return true;
    }
    if(start === "10") {
        if(end === "00" || end === "20" || end === "11")
            return true;
    }
    if(start === "21") {
        if(end === "20" || end === "22" || end === "11")
            return true;
    }
    if(start === "12") {
        if(end === "02" || end === "22" || end === "11")
            return true;
    }

    return false;
}

// Move execution function
function moveTo(id1, id2) {
    var start = id1.split("-")[1].split("");
    var end = id2.split("-")[1].split("");

    if(tab[end[0]][end[1]] != 0) {
        console.log("Erreur!!");
        return;
    }

    tab[end[0]][end[1]] = tab[start[0]][start[1]];
    tab[start[0]][start[1]] = 0;
}

// AI Implementation
function makeAIMove() {
    let bestMove = findBestMove();
    if (bestMove) {
        let fromElement = document.getElementById(`c-${bestMove.from[0]}${bestMove.from[1]}`);
        let toElement = document.getElementById(`c-${bestMove.to[0]}${bestMove.to[1]}`);

        // Execute AI move
        fromElement.classList.remove("p2");
        moveTo(`c-${bestMove.from[0]}${bestMove.from[1]}`, `c-${bestMove.to[0]}${bestMove.to[1]}`);
        movedPieces.player2.add(`c-${bestMove.from[0]}${bestMove.from[1]}`); // Track AI moved piece
        toElement.classList.add("p2");

        if(gameOver(2) && movedPieces.player2.size >= 3){
            alert("Bleu (AI) a gagné");
            window.location.reload();
        }

        // Switch back to player 1
        turn.classList.remove("player2");
        turn.classList.add("player1");
    }
}

function findBestMove() {
    let bestScore = -Infinity;
    let bestMove = null;

    // Try all possible moves
    for(let i = 0; i < 3; i++) {
        for(let j = 0; j < 3; j++) {
            if(tab[i][j] === 2) { // AI piece
                // Try all possible destinations
                for(let x = 0; x < 3; x++) {
                    for(let y = 0; y < 3; y++) {
                        if(tab[x][y] === 0 && isValid(`c-${i}${j}`, `c-${x}${y}`)) {
                            // Make the move
                            let oldValue = tab[i][j];
                            tab[i][j] = 0;
                            tab[x][y] = 2;

                            let score = minimax(tab, 3, false);

                            // Undo the move
                            tab[i][j] = oldValue;
                            tab[x][y] = 0;

                            if(score > bestScore) {
                                bestScore = score;
                                bestMove = {
                                    from: [i, j],
                                    to: [x, y]
                                };
                            }
                        }
                    }
                }
            }
        }
    }
    return bestMove;
}
// Remplacer la fonction minimax par cette version qui utilise des copies locales pour le suivi des mouvements
function minimax(board, depth, isMaximizing, movedPieces1 = new Set([...movedPieces.player1]), movedPieces2 = new Set([...movedPieces.player2])) {
    // Terminal conditions - using local copies
    if(gameOver(2) && movedPieces2.size >= 3) return 100;
    if(gameOver(1) && movedPieces1.size >= 3) return -100;
    if(depth === 0) return evaluateBoard(movedPieces1, movedPieces2);

    if(isMaximizing) {
        let bestScore = -Infinity;
        for(let i = 0; i < 3; i++) {
            for(let j = 0; j < 3; j++) {
                if(board[i][j] === 2) {
                    for(let x = 0; x < 3; x++) {
                        for(let y = 0; y < 3; y++) {
                            if(board[x][y] === 0 && isValid(`c-${i}${j}`, `c-${x}${y}`)) {
                                // Make a local copy of the moved pieces set
                                let newMovedPieces2 = new Set([...movedPieces2]);
                                newMovedPieces2.add(`c-${i}${j}`);
                                
                                let oldValue = board[i][j];
                                board[i][j] = 0;
                                board[x][y] = 2;
                                
                                let score = minimax(board, depth - 1, false, movedPieces1, newMovedPieces2);
                                
                                board[i][j] = oldValue;
                                board[x][y] = 0;
                                bestScore = Math.max(score, bestScore);
                            }
                        }
                    }
                }
            }
        }
        return bestScore;
    } else {
        let bestScore = Infinity;
        for(let i = 0; i < 3; i++) {
            for(let j = 0; j <3; j++) {
                if(board[i][j] === 1) {
                    for(let x = 0; x < 3; x++) {
                        for(let y = 0; y < 3; y++) {
                            if(board[x][y] === 0 && isValid(`c-${i}${j}`, `c-${x}${y}`)) {
                                // Make a local copy of the moved pieces set
                                let newMovedPieces1 = new Set([...movedPieces1]);
                                newMovedPieces1.add(`c-${i}${j}`);
                                
                                let oldValue = board[i][j];
                                board[i][j] = 0;
                                board[x][y] = 1;
                                
                                let score = minimax(board, depth - 1, true, newMovedPieces1, movedPieces2);
                                
                                board[i][j] = oldValue;
                                board[x][y] = 0;
                                bestScore = Math.min(score, bestScore);
                            }
                        }
                    }
                }
            }
        }
        return bestScore;
    }
}


// Mise à jour de evaluateBoard pour accepter les ensembles locaux
function evaluateBoard(movedPieces1 = movedPieces.player1, movedPieces2 = movedPieces.player2) {
    let score = 0;
    
    // Only consider alignment if all pieces have been moved
    if (movedPieces2.size >= 3 && gameOver(2)) {
        score += 50;
    }
    
    if (movedPieces1.size >= 3 && gameOver(1)) {
        score -= 50;
    }
    
    // Encourage moving different pieces
    score += movedPieces2.size * 2;
    score -= movedPieces1.size * 2;
    
    // Evaluate positions
    for(let i = 0; i <3; i++) {
        for(let j = 0; j < 3; j++) {
            if(tab[i][j] === 2) score += 1; // AI piece
            if(tab[i][j] === 1) score -= 1; // Player piece
            // Bonus for center position
            if(i === 1 && j === 1) {
                if(tab[i][j] === 2) score += 3;
                if(tab[i][j] === 1) score -= 3;
            }
        }
    }
    
    return score;
}



// Ajout d'une fonction d'aide pour afficher un message si on détecte un alignement sans que tous les pions aient bougé
function checkAlignmentWithoutWin() {
    // Pour le joueur 1
    if(gameOver(1) && movedPieces.player1.size < 3) {
        alert("Les pions rouges sont alignés, mais tous les pions doivent bouger au moins une fois pour gagner!");
    }
    
    // Pour le joueur 2 (AI)
    if(gameOver(2) && movedPieces.player2.size < 3) {
        alert("Les pions bleus sont alignés, mais tous les pions doivent bouger au moins une fois pour gagner!");
    }
}



// Win condition checking functions
function isAlignedX(x) {
    var compt = 0;
    for(var i = 0; i < 3; i++) {
        for(var j = 0; j < 3; j++) {
            if(tab[i][j] == x) {
                compt++;
            }
        }
        if(compt == 3) {
            return true;
        }
        compt = 0;
    }
    return false;
}

function isAlignedY(x) {
    var compt = 0;
    for(var i = 0; i < 3; i++) {
        for(var j = 0; j < 3; j++) {
            if(tab[j][i] == x) {
                compt++;
            }
        }
        if(compt == 3) {
            return true;
        }
        compt = 0;
    }
    return false;
}

function isAlignedDiag(x) {
    if(x == tab[0][0] || x == tab[2][2] || x == tab[1][1])
        if(tab[1][1] == tab[0][0] && tab[1][1] == tab[2][2])
            return true;
    
    if(x == tab[0][2] || x == tab[2][0] || x == tab[1][1])
        if(tab[1][1] == tab[0][2] && tab[1][1] == tab[2][0])
            return true;

    return false;
}

function gameOver(x) {
    if(isAlignedX(x) || isAlignedY(x) || isAlignedDiag(x))
        return true;
    return false;
}

// Reset moved pieces tracking when the game starts/resets
window.onload = function() {
    movedPieces.player1.clear();
    movedPieces.player2.clear();
};