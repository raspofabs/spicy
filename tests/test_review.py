"""Test the use-cases parser."""

import logging
import re
from pathlib import Path
from typing import Any

import pytest

from spicy.gather import gather_all_elements
from spicy.parser.spec_element import SpecElement
from spicy.review import render_issues_with_elements


class DummyElement(SpecElement):
    """Testing support class for SpecElement."""

    def __init__(
        self,
        file_path: Path,
        expected_links: dict[str, list[tuple[str, str, str]]],
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

    def get_issues(self, config: dict[str, Any]) -> list[str]:
        """Return an empty list of issues for DummyElement."""
        return []


def test_render_issues_with_elements(test_data_path: Path) -> None:
    """Test we can render some issues with obvious errors."""
    spec_elements = gather_all_elements("TD", test_data_path / "simple" / "duped.md")

    lines = []

    render_issues_with_elements(spec_elements, config={}, render_function=lambda x: lines.append(x))
    assert not any(re.search(r"Non unique name TD_STK_REQ.*", line) for line in lines)
    assert any(re.search(r"Non unique name TD_SYS_REQ_dupe.*", line) for line in lines)


CASE_LIST = [
    ("simple/duped.md", [r"Non unique name TD_SYS_REQ_dupe.*"], []),
    ("simple/missing_links.md", [r"Missing links for \[Derived from StakeholderRequirement\]"], []),
    (
        "simple/unexpected_links.md",
        [
            r"SystemRequirement TD_SYS_REQ_unexpected in [\w./]+: "
            r"Derived from unexpected StakeholderRequirement TD_STK_REQ_oops",
        ],
        [],
    ),
    (
        "linkage/non_functional_software_requirement.md",
        [],
        [
            r"Missing links for \[Decomposes SystemElement\]",
            r"Missing links for \[Realises SystemRequirement\]",
        ],
    ),
]


@pytest.mark.parametrize(("specific_file", "expected_errors", "unexpected_errors"), CASE_LIST)
def test_render_issues_with_elements_expected_errors(
    test_data_path: Path,
    caplog: pytest.LogCaptureFixture,
    specific_file: str,
    expected_errors: list[str],
    unexpected_errors: list[str],
) -> None:
    """Test we can detect all expected errors in files."""
    spec_elements = gather_all_elements("TD", test_data_path / specific_file)
    lines = []
    with caplog.at_level(logging.DEBUG):
        render_issues_with_elements(spec_elements, config={}, render_function=lambda x: lines.append(x))
    assert lines
    for expected_error in expected_errors:
        assert any(re.search(expected_error, line) for line in lines), lines
    for unexpected_error in unexpected_errors:
        assert not any(re.search(unexpected_error, line) for line in lines), lines


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
    (
        "non_functional_software_requirement.md",
        [],
        [
            "Missing links for [Decomposes SystemElement]",
            "Missing links for [Realises SystemRequirement]",
        ],
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
        render_issues_with_elements(spec_elements, config={}, render_function=lambda x: lines.append(x))

    for expected_output in expected_outputs:
        assert any(re.search(expected_output, line) for line in lines), lines
    for unexpected_output in unexpected_outputs:
        assert not any(re.search(unexpected_output, line) for line in lines), lines
