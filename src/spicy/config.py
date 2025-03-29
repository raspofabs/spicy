"""Handle looking for and loading the spicy config file for a target document directory."""

from pathlib import Path

import yaml


def load_spicy_config(config_directory: Path) -> dict[str, str]:
    """Load the spicy.yaml file from the config path provided, or default to an empty dictionary."""
    try:
        with open(config_directory / "spicy.yaml") as fh:
            config = yaml.safe_load(fh)
        return config
    except FileNotFoundError:
        return {}
