import importlib.util
import inspect
import sys
from pathlib import Path

from game_script_base import GameScriptBase


def load(file_path_py: Path) -> type[GameScriptBase] | None:
    module_name = file_path_py.stem

    spec = importlib.util.spec_from_file_location(module_name, file_path_py)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    game_script_class: type[GameScriptBase] | None = None
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if module.__name__ != obj.__module__:
            continue

        if not issubclass(obj, GameScriptBase):
            continue

        game_script_class = obj
        break

    return game_script_class
