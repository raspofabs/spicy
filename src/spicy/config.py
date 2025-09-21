"""Handle looking for and loading the spicy config file for a target document directory."""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def load_spicy_config(config_directory: Path, **kwargs: str | None) -> dict[str, Any]:
    """Load the spicy.yaml file from the config path provided, or default to an empty dictionary."""
    config: dict[str, str] = {}
    if not config_directory.is_dir():
        config_directory = config_directory.parent
    config_file_path = config_directory / "spicy.yaml"
    loaded_config: dict[Any, Any] | None = None
    try:
        with config_file_path.open() as fh:
            loaded_config = yaml.safe_load(fh)
    except FileNotFoundError:
        logger.warning("No config found at %s", config_file_path)

    if loaded_config is not None:
        config = {key: value for key, value in loaded_config.items() if isinstance(key, str)}

    for keyword, value in kwargs.items():
        if isinstance(value, str):
            config[keyword] = value
    return config
