# Copyright (c) 2025 Daniel Stolpmann <dstolpmann@tegtmeier-inkubator.de>
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

import string
import time

from input_emulation.keyboard import Keyboard


def type_key(keyboard: Keyboard, key: str) -> None:
    setattr(keyboard, key, True)
    keyboard.update()

    time.sleep(0.01)

    setattr(keyboard, key, False)
    keyboard.update()

    time.sleep(0.01)


def main() -> None:
    keyboard = Keyboard()

    time.sleep(3)

    # Letters
    for letter in string.ascii_lowercase:
        type_key(keyboard, f"key_{letter}")

    # Numbers
    for number in range(10):
        type_key(keyboard, f"num_{number}")

    # Numbers (numpad)
    for number in range(10):
        type_key(keyboard, f"numpad_{number}")

    # Special characters
    for key in [
        "numpad_decimal",
        "numpad_divide",
        "numpad_multiply",
        "numpad_subtract",
        "numpad_add",
        "numpad_enter",
        "backtick",
        "minus",
        "equals",
        "backslash",
        "left_bracket",
        "right_bracket",
        "semicolon",
        "apostrophe",
        "comma",
        "dot",
        "slash",
    ]:
        type_key(keyboard, key)


if __name__ == "__main__":
    main()
