"""pytest configuration and fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def test_data_path():
    """Return the path to the test data directory."""
    return Path(__file__).parent / "test_data"
