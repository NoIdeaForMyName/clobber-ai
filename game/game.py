from enum import Enum

from .game_exceptions import *


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


class Clobber:
    def __init__(self, n=5, m=6):
        self._n = n
        self._m = m
        pawn = Pawn.WHITE if m % 2 == 0 else Pawn.BLACK
        self._board = [[] for _ in range(m)]
        for row in self._board:
            for _ in range(n):
                row.append(pawn)
                pawn = self.__other_player(pawn)
        self._current_player = Pawn.WHITE
        self._game_status = GameStatus.NOT_STARTED
        self._rounds_nb = 0

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
        return self.__other_player(self.current_player)

    def __other_player(self, turn=None):
        if not turn:
            turn = self._current_player
        return Pawn.WHITE if turn == Pawn.BLACK else Pawn.BLACK

    def __validate_move(self, i, j, player):
        if i < 0 or i > self._m - 1 or j < 0 or j > self._n - 1:
            return False
        if self._board[i][j] != self.__other_player(player):
            return False
        return True

    def __can_clobber(self, i, j):
        player = self._board[i][j]
        neighbors = []
        neigbors_pos = [
            (i-1, j),
            (i+1, j),
            (i, j-1),
            (i, j+1)
        ]
        for n_i, n_j in neigbors_pos:
            if self.__validate_move(n_i, n_j, player):
                neighbors.append(self._board[n_i][n_j])
        for n in neighbors:
            if n == self.__other_player(player):
                return True
        return False

    def __game_ended(self):
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                field = self._board[i][j]
                if field == Pawn.WHITE:
                    if self.__can_clobber(i, j):
                        return False
        return True

    def move(self, i, j, direction):
        chosen_pawn = self._board[i][j]
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
        if not self.__validate_move(next_i, next_j, self._current_player):
            raise InvalidMoveException

        self._board[i][j] = Pawn.EMPTY
        self._board[next_i][next_j] = self._current_player
        self._current_player = self.__other_player()

        self._rounds_nb += 1
        self._game_status = GameStatus.IN_PROGRESS
        if self.__game_ended():
            self._game_status = GameStatus.ENDED

    def print(self, field_names=False):
        if field_names:
            print(end='    ')
            print('  '.join((chr(letter) for letter in range(ord('A'), ord('A')+self._n))))
            print(end='    ')
            print('  '.join(('_' for _ in range(self._n))))
        for i in range(len(self._board)):
            row = self._board[i]
            if field_names:
                print(f'{self._m-i}|', end='  ')
            print('  '.join((str(v) for v in row)))
