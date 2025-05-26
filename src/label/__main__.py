from __future__ import annotations

from label._dataclass import RunnerSettings
from label.utils.config import load_settings_file


def main():
    settings = load_settings_file(
        setting_name="config.toml",
        setting=RunnerSettings,
    )
    print(settings)
