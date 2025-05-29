from typing import List, Tuple, Dict, Optional
from game import Pawn, Direction, Clobber
import time


WINNING_VALUE = 1000


class ClobberState:
    def __init__(self, board: List[List[Pawn]], current_player: Pawn):
        self.board = board
        self.current_player = current_player
        self._m = len(board)
        self._n = len(board[0]) if self._m > 0 else 0

    def get_possible_moves(self) -> List[Tuple[int, int, Direction]]:
        moves = []
        for i in range(self._m):
            for j in range(self._n):
                if self.board[i][j] == self.current_player:
                    for direction in Direction:
                        di, dj = 0, 0
                        if direction == Direction.UP:
                            di = -1
                        elif direction == Direction.DOWN:
                            di = 1
                        elif direction == Direction.LEFT:
                            dj = -1
                        elif direction == Direction.RIGHT:
                            dj = 1
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self._m and 0 <= nj < self._n:
                            if self.board[ni][nj] == Clobber.other_player(self.current_player):
                                moves.append((i, j, direction))
        return moves

    def make_move(self, move: Tuple[int, int, Direction]) -> 'ClobberState':
        i, j, direction = move
        new_board = [row.copy() for row in self.board]

        di, dj = 0, 0
        if direction == Direction.UP:
            di = -1
        elif direction == Direction.DOWN:
            di = 1
        elif direction == Direction.LEFT:
            dj = -1
        elif direction == Direction.RIGHT:
            dj = 1

        ni, nj = i + di, j + dj
        new_board[i][j] = Pawn.EMPTY
        new_board[ni][nj] = self.current_player
        next_player = Clobber.other_player(self.current_player)
        return ClobberState(new_board, next_player)

    def is_terminal(self) -> bool:
        return len(self.get_possible_moves()) == 0

    def __str__(self):
        return "\n".join(" ".join(p.value for p in row) for row in self.board)


def utility(state: ClobberState, maximizing_player: Pawn) -> int:
    winner = Clobber.other_player(state.current_player)
    return WINNING_VALUE if winner == maximizing_player else -WINNING_VALUE


def minimax(state: ClobberState, depth: int, maximizing_player: Pawn, heuristic, stats: Dict) -> int:
    stats['nodes'] += 1
    if depth == 0 or state.is_terminal():
        if state.is_terminal():
            return utility(state, maximizing_player)
        return heuristic(state.board, maximizing_player)

    if state.current_player == maximizing_player:
        value = -float('inf')
        for move in state.get_possible_moves():
            new_state = state.make_move(move)
            value = max(value, minimax(new_state, depth - 1, maximizing_player, heuristic, stats))
        return value
    else:
        value = float('inf')
        for move in state.get_possible_moves():
            new_state = state.make_move(move)
            value = min(value, minimax(new_state, depth - 1, maximizing_player, heuristic, stats))
        return value


def alphabeta(state: ClobberState, depth: int, alpha: float, beta: float,
              maximizing_player: Pawn, heuristic, stats: Dict) -> int:
    stats['nodes'] += 1
    if depth == 0 or state.is_terminal():
        if state.is_terminal():
            return utility(state, maximizing_player)
        return heuristic(state.board, maximizing_player)

    if state.current_player == maximizing_player:
        value = -float('inf')
        for move in state.get_possible_moves():
            new_state = state.make_move(move)
            value = max(value, alphabeta(new_state, depth - 1, alpha, beta, maximizing_player, heuristic, stats))
            alpha = max(alpha, value)
            if value >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in state.get_possible_moves():
            new_state = state.make_move(move)
            value = min(value, alphabeta(new_state, depth - 1, alpha, beta, maximizing_player, heuristic, stats))
            beta = min(beta, value)
            if value <= alpha:
                break
        return value


def find_best_move(state: ClobberState, depth: int, player: Pawn, heuristic,
                   use_alpha_beta: bool, stats: Dict) -> Tuple[Optional[Tuple[int, int, Direction]], float, int, float]:
    moves = state.get_possible_moves()
    if not moves:
        return None, 0, 0, 0.0

    is_maximizing = (player == state.current_player)

    best_value = -float('inf') if is_maximizing else float('inf')
    best_move = None
    alpha = -float('inf')
    beta = float('inf')

    start_time = time.time()
    stats['nodes'] = 0

    for move in moves:
        new_state = state.make_move(move)

        if use_alpha_beta:
            value = alphabeta(
                new_state,
                depth - 1,
                alpha,
                beta,
                player,
                heuristic,
                stats
            )
        else:
            value = minimax(
                new_state,
                depth - 1,
                player,
                heuristic,
                stats
            )

        if is_maximizing:
            if value > best_value:
                best_value = value
                best_move = move
                alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
                beta = min(beta, best_value)

        # alpha-beta pruning
        if use_alpha_beta and alpha >= beta:
            break

    elapsed = time.time() - start_time
    return best_move, best_value, stats['nodes'], elapsed
