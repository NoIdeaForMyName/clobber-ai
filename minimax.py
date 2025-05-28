from game import *
from heuristics import active_pawns_heuristics, center_occupying_heuristics, pawns_accumulations_heuristics

import copy
import math


n = 5
m = 6

maximizing_player = Pawn.WHITE

depth = 3


def main():
    clobber = Clobber(n, m)
    curr_board = clobber.board
    player_turn = Pawn.WHITE
    game_ended = False
    result_board = None
    winner = None
    moves_nb = 0

    while not game_ended:
        curr_board, curr_score = minimax(
            board=curr_board,
            maximizing_player=maximizing_player,
            player_turn=player_turn,
            depth=depth,
            heuristic=pawns_accumulations_heuristics
        )
        if curr_score == -math.inf or curr_score == math.inf:
            result_board = curr_board
            winner = maximizing_player if curr_score == math.inf else Clobber.other_player(maximizing_player)
            game_ended = True
        moves_nb += 1
        player_turn = Clobber.other_player(player_turn)

    print("Simulation ended!\nResults:\n")
    print("Final board:")
    Clobber.print_board(result_board, n, m)
    print()
    print("Winner:", winner)
    print("Number of moves:", moves_nb)


def minimax(board: Board, maximizing_player: Pawn, player_turn: Pawn, depth: int, heuristic) -> tuple[Board, float]:
    best_move, best_score = None, -math.inf
    for new_board in generate_possible_moves(board, player=player_turn):
        _, curr_score = (
            minimax_inner(
                board=new_board,
                maximizing_player=maximizing_player,
                player_turn=Clobber.other_player(player_turn),
                depth=depth - 1,
                heuristic=heuristic
            )
        )
        if curr_score > best_score:
            best_move, best_score = new_board, curr_score
            if best_score == math.inf:
                break
    if Clobber.game_ended(best_move):
        score = math.inf if maximizing_player == player_turn else -math.inf
    else:
        score = heuristic(best_move, maximizing_player)
    return best_move, score


def minimax_inner(board: Board, maximizing_player: Pawn, player_turn: Pawn, depth: int, heuristic) -> tuple[Board, float]:
    if Clobber.game_ended(board):
        score = -math.inf if maximizing_player == player_turn else math.inf
        return copy.deepcopy(board), score
    if depth == 0:
        return copy.deepcopy(board), heuristic(board, maximizing_player)
    minimax_func = max if player_turn == maximizing_player else min
    return minimax_func(
        [
            minimax_inner(
                board=new_board,
                maximizing_player=maximizing_player,
                player_turn=Clobber.other_player(player_turn),
                depth=depth - 1,
                heuristic=heuristic
            )
            for new_board in generate_possible_moves(board, player=player_turn)
        ],
        key=lambda result: result[1]
    )


def generate_possible_moves(board: Board, player: Pawn) -> list[Board]:

    outcomes = []

    for i, row in enumerate(board):
        for j, pawn in enumerate(row):
            if pawn == player:
                for move_i, move_j in Clobber.neighbor_moves(i, j):
                    if Clobber.validate_move(board, move_i, move_j, player):
                        new_board = copy.deepcopy(board)
                        new_board[i][j] = Pawn.EMPTY
                        new_board[move_i][move_j] = player
                        outcomes.append(new_board)
    return outcomes


if __name__ == '__main__':
    main()
