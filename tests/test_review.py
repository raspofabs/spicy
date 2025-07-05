"""Test the use-cases parser."""

import logging
import re
from pathlib import Path

import pytest

from spicy.gather import gather_all_elements
from spicy.parser.spec_element import SpecElement
from spicy.review import render_issues_with_elements, render_spec_link_markdown_reference_issues


class DummyElement(SpecElement):
    """Testing support class for SpecElement."""

    def __init__(
        self,
        file_path: Path,
        expected_links: dict[str, list[tuple[str, str]]],
        content: dict[str, list[str]],
    ) -> None:
        """Initialize DummyElement with required attributes."""
        super().__init__(
            name="DUMMY_ELEMENT",
            variant="Dummy",
            ordering_id=0,
            file_path=file_path,
        )
        self.expected_links = expected_links
        self.content = content

    def get_issues(self) -> list[str]:
        """Return an empty list of issues for DummyElement."""
        return []


def test_render_issues_with_elements(test_data_path: Path) -> None:
    """Test we can render some issues with obvious errors."""
    spec_elements = gather_all_elements("TD", test_data_path / "simple" / "duped.md")

    lines = []

    render_issues_with_elements(spec_elements, lambda x: lines.append(x))
    assert not any(re.search(r"Non unique name TD_STK_REQ.*", line) for line in lines)
    assert any(re.search(r"Non unique name TD_SYS_REQ_dupe.*", line) for line in lines)


CASE_LIST = [
    ("simple/duped.md", [r"Non unique name TD_SYS_REQ_dupe.*"]),
    ("simple/missing_links.md", [r"Missing links for \[Derived from StakeholderRequirement\]"]),
    (
        "simple/unexpected_links.md",
        [
            r"SystemRequirement TD_SYS_REQ_unexpected Derived from unexpected StakeholderRequirement TD_STK_REQ_oops",
        ],
    ),
]


@pytest.mark.parametrize(("specific_file", "expected_errors"), CASE_LIST)
def test_render_issues_with_elements_expected_errors(
    test_data_path: Path,
    caplog: pytest.LogCaptureFixture,
    specific_file: str,
    expected_errors: list[str],
) -> None:
    """Test we can detect all expected errors in files."""
    spec_elements = gather_all_elements("TD", test_data_path / specific_file)
    lines = []
    with caplog.at_level(logging.DEBUG):
        render_issues_with_elements(spec_elements, lambda x: lines.append(x))
    assert lines
    for expected_error in expected_errors:
        assert any(re.search(expected_error, line) for line in lines), lines


LINKAGE_CASES: list[tuple[str, list[str], list[str]]] = [
    ("use_case_to_stakeholder_need.md", [], ["Fulfils unexpected StakeholderNeed", "without a UseCase"]),
    ("use_case_to_stakeholder_needs_plural.md", [], ["Fulfils unexpected StakeholderNeed", "without a UseCase"]),
    ("system_element_to_stakeholder_requirement.md", [], ["Implements unexpected StakeholderRequirement"]),
    ("software_component_to_software_requirement.md", [], ["Realises unexpected SoftwareArchitecture"]),
    ("system_requirement_to_system_element.md", [], ["SystemRequirement without a SystemElement"]),
    ("non_software_system_element.md", [], ["SystemElement without a SoftwareRequirement"]),
    ("stakeholder_requirement_qualification_relevant.md", [], ["Qualification"]),
    (
        "sys_req_with_specification.md",
        [
            "unexpected StakeholderRequirement "
            "TD_STK_REQ_have_a_stakeholder_requirement, "
            "TD_STK_REQ_safe_stakeholder_requirement",
        ],
        ["Qualification relevant"],
    ),
]


@pytest.mark.parametrize(("test_filename", "expected_outputs", "unexpected_outputs"), LINKAGE_CASES)
def test_linkage(
    test_data_path: Path,
    caplog: pytest.LogCaptureFixture,
    test_filename: str,
    expected_outputs: list[str],
    unexpected_outputs: list[str],
) -> None:
    """Test linkages with different cases."""
    with caplog.at_level(logging.DEBUG):
        spec_elements = gather_all_elements("TD", test_data_path / "linkage" / test_filename)
    lines = []
    with caplog.at_level(logging.DEBUG):
        render_issues_with_elements(spec_elements, lambda x: lines.append(x))

    for expected_output in expected_outputs:
        assert any(re.search(expected_output, line) for line in lines), lines
    for unexpected_output in unexpected_outputs:
        assert not any(re.search(unexpected_output, line) for line in lines), lines


def test_render_spec_link_markdown_reference_issues_missing_and_bad_links(tmp_path: Path) -> None:
    """Test render_spec_link_markdown_reference_issues for missing and bad links."""
    file_path = tmp_path / "dummy.md"
    el_missing = DummyElement(
        file_path=file_path,
        expected_links={"section1": [("target1", "[target1](#target1)")]},
        content={"section1": ["- somethingelse"]},
    )
    el_bad = DummyElement(
        file_path=file_path,
        expected_links={"section1": [("target2", "[target2](#target2)")]},
        content={"section1": ["- [target2](#wrong-link)"]},
    )
    lines: list[str] = []
    render_spec_link_markdown_reference_issues(
        [el_missing, el_bad],
        lambda x: lines.append(x),
    )
    assert any("No expected link for [- somethingelse]" in line for line in lines)
    assert any(
        "No expected link for [- target2]" in line or "No expected link for [- [target2]" in line for line in lines
    ), f"Expected missing link for target2 in lines: {lines}"
    assert any("but had - [target2](#wrong-link)" in line for line in lines)


def test_render_spec_link_markdown_reference_issues_link_mismatch(tmp_path: Path) -> None:
    """Test render_spec_link_markdown_reference_issues for a link mismatch (expected vs actual).

    Covers lines 55-58 in review.py.
    """
    file_path = tmp_path / "dummy.md"
    el = DummyElement(
        file_path=file_path,
        expected_links={"section1": [("target1", "[target1](#target1)")]},
        content={"section1": ["- [target1](#not-the-right-link)"]},
    )
    lines: list[str] = []
    render_spec_link_markdown_reference_issues(
        [el],
        lambda x: lines.append(x),
    )
    assert any(
        "No expected link for [- target1]" in line or "No expected link for [- [target1]" in line for line in lines
    ), f"Expected missing link for target1 in lines: {lines}"
    assert any("but had - [target1](#not-the-right-link)" in line for line in lines)
