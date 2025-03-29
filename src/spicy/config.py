"""Handle looking for and loading the spicy config file for a target document directory."""

import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


def load_spicy_config(config_directory: Path, **kwargs) -> dict[str, str]:
    """Load the spicy.yaml file from the config path provided, or default to an empty dictionary."""
    config = {}
    if not config_directory.is_dir():
        config_directory = config_directory.parent
    config_file_path = config_directory / "spicy.yaml"
    try:
        with open(config_file_path) as fh:
            config = yaml.safe_load(fh)
    except FileNotFoundError:
        logger.warning("No config found at %s", config_file_path)

    for keyword, value in kwargs.items():
        if value is not None:
            config[keyword] = value
    return config
