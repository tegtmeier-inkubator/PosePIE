import sys
from pathlib import Path

from script.loader import load


def main():
    try:
        game_script_path = Path(sys.argv[1])
    except IndexError:
        print("Please provide a game script as command-line argument!")
        sys.exit(1)

    game_script_class = load(game_script_path)
    if game_script_class is None:
        print("Cannot load game script!")
        sys.exit(1)

    game_script = game_script_class()
    game_script.run()


if __name__ == "__main__":
    main()
