"""Test the use-cases parser."""

import logging
import pytest
from pathlib import Path

from spicy.spec import get_elements_from_files
from spicy.spec.parser import SpecElement, SpecParser, parse_syntax_tree_to_spec_elements
from spicy.md_read import load_syntax_tree, parse_text_to_syntax_tree

def test_parse_use_case(test_data_path: Path) -> None:
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

    issues = use_case.get_issues()
    assert not issues


def test_detect_spec_heading():
    parser = SpecParser("my_file.md", "TD")
    assert parser.parsed_spec_count == 0
    tree_part = parse_text_to_syntax_tree("# TD_SYS_REQ_a_system_requirement")
    for child in tree_part.children:
        parser.parse_node(child)
    assert parser.parsed_spec_count == 1


def test_parse_sys_req_from_text(test_data_path: Path, caplog) -> None:
    from_file = test_data_path / "simple" / "sys_req.md"
    project_prefix = "TD"
    spec_text = "\n\n".join((
        "# TD_SYS_REQ_simple_sys_req",
        "The **TD** shall have a simple system requirement",
        "Derived from:",
        "- [TD_STK_REQ_simple_stk_req](#td_stk_req_simple_stk_req)",
        "TQP relevant: yes",
        "Verification Criteria:",
        "- check we have a simple sys req.",
        ))
    tree = parse_text_to_syntax_tree(spec_text)

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

    assert "Handle bullet-list" in caplog.text

    assert spec.description_text(), str(spec)
    assert spec.is_qualification_related
    assert spec.variant == "SystemRequirement"
    assert spec.verification_criteria(), str(spec)
    assert spec.get_linked_by("derived_from"), str(spec)

    issues = spec.get_issues()
    assert not issues


def test_parse_sys_req(test_data_path: Path) -> None:
    from_file = test_data_path / "simple" / "sys_req.md"
    project_prefix = "TD"
    node = load_syntax_tree(from_file)

    spec_text = "\n\n".join((
        "# TD_SYS_REQ_simple_sys_req",
        "The **TD** shall have a simple system requirement"
        "Derived from:",
        "- [TD_STK_REQ_simple_stk_req](#td_stk_req_simple_stk_req)",
        "TQP relevant: yes",
        "Verification Criteria:",
        "- Check the order list on the operator terminal to verify ordering is successful."
        ))

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

    issues = spec.get_issues()
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

    issues = use_case.get_issues()
    assert not issues


def test_valid_sys_req(test_data_path: Path) -> None:
    """Positive test the tooling using good data."""
    spec_element_list = get_elements_from_files("TD", [test_data_path / "simple" / "sys_req.md"])

    assert isinstance(spec_element_list, list)
    assert len(spec_element_list) == 1

    spec = spec_element_list[0]

    assert spec.name == "TD_SYS_REQ_simple_sys_req"
    assert spec.description_text()
    assert spec.is_qualification_related
    assert spec.variant == "SystemRequirement"
    assert spec.verification_criteria(), str(spec)
    assert spec.get_linked_by("derived_from"), str(spec)

    issues = spec.get_issues()
    assert not issues
