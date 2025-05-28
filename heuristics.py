from game import Clobber, Pawn, Board

from functools import lru_cache


def temp_heuristics(board: Board, maximizing_player: Pawn):
    from random import uniform
    return uniform(-1, 1)


def active_pawns_heuristics(board: Board, maximizing_player: Pawn):
    max_active_pawns_nb = 0
    min_active_pawns_nb = 0

    for i, row in enumerate(board):
        for j, pawn in enumerate(row):
            if pawn == Pawn.EMPTY:
                continue
            if Clobber.can_clobber(board, i, j):
                if pawn == maximizing_player:
                    max_active_pawns_nb += 1
                else:
                    min_active_pawns_nb += 1
    return max_active_pawns_nb - min_active_pawns_nb


def center_occupying_heuristics(board: Board, maximizing_player: Pawn):
    m = len(board)
    n = len(board[0])
    weight_grid = generate_weight_grid(n, m)

    max_player_score = 0
    min_player_score = 0

    for i, row in enumerate(board):
        for j, pawn in enumerate(row):
            w = weight_grid[i][j]
            if pawn == Pawn.EMPTY:
                continue
            elif pawn == maximizing_player:
                max_player_score += w
            else:
                min_player_score += w
    return max_player_score - min_player_score


@lru_cache
def generate_weight_grid(n, m):
    def calculate_weight(i, j, rows, cols):
        dist_i = min(i, rows - 1 - i)
        dist_j = min(j, cols - 1 - j)

        base = dist_i + dist_j
        bonus = min(dist_i, dist_j)

        return base + bonus

    return [[calculate_weight(i, j, rows=m, cols=n) for j in range(n)] for i in range(m)]


def pawns_accumulations_heuristics(board: Board, maximizing_player: Pawn):
    max_player_islands = 0
    min_player_islands = 0

    positions_checked = set()
    curr_i, curr_j = 0, 0
    while len(positions_checked) < len(board)*len(board[0]):
        if not (curr_i, curr_j) in positions_checked:
            pawn = board[curr_i][curr_j]
            if pawn == Pawn.EMPTY:
                positions_checked.add((curr_i, curr_j))
            else:
                lookup_pawns_island(curr_i, curr_j, board, positions_checked)
                if pawn == maximizing_player:
                    max_player_islands += 1
                else:
                    min_player_islands += 1
        curr_j = (curr_j+1) % len(board[0])
        if curr_j == 0:
            curr_i += 1
    return min_player_islands - max_player_islands


def lookup_pawns_island(i, j, board: Board, checked: set[tuple[int, int]]):
    if (i, j) in checked:
        return
    checked.add((i, j))
    pawn = board[i][j]
    for n_i, n_j in Clobber.neighbor_moves(i, j):
        if (0 <= n_i < len(board)) and (0 <= n_j < len(board[0])) and board[n_i][n_j] == pawn:
            lookup_pawns_island(n_i, n_j, board, checked)

