# Copyright (c) 2024 Daniel Stolpmann <dstolpmann@tegtmeier-inkubator.de>
#
# This file is part of PosePIE.
#
# PosePIE is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# PosePIE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with PosePIE. If
# not, see <https://www.gnu.org/licenses/>.

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

    try:
        spec.loader.exec_module(module)
    except FileNotFoundError:
        return None

    script_class: type[ScriptBase] | None = None
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if module.__name__ != obj.__module__:
            continue

        if not issubclass(obj, ScriptBase):
            continue

        script_class = obj
        break

    return script_class
