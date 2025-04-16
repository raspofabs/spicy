"""Test the use-cases parser."""

from pathlib import Path

import pytest

from spicy.parser.spec_element import SpecElement

TEST_NAME = "PRJ_DOC_installation_manual"
TEST_VARIANT = "Documentation"
ARBITRARY_NTH = 5
TEST_PATH = Path("path/to/spec.md")


@pytest.fixture
def basic_spec_element() -> SpecElement:
    return SpecElement(TEST_NAME, TEST_VARIANT, ARBITRARY_NTH, TEST_PATH)


@pytest.fixture
def spec_element_with_links(basic_spec_element: SpecElement) -> SpecElement:
    basic_spec_element.content["verification_criteria"] = ["Can be used by someone who reads"]
    basic_spec_element.content["fulfils"] = ["PRJ_SYS_REQ_installation_guidance"]
    return basic_spec_element


@pytest.fixture
def spec_element_for_qualification(basic_spec_element: SpecElement) -> SpecElement:
    basic_spec_element.qualification_related = True
    return basic_spec_element


def test_spec_element_construction(basic_spec_element: SpecElement) -> None:
    """Test the basic spec element construction."""
    assert not basic_spec_element.is_qualification_related
    assert f"{TEST_VARIANT}:{TEST_NAME}({TEST_PATH}:{ARBITRARY_NTH})" in str(basic_spec_element)

    assert not basic_spec_element.verification_criteria()
    assert not basic_spec_element.description_text()
    assert not basic_spec_element.get_linked_by("fulfils")


def test_spec_element_links(spec_element_with_links: SpecElement) -> None:
    """Test the basic spec element construction."""
    assert not spec_element_with_links.is_qualification_related
    assert spec_element_with_links.verification_criteria()
    assert not spec_element_with_links.description_text()
    assert spec_element_with_links.get_linked_by("fulfils")


def test_spec_element_qualification(spec_element_for_qualification: SpecElement) -> None:
    """Test the basic spec element construction."""
    assert spec_element_for_qualification.is_qualification_related


def test_spec_element_as_use_case() -> None:
    use_case = SpecElement("use_case_1", "UseCase", 0, Path())
