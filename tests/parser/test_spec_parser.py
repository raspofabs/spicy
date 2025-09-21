"""Test the use-cases parser."""

import logging
from pathlib import Path

import pytest

from spicy.gather import get_elements_from_files
from spicy.md_read import load_syntax_tree, parse_text_to_syntax_tree
from spicy.parser.spec_element import SpecElement
from spicy.parser.spec_parser import (
    SpecParser,
    looks_like_non_sticky_section,
    looks_like_single_line_field,
    parse_syntax_tree_to_spec_elements,
)


def test_parse_use_case(test_data_path: Path) -> None:
    """Test we can parse a use-case file and detect the use case spec."""
    from_file = test_data_path / "use_cases" / "01_simple_valid.md"
    project_prefix = "TD"
    node = load_syntax_tree(from_file)
    spec_element_list = parse_syntax_tree_to_spec_elements(project_prefix, node, from_file)

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) == 1

    use_case = spec_element_list[0]
    assert isinstance(use_case, SpecElement)

    assert use_case.name == "FEAT_COOKIE_ORDERING_PAGE"
    assert use_case.description_text()
    assert use_case.features_text()
    assert use_case.inputs()
    assert use_case.outputs()
    assert use_case.impact_rationale()
    assert use_case.detectability_rationale()

    assert use_case.impact == "TI2"
    assert use_case.detectability == "TD1"
    assert use_case.tcl == "TCL1"

    issues = use_case.get_issues({})
    assert not issues


def test_parse_multiple_use_cases(test_data_path: Path) -> None:
    """Test we can parse a file with multiple use-cases and detect the use case specs."""
    from_file = test_data_path / "use_cases" / "03_multiple_valid.md"
    project_prefix = "TD"
    node = load_syntax_tree(from_file)
    spec_element_list = parse_syntax_tree_to_spec_elements(project_prefix, node, from_file)

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) > 1

    assert all(isinstance(x, SpecElement) for x in spec_element_list)
    assert all(x.variant == "UseCase" for x in spec_element_list)


def test_parse_invalid_use_cases(test_data_path: Path) -> None:
    """Test we can parse a file with multiple use-cases and detect the use case specs."""
    from_file = test_data_path / "use_cases" / "05_more_invalid.md"
    project_prefix = "TD"
    node = load_syntax_tree(from_file)
    spec_element_list = parse_syntax_tree_to_spec_elements(project_prefix, node, from_file)

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) > 1

    assert all(isinstance(x, SpecElement) for x in spec_element_list)
    assert all(x.variant == "UseCase" for x in spec_element_list)


def test_detect_spec_heading() -> None:
    """Test that we can detect a design spec heading from its name."""
    parser = SpecParser(Path("my_file.md"), "TD")
    assert parser.parsed_spec_count == 0
    tree_part = parse_text_to_syntax_tree("# TD_SYS_REQ_a_system_requirement")
    for child in tree_part.children:
        parser.parse_node(child)
    assert parser.parsed_spec_count == 1


@pytest.mark.parametrize(("header_level", "spec_count"), [(1, 3), (2, 2), (3, 4)])
def test_builder_depth(
    test_data_path: Path,
    caplog: pytest.LogCaptureFixture,
    header_level: int,
    spec_count: int,
) -> None:
    """Test that we can parse with sub-builders."""
    from_file = test_data_path / "simple" / "sys_req.md"
    project_prefix = "TD"

    lines: list[str] = []
    for i in range(spec_count):
        lines.extend(
            [
                "#" * header_level + f" TD_SYS_REQ_simple_sys_req_{i}",
                "The **TD** shall have a few simple system requirements",
            ],
        )
    spec_text = "\n\n".join(lines)
    tree = parse_text_to_syntax_tree(spec_text)
    assert len(lines) == len(tree.children)

    parser = SpecParser(from_file, project_prefix)
    with caplog.at_level(logging.DEBUG):
        for child in tree.children:
            parser.parse_node(child)
    assert parser.parsed_spec_count == spec_count


def test_parse_sys_req_from_text(test_data_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test parsing with a simple system requirement, from raw text."""
    from_file = test_data_path / "simple" / "sys_req.md"
    project_prefix = "TD"
    lines = [
        "# TD_SYS_REQ_simple_sys_req",
        "The **TD** shall have a simple system requirement",
        "Derived from:",
        "- [TD_STK_REQ_simple_stk_req](#td_stk_req_simple_stk_req)",
        "TQP relevant: yes",
        "Verification Criteria:",
        "- check we have a simple sys req.",
    ]
    spec_text = "\n\n".join(lines)
    tree = parse_text_to_syntax_tree(spec_text)
    assert len(lines) == len(tree.children)

    parser = SpecParser(from_file, project_prefix)
    with caplog.at_level(logging.DEBUG):
        for child in tree.children:
            parser.parse_node(child)
    assert parser.parsed_spec_count == 1
    spec_element_list = [spec.build() for spec in parser.spec_builders]

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) == 1

    spec = spec_element_list[0]
    assert spec.name == "TD_SYS_REQ_simple_sys_req"

    assert "Handle bullet_list" in caplog.text

    assert spec.description_text(), str(spec)
    assert spec.is_qualification_related
    assert spec.variant == "SystemRequirement"
    assert spec.verification_criteria(), str(spec)
    assert spec.get_linked_by("derived_from"), str(spec)

    issues = spec.get_issues({})
    assert not issues


def test_parse_sys_req(test_data_path: Path) -> None:
    """Test parsing using a simple system requirement from a file."""
    from_file = test_data_path / "simple" / "sys_req.md"
    project_prefix = "TD"
    node = load_syntax_tree(from_file)

    tree = parse_text_to_syntax_tree("# TD_SYS_REQ_a_system_requirement")
    parser = SpecParser(from_file, project_prefix)
    for child in tree.children:
        parser.parse_node(child)
    assert parser.parsed_spec_count == 1
    spec_element_list = [spec.build() for spec in parser.spec_builders]

    spec_element_list = parse_syntax_tree_to_spec_elements(project_prefix, node, from_file)

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) == 1

    spec = spec_element_list[0]

    assert spec.name == "TD_SYS_REQ_simple_sys_req"
    assert spec.description_text(), str(spec)
    assert spec.is_qualification_related
    assert spec.variant == "SystemRequirement"
    assert spec.verification_criteria(), str(spec)
    assert spec.get_linked_by("derived_from"), str(spec)

    issues = spec.get_issues({})
    assert not issues


# test high level functions


def test_valid_use_case(test_data_path: Path) -> None:
    """Positive test the tooling using good data."""
    spec_element_list = get_elements_from_files("TD", [test_data_path / "use_cases" / "01_simple_valid.md"])

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) == 1

    use_case = spec_element_list[0]
    assert isinstance(use_case, SpecElement)

    assert use_case.name == "FEAT_COOKIE_ORDERING_PAGE"
    assert use_case.description_text()
    assert use_case.features_text()
    assert use_case.inputs()
    assert use_case.outputs()
    assert use_case.impact_rationale()
    assert use_case.detectability_rationale()

    assert use_case.impact == "TI2"
    assert use_case.detectability == "TD1"
    assert use_case.tcl == "TCL1"

    issues = use_case.get_issues({})
    assert not issues


def test_valid_sys_req(test_data_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Positive test the tooling using good data."""
    with caplog.at_level(logging.INFO):
        spec_element_list = get_elements_from_files("TD", [test_data_path / "simple" / "sys_req.md"])

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) == 1

    spec = spec_element_list[0]

    assert spec.name == "TD_SYS_REQ_simple_sys_req"
    assert spec.description_text()
    assert spec.is_qualification_related
    assert spec.variant == "SystemRequirement"
    assert spec.verification_criteria(), str(spec)

    verification_criteria = spec.verification_criteria()
    assert "Check we have a simple sys req" in verification_criteria
    assert "Not part of the verification criteria." not in verification_criteria

    assert spec.get_linked_by("derived_from"), str(spec)

    notes: list[str] | None = spec.content.get("Notes")
    assert notes is not None
    assert "This is just a little note." in notes

    issues = spec.get_issues({})
    assert not issues


# test the free functions


def test_looks_like_non_sticky_section() -> None:
    """Test the looks_like_non_sticky_section function."""
    assert looks_like_non_sticky_section("Ok:")

    # nothing after
    assert not looks_like_non_sticky_section("Ok: yes")

    # one line only
    assert not looks_like_non_sticky_section("not\nOk:")

    # not too many words
    assert looks_like_non_sticky_section("Could be a valid section:")
    assert not looks_like_non_sticky_section("Almost certainly not a valid section:")


def test_looks_like_single_line_field() -> None:
    """Test the looks_like_single_line_field function."""
    assert looks_like_single_line_field("Ok: yes")

    # one line only
    assert not looks_like_single_line_field("not\nOk:")

    # must have something after
    assert not looks_like_single_line_field("Ok:")

    # must have something before
    assert not looks_like_single_line_field(": nope")

    # but only two parts, please!
    assert not looks_like_single_line_field("before: middle: oops")

    # not too many words
    assert looks_like_single_line_field("Could be a valid option: yes!")
    assert not looks_like_single_line_field("Almost certainly not a valid section: nope!")
