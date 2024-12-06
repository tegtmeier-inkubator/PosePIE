from pydantic import Field
from pydantic_settings import BaseSettings, CliPositionalArg, SettingsConfigDict

from pose.camera import CameraConfig
from pose.model import PoseModelConfig


class Config(BaseSettings, cli_parse_args=True):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    camera: CameraConfig = CameraConfig()
    pose: PoseModelConfig = PoseModelConfig()

    show_camera: bool = Field(
        True,
        description="show window with annotated camera image",
    )

    script: CliPositionalArg[str]
