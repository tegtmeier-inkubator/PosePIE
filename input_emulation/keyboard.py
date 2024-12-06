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

            self._device = uinput.Device(events)

        def update(self) -> None:
            self._device.emit(uinput.KEY_UP, int(self.arrow_up), syn=False)
            self._device.emit(uinput.KEY_DOWN, int(self.arrow_down), syn=False)
            self._device.emit(uinput.KEY_LEFT, int(self.arrow_left), syn=False)
            self._device.emit(uinput.KEY_RIGHT, int(self.arrow_right), syn=False)

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

            self._device.syn()

else:
    raise NotImplementedError(f"Keyboard not supported on platform {platform}!")
