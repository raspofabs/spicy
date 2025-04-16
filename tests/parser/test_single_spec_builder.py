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


def test_single_spec_builder_construction(basic_builder: SingleSpecBuilder) -> None:
    """Test a simple builder using only name and basic required details."""
    assert str(TEST_PATH) in basic_builder.location
    assert str(ARBITRARY_NTH) in basic_builder.location
    assert TEST_NAME in basic_builder.location


def test_single_spec_builder_build_method(basic_builder: SingleSpecBuilder) -> None:
    """Test building from a simple builder."""
    spec_element = basic_builder.build()
    assert f"{TEST_VARIANT}:{TEST_NAME}({TEST_PATH}:{ARBITRARY_NTH})" in str(spec_element)
