from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

HUMAN = "X"
AI = "O"

board = [""] * 9
difficulty = "easy"


# ---------------- GAME LOGIC ---------------- #
def check_winner(b):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    for a, b1, c in wins:
        if b[a] and b[a] == b[b1] == b[c]:
            return b[a]
    if "" not in b:
        return "Draw"
    return None


def available_moves(b):
    return [i for i, cell in enumerate(b) if cell == ""]


# ---------------- AI LOGIC ---------------- #
def easy_ai_move():
    return available_moves(board)[0]


def medium_ai_move():
    import random

    if random.choice([True, False]):
        return easy_ai_move()
    return hard_ai_move()


def minimax(b, is_max):
    result = check_winner(b)
    if result == AI:
        return 1
    if result == HUMAN:
        return -1
    if result == "Draw":
        return 0

    scores = []
    for move in available_moves(b):
        b[move] = AI if is_max else HUMAN
        score = minimax(b, not is_max)
        b[move] = ""
        scores.append(score)

    return max(scores) if is_max else min(scores)


def hard_ai_move():
    best_score = -100
    best_move = None

    for move in available_moves(board):
        board[move] = AI
        score = minimax(board, False)
        board[move] = ""
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def ai_move():
    if difficulty == "easy":
        move = easy_ai_move()
    elif difficulty == "medium":
        move = medium_ai_move()
    else:
        move = hard_ai_move()

    board[move] = AI


# ---------------- ROUTES ---------------- #
@app.route("/", methods=["GET", "POST"])
def index():
    global difficulty

    if request.method == "POST":
        if "difficulty" in request.form:
            difficulty = request.form["difficulty"]
            reset_game()
            return redirect(url_for("index"))

        move = int(request.form["move"])
        if board[move] == "":
            board[move] = HUMAN

            if not check_winner(board):
                ai_move()

    winner = check_winner(board)
    return render_template(
        "index.html",
        board=board,
        winner=winner,
        difficulty=difficulty,
    )


@app.route("/reset")
def reset():
    reset_game()
    return redirect(url_for("index"))


def reset_game():
    global board
    board = [""] * 9


if __name__ == "__main__":
    app.run(debug=True)
