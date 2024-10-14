from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# ... (keep all the previous functions: check_winner, is_board_full, get_empty_cells, find_winning_move, computer_move)
def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def find_winning_move(board, player):
    for row, col in get_empty_cells(board):
        board[row][col] = player
        if check_winner(board, player):
            board[row][col] = " "
            return row, col
        board[row][col] = " "
    return None

def computer_move(board, computer_player, human_player):
    winning_move = find_winning_move(board, computer_player)
    if winning_move:
        return winning_move

    blocking_move = find_winning_move(board, human_player)
    if blocking_move:
        return blocking_move

    return random.choice(get_empty_cells(board))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    board = data['board']
    row = data['row']
    col = data['col']

    # Human move
    if board[row][col] != " ":
        return jsonify({"error": "Invalid move"}), 400

    board[row][col] = "X"

    if check_winner(board, "X"):
        return jsonify({"board": board, "game_over": True, "winner": "human"})

    if is_board_full(board):
        return jsonify({"board": board, "game_over": True, "winner": "tie"})

    # Computer move
    comp_row, comp_col = computer_move(board, "O", "X")
    board[comp_row][comp_col] = "O"

    if check_winner(board, "O"):
        return jsonify({"board": board, "game_over": True, "winner": "computer"})

    if is_board_full(board):
        return jsonify({"board": board, "game_over": True, "winner": "tie"})

    return jsonify({"board": board, "game_over": False})

if __name__ == '__main__':
    app.run(debug=True)