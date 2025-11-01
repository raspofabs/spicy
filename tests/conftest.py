"""pytest configuration and fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def test_data_path() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def positive_test_data_path(test_data_path: Path) -> Path:
    """Return the path to the test data directory."""
    return test_data_path / "simple_test_spec"


@pytest.fixture
def bad_link_data_path(test_data_path: Path) -> Path:
    """Return the path to the test data directory."""
    return test_data_path / "bad_links_spec"


@pytest.fixture
def fixable_link_data_path(test_data_path: Path) -> Path:
    """Return the path to the test data directory."""
    return test_data_path / "fixable_links_spec"


@pytest.fixture
def cookie_data_path(test_data_path: Path) -> Path:
    """Return the path to the test data directory."""
    return test_data_path / "cookie_spec"
