"""Test the use-cases parser."""

from pathlib import Path

import pytest

from spicy.parser.single_spec_builder import SingleSpecBuilder

TEST_NAME = "PRJ_DOC_installation_manual"
TEST_VARIANT = "Documentation"
ARBITRARY_NTH = 5
TEST_PATH = Path("path/to/spec.md")


@pytest.fixture
def basic_builder() -> SingleSpecBuilder:
    """Fixture for basic single spec builder without any details."""
    return SingleSpecBuilder(TEST_NAME, TEST_VARIANT, ARBITRARY_NTH, TEST_PATH, TEST_NAME)


def test_simple_spec_building(basic_builder: SingleSpecBuilder) -> None:
    """Test a simple builder which only passes name and basic required details."""
    spec_element = basic_builder.build()
    assert f"{TEST_VARIANT}:{TEST_NAME}({TEST_PATH}:{ARBITRARY_NTH})" in str(spec_element)
