import sys
from pathlib import Path

from config import Config
from script.loader import load_script


def main():
    try:
        script_path = Path(sys.argv.pop())
    except IndexError:
        print("Please provide a script as last command-line argument!")
        sys.exit(1)

    config = Config()

    script_class = load_script(script_path)
    if script_class is None:
        print("Cannot load script!")
        sys.exit(1)

    script = script_class(config)
    script.run()


if __name__ == "__main__":
    main()
