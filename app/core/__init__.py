import os
import yaml
from typing import Union

from app.core.config import AppConfig

BaseDir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CONFIG: Union[AppConfig | None] = None


def load_config(file: str) -> AppConfig:
    with open(file, "r") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)


if not CONFIG:
    file_path: str = os.path.join(BaseDir, "configs/config.yaml")
    CONFIG = load_config(file_path)
