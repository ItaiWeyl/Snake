import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay


def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    # INIT OBJECTS
    game = SnakeGame(args.width, args.height, args.debug)
    gd.show_score(0)
    # DRAW BOARD
    walls = args.walls
    apples = args.apples
    rounds = args.rounds
    debug = args.debug
    game.first_turn(walls, apples)
    gd.show_score(game.score)
    game.draw_board(gd)
    # END OF ROUND 0
    game.end_round()
    gd.end_round()
    over = False
    while (rounds == -1 or game.round <= rounds) and (not game.is_game_over()):
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # UPDATE OBJECTS
        game.update_objects(walls, apples)
        # DRAW BOARD
        game.is_over()
        game.draw_board(gd)
        gd.show_score(game.score)
        # WAIT FOR NEXT ROUND:
        game.end_round()
        gd.end_round()


if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py")
