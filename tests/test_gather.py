"""Test the use-cases parser."""

import logging
import re
from pathlib import Path

import pytest

from spicy.gather import gather_all_elements, get_elements_from_files, render_issues_with_elements


def test_gather_on_directory(test_data_path: Path) -> None:
    """Test we can gather from a directory, not just a single file."""
    spec_element_list = get_elements_from_files("TD", [test_data_path / "use_cases"])

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) > 1


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
