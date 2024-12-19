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

from input_emulation.mouse import Mouse
from script.plugin import PluginBase


class MousePlugin(PluginBase):
    def __init__(self, mouse: Mouse):
        self._mouse = mouse

    def create(self) -> None:
        pass

    def pre_update(self) -> None:
        pass

    def post_update(self) -> None:
        self._mouse.update()

    def destroy(self) -> None:
        pass
