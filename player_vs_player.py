from game import *

GAME_SIZE = (5, 6)

def main():
    clobber = Clobber(*GAME_SIZE)
    while clobber.game_status != GameStatus.ENDED:
        clobber.print(field_names=True)
        move = None
        if clobber.current_player == Pawn.WHITE:
            print("White player move eg. [A1 B2] ... ", end='')
        else:
            print("Black player move eg. [A1 B2] ... ", end='')
        while True:
            try:
                move = parse_move(input())
                break
            except ValueError as error:
                print(error)
                continue
        clobber.move(*move)
    print("Game has ended")
    print("Winner: ", "WHITE" if clobber.winner() == Pawn.WHITE else "BLACK")

def parse_move(move: str):
    move_split = move.split()
    parsed_move = []
    try:
        for i in range(len(move_split)):
            mov_j_chr, mov_i_rev = move_split[i][0], move_split[i][1:]
            mov_i = GAME_SIZE[1] - (int(mov_i_rev))
            mov_j = ord(mov_j_chr) - ord('A')
            parsed_move.append((mov_i, mov_j))
    except:
        raise ValueError(f'Invalid input: {move}')
    direction = (parsed_move[1][0]-parsed_move[0][0], parsed_move[1][1] - parsed_move[0][1])
    match direction:
        case (1, 0):
            direction_ = Direction.DOWN
        case (-1, 0):
            direction_ = Direction.UP
        case (0, 1):
            direction_ = Direction.RIGHT
        case (0, -1):
            direction_ = Direction.LEFT
        case _:
            raise ValueError(f'Invalid input: {move}')
    return *parsed_move[0], direction_

if __name__ == '__main__':
    main()
