from game import Clobber, Pawn, Board
from functools import lru_cache
from random import uniform


def random_heuristics(board: Board, maximizing_player: Pawn) -> float:
    return uniform(-1, 1)


def active_pawns_heuristics(board: Board, maximizing_player: Pawn) -> int:
    max_active = 0
    min_active = 0
    for i, row in enumerate(board):
        for j, pawn in enumerate(row):
            if pawn == Pawn.EMPTY:
                continue
            if Clobber.can_clobber(board, i, j):
                if pawn == maximizing_player:
                    max_active += 1
                else:
                    min_active += 1
    return max_active - min_active


def center_occupying_heuristics(board: Board, maximizing_player: Pawn) -> int:
    m = len(board)
    n = len(board[0])
    weights = generate_weight_grid(n, m)
    max_score = 0
    min_score = 0
    for i, row in enumerate(board):
        for j, pawn in enumerate(row):
            if pawn == Pawn.EMPTY:
                continue
            weight = weights[i][j]
            if pawn == maximizing_player:
                max_score += weight
            else:
                min_score += weight
    return max_score - min_score

@lru_cache
def generate_weight_grid(n: int, m: int) -> list[list[int]]:
    def calculate_weight(i, j, rows, cols):
        dist_i = min(i, rows - 1 - i)
        dist_j = min(j, cols - 1 - j)

        base = dist_i + dist_j
        bonus = min(dist_i, dist_j)

        return base + bonus

    return [[calculate_weight(i, j, rows=m, cols=n) for j in range(n)] for i in range(m)]


def pawns_accumulations_heuristics(board: Board, maximizing_player: Pawn) -> int:
    max_islands = 0
    min_islands = 0
    visited = set()
    for i, row in enumerate(board):
        for j, pawn in enumerate(row):
            if (i, j) in visited or pawn == Pawn.EMPTY:
                continue
            stack = [(i, j)]
            while stack:
                x, y = stack.pop()
                if (x, y) in visited:
                    continue
                visited.add((x, y))
                for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
                        if board[nx][ny] == pawn and (nx, ny) not in visited:
                            stack.append((nx, ny))
            if pawn == maximizing_player:
                max_islands += 1
            else:
                min_islands += 1
    return min_islands - max_islands


def first_center_then_aggressive(board: Board, player: Pawn) -> float:
    pawns_left_coeff = pawns_left_coefficient(board, player)
    if pawns_left_coeff >= 0.6:
        return center_occupying_heuristics(board, player)
    elif pawns_left_coeff >= 0.4:
        return active_pawns_heuristics(board, player) * 0.7 + center_occupying_heuristics(board, player) * 0.3
    else:
        return active_pawns_heuristics(board, player)

def group_then_fight(board: Board, player: Pawn) -> float:
    pawns_left_coeff = pawns_left_coefficient(board, player)
    if pawns_left_coeff >= 0.6:
        return pawns_accumulations_heuristics(board, player)
    elif pawns_left_coeff >= 0.4:
        return pawns_accumulations_heuristics(board, player) * 0.4 + active_pawns_heuristics(board, player) * 0.6
    else:
        return active_pawns_heuristics(board, player)

def take_middle_stay_in_group(board: Board, player: Pawn) -> float:
    pawns_left_coeff = pawns_left_coefficient(board, player)
    if pawns_left_coeff >= 0.6:
        return center_occupying_heuristics(board, player)
    elif pawns_left_coeff >= 0.4:
        return center_occupying_heuristics(board, player) * 0.5 + pawns_accumulations_heuristics(board, player) * 0.5
    else:
        return pawns_accumulations_heuristics(board, player)

def pawns_left_coefficient(board: Board, player: Pawn) -> float:
    initial_pawns = len(board) * len(board[0]) / 2
    count = 0
    for row in board:
        for pawn in row:
            if pawn == player:
                count += 1
    return count / initial_pawns


HEURISTIC_MAP = {
    'active': active_pawns_heuristics,
    'center': center_occupying_heuristics,
    'accumulation': pawns_accumulations_heuristics
}

HEURISTIC_MAP_EXTENDED = {
    'first_center_then_aggressive': first_center_then_aggressive,
    'group_then_fight': group_then_fight,
    'take_middle_stay_in_group': take_middle_stay_in_group,
    **HEURISTIC_MAP
}
