from game import Clobber
from game.game import Pawn, Board

from time import sleep

import copy

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
            heuristic=temp_heuristics
        )
        if curr_score == -1 or curr_score == 1:
            result_board = curr_board
            winner = maximizing_player if curr_score == 1 else Clobber.other_player(maximizing_player)
            game_ended = True
        moves_nb += 1
        player_turn = Clobber.other_player(player_turn)

        # print("Player moved. State:")
        # Clobber.print_board(curr_board, n, m)
        # print("moves nb:", moves_nb)
        # sleep(1)

    print("Simulation ended!\nResults:\n")
    print("Final board:")
    Clobber.print_board(result_board, n, m)
    print()
    print("Winner:", winner)
    print("Number of moves:", moves_nb)



def temp_heuristics(board: Board, maximizing_player: Pawn, player_turn: Pawn):
    from random import uniform
    return uniform(-1, 1)


def minimax(board: Board, maximizing_player: Pawn, player_turn: Pawn, depth: int, heuristic) -> tuple[Board, float]:
    best_move, best_score = None, -1
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
    return best_move, best_score

def minimax_inner(board: Board, maximizing_player: Pawn, player_turn: Pawn, depth: int, heuristic) -> tuple[Board, float]:
    if Clobber.game_ended(board):
        score = -1 if maximizing_player == player_turn else 1
        return copy.deepcopy(board), score
    if depth == 0:
        return copy.deepcopy(board), heuristic(board, maximizing_player, player_turn)
    return max(
        [
            minimax(
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

    # return max(
    #     generate_possible_moves(board, player=Clobber.other_player(player_turn)),
    #     key=lambda result: result[1]
    # )


def generate_possible_moves(board: Board, player: Pawn) -> list[Board]:
    def all_moves(i, j):
        return [
            (i-1, j),
            (i+1, j),
            (i, j-1),
            (i, j+1)
        ]

    outcomes = []

    for i, row in enumerate(board):
        for j, pawn in enumerate(row):
            if pawn == player:
                for move_i, move_j in all_moves(i, j):
                    if Clobber.validate_move(board, move_i, move_j, player):
                        new_board = copy.deepcopy(board)
                        new_board[i][j] = Pawn.EMPTY
                        new_board[move_i][move_j] = player
                        outcomes.append(new_board)
    return outcomes


if __name__ == '__main__':
    main()
