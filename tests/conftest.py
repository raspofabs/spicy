"""pytest configuration and fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def test_data_path() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def positive_test_data_path(test_data_path) -> Path:
    """Return the path to the test data directory."""
    return test_data_path / "simple_test_spec"


@pytest.fixture
def cookie_data_path(test_data_path) -> Path:
    """Return the path to the test data directory."""
    return test_data_path / "cookie_spec"
