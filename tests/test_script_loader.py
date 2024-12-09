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
