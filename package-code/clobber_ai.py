import argparse
import sys
from game import Pawn, Clobber
from clobber_state import ClobberState, find_best_move
from heuristics import HEURISTIC_MAP_EXTENDED


def main():
    parser = argparse.ArgumentParser(description='Clobber AI')
    parser.add_argument('--m', type=int, default=5, help='Number of rows in the board')
    parser.add_argument('--n', type=int, default=6, help='Number of columns in the board')

    parser.add_argument('--depth', type=int, help='Depth limit for both players (basic mode)')
    parser.add_argument('--heuristic', type=str, help='Heuristic for both players (basic mode)')
    parser.add_argument('--alpha_beta', action='store_true', help='Use alpha-beta pruning')

    parser.add_argument('--black_heuristic', type=str, help='Heuristic for black (extended mode)')
    parser.add_argument('--black_depth', type=int, help='Depth for black (extended mode)')
    parser.add_argument('--white_heuristic', type=str, help='Heuristic for white (extended mode)')
    parser.add_argument('--white_depth', type=int, help='Depth for white (extended mode)')

    args = parser.parse_args()

    m = args.m
    n = args.n
    clobber = Clobber(n=n, m=m)
    board = clobber.board
    state = ClobberState(board, Pawn.BLACK)
    round_count = 0
    total_nodes = 0
    total_time = 0.0

    if args.black_heuristic or args.white_heuristic:
        # extended configuration
        if not all([args.black_heuristic, args.white_heuristic,
                    args.black_depth is not None, args.white_depth is not None]):
            print(
                "Extended mode requires all parameters: --black_heuristic, --black_depth, --white_heuristic, --white_depth",
                file=sys.stderr)
            sys.exit(1)

        black_heuristic = HEURISTIC_MAP_EXTENDED.get(args.black_heuristic)
        white_heuristic = HEURISTIC_MAP_EXTENDED.get(args.white_heuristic)
        if black_heuristic is None or white_heuristic is None:
            print(f"Invalid heuristic. Available: {list(HEURISTIC_MAP_EXTENDED.keys())}", file=sys.stderr)
            sys.exit(1)

        black_depth = args.black_depth
        white_depth = args.white_depth
    else:
        # basic configuration
        if args.depth is None or args.heuristic is None:
            print("Basic mode requires --depth and --heuristic", file=sys.stderr)
            sys.exit(1)

        heuristic = HEURISTIC_MAP_EXTENDED.get(args.heuristic)
        if heuristic is None:
            print(f"Invalid heuristic. Available: {list(HEURISTIC_MAP_EXTENDED.keys())}", file=sys.stderr)
            sys.exit(1)

        black_heuristic = white_heuristic = heuristic
        black_depth = white_depth = args.depth

    use_alpha_beta = args.alpha_beta

    # MAIN LOOP
    stats = {'nodes': 0}
    while not state.is_terminal():
        current_player = state.current_player
        if current_player == Pawn.BLACK:
            depth = black_depth
            heuristic_func = black_heuristic
            player_name = "BLACK"
        else:
            depth = white_depth
            heuristic_func = white_heuristic
            player_name = "WHITE"

        move, value, nodes, elapsed = find_best_move(
            state, depth, current_player, heuristic_func, use_alpha_beta, stats
        )

        if move is None:
            print(f"{player_name} has no valid moves!", file=sys.stderr)
            break

        print(
            f"Round {round_count + 1}, {player_name} move: {move}, value: {value:.2f}, nodes: {nodes}, time: {elapsed:.4f}s",
            file=sys.stderr)
        state = state.make_move(move)
        round_count += 1
        total_nodes += nodes
        total_time += elapsed

    # end result
    print("Final board:")
    Clobber.print_board(state.board)

    winner = "NONE"
    if state.is_terminal():
        winner = "BLACK" if state.current_player == Pawn.WHITE else "WHITE"
    print(f"\nRounds: {round_count}, Winner: {winner}")
    print(f"Total nodes: {total_nodes}, Total time: {total_time:.4f}s", file=sys.stderr)


if __name__ == '__main__':
    main()
