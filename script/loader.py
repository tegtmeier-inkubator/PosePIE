import importlib.util
import inspect
import sys
from pathlib import Path

from script.base import ScriptBase


def load_script(file_path_py: Path) -> type[ScriptBase] | None:
    module_name = file_path_py.stem

    spec = importlib.util.spec_from_file_location(module_name, file_path_py)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    script_class: type[ScriptBase] | None = None
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if module.__name__ != obj.__module__:
            continue

        if not issubclass(obj, ScriptBase):
            continue

        script_class = obj
        break

    return script_class
