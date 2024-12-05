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
            events.extend([uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT])

            self._device = uinput.Device(events)

        def update(self) -> None:
            self._device.emit(uinput.KEY_UP, int(self.arrow_up), syn=False)
            self._device.emit(uinput.KEY_DOWN, int(self.arrow_down), syn=False)
            self._device.emit(uinput.KEY_LEFT, int(self.arrow_left), syn=False)
            self._device.emit(uinput.KEY_RIGHT, int(self.arrow_right), syn=False)

            self._device.syn()

else:
    raise NotImplementedError(f"Keyboard not supported on platform {platform}!")
