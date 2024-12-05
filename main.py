import sys
from pathlib import Path

from config import Config
from script.loader import load_script


def main():
    config = Config()

    script_class = load_script(Path(config.script))
    if script_class is None:
        print("Cannot load script!")
        sys.exit(1)

    script = script_class(config)
    script.run()


if __name__ == "__main__":
    main()
