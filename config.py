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

from pydantic import Field
from pydantic_settings import BaseSettings, CliPositionalArg, SettingsConfigDict

from pose.camera import CameraConfig
from pose.model import PoseModelConfig


class Config(BaseSettings, cli_parse_args=True, cli_hide_none_type=True):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    camera: CameraConfig = CameraConfig()
    pose: PoseModelConfig = PoseModelConfig()

    show_camera: bool = Field(
        True,
        description="show window with annotated camera image",
    )

    script: CliPositionalArg[str] = Field(
        description="path to the user script",
    )
