"""Test the use-cases parser."""

import logging
from pathlib import Path

import pytest

from spicy.parser.spec_element import SpecElement

TEST_NAME = "PRJ_DOC_installation_manual"
TEST_VARIANT = "Documentation"
ARBITRARY_NTH = 5
TEST_PATH = Path("path/to/spec.md")


@pytest.fixture
def basic_spec_element() -> SpecElement:
    """Fixture for basic spec element without any details."""
    return SpecElement(TEST_NAME, TEST_VARIANT, ARBITRARY_NTH, TEST_PATH)


@pytest.fixture
def spec_element_with_links() -> SpecElement:
    """Fixture for basic spec element with a link to another spec."""
    spec = SpecElement(TEST_NAME, TEST_VARIANT, ARBITRARY_NTH, TEST_PATH)
    spec.content["verification_criteria"] = ["Can be used by someone who reads"]
    spec.content["fulfils"] = ["PRJ_SYS_REQ_installation_guidance"]
    return spec


@pytest.fixture
def spec_element_for_qualification() -> SpecElement:
    """Fixture for basic spec element which is qualification relevant."""
    spec = SpecElement(TEST_NAME, TEST_VARIANT, ARBITRARY_NTH, TEST_PATH)
    spec.qualification_related = True
    return spec


@pytest.fixture
def spec_element_for_non_software() -> SpecElement:
    """Fixture for basic spec element which is not software relevant."""
    spec = SpecElement(TEST_NAME, TEST_VARIANT, ARBITRARY_NTH, TEST_PATH)
    spec.software_requirement = False
    return spec


def test_spec_element_construction(basic_spec_element: SpecElement) -> None:
    """Test the basic spec element construction."""
    assert not basic_spec_element.is_qualification_related
    assert f"{TEST_VARIANT}:{TEST_NAME}({TEST_PATH}:{ARBITRARY_NTH})" in str(basic_spec_element)

    assert not basic_spec_element.verification_criteria()
    assert not basic_spec_element.description_text()
    assert not basic_spec_element.get_linked_by("fulfils")


def test_spec_element_misuse(basic_spec_element: SpecElement, caplog: pytest.LogCaptureFixture) -> None:
    """Test the basic spec element construction."""
    basic_spec_element.content["non-list"] = "This is just a string"  # type: ignore[assignment]

    with caplog.at_level(logging.DEBUG):
        assert basic_spec_element.get_linked_by("non-list") == []
    assert "No list content for non-list" in caplog.text


def test_spec_element_links(spec_element_with_links: SpecElement) -> None:
    """Test a spec which links to another spec."""
    assert not spec_element_with_links.is_qualification_related
    assert spec_element_with_links.verification_criteria()
    assert not spec_element_with_links.description_text()
    assert spec_element_with_links.get_linked_by("fulfils")


def test_spec_element_qualification(
    basic_spec_element: SpecElement,
    spec_element_for_qualification: SpecElement,
) -> None:
    """Test a qualification relevant spec."""
    assert not basic_spec_element.is_qualification_related
    assert spec_element_for_qualification.is_qualification_related


def test_spec_element_software_relevance(
    basic_spec_element: SpecElement,
    spec_element_for_non_software: SpecElement,
) -> None:
    """Test a qualification relevant spec."""
    assert basic_spec_element.is_software_element
    assert not spec_element_for_non_software.is_software_element


def test_spec_element_as_use_case() -> None:
    """Test the construction of use-cases as they are a bit different."""
    use_case = SpecElement("use_case_1", "UseCase", 0, Path())

    assert not use_case.is_qualification_related

    use_case.impact = "TI1"
    use_case.detectability = "TD1"

    assert not use_case.is_qualification_related

    use_case.impact = "TI2"
    use_case.detectability = "TD2"

    assert use_case.is_qualification_related


def test_spec_element_use_case_issues() -> None:
    """Test the issue detection code for a simple UseCase SpecElement."""
    use_case = SpecElement("use_case_1", "UseCase", 0, Path())
    issues = use_case.get_issues({})
    assert issues
    assert "no impact" in issues
    assert "no detectability" in issues
    all_text = " ".join(issues)
    assert "no usage:" in all_text
    assert "no section information for:" in all_text

    use_case.impact = "TI1"
    use_case.detectability = "TD1"

    issues = use_case.get_issues({})
    assert issues
    assert "no impact" not in issues
    assert "no detectability" not in issues
    all_text = " ".join(issues)
    assert "no usage:" in all_text
    assert "no section information for:" in all_text


def test_spec_element_issues(basic_spec_element: SpecElement) -> None:
    """Test the issue detection code for a simple SpecElement."""
    issues = basic_spec_element.get_issues({})
    assert not issues

    # detect missing links
    spec_with_missing_links = SpecElement(
        "PRJ_SW_UNIT_simple_unit",
        "SoftwareUnit",  # SoftwareUnit requires "Implements: SoftwareComponent"
        5,
        Path("path/to/file"),
    )

    issues = spec_with_missing_links.get_issues({})
    assert issues
    assert "Missing links for [Implements SoftwareComponent]" in issues

    # allow ignoring missing links
    ignored_config = {
        "ignored_links": {
            "SoftwareUnit": [
                "Implements SoftwareComponent",
            ],
        },
    }
    issues = spec_with_missing_links.get_issues(ignored_config)
    assert not issues
