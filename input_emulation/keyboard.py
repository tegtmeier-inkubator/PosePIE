# Copyright (c) 2024, 2025 Daniel Stolpmann <dstolpmann@tegtmeier-inkubator.de>
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

from sys import platform

if platform == "linux":
    import uinput

    class Keyboard:
        def __init__(self) -> None:
            events = []

            self.arrow_up: bool = False
            self.arrow_down: bool = False
            self.arrow_left: bool = False
            self.arrow_right: bool = False
            events.extend(
                [
                    uinput.KEY_UP,
                    uinput.KEY_DOWN,
                    uinput.KEY_LEFT,
                    uinput.KEY_RIGHT,
                ]
            )

            self.enter: bool = False
            self.backspace: bool = False
            self.esc: bool = False
            self.space: bool = False
            self.ctrl_left: bool = False
            self.ctrl_right: bool = False
            self.alt_left: bool = False
            self.alt_right: bool = False
            self.shift_left: bool = False
            self.shift_right: bool = False
            self.meta_left: bool = False
            self.meta_right: bool = False
            self.menu: bool = False
            self.caps_lock: bool = False
            self.tab: bool = False
            events.extend(
                [
                    uinput.KEY_ENTER,
                    uinput.KEY_BACKSPACE,
                    uinput.KEY_ESC,
                    uinput.KEY_SPACE,
                    uinput.KEY_LEFTCTRL,
                    uinput.KEY_RIGHTCTRL,
                    uinput.KEY_LEFTALT,
                    uinput.KEY_RIGHTALT,
                    uinput.KEY_LEFTSHIFT,
                    uinput.KEY_RIGHTSHIFT,
                    uinput.KEY_LEFTMETA,
                    uinput.KEY_RIGHTMETA,
                    uinput.KEY_MENU,
                    uinput.KEY_CAPSLOCK,
                    uinput.KEY_TAB,
                ]
            )

            self.print_screen: bool = False
            self.scroll_lock: bool = False
            self.pause: bool = False
            self.insert: bool = False
            self.home: bool = False
            self.page_up: bool = False
            self.delete: bool = False
            self.end: bool = False
            self.page_down: bool = False
            events.extend(
                [
                    uinput.KEY_PRINT,
                    uinput.KEY_SCROLLLOCK,
                    uinput.KEY_PAUSE,
                    uinput.KEY_INSERT,
                    uinput.KEY_HOME,
                    uinput.KEY_PAGEUP,
                    uinput.KEY_DELETE,
                    uinput.KEY_END,
                    uinput.KEY_PAGEDOWN,
                ]
            )

            self.key_a: bool = False
            self.key_b: bool = False
            self.key_c: bool = False
            self.key_d: bool = False
            self.key_e: bool = False
            self.key_f: bool = False
            self.key_g: bool = False
            self.key_h: bool = False
            self.key_i: bool = False
            self.key_j: bool = False
            self.key_k: bool = False
            self.key_l: bool = False
            self.key_m: bool = False
            self.key_n: bool = False
            self.key_o: bool = False
            self.key_p: bool = False
            self.key_q: bool = False
            self.key_r: bool = False
            self.key_s: bool = False
            self.key_t: bool = False
            self.key_u: bool = False
            self.key_v: bool = False
            self.key_w: bool = False
            self.key_x: bool = False
            self.key_y: bool = False
            self.key_z: bool = False
            events.extend(
                [
                    uinput.KEY_A,
                    uinput.KEY_B,
                    uinput.KEY_C,
                    uinput.KEY_D,
                    uinput.KEY_E,
                    uinput.KEY_F,
                    uinput.KEY_G,
                    uinput.KEY_H,
                    uinput.KEY_I,
                    uinput.KEY_J,
                    uinput.KEY_K,
                    uinput.KEY_L,
                    uinput.KEY_M,
                    uinput.KEY_N,
                    uinput.KEY_O,
                    uinput.KEY_P,
                    uinput.KEY_Q,
                    uinput.KEY_R,
                    uinput.KEY_S,
                    uinput.KEY_T,
                    uinput.KEY_U,
                    uinput.KEY_V,
                    uinput.KEY_W,
                    uinput.KEY_X,
                    uinput.KEY_Y,
                    uinput.KEY_Z,
                ]
            )

            self.num_0: bool = False
            self.num_1: bool = False
            self.num_2: bool = False
            self.num_3: bool = False
            self.num_4: bool = False
            self.num_5: bool = False
            self.num_6: bool = False
            self.num_7: bool = False
            self.num_8: bool = False
            self.num_9: bool = False
            events.extend(
                [
                    uinput.KEY_0,
                    uinput.KEY_1,
                    uinput.KEY_2,
                    uinput.KEY_3,
                    uinput.KEY_4,
                    uinput.KEY_5,
                    uinput.KEY_6,
                    uinput.KEY_7,
                    uinput.KEY_8,
                    uinput.KEY_9,
                ]
            )

            self.backtick: bool = False
            self.minus: bool = False
            self.equals: bool = False
            self.backslash: bool = False
            self.left_bracket: bool = False
            self.right_bracket: bool = False
            self.semicolon: bool = False
            self.apostrophe: bool = False
            self.comma: bool = False
            self.dot: bool = False
            self.slash: bool = False
            events.extend(
                [
                    uinput.KEY_GRAVE,
                    uinput.KEY_MINUS,
                    uinput.KEY_EQUAL,
                    uinput.KEY_BACKSLASH,
                    uinput.KEY_LEFTBRACE,
                    uinput.KEY_RIGHTBRACE,
                    uinput.KEY_SEMICOLON,
                    uinput.KEY_APOSTROPHE,
                    uinput.KEY_COMMA,
                    uinput.KEY_DOT,
                    uinput.KEY_SLASH,
                ]
            )

            self.f1: bool = False
            self.f2: bool = False
            self.f3: bool = False
            self.f4: bool = False
            self.f5: bool = False
            self.f6: bool = False
            self.f7: bool = False
            self.f8: bool = False
            self.f9: bool = False
            self.f10: bool = False
            self.f11: bool = False
            self.f12: bool = False
            events.extend(
                [
                    uinput.KEY_F1,
                    uinput.KEY_F2,
                    uinput.KEY_F3,
                    uinput.KEY_F4,
                    uinput.KEY_F5,
                    uinput.KEY_F6,
                    uinput.KEY_F7,
                    uinput.KEY_F8,
                    uinput.KEY_F9,
                    uinput.KEY_F10,
                    uinput.KEY_F11,
                    uinput.KEY_F12,
                ]
            )

            self.numpad_lock: bool = False
            self.numpad_0: bool = False
            self.numpad_1: bool = False
            self.numpad_2: bool = False
            self.numpad_3: bool = False
            self.numpad_4: bool = False
            self.numpad_5: bool = False
            self.numpad_6: bool = False
            self.numpad_7: bool = False
            self.numpad_8: bool = False
            self.numpad_9: bool = False
            self.numpad_decimal: bool = False
            self.numpad_divide: bool = False
            self.numpad_multiply: bool = False
            self.numpad_subtract: bool = False
            self.numpad_add: bool = False
            self.numpad_enter: bool = False
            events.extend(
                [
                    uinput.KEY_NUMLOCK,
                    uinput.KEY_KP0,
                    uinput.KEY_KP1,
                    uinput.KEY_KP2,
                    uinput.KEY_KP3,
                    uinput.KEY_KP4,
                    uinput.KEY_KP5,
                    uinput.KEY_KP6,
                    uinput.KEY_KP7,
                    uinput.KEY_KP8,
                    uinput.KEY_KP9,
                    uinput.KEY_KPDOT,
                    uinput.KEY_KPSLASH,
                    uinput.KEY_KPASTERISK,
                    uinput.KEY_KPMINUS,
                    uinput.KEY_KPPLUS,
                    uinput.KEY_KPENTER,
                ]
            )

            self._device = uinput.Device(events)

        def reset(self) -> None:
            pass

        def update(self) -> None:
            self._device.emit(uinput.KEY_UP, int(self.arrow_up), syn=False)
            self._device.emit(uinput.KEY_DOWN, int(self.arrow_down), syn=False)
            self._device.emit(uinput.KEY_LEFT, int(self.arrow_left), syn=False)
            self._device.emit(uinput.KEY_RIGHT, int(self.arrow_right), syn=False)

            self._device.emit(uinput.KEY_ENTER, int(self.enter), syn=False)
            self._device.emit(uinput.KEY_BACKSPACE, int(self.backspace), syn=False)
            self._device.emit(uinput.KEY_ESC, int(self.esc), syn=False)
            self._device.emit(uinput.KEY_SPACE, int(self.space), syn=False)
            self._device.emit(uinput.KEY_LEFTCTRL, int(self.ctrl_left), syn=False)
            self._device.emit(uinput.KEY_RIGHTCTRL, int(self.ctrl_right), syn=False)
            self._device.emit(uinput.KEY_LEFTALT, int(self.alt_left), syn=False)
            self._device.emit(uinput.KEY_RIGHTALT, int(self.alt_right), syn=False)
            self._device.emit(uinput.KEY_LEFTSHIFT, int(self.shift_left), syn=False)
            self._device.emit(uinput.KEY_RIGHTSHIFT, int(self.shift_right), syn=False)
            self._device.emit(uinput.KEY_LEFTMETA, int(self.meta_left), syn=False)
            self._device.emit(uinput.KEY_RIGHTMETA, int(self.meta_right), syn=False)
            self._device.emit(uinput.KEY_MENU, int(self.menu), syn=False)
            self._device.emit(uinput.KEY_CAPSLOCK, int(self.caps_lock), syn=False)
            self._device.emit(uinput.KEY_TAB, int(self.tab), syn=False)

            self._device.emit(uinput.KEY_PRINT, int(self.print_screen), syn=False)
            self._device.emit(uinput.KEY_SCROLLLOCK, int(self.scroll_lock), syn=False)
            self._device.emit(uinput.KEY_PAUSE, int(self.pause), syn=False)
            self._device.emit(uinput.KEY_INSERT, int(self.insert), syn=False)
            self._device.emit(uinput.KEY_HOME, int(self.home), syn=False)
            self._device.emit(uinput.KEY_PAGEUP, int(self.page_up), syn=False)
            self._device.emit(uinput.KEY_DELETE, int(self.delete), syn=False)
            self._device.emit(uinput.KEY_END, int(self.end), syn=False)
            self._device.emit(uinput.KEY_PAGEDOWN, int(self.page_down), syn=False)

            self._device.emit(uinput.KEY_A, int(self.key_a), syn=False)
            self._device.emit(uinput.KEY_B, int(self.key_b), syn=False)
            self._device.emit(uinput.KEY_C, int(self.key_c), syn=False)
            self._device.emit(uinput.KEY_D, int(self.key_d), syn=False)
            self._device.emit(uinput.KEY_E, int(self.key_e), syn=False)
            self._device.emit(uinput.KEY_F, int(self.key_f), syn=False)
            self._device.emit(uinput.KEY_G, int(self.key_g), syn=False)
            self._device.emit(uinput.KEY_H, int(self.key_h), syn=False)
            self._device.emit(uinput.KEY_I, int(self.key_i), syn=False)
            self._device.emit(uinput.KEY_J, int(self.key_j), syn=False)
            self._device.emit(uinput.KEY_K, int(self.key_k), syn=False)
            self._device.emit(uinput.KEY_L, int(self.key_l), syn=False)
            self._device.emit(uinput.KEY_M, int(self.key_m), syn=False)
            self._device.emit(uinput.KEY_N, int(self.key_n), syn=False)
            self._device.emit(uinput.KEY_O, int(self.key_o), syn=False)
            self._device.emit(uinput.KEY_P, int(self.key_p), syn=False)
            self._device.emit(uinput.KEY_Q, int(self.key_q), syn=False)
            self._device.emit(uinput.KEY_R, int(self.key_r), syn=False)
            self._device.emit(uinput.KEY_S, int(self.key_s), syn=False)
            self._device.emit(uinput.KEY_T, int(self.key_t), syn=False)
            self._device.emit(uinput.KEY_U, int(self.key_u), syn=False)
            self._device.emit(uinput.KEY_V, int(self.key_v), syn=False)
            self._device.emit(uinput.KEY_W, int(self.key_w), syn=False)
            self._device.emit(uinput.KEY_X, int(self.key_x), syn=False)
            self._device.emit(uinput.KEY_Y, int(self.key_y), syn=False)
            self._device.emit(uinput.KEY_Z, int(self.key_z), syn=False)

            self._device.emit(uinput.KEY_0, int(self.num_0), syn=False)
            self._device.emit(uinput.KEY_1, int(self.num_1), syn=False)
            self._device.emit(uinput.KEY_2, int(self.num_2), syn=False)
            self._device.emit(uinput.KEY_3, int(self.num_3), syn=False)
            self._device.emit(uinput.KEY_4, int(self.num_4), syn=False)
            self._device.emit(uinput.KEY_5, int(self.num_5), syn=False)
            self._device.emit(uinput.KEY_6, int(self.num_6), syn=False)
            self._device.emit(uinput.KEY_7, int(self.num_7), syn=False)
            self._device.emit(uinput.KEY_8, int(self.num_8), syn=False)
            self._device.emit(uinput.KEY_9, int(self.num_9), syn=False)

            self._device.emit(uinput.KEY_GRAVE, int(self.backtick), syn=False)
            self._device.emit(uinput.KEY_MINUS, int(self.minus), syn=False)
            self._device.emit(uinput.KEY_EQUAL, int(self.equals), syn=False)
            self._device.emit(uinput.KEY_BACKSLASH, int(self.backslash), syn=False)
            self._device.emit(uinput.KEY_LEFTBRACE, int(self.left_bracket), syn=False)
            self._device.emit(uinput.KEY_RIGHTBRACE, int(self.right_bracket), syn=False)
            self._device.emit(uinput.KEY_SEMICOLON, int(self.semicolon), syn=False)
            self._device.emit(uinput.KEY_APOSTROPHE, int(self.apostrophe), syn=False)
            self._device.emit(uinput.KEY_COMMA, int(self.comma), syn=False)
            self._device.emit(uinput.KEY_DOT, int(self.dot), syn=False)
            self._device.emit(uinput.KEY_SLASH, int(self.slash), syn=False)

            self._device.emit(uinput.KEY_F1, int(self.f1), syn=False)
            self._device.emit(uinput.KEY_F2, int(self.f2), syn=False)
            self._device.emit(uinput.KEY_F3, int(self.f3), syn=False)
            self._device.emit(uinput.KEY_F4, int(self.f4), syn=False)
            self._device.emit(uinput.KEY_F5, int(self.f5), syn=False)
            self._device.emit(uinput.KEY_F6, int(self.f6), syn=False)
            self._device.emit(uinput.KEY_F7, int(self.f7), syn=False)
            self._device.emit(uinput.KEY_F8, int(self.f8), syn=False)
            self._device.emit(uinput.KEY_F9, int(self.f9), syn=False)
            self._device.emit(uinput.KEY_F10, int(self.f10), syn=False)
            self._device.emit(uinput.KEY_F11, int(self.f11), syn=False)
            self._device.emit(uinput.KEY_F12, int(self.f12), syn=False)

            self._device.emit(uinput.KEY_NUMLOCK, int(self.numpad_lock), syn=False)
            self._device.emit(uinput.KEY_KP0, int(self.numpad_0), syn=False)
            self._device.emit(uinput.KEY_KP1, int(self.numpad_1), syn=False)
            self._device.emit(uinput.KEY_KP2, int(self.numpad_2), syn=False)
            self._device.emit(uinput.KEY_KP3, int(self.numpad_3), syn=False)
            self._device.emit(uinput.KEY_KP4, int(self.numpad_4), syn=False)
            self._device.emit(uinput.KEY_KP5, int(self.numpad_5), syn=False)
            self._device.emit(uinput.KEY_KP6, int(self.numpad_6), syn=False)
            self._device.emit(uinput.KEY_KP7, int(self.numpad_7), syn=False)
            self._device.emit(uinput.KEY_KP8, int(self.numpad_8), syn=False)
            self._device.emit(uinput.KEY_KP9, int(self.numpad_9), syn=False)
            self._device.emit(uinput.KEY_KPDOT, int(self.numpad_decimal), syn=False)
            self._device.emit(uinput.KEY_KPSLASH, int(self.numpad_divide), syn=False)
            self._device.emit(uinput.KEY_KPASTERISK, int(self.numpad_multiply), syn=False)
            self._device.emit(uinput.KEY_KPMINUS, int(self.numpad_subtract), syn=False)
            self._device.emit(uinput.KEY_KPPLUS, int(self.numpad_add), syn=False)
            self._device.emit(uinput.KEY_KPENTER, int(self.numpad_enter), syn=False)

            self._device.syn()

elif platform == "win32":
    from typing import Generator

    import win32api
    import win32con

    KEYBOARD_SCANCODES: dict[str, int] = {
        "arrow_up": 0x26,
        "arrow_down": 0x28,
        "arrow_left": 0x25,
        "arrow_right": 0x27,
        #
        "enter": 0x0D,
        "backspace": 0x08,
        "esc": 0x1B,
        "space": 0x20,
        "ctrl_left": 0xA2,
        "ctrl_right": 0xA3,
        "alt_left": 0xA4,
        "alt_right": 0xA5,
        "shift_left": 0xA0,
        "shift_right": 0xA1,
        "meta_left": 0x5B,
        "meta_right": 0x5C,
        "menu": 0x5D,
        "caps_lock": 0x14,
        "tab": 0x09,
        #
        "print_screen": 0x2C,
        "scroll_lock": 0x91,
        "pause": 0x13,
        "insert": 0x2D,
        "home": 0x24,
        "page_up": 0x21,
        "delete": 0x2E,
        "end": 0x23,
        "page_down": 0x22,
        #
        "key_a": 0x41,
        "key_b": 0x42,
        "key_c": 0x43,
        "key_d": 0x44,
        "key_e": 0x45,
        "key_f": 0x46,
        "key_g": 0x47,
        "key_h": 0x48,
        "key_i": 0x49,
        "key_j": 0x4A,
        "key_k": 0x4B,
        "key_l": 0x4C,
        "key_m": 0x4D,
        "key_n": 0x4E,
        "key_o": 0x4F,
        "key_p": 0x50,
        "key_q": 0x51,
        "key_r": 0x52,
        "key_s": 0x53,
        "key_t": 0x54,
        "key_u": 0x55,
        "key_v": 0x56,
        "key_w": 0x57,
        "key_x": 0x58,
        "key_y": 0x59,
        "key_z": 0x5A,
        #
        "num_0": 0x30,
        "num_1": 0x31,
        "num_2": 0x32,
        "num_3": 0x33,
        "num_4": 0x34,
        "num_5": 0x35,
        "num_6": 0x36,
        "num_7": 0x37,
        "num_8": 0x38,
        "num_9": 0x39,
        #
        "backtick": 0xC0,
        "minus": 0xBD,
        "equals": 0xBB,
        "backslash": 0xDC,
        "left_bracket": 0xDB,
        "right_bracket": 0xDD,
        "semicolon": 0xBA,
        "apostrophe": 0xDE,
        "comma": 0xBC,
        "dot": 0xBE,
        "slash": 0xBF,
        #
        "f1": 0x70,
        "f2": 0x71,
        "f3": 0x72,
        "f4": 0x73,
        "f5": 0x74,
        "f6": 0x75,
        "f7": 0x76,
        "f8": 0x77,
        "f9": 0x78,
        "f10": 0x79,
        "f11": 0x7A,
        "f12": 0x7B,
        #
        "numpad_lock": 0x90,
        "numpad_0": 0x60,
        "numpad_1": 0x61,
        "numpad_2": 0x62,
        "numpad_3": 0x63,
        "numpad_4": 0x64,
        "numpad_5": 0x65,
        "numpad_6": 0x66,
        "numpad_7": 0x67,
        "numpad_8": 0x68,
        "numpad_9": 0x69,
        "numpad_decimal": 0x6E,
        "numpad_divide": 0x6F,
        "numpad_multiply": 0x6A,
        "numpad_subtract": 0x6D,
        "numpad_add": 0x6B,
        "numpad_enter": 0x0D,
    }

    class Keyboard:  # type: ignore[no-redef]
        def __init__(self) -> None:
            self.arrow_up: bool = False
            self.arrow_down: bool = False
            self.arrow_left: bool = False
            self.arrow_right: bool = False

            self.enter: bool = False
            self.backspace: bool = False
            self.esc: bool = False
            self.space: bool = False
            self.ctrl_left: bool = False
            self.ctrl_right: bool = False
            self.alt_left: bool = False
            self.alt_right: bool = False
            self.shift_left: bool = False
            self.shift_right: bool = False
            self.meta_left: bool = False
            self.meta_right: bool = False
            self.menu: bool = False
            self.caps_lock: bool = False
            self.tab: bool = False

            self.print_screen: bool = False
            self.scroll_lock: bool = False
            self.pause: bool = False
            self.insert: bool = False
            self.home: bool = False
            self.page_up: bool = False
            self.delete: bool = False
            self.end: bool = False
            self.page_down: bool = False

            self.key_a: bool = False
            self.key_b: bool = False
            self.key_c: bool = False
            self.key_d: bool = False
            self.key_e: bool = False
            self.key_f: bool = False
            self.key_g: bool = False
            self.key_h: bool = False
            self.key_i: bool = False
            self.key_j: bool = False
            self.key_k: bool = False
            self.key_l: bool = False
            self.key_m: bool = False
            self.key_n: bool = False
            self.key_o: bool = False
            self.key_p: bool = False
            self.key_q: bool = False
            self.key_r: bool = False
            self.key_s: bool = False
            self.key_t: bool = False
            self.key_u: bool = False
            self.key_v: bool = False
            self.key_w: bool = False
            self.key_x: bool = False
            self.key_y: bool = False
            self.key_z: bool = False

            self.num_0: bool = False
            self.num_1: bool = False
            self.num_2: bool = False
            self.num_3: bool = False
            self.num_4: bool = False
            self.num_5: bool = False
            self.num_6: bool = False
            self.num_7: bool = False
            self.num_8: bool = False
            self.num_9: bool = False

            self.backtick: bool = False
            self.minus: bool = False
            self.equals: bool = False
            self.backslash: bool = False
            self.left_bracket: bool = False
            self.right_bracket: bool = False
            self.semicolon: bool = False
            self.apostrophe: bool = False
            self.comma: bool = False
            self.dot: bool = False
            self.slash: bool = False

            self.f1: bool = False
            self.f2: bool = False
            self.f3: bool = False
            self.f4: bool = False
            self.f5: bool = False
            self.f6: bool = False
            self.f7: bool = False
            self.f8: bool = False
            self.f9: bool = False
            self.f10: bool = False
            self.f11: bool = False
            self.f12: bool = False

            self.numpad_lock: bool = False
            self.numpad_0: bool = False
            self.numpad_1: bool = False
            self.numpad_2: bool = False
            self.numpad_3: bool = False
            self.numpad_4: bool = False
            self.numpad_5: bool = False
            self.numpad_6: bool = False
            self.numpad_7: bool = False
            self.numpad_8: bool = False
            self.numpad_9: bool = False
            self.numpad_decimal: bool = False
            self.numpad_divide: bool = False
            self.numpad_multiply: bool = False
            self.numpad_subtract: bool = False
            self.numpad_add: bool = False
            self.numpad_enter: bool = False

            self._old_key_states: dict[str, bool] = {}
            self.reset()

        def _get_keys(self) -> Generator[tuple[str, bool], None, None]:
            for name, obj in self.__dict__.items():
                if not isinstance(obj, bool):
                    continue

                yield name, obj

        def reset(self) -> None:
            for key, pressed in self._get_keys():
                self._old_key_states[key] = pressed

        def update(self) -> None:
            for key, pressed in self._get_keys():
                if pressed != self._old_key_states[key]:
                    win32api.keybd_event(KEYBOARD_SCANCODES[key], 0, 0 if pressed else win32con.KEYEVENTF_KEYUP, 0)

else:

    class Keyboard:  # type: ignore[no-redef]
        def __init__(self) -> None:
            raise NotImplementedError(f"Keyboard not supported on platform {platform}!")
