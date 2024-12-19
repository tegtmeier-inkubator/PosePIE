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

from pathlib import Path

from script.base import ScriptBase
from script.loader import load_script

ASSETS_PATH = Path(__file__).parent / "assets"


class TestLoadScript:
    def test_valid(self) -> None:
        script_class = load_script(ASSETS_PATH / "testscript.py")

        assert script_class is not None
        assert issubclass(script_class, ScriptBase)

    def test_invalid_not_derived(self) -> None:
        script_class = load_script(ASSETS_PATH / "testscript_invalid.py")

        assert script_class is None

    def test_invalid_not_existing(self) -> None:
        script_class = load_script(ASSETS_PATH / "testscript_not_existing.py")

        assert script_class is None

    def test_invalid_folder(self) -> None:
        script_class = load_script(ASSETS_PATH)

        assert script_class is None
