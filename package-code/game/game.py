from enum import Enum

from .game_exceptions import *

from typing import List

class Pawn(Enum):
    WHITE = 'W'
    BLACK = 'B'
    EMPTY = '_'
    def __str__(self):
        return self.value

class GameStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    ENDED = 2

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

Board = List[List[Pawn]]

class Clobber:
    def __init__(self, n=5, m=6):
        self._n = n
        self._m = m
        pawn = Pawn.WHITE if m % 2 == 0 else Pawn.BLACK
        self._board = [[] for _ in range(m)]
        for row in self._board:
            for _ in range(n):
                row.append(pawn)
                pawn = self.other_player(pawn)
        self._current_player = Pawn.WHITE
        self._game_status = GameStatus.NOT_STARTED
        self._rounds_nb = 0

    @property
    def board(self):
        return self._board

    @property
    def game_status(self):
        return self._game_status

    @property
    def current_player(self):
        return self._current_player

    @property
    def round_nb(self):
        return self._rounds_nb

    def winner(self):
        if self.game_status != GameStatus.ENDED:
            return None
        return self.other_player(self.current_player)

    @staticmethod
    def other_player(player):
        if player == Pawn.WHITE:
            return Pawn.BLACK
        elif player == Pawn.BLACK:
            return Pawn.WHITE
        else:
            return None

    @staticmethod
    def validate_move(board, i, j, player):
        m = len(board)
        n = len(board[0]) if m > 0 else 0
        if i < 0 or i >= m or j < 0 or j >= n:
            return False
        if board[i][j] != Clobber.other_player(player):
            return False
        return True

    @staticmethod
    def can_clobber(board, i, j):
        player = board[i][j]
        neighbor_positions = [
            (i - 1, j),
            (i + 1, j),
            (i, j - 1),
            (i, j + 1)
        ]
        for ni, nj in neighbor_positions:
            if Clobber.validate_move(board, ni, nj, player):
                return True
        return False

    @staticmethod
    def game_ended(board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                field = board[i][j]
                if field in (Pawn.BLACK, Pawn.WHITE):
                    if Clobber.can_clobber(board, i, j):
                        return False
        return True

    @staticmethod
    def neighbor_moves(i, j):
        return [
            (i-1, j),
            (i+1, j),
            (i, j-1),
            (i, j+1)
        ]

    def move(self, i, j, direction):
        chosen_pawn = self.board[i][j]
        if chosen_pawn != self._current_player:
            raise WrongTurnException
        match direction:
            case Direction.UP:
                move_i = -1
                move_j = 0
            case Direction.DOWN:
                move_i = 1
                move_j = 0
            case Direction.RIGHT:
                move_i = 0
                move_j = 1
            case Direction.LEFT:
                move_i = 0
                move_j = -1
            case _:
                raise WrongDirectionException
        next_i = i+move_i
        next_j = j+move_j
        if not self.validate_move(self.board, next_i, next_j, self._current_player):
            raise InvalidMoveException

        self.board[i][j] = Pawn.EMPTY
        self.board[next_i][next_j] = self._current_player
        self._current_player = self.other_player(self.current_player)

        self._rounds_nb += 1
        self._game_status = GameStatus.IN_PROGRESS
        if self.game_ended(self.board):
            self._game_status = GameStatus.ENDED

    def print(self, field_names=False):
        self.print_board(self.board, self._n, self._m, field_names)

    @staticmethod
    def print_board(board, field_names=False):
        n = len(board[0])
        m = len(board)
        if field_names:
            print(end='    ')
            print('  '.join((chr(letter) for letter in range(ord('A'), ord('A')+n))))
            print(end='    ')
            print('  '.join(('_' for _ in range(n))))
        for i in range(len(board)):
            row = board[i]
            if field_names:
                print(f'{m-i}|', end='  ')
            print('  '.join((str(v) for v in row)))
